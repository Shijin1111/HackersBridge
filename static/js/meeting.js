console.log('main.js loaded');

var mapPeers = {};  
var labelUsername = document.getElementById('label-username');
var inputUsername = document.getElementById('username');
var btnjoin = document.getElementById('btn-join');
var username;
var webSocket;

function webSocketOnMessage(e) {
    var parsedData = JSON.parse(e.data);
    var peerUsername = parsedData['peer'];
    var action = parsedData['action'];
    if(username == peerUsername) {
        return;
    }
    var receiver_channel_name = parsedData['message']['receiver_channel_name'];
    if(action == 'new-peer') { 
        createOfferer(peerUsername, receiver_channel_name);
        return;
    }
    if(action == 'new-offer') {
        var offer = parsedData['message']['sdp'];
        createAnswerer(offer, peerUsername, receiver_channel_name);
        return;
    }
    if(action == 'new-answer') {
        var answer = parsedData['message']['sdp'];
        var peer = mapPeers[peerUsername][0];
        peer.setRemoteDescription(answer);
        return;
    }
}
btnjoin.addEventListener('click', function() {
    username = inputUsername.value;
    if (username) {
        console.log('username:', username);
        labelUsername.innerHTML = 'Username: ' + username;
    }
    inputUsername.value = '';
    inputUsername.disabled = true;
    inputUsername.style.display = 'none';
    btnjoin.disabled = true;
    btnjoin.style.display = 'none';
    labelUsername.innerHTML = 'Username: ' + username;

    // Get the team_id passed in the URL
    var teamId = document.getElementById('team_id').textContent.trim();  // Assuming team_id is rendered into an HTML element
    
    var loc = window.location;
    var wsStart = loc.protocol === 'https:' ? 'wss://' : 'ws://';
    var endpoint = wsStart + loc.host + "/ws/video/" + teamId + "/";

    console.log('WebSocket Endpoint:', endpoint);

    webSocket = new WebSocket(endpoint);
    webSocket.addEventListener('open', function(e) {
        console.log('Connection opened');
        sendSignal('new-peer', {});  
    });
    webSocket.addEventListener('message', webSocketOnMessage);
    webSocket.addEventListener('close', function(e) {
        console.log('Connection closed');
    });
    webSocket.addEventListener('error', function(e) {
        console.log('Error:', e);
    });
});


var localStream = new MediaStream();

const constraints = {
    video: true,
    audio: true
};
const localVideo = document.getElementById('local-video');
const btnToggleAudio = document.getElementById('btn-toggle-audio');
const btnToggleVideo = document.getElementById('btn-toggle-video');

var userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(function(stream) {
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;
        var audioTracks = stream.getAudioTracks();
        var videoTracks = stream.getVideoTracks();
        audioTracks[0].enabled = true;
        videoTracks[0].enabled = true;
        btnToggleAudio.addEventListener('click', function() {
            audioTracks[0].enabled = !audioTracks[0].enabled;
            if (audioTracks[0].enabled) {
                btnToggleAudio.innerHTML = 'Mute Audio';
                return;
            }
            btnToggleAudio.innerHTML = 'Unmute Audio';
        });
        btnToggleVideo.addEventListener('click', function() {
            videoTracks[0].enabled = !videoTracks[0].enabled;
            if (videoTracks[0].enabled) {
                btnToggleVideo.innerHTML = 'Mute Video';
                return;
            }
            btnToggleVideo.innerHTML = 'Unmute Video';
        });
    })
    .catch(function(error) {
        console.log('Error accessing media devices.', error);
    });

var btnSendMsg = document.getElementById('btn-send-msg');
var messageList = document.getElementById('messages-list');

btnSendMsg.addEventListener('click', sendMsgOnClick);

function sendMsgOnClick() {
    var messageInput = document.getElementById('msg');
    var message = messageInput.value;
    messageInput.value = '';
    var li = document.createElement('li');
    li.appendChild(document.createTextNode('Me: ' + message));
    messageList.appendChild(li);
    var datachannels = getDataChannels();
    message = username + ': ' + message;
    for (index in datachannels) {
        datachannels[index].send(message);
    }
    messageInput.value = '';
}

function sendSignal(action, message) {
    var jsonStr = JSON.stringify({
        'peer': username,
        'action': action,
        'message': message,
    });
    webSocket.send(jsonStr);
}

function createOfferer(peerUsername, receiver_channel_name) {
    var peer = new RTCPeerConnection(null);
    addLocalTracks(peer);
    var dc = peer.createDataChannel('channel');
    dc.addEventListener('open', function() {
        console.log('Connection opened');
    });
    dc.addEventListener('message', dcOnMessage);
    
    // Create unique video element for the peer
    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, peerUsername, remoteVideo);  // Pass remoteVideo here
    mapPeers[peerUsername] = [peer, dc];
    
    peer.addEventListener('iceconnectionstatechange', function() {
        var iceConnectionState = peer.iceConnectionState;
        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
            delete mapPeers[peerUsername];
            if (iceConnectionState != 'closed') {
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    });
    
    peer.addEventListener('icecandidate', function(event) {
        if (event.candidate) {
            return;
        }
        sendSignal('new-offer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name
        });
    });
    
    peer.createOffer()
        .then(o => peer.setLocalDescription(o))
        .then(function() {
            console.log('Local description set successfully');
        });
}

function createAnswerer(offer, peerUsername, receiver_channel_name) {
    var peer = new RTCPeerConnection(null);
    addLocalTracks(peer);

    // Create unique video element for the peer
    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, peerUsername, remoteVideo);  // Pass remoteVideo here

    peer.addEventListener('datachannel', function(e) {
        peer.dc = e.channel;
        peer.dc.addEventListener('open', function() {
            console.log('Connection opened');
        });
        peer.dc.addEventListener('message', dcOnMessage);
        mapPeers[peerUsername] = [peer, peer.dc];
    });

    peer.addEventListener('iceconnectionstatechange', function() {
        var iceConnectionState = peer.iceConnectionState;
        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
            delete mapPeers[peerUsername];
            if (iceConnectionState != 'closed') {
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    });

    peer.addEventListener('icecandidate', function(event) {
        if (event.candidate) {
            return;
        }
        sendSignal('new-answer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name
        });
    });

    peer.setRemoteDescription(offer)
        .then(function() {
            console.log('Remote description set successfully for %s', peerUsername);
            return peer.createAnswer();
        })
        .then(a => {
            console.log('Answer created');
            peer.setLocalDescription(a);
        });
}

function addLocalTracks(peer) {
    localStream.getTracks().forEach(track => {
        peer.addTrack(track, localStream);
    });
    return;
}

function dcOnMessage(event)
{
    var message = event.data;
    var li = document.createElement('li');
    li.appendChild(document.createTextNode(message));
    messageList.appendChild(li);
}

function createVideo(peerUsername) {
    var videoContainer = document.getElementById('video-container');
    var remoteVideo = document.createElement('video');
    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;
    var videoWrapper = document.createElement('div');
    videoWrapper.classList.add('video-wrapper');
    videoContainer.appendChild(videoWrapper);
    videoWrapper.appendChild(remoteVideo);
    return remoteVideo;
}

function setOnTrack(peer, peerUsername, remoteVideo) {
    var remoteStream = new MediaStream();
    remoteVideo.srcObject = remoteStream;
    peer.addEventListener('track', async function(event) {
        remoteStream.addTrack(event.track, remoteStream);
    });
}

function removeVideo(video) {
    var videoWrapper = video.parentNode;
    videoWrapper.parentNode.removeChild(videoWrapper);
}

function getDataChannels() {
    var dataChannels = [];
    for (var peerUsername in mapPeers) {
        var dataChannel = mapPeers[peerUsername][1];
        dataChannels.push(dataChannel);
    }
    return dataChannels;
}