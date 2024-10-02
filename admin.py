from django.contrib import admin
from .models import *


# Register your models here.
class contactusAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Email','Mobile','Message')

admin.site.register(contactus,contactusAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name','category_picture')

admin.site.register(category,categoryAdmin)

class tbl_registerAdmin(admin.ModelAdmin):
    list_display = ('name','email','mobile','pincode','city','address','passwd','picture')

admin.site.register(tbl_register,tbl_registerAdmin)

class tbl_sliderAdmin(admin.ModelAdmin):
    list_display = ('picture','title','description')

admin.site.register(tbl_slider,tbl_sliderAdmin)

class service_providerAdmin(admin.ModelAdmin):
    list_display = ('id','provider_name','provider_picture','avg_price','discount_price','service_name','details','availability','provider_mobile','city','address','service_picture','service_category','pincode','added_date')

admin.site.register(service_provider,service_providerAdmin)

class servicesAdmin(admin.ModelAdmin):
    list_display=('service_title','provider_name','description','cost','avg_time','service_pic')

admin.site.register(services,servicesAdmin)

class tbl_bookingAdmin(admin.ModelAdmin):
    list_display = ('id','provider','email','date','time','details','address','city','pincode','payment','reqdate','status')

admin.site.register(tbl_booking,tbl_bookingAdmin)