from django.utils import timezone
from AUC.models import Profile
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from .utils import SendMessage

def ErrorHandler404(request):
    return render(request, "AUC/Error404.html")

@never_cache
def Confirm_Email(request):
    m = SendMessage(request)
    try:
        user = Profile.objects.get(pk=force_text(urlsafe_base64_decode(request.GET.get('uid'))))
    except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
    if user is not None and user.confirm_email(request.GET.get('t')):
        if not request.user.is_authenticated or request.user != user:
            login(request, user)
        m.Warning(f"You are logged in as {request.user.username} <br> <a href='{reverse('logout')}'>Signup with different account</a>", extras=request.user.profile_pic.url)
        m.Info("Your email verification was successful")
        return HttpResponseRedirect(f"/")
    return render(request, "AUC/AuthenticateProfile.html", {"link_verify": "-"})

@never_cache
def register(request):
    m = SendMessage(request)
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=False).set_password(form.cleaned_data["password"])
            user = form.save().SendMail(title='AConfirmation', domain=get_current_site(request))
            login(request, user)
            m.Success(f"Welcome to the family {user.username} !! <br> <span> Check in your email for confirmation</span>")
            return HttpResponseRedirect(request.POST.get('next'))
        return render(request, "AUC/AuthenticateProfile.html", {"form": form})
    elif request.user.is_authenticated:
        m.Warning(f"You are already logged in as {request.user.username} <br> <a href='{reverse('logout')}'>Signup with different account</a>", extras=request.user.profile_pic.url)
        if not request.user.Email_verified:
            m.Error(f"Please verify your account to help you explore more of us <br> <a href='/accounts/user/send_verification/'>Click here to re-send the email</a>", extras='true')
        return HttpResponseRedirect(f"/")
    return render(request, "AUC/AuthenticateProfile.html",  {"form": UserRegisterForm()})


@never_cache
def login_view(request):
    form = UserRegisterForm()
    m = SendMessage(request)
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
            m.Warning("Welcome back fam!! We missed you so much!", extras=request.user.profile_pic.url)
            m.Info(f"Successfully Logged in as {user.get_username()}")
            return HttpResponseRedirect(request.POST.get('next'))
        m.Error("Invalid Username/Email and/or password <br> Note that both fields may be case-sensitive")
        return render(request, "AUC/AuthenticateProfile.html", {"form": form})
    elif request.user.is_authenticated:
        m.Warning(f"You are already logged in as {request.user.username} <br> <a href='{reverse('logout')}'>Signup with different account</a>", extras=request.user.profile_pic.url)
        if not request.user.Email_verified:
            m.Error(f"Please verify your account to help you explore more of us <br> <a href='/accounts/user/send_verification/'>Click here to re-send the email</a>", extras='true')
        
        return HttpResponseRedirect(f"/")
    print("-->", form.getImageURL())
    return render(request, "AUC/AuthenticateProfile.html",  {"form": form})


def logout_view(request):
    logout(request)
    SendMessage(request).Success("<b style='color: var(--color-common)'> Successfully Logged Out<br>Login here with different account </b>")
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def userCheck(request):
    if request.is_ajax or request.method == 'POST':
        print(request.POST);
        username = request.POST.get("username_email")
        print(username)
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
    SendMessage(request).Success("<b style='color: var(--color-common)'> Password reset was successful<br> You may now login with the new password</b>")
    return HttpResponseRedirect(reverse('login'))

@never_cache
@login_required 
def ReVerificationEmail(request):
    m = SendMessage(request)
    if request.user.Email_verified:
        m.Success("Your email is already verified. <br> <span>We appreciate your support.</span>")
        return HttpResponseRedirect(reverse('testing'))
    if request.method == "POST":
        if (timezone.now() - request.user.last_verify_email).total_seconds() < 600:
            return HttpResponseRedirect(reverse('send_verify'))
        email = request.POST.get('verify_email')
        if request.user.Unique_Email(email, commit=True):
            request.user.save()
            request.user.SendMail(title='AConfirmation', domain=get_current_site(request))
            request.user.last_verify_email = timezone.now()
            return render(request, "AUC/AuthenticateProfile.html", {"re_sent": "an account verification"})
        m.Error("Email Address already exists with another account. Please logout & login with the associated email.")
    return render(request, "AUC/AuthenticateProfile.html", {"time": timezone.now() - request.user.last_verify_email})

def testing(request):
    return render(request, "AUC/layout.html")