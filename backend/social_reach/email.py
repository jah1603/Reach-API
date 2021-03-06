from django.contrib.auth.tokens import default_token_generator

from templated_mail.mail import BaseEmailMessage
from activation_tokens import TokenGenerator
from djoser import utils
from djoser.conf import settings
from django.utils.encoding import force_bytes, force_text

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class ActivationEmail(BaseEmailMessage):
    template_name = '../templates/reach/activation_email.html'

    def get_context_data(self):
        context = super(ActivationEmail, self).get_context_data()

        user = context.get('user')
        context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        context['token'] = account_activation_token = TokenGenerator().make_token(user)
        context['url'] = settings.ACTIVATION_URL.format(**context)
        return context


class ConfirmationEmail(BaseEmailMessage):
    template_name = 'email/confirmation.html'


class PasswordResetEmail(BaseEmailMessage):
    template_name = '../templates/reach/password_reset.html'

    def get_context_data(self):
        context = super(PasswordResetEmail, self).get_context_data()

        user = context.get('user')
        context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        context['token'] = account_activation_token = TokenGenerator().make_token(user)
        return context
