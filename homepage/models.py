from django.db import models
from django.core import validators as v
from django.urls import reverse


class VisitorData(models.Model):
    email = models.EmailField(help_text="Enter your email", primary_key=True)
    cookie = models.CharField(max_length=128, null=True, unique=True)
    date = models.DateField(auto_now=True)
    packages_count = models.IntegerField(validators=[v.MaxValueValidator(100), v.MinValueValidator(1)], default=1)
    meals_per_day = models.IntegerField(validators=[v.MaxValueValidator(5), v.MinValueValidator(1)], default=2)
    package_volume = models.IntegerField(validators=[v.MaxValueValidator(5000), v.MinValueValidator(100)], default=1000)
    wb_per_meal = models.IntegerField(validators=[v.MaxValueValidator(500), v.MinValueValidator(100)], default=200)
    hungry_people = models.IntegerField(validators=[v.MaxValueValidator(10), v.MinValueValidator(1)], default=1)

    class Meta:
        ordering = ["date", "email"]

    def __str__(self):
        return "User " + self.email + \
               " participated on " + str(self.date) + \
               "[packages_count=" + str(self.packages_count) + \
               " meals_per_day=" + str(self.meals_per_day) + \
               " package_volume=" + str(self.package_volume) + \
               " wb_per_meal=" + str(self.wb_per_meal) + \
               " hungry_people=" + str(self.hungry_people) + "]"


class InviteEntry(models.Model):
    # Сохраним только последний инвайт для участника
    email = models.EmailField(help_text="Enter your email", primary_key=True)
    invite_id = models.CharField(max_length=128, null=True, unique=True)
    date = models.DateTimeField(auto_now=True)
    is_validated = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', '-is_validated']

    def __str__(self):
        return "Invite # " + self.invite_id + \
                " sent on " + str(self.date) + \
                " to " + self.email + \
                " validated: " + str(self.is_validated)


class Comment(models.Model):
    comment_id = models.CharField(max_length=128, null=False, primary_key=True)
    email = models.EmailField(null=False)
    nickname = models.CharField(max_length=128, null=True)
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=256, null=False)
    likes = models.IntegerField(validators=[v.MinValueValidator(0)], default=0)
    dislikes = models.IntegerField(validators=[v.MinValueValidator(0)], default=0)

    class Meta:
        ordering = ['likes', '-date']

    def __str__(self):
        return "Comment # " + str(self.comment_id) + \
                " created on " + str(self.date) + \
                " by " + self.nickname + \
                " aka " + self.email + \
                " and said " + self.text + \
                " has " + str(self.likes) + " likes " + \
                " and " + str(self.dislikes) + " dislikes"


class RatingEntry(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    email = models.ForeignKey(VisitorData, models.SET_NULL, blank=True, null=True)
    ACTION_CHOICES = [
        ('L', 'Like'),
        ('D', 'Dislike')
    ]
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)

    def __str__(self):
        return "User " + self.email + \
                " commited " + self.action + \
                " to comment # " + self.comment_id