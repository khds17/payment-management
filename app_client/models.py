from django.db import models
from cnpj_field.models import CNPJField

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        
    def __str__(self):
        return f'{self.name}, {self.price}'
    
class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    
    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'
        
    def __str__(self):
        return self.name

class PlanService(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Plan Service'
        verbose_name_plural = 'Plan Services'
        
    def __str__(self):
        return f'{self.plan.name} - {self.service.name}'
    
class Client(models.Model):
    name = models.CharField(max_length=100)
    cnpj = CNPJField(blank=True, null=True)
    cpf = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField()
    phone = models.BigIntegerField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postalcode = models.IntegerField()
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        
    def __str__(self):
        return f'{self.name}, {self.email}, {self.phone}'
    
class Subscription(models.Model):
    customer = models.ForeignKey(Client, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        
    def __str__(self):
        return f'{self.customer.name} - {self.plan.name}'
    
class SubscriptionService(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Subscription Service'
        verbose_name_plural = 'Subscription Services'
        
    def __str__(self):
        return f'{self.subscription.customer.name} - {self.service.name}'

    
class Bill(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('partially_paid', 'Partially Paid'),
        ('bonus', 'Bonus'),
    ]
        
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    reference_month = models.DateField()
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'
        
    def __str__(self):
        return f'{self.subscription.customer.name} - {self.due_date} - {self.amount}'
    
class BillService(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Bill Service'
        verbose_name_plural = 'Bill Services'
        
    def __str__(self):
        return f'{self.bill.subscription.customer.name} - {self.service.name}'


