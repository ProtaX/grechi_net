from django.db import models
from django.core import validators as v
from django.urls import reverse


class VisitorData(models.Model):
    email = models.EmailField(help_text="Enter your email", primary_key=True)
    date = models.DateField(auto_now=True)
    package_count = models.IntegerField(validators=[v.MaxValueValidator(100), v.MinValueValidator(1)], default=1)
    meals_per_day = models.IntegerField(validators=[v.MaxValueValidator(5), v.MinValueValidator(1)], default=2)
    package_weight = models.IntegerField(validators=[v.MaxValueValidator(5000), v.MinValueValidator(100)], default=1000)
    weight_per_meal = models.IntegerField(validators=[v.MaxValueValidator(500), v.MinValueValidator(100)], default=200)
    hungry_people = models.IntegerField(validators=[v.MaxValueValidator(10), v.MinValueValidator(1)], default=1)
    cookie = models.CharField(max_length=30, null=True)
    # TODO: Meal field (kkal)

    class Meta:
        ordering = ["date", "email"]

    def __str__(self):
        return "User " + self.email + \
               " visited on " + self.date + \
               "[package_count=" + self.package_count + \
               "meals_per_day=" + self.meals_per_day + \
               "package_weight=" + self.package_weight + \
               " weight_per_meal=" + self.weight_per_meal + \
               " hungry_people=" + self.hungry_people + "]"

    def get_absolute_url(self):
        return reverse('visitordata-detail', args=[str(self.id)])
