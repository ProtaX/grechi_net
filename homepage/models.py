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
               " participated on " + self.date + \
               "[packages_count=" + self.packages_count + \
               " meals_per_day=" + self.meals_per_day + \
               " package_volume=" + self.package_volume + \
               " wb_per_meal=" + self.wb_per_meal + \
               " hungry_people=" + self.hungry_people + "]"


class InviteEntry(models.Model):
    email = models.EmailField(help_text="Enter your email", primary_key=True)
    invite_id = models.CharField(max_length=128, null=True, unique=True)
    date = models.DateTimeField(auto_now=True)
    is_validated = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', '-is_validated']

    def __str__(self):
        return "Invite # " + self.invite_id + \
                " sent on " + self.date + \
                " to " + self.email + \
                " validated: " + self.is_validated