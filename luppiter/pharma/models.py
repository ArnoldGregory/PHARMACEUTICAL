from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# Create your models here.

medicine_type = (
    ('painkiller', 'PAINKILLERS'),
    ('cardiovascular', 'CARDIOVASCULAR'),
)

class Pharmacist(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    specialization = models.CharField(max_length=100)

    def dispense_medicine(self, customer_name, medicine):
        return f"{self.first_name} is dispensing {medicine} to {customer_name}."


class Total_Customers(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Total_Customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    medical_type = models.CharField(max_length=100, choices=medicine_type)
    buy_price = models.DecimalField(max_digits=8, decimal_places=2)
    sell_price = models.DecimalField(max_digits=8, decimal_places=2)
    batch_number = models.CharField(max_length=50)
    expiration_date = models.DateField()
    manufacturing_date = models.DateField()
    company = models.CharField(max_length=100)
    description = models.TextField()
    in_stock = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.medical_type}"

    class Meta:
        verbose_name_plural = 'Medicine'


class Sale(models.Model):
    pharmacist = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Sale'

    def __str__(self):
        return f"{self.medicine} ({self.quantity}) on {self.date}"


User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class Bill(models.Model):
    customer = models.ForeignKey(Total_Customers, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicine, through='BillItem')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill {self.pk} - {self.customer}"


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Bill Item #{self.pk} - {self.bill} - {self.medicine}"


class Order(models.Model):
    medicine = models.ManyToManyField(Medicine)
    pharmacist = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)

    date_ordered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.medicine} ordered by {self.pharmacist}"