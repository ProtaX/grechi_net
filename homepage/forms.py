from django import forms


class ParticipateForm(forms.Form):
    email = forms.EmailField(help_text="Email", required=True)
