from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    unhashed_password = models.CharField(max_length=128, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True , max_length=255)

    class Meta:
        permissions = [
            ("change_user_permissions", "Can change user permissions"),
            ("view_user_permissions", "Can view user permissions"),
            ("change_group", "Can change group"),
            ("view_group", "Can view group")
        ]
        unique_together = [['unhashed_password', 'phone_number']]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    inviter = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='invitees')
    invitation_code = models.CharField(max_length=8, unique=True)
    wallet_address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def generate_invitation_code(self):
        chars = string.ascii_uppercase + string.digits
        self.invitation_code = ''.join(random.choice(chars) for _ in range(8))

    def save(self, *args, **kwargs):
        if not self.invitation_code:
            self.generate_invitation_code()
        super().save(*args, **kwargs)

    @property
    def invitees(self):
        return UserProfile.objects.filter(inviter=self.user)
    
    @property
    def url(self):
        return f'https://bitrader.onrender.com/?invitation_code={self.invitation_code}'
    @property
    def media(self):
        facebook_share_url = "https://www.facebook.com/sharer.php?u=" + self.url
        instagram_share_url = "http://instagram.com/?url=" + self.url
        telegram_share_url = f"https://telegram.me/share/url?url={self.url}&text=انضم إلينا الآن واستفد من فرصة استثمار مذهلة على منصتنا! احصل على ميزات السحب الفوري والأمان والضمان، واحصل على 10 USDT مجانًا عند التسجيل. لا تفوت هذه الفرصة الذهبية!"
        whatsapp_share_url = "https://api.whatsapp.com/send?text=" + self.url
        twitter_share_url = "https://twitter.com/intent/tweet?text=" + self.url

        return {
            'facebook': facebook_share_url,
            'instagram': instagram_share_url,
            'telegram': telegram_share_url,
            'whatsapp': whatsapp_share_url,
            'x': twitter_share_url
            
        }
