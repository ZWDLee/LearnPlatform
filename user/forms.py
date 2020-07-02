import re
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名或邮箱',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
    )
    verification_code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入验证码'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            else:
                raise forms.ValidationError('* 用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

    def clean_verification_code(self):
        receive_code = self.cleaned_data['verification_code']
        store_code = self.request.session.get('verification_code', '')
        if receive_code.lower() != store_code.lower() or receive_code == '':
            raise forms.ValidationError('* 验证码错误')
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入3-30位的用户名'})
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'})
    )
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )
    password_again = forms.CharField(
        label='再次输入密码',
        min_length=8,
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        reg = '[^0-9A-Za-z\u4e00-\u9fa5]'
        if len(re.findall(reg, username)) > 0:
            raise forms.ValidationError('用户名不能包含特殊符号')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')
        return email

    def clean_password_again(self):
        password = self.cleaned_data.get('password', '')
        password_again = self.cleaned_data.get('password_again', '')
        if password != password_again:
            raise forms.ValidationError('输入的密码不一致')
        return password_again


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入被绑定的邮箱'})
    )
    verification_code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入验证码'})
    )
    new_password = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱未被绑定')
        return email

    def clean_verification_code(self):
        receive_code = self.cleaned_data['verification_code']
        store_code = self.request.session.get('forgot_password_code', '')
        if receive_code != store_code or receive_code == '':
            raise forms.ValidationError('验证码错误')
        return self.cleaned_data


class UserProfileForm(forms.Form):
    nickname = forms.CharField(
        label='*昵称',
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '你的昵称'})
    )
    avatar = forms.ImageField(
        label='头像',
        required=False,
    )
    GENDER = (
        (0, '男'),
        (1, '女'),
        (2, '保密')
    )
    gender = forms.ChoiceField(
        label='*性别',
        choices=GENDER,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    birth = forms.DateField(
        label='生日',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    EDUCATION = (
        (0, '小学'),
        (1, '初中'),
        (2, '高中'),
        (3, '专科'),
        (4, '本科'),
        (5, '研究生'),
        (6, '硕士'),
        (7, '博士'),
        (8, '其他')
    )
    education = forms.ChoiceField(
        label='*教育水平',
        choices=EDUCATION,
        widget=forms.RadioSelect(attrs={'class': 'education_radio'}),
    )
    profile_introduction = forms.CharField(
        label='简介',
        max_length=50,
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': '3',
                   'style': 'resize:none;width:300px;',
                   'placeholder': '添加您的简介- ( ゜- ゜)つロ'
                   }
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname'].strip()
        reg = '[^0-9A-Za-z\u4e00-\u9fa5]'
        if len(re.findall(reg, nickname)) > 0:
            raise forms.ValidationError('* 昵称不能包含特殊符号')
        if nickname == '':
            raise forms.ValidationError('昵称不能为空！')
        return nickname

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', '')
        try:
            if avatar.name.endswith('.gif'):
                raise forms.ValidationError('格式错误')
            if avatar.size > 5242880:
                raise forms.ValidationError('文件大小不能超过5MB')
        except:
            pass
        return avatar


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='原密码',
        min_length=8,
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        label='新密码',
        min_length=8,
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password_again = forms.CharField(
        label='重复新密码',
        min_length=8,
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码错误')
        return old_password

    def clean_new_password_again(self):
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('密码不一致')
        return new_password_again


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        if verification_code == '':
            raise forms.ValidationError('* 验证码不能为空')
        if not code == verification_code:
            raise forms.ValidationError('* 验证码不正确')
        return self.cleaned_data
