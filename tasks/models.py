from django.db import models

# Create your models here.
class Task(models.Model):
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