import uuid
from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from django.contrib.auth.models import User
from cnpj_field.models import CNPJField

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postalcode = models.IntegerField()
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        
    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}, {self.postalcode}'

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    cnpj = CNPJField()
    phone = models.BigIntegerField()
    tenant = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='companies')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='companies')

    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        
    def __str__(self):
        return f'{self.name}, {self.cnpj}, {self.phone}'
    
class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

class Domain(DomainMixin):
    pass

class UserCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        
    def __str__(self):
        return f'{self.user.username}'



