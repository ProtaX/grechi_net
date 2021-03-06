from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import SHA1PasswordHasher
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse
from .models import VisitorData
from .models import InviteEntry
from .models import Comment
from .models import RatingEntry
from .forms import ParticipateForm
from .forms import CommentForm
from bs4 import BeautifulSoup
import pytz
import json
import requests as r
import random as rnd
import datetime as dt

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
    context['is_user_auth'] = False
    if request.method == 'POST':
        form = ParticipateForm(request.POST)

        if form.is_valid():
            context['is_participant_email_valid'] = True
            email_from_form = form.cleaned_data['email']
            hasher = SHA1PasswordHasher()
            try:
                participant = VisitorData.objects.get(email=email_from_form)
                try:
                    invite = InviteEntry.objects.get(email=email_from_form)
                    if invite.is_validated == False:
                        context['is_invite_exists'] = True
                    else:
                        raise ObjectDoesNotExist()
                except:
                    tmp_uid = hasher.encode(email_from_form, dt.datetime.now().__str__())
                    invite = InviteEntry(email=email_from_form,
                                        invite_id=tmp_uid)
                    invite.save()
                    context['is_invite_exists'] = False
                # Здесь посетитель пытается участвовать, но запись о нем уже есть
                # Для разрешения такой ситуации шлем ему письмо со ссылкой,
                # он переходит по нашей ссылке - и 'входит' на сайт
                
                context['is_email_known'] = True

            except ObjectDoesNotExist:
                # Посетитель хочет участвовать впервые - созадим запись о нем
                participant = VisitorData(email=email_from_form, 
                                        packages_count=form.cleaned_data['packages_count'], 
                                        meals_per_day=form.cleaned_data['meals_per_day'],
                                        wb_per_meal=form.cleaned_data['wb_per_meal'],
                                        package_volume=form.cleaned_data['package_volume'],
                                        hungry_people=form.cleaned_data['hungry_people'])
                # cookie = hasher.encode(email_from_form, dt.datetime.now().__str__())
                salt_num = int(rnd.random() * 10000000000000000)
                cookie = hasher.encode(email_from_form, str(salt_num))
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

                salt_num = int(rnd.random() * 10000000000000000)
                hasher = SHA1PasswordHasher()
                cookie = hasher.encode(email, str(salt_num))

                participant.cookie = cookie
                request.session['cookie'] = participant.cookie
                invite.is_validated = True

                participant.save()
                invite.save()
                print('[validate_invite], invite invalidated')
                # TODO: удалить эту запись из базы?
            except:
                pass
    except:
        print('[validate_invite], invite no found: ' + invite_id)
    
    return redirect('index')

def update_participant_data(request):
    pass

def logout(request):
    request.session.clear()
    return redirect('index')

def load_prices(request):
    use_mock = 1
    product_list = []

    if not use_mock:
        yandex_market_url = 'https://market.yandex.ru/catalog--grechnevaia-krupa/72212/list'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Connection': 'keep-alive'
        }
        s = r.Session()
        page = s.get(yandex_market_url, headers=headers).text
        soup = BeautifulSoup(page, features="html.parser")
        #product_list_container_html = soup.find('div', {'class':'n-snippet-list'})
        product_list_html = soup.find_all('div', {'class':'n-snippet-card2'})
        for product_html in product_list_html:
            product_name = product_html.find('h3', {'class':'n-snippet-card2__title'}).text
            product_price = product_html.find('div', {'class':'price'}).text
            product_list.append({product_name: product_price})
    else:
        product_list = [{'Гречневая крупа Мистраль Ядрица 900 г': '115\xa0₽'}, {'Гречневая крупа Мистраль Ядрица 2 кг': '216\xa0₽'}, {'Група Мистраль Ядрица 5 кг': '569\xa0₽'}, {'Гречневая крупа Мистраль Зелёная 450 г': '81\xa0₽'}, {'Гречневая крупа Мистралая 900 г': '136\xa0₽'}, {'Гречневая крупа Агро-Альянс ядрица Экстра: 900 г': '104\xa0₽'}, 
                        {'Гречневая крупа Увелка крупкаах для варки 400 г': '498\xa0₽'}, {'Гречневая крупа Здравое зерно зелёная 500 г': '125\xa0₽'}, {'Гречневая крупа Макфа яд': '108\xa0₽'}, {'Гречневая крупа Увелка Ядрица в пакетиках для варки 400 г': '81\xa0₽'}, {'Гречневая крупа Мистраль Ядрицельная в пакетиках 400 г': '79\xa0₽'}, 
                        {'Гречневая крупа Maltagliati Ядрица быстроразваривающаяся 900 г': '86\xa0₽'}, {'крупа Агрохолдинг СТЕПЬ ядрица 900 г': '79\xa0₽'}]

    return render(
        request,
        'prices.html',
        context={'product_list':product_list[:10]}
    )

def load_comments(request):
    last_comment = request.GET['lastComment']
    if (last_comment is None or last_comment == '0'):
        print("Comments loading first time")
    else:
        print('Need to load comments after ' + last_comment)
    context = {'comments':[]}
    
    comments = Comment.objects.all()
    is_comment_yours = False
    visitor = None
    try:
        # TODO: брать только после полученной даты 
        visitor = VisitorData.objects.get(cookie=request.session['cookie'])
    except:
        pass
    # TODO: лайк/дизлайк коммента текущим пользователем
    for comment in comments:
        if visitor is not None and visitor.email == comment.email:
            is_comment_yours = True
        comment_info = [comment.nickname,
                        comment.text,
                        comment.date,
                        comment.likes,
                        comment.dislikes,
                        is_comment_yours,
                        comment.comment_id]
        context['comments'].append(comment_info)

    return render(
        request,
        'comment-card.html',
        context=context
    )

def add_comment(request):
    if request.method == 'POST':
        try:
            email = VisitorData.objects.get(cookie=request.session['cookie']).email
            nickname = request.POST['nickname']
            text = request.POST['comment']
            hasher = SHA1PasswordHasher()
            salt_num = int(rnd.random() * 10000000000000000)
            comment_id = hasher.encode(nickname, str(salt_num))
            comment = Comment(comment_id=comment_id, 
                                email=email, 
                                nickname=nickname,
                                text=text)
            comment.save()
        except:
            return redirect('index')
    else:
        return redirect('index')
    return HttpResponse()

def update_comment(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        comment_id = req['comment_id']
        action = req['action']
        try:
            comment = Comment.objects.get(comment_id=comment_id)
            visitor = VisitorData.objects.get(cookie=request.session['cookie'])
        except:
            return HttpResponse()

        if action == 'delete':
            if comment.email != visitor.email:
                return HttpResponse()
            comment.delete()
        elif action == 'like':
            pass
        elif action == 'dislike':
            pass
        return HttpResponse()
    else:
        return redirect('index')