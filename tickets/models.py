from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):

    STATUS = [
        ('Open','Open'),
        ('In Progress','In Progress'),
        ('Resolved','Resolved')
    ]

    PRIORITY = [
        ('Low','Low'),
        ('Medium','Medium'),
        ('High','High')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    status = models.CharField(max_length=20,choices=STATUS,default='Open')

    priority = models.CharField(max_length=20,choices=PRIORITY)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.ticket}"