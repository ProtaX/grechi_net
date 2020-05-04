from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import redirect
from .models import VisitorData
from .models import InviteEntry
from .forms import ParticipateForm
from django.contrib.auth.hashers import SHA1PasswordHasher
import pytz
import datetime as dt
from django.utils.dateparse import parse_datetime


def index(request):
    context = {}
    try:
        cookie = request.session['cookie']
        visitor = VisitorData.objects.get(cookie=cookie)
        context['participant_email'] = visitor.email.split('@')[0]
        context['is_user_auth'] = True
    except:
        context['is_user_auth'] = False
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
            hasher = SHA1PasswordHasher()
            try:
                participant = VisitorData.objects.get(email=email_from_form)
                # Здесь посетитель пытается участвовать, но запись о нем уже есть
                # Для разрешения такой ситуации шлем ему письмо со ссылкой,
                # он переходит по нашей ссылке - и 'входит' на сайт
                
                tmp_uid = hasher.encode(email_from_form, dt.datetime.now().__str__())
                invite = InviteEntry(email=email_from_form,
                                    invite_id=tmp_uid)
                invite.save()
                context['is_email_known'] = True
                context['is_user_auth'] = False

            except ObjectDoesNotExist:
                # Посетитель хочет участвовать впервые - созадим запись о нем
                participant = VisitorData(email=email_from_form, 
                                        packages_count=form.cleaned_data['packages_count'], 
                                        meals_per_day=form.cleaned_data['meals_per_day'],
                                        wb_per_meal=form.cleaned_data['wb_per_meal'],
                                        package_volume=form.cleaned_data['package_volume'],
                                        hungry_people=form.cleaned_data['hungry_people'])
                # cookie = hasher.encode(email_from_form, dt.datetime.now().__str__())
                cookie = hasher.encode(email_from_form, '12345')
                participant.cookie = cookie
                participant.save()
                request.session['cookie'] = cookie
                context['is_user_auth'] = True

            context['participant_email'] = email_from_form

        else:
            context['is_participant_email_valid'] = False
    return render(
        request,
        'index.html',
        context=context
    )


def email_invite(request, email):
    # Сейчас это 'наша' страница, но, по идее, эта страница
    # видна только на почте пользователя. Поэтому верим, что 
    # он никому не расскажет ссылку-приглашение и что почта 
    # действительно его

    print('[email_invite] email: ' + email)
    context = {'email': email}
    try:
        invite = InviteEntry.objects.get(email=email)
        context['invite_id'] = invite.invite_id
        print('[email_invite] valid invite, id: ' + invite.invite_id)
    except:
        return redirect('index')
    return render(
        request,
        'invite.html',
        context=context
    )


def validate_invite(request, invite_id):
    # Считаем, что приглашение действительно, если оно есть в базе
    # и с момента его отправки прошло не более 24 часов, и оно 
    # не было использовано ранее

    try:
        invite = InviteEntry.objects.get(invite_id=invite_id)
        email = invite.email
        invite_datetime = parse_datetime(str(invite.date))

        if (dt.datetime.utcnow().replace(tzinfo=pytz.utc) - invite_datetime > dt.timedelta(hours=24)) or invite.is_validated:
            print('[validate_invite], invalid invite: ' + invite.is_validated)
        else:
            try:
                participant = VisitorData.objects.get(email=email)
                request.session['cookie'] = participant.cookie
                invite.is_validated = True
                invite.save()
                print('[validate_invite], invite invalidated')
                # TODO: удалить эту запись из базы
            except:
                pass
    except:
        pass
    
    return redirect('index')

def logout(request):
    request.session.clear()
    return redirect('index')