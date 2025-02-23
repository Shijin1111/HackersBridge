from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    sample_testcases = models.TextField()

    python_code_prefix = models.TextField(blank=True, null=True)  # Allow blank/null
    python_function_signature = models.TextField(blank=True, null=True)
    python_main = models.TextField(blank=True, null=True)

    cpp_code_prefix = models.TextField(blank=True, null=True)
    cpp_function_signature = models.TextField(blank=True, null=True)
    cpp_main = models.TextField(blank=True, null=True)

    java_code_prefix = models.TextField(blank=True, null=True)
    java_function_signature = models.TextField(blank=True, null=True)
    java_main = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
