import os
import binascii
from django.db import models
from django.utils import timezone


class PrivateFile(models.Model):
    file = models.FileField(upload_to='private/')
    create_at = models.DateTimeField(auto_now_add=True)


def get_expire_at():
    return timezone.now() + timezone.timedelta(hours=1)


class PrivateFileToken(models.Model):
    file = models.ForeignKey(PrivateFile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expire_at = models.DateTimeField(default=get_expire_at)
    create_at = models.DateTimeField(auto_now_add=True)

    def generate_token(self):
        token = binascii.hexlify(os.urandom(15)).decode('utf-8')
        if PrivateFileToken.objects.filter(token=token).exists():
            return self.generate_token()
        return token

    def save(self, *args, **kwargs):
        self.token = self.generate_token()
        return super().save(*args, **kwargs)
