from django.db import models


class Album(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    author = models.CharField(max_length=150)

    class Meta:
        ordering = ['title']


class Image(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images')
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']
