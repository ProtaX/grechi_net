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