from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    phone = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.username

class ModelBase(models.Model):
    active = models.BooleanField(default= True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ImageTour(ModelBase):
    image = models.ImageField(upload_to='imagetour/%Y/%m', default="none")
    descriptions = models.CharField(max_length = 255, null= True)
    tour = models.ForeignKey('Tour', on_delete= models.CASCADE, related_name= 'imagetour', null=True )

    def __str__(self):
        return self.descriptions


class Tour(ModelBase):
    name = models.CharField(max_length=100, null= False, default="none")
    image = models.ImageField(upload_to='tour/%Y/%m', default="none")
    price_for_adults = models.FloatField(default=0)
    price_for_children = models.FloatField(default=0)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    location = models.CharField(max_length=100, default="none")
    note = RichTextField(null=True)
    customers = models.ManyToManyField('User', through='BookTour', related_name='tour')
    tag = models.ManyToManyField('Tag', related_name='tour')
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.name


class Actionbase(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Comment(Actionbase):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='comment', null=True)
    content = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_date"]
    def __str__(self):

        return self.content

class Action(Actionbase):
    LIKE, HAHA, HEART = range(3)
    ACTIONS = [
        (LIKE, 'like'),
        (HAHA, 'haha'),
        (HEART, 'heart')
    ]
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='action', null=True)
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)

class Rate(Actionbase):

    star_rate = models.IntegerField(default=5)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='rate', null=True)
    class Meta:
        unique_together = ('user', 'tour')

    def __str__(self):
        return self.star_rate

class BookTour(ModelBase):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    num_of_adults = models.IntegerField(default=0)
    num_of_children = models.IntegerField(default=0)

    class Meta:
        unique_together =('user','tour')

    def __str__(self):
        return self.tour

class Bill(ModelBase):
    book_tour = models.OneToOneField('BookTour', on_delete=models.CASCADE, primary_key=True)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return self.book_tour

class TourView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    tour = models.OneToOneField('Tour', on_delete=models.CASCADE)
    views = models.IntegerField(default=0)


