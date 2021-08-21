from django.utils import timezone
from AUC.models import Profile
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required

def ErrorHandler404(request):
    return render(request, "AUC/Error404.html")

@never_cache
def Confirm_Email(request):
    try:
        user = Profile.objects.get(pk=force_text(urlsafe_base64_decode(request.GET.get('uid'))))
    except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
    if user is not None and user.confirm_email(request.GET.get('t')):
        if not request.user.is_authenticated or request.user != user:
            login(request, user)
        messages.add_message(request, 30, f"You are logged in as {request.user.username} <br> <a href='/accounts/logout'>Signup with different account</a>", extra_tags=request.user.profile_pic.url)
        messages.info(request, "Your email verification was successful")
        return HttpResponseRedirect(f"/")
    return render(request, "AUC/AuthenticateProfile.html", {"link_verify": "-"})

@never_cache
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=False).set_password(form.cleaned_data["password"])
            user = form.save().SendMail(title='AConfirmation', domain=get_current_site(request))
            login(request, user)
            messages.success(request, f"Welcome to the family {user.username} !! <br> <span> Check in your email for confirmation</span>")
            return HttpResponseRedirect(request.POST.get('next'))
        return render(request, "AUC/AuthenticateProfile.html", {"form": form})
    elif request.user.is_authenticated:
        messages.add_message(request, 30, f"You are already logged in as {request.user.username} <br> <a href='/accounts/logout'>Signup with different account</a>", extra_tags=request.user.profile_pic.url)
        if not request.user.Email_verified:
            messages.error(request, f"Please verify your account to help you explore more of us <br> <a href='/accounts/user/send_verification/'>Click here to re-send the email</a>", extra_tags='true')
        return HttpResponseRedirect(f"/")
    return render(request, "AUC/AuthenticateProfile.html",  {"form": UserRegisterForm()})


@never_cache
def login_view(request):
    form = UserRegisterForm()
    if request.method == "POST":
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password')
        if email:
            try:
                username = (Profile.objects.get(email=email)).username
            except Profile.DoesNotExist:
                pass
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not bool(request.POST.get('remember_me')):
                request.session.set_expiry(0)
            messages.warning(request, "Welcome back fam!! We missed you so much!",
                             extra_tags=request.user.profile_pic.url)
            messages.info(
                request, f"Successfully Logged in as {user.get_username()}")
            return HttpResponseRedirect(request.POST.get('next'))
        messages.error(
            request, "Invalid Username/Email and/or password <br> Note that both fields may be case-sensitive")
        return render(request, "AUC/AuthenticateProfile.html", {"form": form})
    elif request.user.is_authenticated:
        messages.add_message(
            request, 30, f"You are already logged in as {request.user.username} <br> <a href='/accounts/logout'>Signup with different account</a>", extra_tags=request.user.profile_pic.url)
        if not request.user.Email_verified:
            messages.error(request, f"Please verify your account to help you explore more of us <br> <a href='/accounts/user/send_verification/'>Click here to re-send the email</a>", extra_tags='true')
        
        return HttpResponseRedirect(f"/")
    print("-->", form.getImageURL())
    return render(request, "AUC/AuthenticateProfile.html",  {"form": form})


def logout_view(request):
    logout(request)
    messages.success(
        request, "<b style='color: var(--color-common)'> Successfully Logged Out<br>Login here with different account </b>")
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def userCheck(request):
    if request.is_ajax and request.method == 'POST':
        username = request.POST.get("username_email")
        try:
            user = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            try:
                user = Profile.objects.get(email=username)
            except Profile.DoesNotExist:
                return JsonResponse({'exists': 0}, status=200)
        return JsonResponse({'exists': 1, 'url': user.profile_pic.url}, status=200)
    return HttpResponseNotAllowed(('POST',))

def password_reset_successfully(request):
    messages.success(
        request, "<b style='color: var(--color-common)'> Password reset was successful<br> You may now login with the new password</b>")
    return HttpResponseRedirect(reverse('login'))

@never_cache
@login_required
def ReVerificationEmail(request):
    if request.user.Email_verified:
        messages.success(request, "Your email is already verified. <br> <span>We appreciate your support.</span>")
        return HttpResponseRedirect(reverse('testing'))
    if request.method == "POST":
        if (timezone.now() - request.user.last_verify_email).total_seconds() < 600:
            return HttpResponseRedirect(reverse('send_verify'))
        email = request.POST.get('verify_email')
        if request.user.Unique_Email(email, commit=True):
            request.user.last_verify_email = timezone.now()
            request.user.save()
            request.user.SendMail(title='AConfirmation', domain=get_current_site(request))
            return render(request, "AUC/AuthenticateProfile.html", {"re_sent": "an account verification"})
        messages.error(request, "Email Address already exists with another account. Please logout & login with the associated email.")
    return render(request, "AUC/AuthenticateProfile.html", {"time": timezone.now() - request.user.last_verify_email})

def testing(request):
    return render(request, "AUC/layout.html")