from allauth.account.forms import LoginForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CaptchaLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CaptchaLoginForm, self).__init__(*args, **kwargs)
        self.fields['captcha'] = ReCaptchaField(widget=ReCaptchaWidget())
