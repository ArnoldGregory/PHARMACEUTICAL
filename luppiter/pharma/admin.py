from django.contrib import admin
from .models import Total_Customers, Sale, Medicine, Order, Pharmacist
from django.contrib.auth.models import Group

admin.site.site_header = 'LUPPITER PHARMACEUTICALS'


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


# Register your models here.

admin.site.register(Total_Customers)
admin.site.register(Sale)
admin.site.register(Order)
admin.site.register(Pharmacist)
admin.site.register(Medicine, MedicineAdmin)

