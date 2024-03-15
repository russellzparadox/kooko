from django import forms

from accounts.models import User


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder_text = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'password': 'رمز عبور',
        }
        self.fields.update({
            'username': forms.CharField(label='', help_text=None),
            'email': forms.EmailField(label=''),
            'first_name': forms.CharField(label=''),
            'last_name': forms.CharField(label=''),
            'password': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}), label=''),
        })
        for field_name, placeholder in placeholder_text.items():
            self.fields[field_name].widget.attrs.update({'class': '', 'placeholder': placeholder})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="")
    password = forms.CharField(widget=forms.PasswordInput, label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder_text = {
            'username': 'نام کاربری',
            'password': 'رمز عبور',
        }
        self.fields.update({
            'username': forms.CharField(label='', help_text=None),
            'password': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}), label=''),
        })
        for field_name, placeholder in placeholder_text.items():
            self.fields[field_name].widget.attrs.update({'class': '', 'placeholder': placeholder})


class PostForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'id': 'image'})

    # self.fields['body'].widget.attrs.update({'placeholder': 'چه خبرا؟'})
    #
    # my_text_area = forms.CharField(widget=forms.Textarea)
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'چه خبرا؟'}), label='')
    image = forms.ImageField(required=False)

    # username = forms.CharField(max_length=100, label="")


class EditProfileForm(forms.ModelForm):
    # description = forms.CharField(widget=forms.Textarea, required=False)
    # picture = forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # lable_text = {
        #     'username': 'نام کاربری',
        #     'first_name': 'نام',
        #     'last_name': 'نام خانوادگی',
        #     'email': 'ایمیل',
        #     'password': 'رمز عبور',
        #     'description': 'توضیحات'
        # }
        self.fields.update({
            'username': forms.CharField(label='نام کاربری', help_text=None),
            'email': forms.EmailField(label='ایمیل'),
            'first_name': forms.CharField(label='نام'),
            'last_name': forms.CharField(label='نام خانوادگی'),
            'password': forms.CharField(widget=forms.PasswordInput(), label='رمز عبور', required=False),
            'description': forms.CharField(widget=forms.Textarea(), label='توضیحات', required=False)
        })

    # password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'description')
