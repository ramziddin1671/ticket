from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('hardware', 'Hardware Issue'),
        ('software', 'Software Issue'),
        ('network', 'Network Issue'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200, default='Untitled Ticket')
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')  # IT mutaxassis)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)  # Fayl maydoni
    created_at = models.DateTimeField(auto_now_add=True)  # Murojaat yuborilgan vaqt
    accepted_at = models.DateTimeField(null=True, blank=True)  # Qabul qilingan vaqt
    completed_at = models.DateTimeField(null=True, blank=True)  # Tugatilgan vaqt



    def __str__(self):
        return self.title


ROLE_CHOICES = (
    ('employee', 'Oddiy xodim'),
    ('it_specialist', 'IT Mutaxassis'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='employee')
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} ({self.role})"