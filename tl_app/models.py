from django.db import models

class Chat(models.Model):
    phno = models.CharField(max_length=12)
    username=models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.phno
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    
