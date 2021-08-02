from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.name}'


class Publication(models.Model):
    preview_image = models.ImageField(default='uploads/preview-images/default.jpg', upload_to='uploads/preview-images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = RichTextUploadingField()
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.date.strftime("%d-%m-%Y %H:%M")}] - {self.title}'


class Response(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1024)
    date = models.DateTimeField(default=timezone.now)
    on_publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.date.strftime("%d-%m-%Y %H:%M")}] {self.sender.username} ~ {self.message}'
