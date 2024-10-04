from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from . import models
import shutil
import hashlib
from django.conf import settings
import os

def md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()

def login(request):
	formtype = "login"#decide header
	username = ""
	password = ""
	errors = [] 

	if(request.method == 'POST'):
		# LOGIN USER #from login.php
		if(request.POST['login_user']):
			#receive all input values from the form
			username = request.POST['username']
			password = request.POST['password']

			if (username==""):
				errors.append("Username is required")
			if (password == ""):
				errors.append("Password is required")

			# Check if the user is an admin
			if (len(errors) == 0):
				try:
					result= models.Admin.objects.get(adname=username)
					if(result.adpassword == password):
						request.session['adname'] = username
						request.session['success'] = "You are now logged in"
						return HttpResponseRedirect('/admins/')
					else:
						errors.append("Wrong Password")
				except:
					pass

				try:
					result= models.User.objects.get(username=username)
					if(result.password == md5(password)):
						request.session['username'] = username
						request.session['success'] = "You are now logged in"
						request.session['user_id'] = result.id
						return HttpResponseRedirect('/member/')
					else:
						errors.append("Wrong Password")
				except:
					pass

				#if password is true:go to the specific page
				#else record the error

				#if there's no error but didn't go to other page
				#not a admin or a user
				if (len(errors) == 0):
					errors.append("Wrong Username")
	len_errors = len(errors) 
	return render(request,'login.html',locals())

def logout(request):
	request.session.clear()
	return HttpResponseRedirect('/login/')

def register(request):
	formtype = "register"#decide header
	username = ""
	email    = ""
	password_1 = ""
	password_2 = ""
	errors = [] 

	if(request.method == 'POST'):
		# REGISTER USER #from register.php
		if(request.POST['reg_user']):
			#receive all input values from the form
			username = request.POST['username']
			email= request.POST['email']
			password_1 = request.POST['password_1']
			password_2 = request.POST['password_2']

			# form validation: ensure that the form is correctly filled ...
			# by adding (errors.append) corresponding error unto $errors array
			if (username==""):
				errors.append("Username is required")
			if (email==""):
				errors.append("Email is required")
			if (password_1 == ""):
				errors.append("Password is required")
			if (password_1 != password_2):
				errors.append("The two passwords do not match")

			# first check the database to make sure 
			#a user does not already exist with the same username
			if (len(errors) == 0):
				try:
					result_user = models.User.objects.get(username=username)
					if(result_user):
						errors.append("Oops! username already exists")
				except:
					pass
				try:
					#a user does not already exist with the same email
					result_user = models.User.objects.get(email=email)
					if(result_user):
						errors.append("Oops! email already exists")
				except:
					pass

			#Finally, register user if there are no errors in the form
			if (len(errors) == 0):
			  	password = md5(password_1);#encrypt the password before saving in the database
			  	new_user = models.User.objects.create(username=username, password=password, email=email)
			  	new_user.save()
			  	errors.append("You are a part of us now >< Please log in again!")
			  	return HttpResponseRedirect('/login/')

			  	# request.session['username'] = username
			  	# request.session['success'] = "You are now logged in !!!";
	len_errors = len(errors)
	return render(request,'register.html',locals())

def admins(request):
	#<!--<a href="{% url 'upd-url' p.id %}" class="option-btn"> <i class="fas fa-edit"></i> update </a>--
	if 'adname' not in request.session.keys():
		if 'username' in request.session.keys():
			return HttpResponseRedirect('/member/')
		else:
			return HttpResponseRedirect('/login/')

	messages = []

	if(request.POST.get('add_product')):#if POST['add_product'] exist
		p_name = request.POST['p_name']
		p_price = request.POST['p_price']
		p_image = request.FILES['p_image']
		file_name  = p_image.name

		try:
			#create a new prod and save it to DB
			new_product = models.Product.objects.create(name=p_name,price=p_price,image=p_image)
			new_product.save()

			#save the picture in PC(for showing on other pages)
			base_path = settings.BASE_DIR #this project's route
			folder_name = 'static/shopping/images' 
			p_image_folder = os.path.join(base_path, folder_name, file_name)
			with open(p_image_folder,'wb') as f:
				for chunk in p_image.chunks():
					f.write(chunk)
			messages.append('product add succesfully')
		except:
			messages.append('could not add the product')
	try:
		products = models.Product.objects.all()
	except:
		pass

	return render(request,'admins/index.html',locals())

def showproduct(request):
	if 'adname' not in request.session.keys():
		return HttpResponseRedirect('/login/')

	try:
		products = models.Product.objects.all()
	except:
		messages.append('could not find products')	
	return render(request,'admins/product.html',locals())

def showmember(request):
	if 'adname' not in request.session.keys():
		return HttpResponseRedirect('/login/')

	try:
		members = models.User.objects.all()
	except:
		messages.append('could not find members')	
	return render(request,'admins/member.html',locals())

def deleteprod(request,del_id):
	if 'adname' not in request.session.keys():
		return HttpResponseRedirect('/login/')
	messages = []
	try:
		del_product = models.Product.objects.get(id=del_id)
		del_product.delete()
		messages.append("the product is deleted")
	except:
		messages.append("can't find the product")

	return HttpResponseRedirect('/admins/')

def delmember(request,del_id):
	if 'adname' not in request.session.keys():
		return HttpResponseRedirect('/login/')
	messages = []
	try:
		del_user = models.User.objects.get(id=del_id)
		del_user.delete()
		messages.append("the memeber is deleted")
	except:
		messages.append("can't find the member")

	return HttpResponseRedirect('/admins/showmember/')

def showorder(request):
	if 'adname' not in request.session.keys():
		return HttpResponseRedirect('/login/')

	try:
		orders = models.Order.objects.all()
	except:
		messages.append('could not find orders')	
	return render(request,'admins/order.html',locals())

def delorder(request,del_id):
	if 'adname' not in request.session.keys():
		return HttpResponseRedirect('/login/')

	messages = []
	try:
		del_order = models.Order.objects.get(id=del_id)
		del_order.delete()
		messages.append("the order is deleted")
	except:
		messages.append("can't find the order")

	return HttpResponseRedirect('/admins/showorder/')

def memberproduct(request):
	# when member login, these sessions are set
	# request.session['username'] = username
	# request.session['success'] = "You are now logged in"
	# request.session['user_id'] = result.id
	if 'username' not in request.session.keys():
		return HttpResponseRedirect('/login/')

	messages = []
	username = request.session.get('username')
	user_id = request.session.get('user_id')
	messages.append(request.session.get('success'))

	#show all the products
	try:
		products= models.Product.objects.all()
	except:
		pass

	#for header of index :show user info
	try:
		user= models.User.objects.get(id=user_id)
	except:
		messages.append("The user doesn't exist")

	try:
		carts = models.Cart.objects.filter(userid=user)
		cart_count = carts.count()
	except:
		cart_count = 0
		messages.append("The cart doesn't exist")

	#add new product
	if(request.POST.get('add_to_cart')):
		product_name = request.POST['product_name']
		product_price = request.POST['product_price']
		product_image = request.POST['product_image']
		product_quantity = 1

		try:
			prod_cart = carts.get(product_name=product_name)
			prod_cart.quantity += 1
			prod_cart.subtotal = prod_cart.quantity * prod_cart.price
			prod_cart.save()
			cart_count = carts.count()
			messages.append('The product has already exist.Update the quantity.')
		except:
			subtotal = product_price*product_quantity
			new_user_prod_cart = models.Cart.objects.create(userid=user, product_name=product_name, price=product_price,image=product_image,quantity=product_quantity, subtotal=subtotal)
			new_user_prod_cart.save()
			cart_count = carts.count()
			messages.append('new product added to cart')

	return render(request,'member/index.html',locals())

def membercart(request):
	if 'username' not in request.session.keys():
		return HttpResponseRedirect('/login/')
	messages = []
	username = request.session.get('username')
	user_id = request.session.get('user_id')
	grandtotal = 0

	try:
		user = models.User.objects.get(id=user_id)
	except:
		pass

	try:
		carts = models.Cart.objects.filter(userid=user)
		cart_count = carts.count()
		for c in carts:
			grandtotal += c.subtotal
		return render(request,'member/cart.html',locals())

	except:
		cart_count = 0
		messages.append("The cart doesn't exist")
		return HttpResponseRedirect('/member/')

def removecart(request,rev_id):
	if 'username' not in request.session.keys():
		return HttpResponseRedirect('/login/')
	messages = []
	try:
		del_cart = models.Cart.objects.get(id=rev_id)
		del_cart.delete()
		messages.append("the cart is deleted")
	except:
		messages.append("can't find the cart")

	return HttpResponseRedirect('/member/cart/')

def deletecart(request):
	if 'username' not in request.session.keys():
		return HttpResponseRedirect('/login/')
	messages = []
	user_id = request.session.get('user_id')
	try:
		user = models.User.objects.get(id=user_id)
	except:
		pass

	try:
		del_carts = models.Cart.objects.filter(userid=user)
		for cart in del_carts:
			cart.delete()
		messages.append("all carts are deleted")
	except:
		messages.append("can't find the cart")

	return HttpResponseRedirect('/member/')

def updatecart(request,upd_id):
	if 'username' not in request.session.keys():
		return HttpResponseRedirect('/login/')
	messages = []
	upd_cart = models.Cart.objects.get(id=upd_id)

	quantity = request.POST['update_quantity']
	product = models.Product.objects.get(name=upd_cart.product_name)

	upd_cart.quantity = quantity
	upd_cart.subtotal = product.price*int(quantity)
	upd_cart.save()

	messages.append("cart is updated")
	return HttpResponseRedirect('/member/cart/')

def checkout(request):
	if 'username' not in request.session.keys():
		return HttpResponseRedirect('/login/')
	messages = []
	username = request.session.get('username')
	user_id = request.session.get('user_id')
	grandtotal = 0

	try:
		user = models.User.objects.get(id=user_id)
	except:
		pass

	if(request.method == 'POST'):
		if(request.POST['order_btn']):
			name = request.POST['name']
			number = request.POST['number']
			method = request.POST['method']

			grandtotal = 0
			total_product = []
			flag = None

			try:
				carts = models.Cart.objects.filter(userid=user)
				for c in carts:
					grandtotal += c.subtotal
					total_product.append(c.product_name+"("+str(c.quantity)+")")

				str_total_product = ' '.join(total_product)
				new_order = models.Order.objects.create(name = name,phone = number,pay_method = method,total_products = str_total_product,total_price = grandtotal)
				new_order.save()
				
				#after checkout, clear his carts
				for c in carts:
					c.delete()
				flag = True


			except:
				pass

	try:
		carts = models.Cart.objects.filter(userid=user)
		cart_count = carts.count()
		for c in carts:
			grandtotal += c.subtotal
		return render(request,'member/checkout.html',locals())

	except:
		cart_count = 0
		messages.append("Your cart is empty! Cannot checkout!")
		return HttpResponseRedirect('/member/cart/')

	