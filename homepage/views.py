from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import VisitorData
from .forms import ParticipateForm


def index(request):
    return render(
        request,
        'index.html',
        context={}
    )


def add_participant(request):
    context = {}
    if request.method == 'POST':
        form = ParticipateForm(request.POST)

        if form.is_valid():
            context['is_participant_email_valid'] = True
            email_from_form = form.cleaned_data['email']
            try:
                participant = VisitorData.objects.get(email=email_from_form)
                # TODO: get email from DB
                context['participant_email'] = 'Welcome back, ...'
            except ObjectDoesNotExist:
                context['participant_email'] = email_from_form
        else:
            context['is_participant_email_valid'] = False
    print(context)
    return render(
        request,
        'index.html',
        context=context
    )