from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def str(self):
        return str(self.id)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_books = models.ManyToManyField('Book', blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Rating for {self.book.name}: {self.value}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

