from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        small_part_of_body = self.body[:10] + '...'
        return f'({self.user.username}) ' + small_part_of_body

    def get_absolute_url(self):
        return reverse('account:detail', args=(self.id,))


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    body = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')

    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        small_part_of_text = self.body[:20] + '...'
        return f'({self.user}) {small_part_of_text}'
