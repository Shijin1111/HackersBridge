import json
from channels.generic.websocket import AsyncWebsocketConsumer
# videocall chat
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the team_id from the URL route
        self.team_id = self.scope["url_route"]["kwargs"]["team_id"]
        
        # Create a unique room name for the team
        self.room_name = f"team_{self.team_id}"
        self.room_group_name = f"chat_{self.room_name}"

        # Add channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the channel from the group when disconnected
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Disconnected")

    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        message = receive_dict["message"]
        action = receive_dict["action"]
        
        if action == "new-offer" or action == "new-answer":
            receiver_channel_name = receive_dict["message"]["receiver_channel_name"]
            receive_dict["message"]["receiver_channel_name"] = self.channel_name
            await self.channel_layer.send(
                receiver_channel_name,
                {
                    "type": "send.sdp",
                    "receive_dict": receive_dict
                }
            )
            return
        
        # Set the receiver_channel_name to the current channel's name
        receive_dict['message']['receiver_channel_name'] = self.channel_name

        # Send the message to all members in the team chat room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send.sdp",
                "receive_dict": receive_dict
            }
        )

    async def send_sdp(self, event):
        receive_dict = event["receive_dict"]

        # Send the data to the WebSocket
        await self.send(text_data=json.dumps(receive_dict))


# chatbox
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class HackathonChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "hackathon_chat"

        # Check if user is authenticated before allowing connection
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Remove user from WebSocket group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = self.scope["user"].username  # Get username from authenticated user

        # Send message to WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,  # Now, username is fetched directly from the authenticated user
            },
        )


    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username}))
