from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=11)

    def __str__(self) -> str:
        return self.name

class LoanApplication(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10)
    type_of_business = models.CharField(max_length=50)
    business_address = models.CharField(max_length=300)
    district = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    amount = models.IntegerField()
    status = models.BooleanField(default=False)
    financial_data = models.JSONField(blank=True, null=True)
    created_at = models.CharField(max_length=100, blank=True, null=True)