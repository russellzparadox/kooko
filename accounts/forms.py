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
