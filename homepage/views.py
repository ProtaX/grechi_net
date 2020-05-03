from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import VisitorData
from .forms import ParticipateForm
from django.contrib.auth.hashers import SHA1PasswordHasher
import datetime as dt


def index(request):
    context = {}
    try:
        cookie = request.session['cookie']
        visitor = VisitorData.objects.get(cookie=cookie)
        context['participant_email'] = visitor.email.split('@')[0]
    except:
        print('New visitor')
    return render(
        request,
        'index.html',
        context=context
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
                # Здесь посетитель пытается участвовать, но запись о нем уже есть
                # Для разрешения такой ситуации шлем ему письмо со ссылкой,
                # он переходит по нашей ссылке - и 'входит' на сайт
                
                request.session['cookie'] = participant.cookie
                context['is_email_known'] = True

            except ObjectDoesNotExist:
                print('Visitor is not registered')
                # Посетитель хочет участвовать впервые - созадим запись о нем
                participant = VisitorData(email=email_from_form, 
                                        packages_count=form.cleaned_data['packages_count'], 
                                        meals_per_day=form.cleaned_data['meals_per_day'],
                                        wb_per_meal=form.cleaned_data['wb_per_meal'],
                                        package_volume=form.cleaned_data['package_volume'],
                                        hungry_people=form.cleaned_data['hungry_people'])
                hasher = SHA1PasswordHasher()
                # cookie = hasher.encode(email_from_form, dt.datetime)
                cookie = hasher.encode(email_from_form, '12345')
                participant.cookie = cookie
                participant.save()
                # TODO: надо ставить куки только после подтверждения email
                request.session['cookie'] = cookie  # DEBUG
                context['participant_email'] = email_from_form

        else:
            context['is_participant_email_valid'] = False
    print(context)
    return render(
        request,
        'index.html',
        context=context
    )