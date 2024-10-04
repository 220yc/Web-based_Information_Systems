from django.db import models

class Admin(models.Model):
	adname = models.CharField(max_length=10)
	adpassword = models.CharField(max_length=50)

	def __str__(self):
		return self.adname

class User(models.Model):
	username = models.CharField(max_length=10)
	password = models.CharField(max_length=50)
	email = models.EmailField()

	def __str__(self):
		return self.username

class Cart(models.Model):
	userid = models.ForeignKey(User,on_delete=models.RESTRICT)
	product_name = models.CharField(max_length=50)
	price = models.PositiveIntegerField(default=0)
	image = models.CharField(max_length=50)
	quantity = models.PositiveIntegerField(default=0)
	subtotal = models.PositiveIntegerField(default=0)

	def __str__(self):
		return (self.userid.username+self.product_name)



class Product(models.Model):
	name = models.CharField(max_length=30)
	price = models.PositiveIntegerField(default=0)
	image = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Order(models.Model):
	PAYMENT = [['CS','cash'],
			   ['CR','credit card'],
	]
	name = models.CharField(max_length=10)#customer
	phone = models.CharField(max_length=20)
	pay_method = models.CharField(max_length=255,choices=PAYMENT)
	total_products = models.CharField(max_length=255)
	total_price = models.PositiveIntegerField(default=0)

	def __str__(self):
		return (self.name + self.pay_method)