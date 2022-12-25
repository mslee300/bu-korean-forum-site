from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from django.contrib.auth import get_user_model

# from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
# from .decorators import user_not_authenticated

from django.contrib import messages

# django_project/users/views.py
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, '이메일 인증에 성공하였습니다. 이제 로그인 하실 수 있습니다.')
        return redirect('index')
    else:
      messages.error(request, '이 가입인증 링크는 만료되었습니다(4시간 초과), 새로운 가입 인증 메일을 확인해주세요.')
    
    return redirect('index')
  

def activateEmail(request, user, to_email):
    mail_subject = '메일인증 안내입니다.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'{user}님, {to_email}로 인증메일이 발송되었습니다. 이메일을 확인해주세요.')
    else:
        messages.error(request, f'메일을 {to_email}에 전송하는 중에 일시적인 문제가 발생했습니다. 운영자에게 문의해주세요')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)  # 사용자 인증
            # login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
