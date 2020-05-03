from django import forms
from django.core import validators as v


class ParticipateForm(forms.Form):
    email = forms.EmailField(help_text="Email", required=True)
    packages_count = forms.IntegerField(validators=[v.MaxValueValidator(100), v.MinValueValidator(1)])
    meals_per_day = forms.IntegerField(validators=[v.MaxValueValidator(5), v.MinValueValidator(1)])
    package_volume = forms.IntegerField(validators=[v.MaxValueValidator(5000), v.MinValueValidator(100)])
    wb_per_meal = forms.IntegerField(validators=[v.MaxValueValidator(500), v.MinValueValidator(100)])
    hungry_people = forms.IntegerField(validators=[v.MaxValueValidator(10), v.MinValueValidator(1)])
