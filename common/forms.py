from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# School email checker
def validate_school(value):
    if value[-4:] != '.edu':
        raise ValidationError(('이메일은 .edu로 끝나야 합니다.'),
            params={'': value},
        )

# School email checker2
def validate_school2(value):
    if value[-4:] == '.edu' and value[-7:] != '@bu.edu':
        raise ValidationError(('지원하지 않는 학교입니다'),
            params={'': value},
        )

# School email checker3
def validate_school3(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(('이미 가입중인 메일입니다. 운영자에게 문의해주세요.'),
            params={'': value},
        )
      
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일", validators=[validate_school, validate_school2, validate_school3])

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
