from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} follows {self.to_user}'


