from django.contrib import admin
from . import models

class AdminAdmin(admin.ModelAdmin):
	list_display = ("adname",'adpassword')

class UserAdmin(admin.ModelAdmin):
	list_display = ("username",'password','email')

class CartAdmin(admin.ModelAdmin):
	list_display = ("userid",'product_name','price','image','quantity','subtotal')

class ProductAdmin(admin.ModelAdmin):
	list_display = ("name",'price','image')

class OrderAdmin(admin.ModelAdmin):
	list_display = ("name",'phone','pay_method','total_products','total_price')

admin.site.register(models.Admin,AdminAdmin)
admin.site.register(models.User,UserAdmin)
admin.site.register(models.Cart,CartAdmin)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Order,OrderAdmin)

