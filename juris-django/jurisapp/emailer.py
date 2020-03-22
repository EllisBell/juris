from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def send_confirmation_email(user, current_site, to_email):
    subject = 'Ative a sua conta jurisprudencia.pt'
    message = render_to_string('jurisapp/registration/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject, message, to=[to_email])
    email.content_subtype='html'
    email.send()
