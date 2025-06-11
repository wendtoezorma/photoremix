from django.db import models

class UploadedPhoto(models.Model):
    original = models.ImageField(upload_to='originals/')
    base = models.ImageField(upload_to='originals/')      # photo de base (tu peux précharger une image ici)
    result = models.ImageField(upload_to='results/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo #{self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
