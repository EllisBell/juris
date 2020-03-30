from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.conf import settings
from jurisapp.models import User, Customer, CustomerUser
from jurisapp.forms import CustomUserCreationForm, ResendEmailForm
from jurisapp.tokens import account_activation_token
from jurisapp import emailer


def register(request):
    # TODO poor man's feature toggle, remove when ready
    if not settings.DEBUG:
        return redirect('juris_index')
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomUserCreationForm(request.POST, label_suffix="")
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            customer = Customer()
            customer.save()
            customer_user = CustomerUser(customer_id = customer, user_id = user)
            customer_user.save()
            current_site = get_current_site(request)
            to_email = form.cleaned_data.get('email')
            emailer.send_confirmation_email(user, current_site, to_email)
            return redirect('account_activation_sent', to_email)
    else:
        form = CustomUserCreationForm(label_suffix="")

    return render(request, 'jurisapp/registration/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print("UID is " + uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('account_activated')
    else:
        return render(request, 'jurisapp/registration/account_activation_invalid.html')


def account_activation_sent(request, email):
    return render(request, 'jurisapp/registration/account_activation_sent.html', {'email': email})


def account_activated(request):
    return render(request, 'jurisapp/registration/account_activated.html')


def resend_confirmation_email(request):
    if request.method == 'POST':
        form = ResendEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # get user
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                current_site = get_current_site(request)
                emailer.send_confirmation_email(user, current_site, email)
            # render view even if user doesn't exist to not divulge data unnecessarily
            return redirect('account_activation_sent', email)
    else:
        form = ResendEmailForm()

    return render(request, 'jurisapp/registration/resend_confirmation_email.html', {'form': form})
