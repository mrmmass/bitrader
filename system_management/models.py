from django.db import models
from accounts.models import UserProfile
from django.utils import timezone

# Create your models here.
class MiningMachine(models.Model):
    name = models.CharField(max_length=100)
    cpu_cores = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    daily_profit = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    image = models.ImageField(upload_to='mining_machine_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    @property
    def total_profit(self):
        return self.daily_profit * self.duration_days
    
    def __str__(self):
        return self.name


class Offer(models.Model):
    machine = models.ForeignKey(MiningMachine, on_delete=models.CASCADE, related_name='offers')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.machine.name} Offer"

class Coupon(models.Model):
    machine = models.ForeignKey(MiningMachine, on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=20, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.machine.name} Coupon"
    
class Purchase(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE , related_name='machine')
    machine = models.ForeignKey(MiningMachine, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    duration_days = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    @property
    def end_date(self):
        return self.purchase_date + timezone.timedelta(days=self.duration_days)

    @property
    def remaining_days(self):
        remaining_days = (self.end_date - timezone.now()).days
        return max(remaining_days, 0)

    @property
    def total_cost(self):
        return self.machine.price * self.duration_days

    @property
    def total_profit(self):
        return self.machine.daily_profit * self.remaining_days

    def stop_machine(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.user.user.username}'s Purchase of {self.machine.name}"

class Deposit(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='deposits')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    user_wallet = models.CharField(max_length=100 , blank=True, null=True)
    system_wallet = models.CharField(max_length=100 , blank=True, null=True)
    deposit_date = models.DateTimeField(auto_now_add=True)
    by_system = models.BooleanField(default=False)

    def __str__(self):
        return f"Deposit for {self.user} of {self.amount_paid}"
    class Meta:
            ordering = ['-deposit_date']

class Withdrawal(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='withdrawals')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    user_wallet = models.CharField(max_length=100 , blank=True, null=True)
    system_wallet = models.CharField(max_length=100 , blank=True, null=True)
    withdrawal_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Withdrawal for {self.user} of {self.amount_paid}"
    class Meta:
            ordering = ['-withdrawal_date']
        

