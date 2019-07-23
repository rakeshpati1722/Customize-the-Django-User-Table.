from django.db import models
from django.conf import settings
from authemail.models import EmailUserManager, EmailAbstractUser
import binascii
import os
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
import random
# Create your models here.

# model signal for creating token for the signuped user
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        print(instance)
        Token.objects.create(user=instance)

post_save.connect(create_token,sender=settings.AUTH_USER_MODEL)

# extended user model with user defined fields
class CustomModel(EmailAbstractUser):
    gender = models.CharField('gender',max_length=243)
    phone_number = models.CharField('phone_number',max_length=243,blank=True, null=True)

    objects = EmailUserManager()

# models signal for generating OTP and the same OTP sending on mail
def create_otp(sender, instance=None,created=False, **kwargs):
   if created:
        OTP.objects.create(user=instance)
        try:    
            o = OTP.objects.get(user=instance)
            key = o.otp
            u = get_user_model().objects.get(email=instance)
            mail(key,u) #calling function to forward the OTP to mail to particular Signuped user
        except OTP.DoesNotExist:
            print("------")


post_save.connect(create_otp,sender=settings.AUTH_USER_MODEL)

def mail(key,u):    
    subject = "OTP"
    message = "OTP to login:"+key
    from_email = "yaseentahasildar@gmail.com"
    mail = str(u)
    print(u)
    try:
        send_mail(subject, message, from_email, [mail])
    except:
        print("-------")

# model for storing OTP
class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    otp = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_otp()
        return super(OTP,self).save(*args,**kwargs)    

    def generate_otp(self):
        # return binascii.hexlify(os.urandom(2))
        for x in range(9):
            a = random.randint(1,10)
            b = random.randint(1,10)
            c = random.randint(1,10)
            d = random.randint(1,10)
        #     f = str(a) +str(b) +str(c) + str(d)
            g = "{}{}{}{}".format(a,b,c,d)
        return g

    def __str__(self):
        return self.otp    