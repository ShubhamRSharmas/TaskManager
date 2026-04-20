from django.db import models
from django.contrib.auth.models import User #Import the built-in User model

# Create your models here.
class Task(models.Model):
    #User: Built-in Django One-to-many relationship (One user many tasks)
    #on_delete=models.CASCADE : If a user deletes their account, all their tasks will be deleted automatically
    #null = True, blank = True: Important temporarily
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    #Instead of 'str', Django uses 'CharField' for short text
    title = models.CharField(max_length = 200)
    #Instead of 'bool', it's 'BooleanField'
    is_completed = models.BooleanField(default=False)
    #Django automatically handles the 'id' field for you!
    
    priority = models.CharField(max_length = 1, choices = PRIORITY_CHOICES, default = 'M')

    def __str__(self):
        status = "✅" if self.is_completed else "❌"
        return f"{self.title} - {status}" 
    
