from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from random import choice
from os.path import isfile, join as path_join
from os import listdir
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, message
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
import six

IMAGE_FILE = ''
IMAGE_FILES = {
    'AConfirmation': {'logo': '/Images/email_images/auc.png', 'connect': '/Images/email_images/connect.png'}
}

def random_img():
    global IMAGE_FILE
    dir_path = 'AUC/static/AUC/images/DefaultImages'
    file = choice([content for content in listdir(dir_path) if isfile(path_join(dir_path, content))])
    IMAGE_FILE = f'DefaultImages/{file}'
    print(IMAGE_FILE)
    return IMAGE_FILE

def getImage():
    return IMAGE_FILE

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
ACCOUNT_VERIFICATION_TOKEN = TokenGenerator()

class Profile(AbstractUser):
    profile_pic = models.ImageField(default=getImage, upload_to="profile_pics/", blank=True)
    bio = models.TextField(max_length=255, verbose_name="profile_bio", blank=True, default='Hi, I am here to connect.')
    private = models.BooleanField(verbose_name='Private_Profile', default=False)
    Email_verified = models.BooleanField(verbose_name='Email Verified', default=False, blank=True)
    slug = AutoSlugField(populate_from='username')
    last_verify_email = models.DateTimeField(blank=True, verbose_name="Verification sent timestamp", default=timezone.now)
    # friends = models.ManyToManyField("Profile", blank=True)
    # def sendEmail(self):

    def SendMail(self, Tomail = None, **kwargs):
        if not Tomail:
            Tomail = [self.email]
        if not IMAGE_FILES[kwargs['title']].get('user'):
            IMAGE_FILES[kwargs['title']]['user'] = self.profile_pic.url
        mail_subject, message = self.EMAIL_HTML_MESSAGES(**kwargs)
        email_message = EmailMultiAlternatives(mail_subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, Tomail)
        email_message.mixed_subkwargs = 'related'
        email_message.attach_alternative(message, "text/html")
        [email_message.attach(self.logo_data(id, file)) for id, file in IMAGE_FILES[kwargs['title']].items()]
        email_message.send(fail_silently=False)
        return self

    @lru_cache()
    def logo_data(self, id, filename):
        with open(finders.find(f'AUC{filename}'), 'rb') as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID', f'<{id}>')
        return logo

    def EMAIL_HTML_MESSAGES(self, **kwargs):
        if kwargs['title']=='AConfirmation':
            return "Activate your AUC account", render_to_string('AUC/Auth/acc_email_confirmation.html', {
            'user': self.first_name,
            'domain': kwargs['domain'].domain,
            'uid':urlsafe_base64_encode(force_bytes(self.pk)),
            'token':ACCOUNT_VERIFICATION_TOKEN.make_token(self),
        })
        return ""
    
    def confirm_email(self, token):
        if ACCOUNT_VERIFICATION_TOKEN.check_token(self, token):
             self.Email_verified = True
             self.save()
             return True
        return False
    
    def Unique_Email(self, email, commit=False):
        user = Profile.objects.filter(email=email).exclude(email=self.email)
        if not user.exists():
            if commit:
                user.update(email=email)
            return True
        return False
        
    def get_absolute_url(self):
        return "/users/{}".format(self.slug)

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):  # delete old file when replacing by updating the file
        try:
            this = Profile.objects.get(username=self.username)
            if this.profile_pic != self.profile_pic:
                this.profile_pic.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(Profile, self).save(*args, **kwargs)

# class FriendRequest(models.Model):
# 	to_user = models.ForeignKey('Profile', related_name='to_user', on_delete=models.CASCADE)
# 	from_user = models.ForeignKey('Profile', related_name='from_user', on_delete=models.CASCADE)
# 	timestamp = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return "From {}, to {}".format(self.from_user.username, self.to_user.username)