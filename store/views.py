from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.contrib.auth.hashers import make_password, check_password

    # Create your views here.


def index(request):
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        data = {}
        if categoryID:
           products = Product.get_all_products_by_categoryid(categoryID)
        else:
           products = Product.get_all_products()
           data['products'] = products
           data['categories'] = categories

        return render(request, 'index.html', data)

def validateCustomer(customer):
        error_message=None
        if(not customer.first_name):
         error_message = "First name Required!"
        elif len(customer.first_name) < 4:
         error_message = "First name must be 4 charatcer long!"
        elif customer.last_name:
         error_message = "Last name Required!"

        elif len(customer.last_name) < 4:
         error_message = "Last name must be 4 charatcer long!"
        elif not customer.phone:
          error_message = "Last name Required!"
        elif len(customer.phone) < 15:
         error_message = "Phone must be 10 charatcer long!"
        elif not customer.password:
         error_message = "Password Required!"

        elif len(customer.password) < 6:
         error_message = "Password must be 6 charatcer long!"
        elif customer.isExists():
               error_message = "Email Allready registered"
        return error_message

def registerUser(request):

        postDate = request.POST
        first_name = postDate.get('firstname')
        last_name = postDate.get('lastname')
        email = postDate.get('email')
        password = postDate.get('password')
        phone = postDate.get('phone')
        # validation
        value={
          'first_name':first_name,
          'last_name':last_name,
          "phone":phone,
          'email':email,




        }
        error_message = None


        customer = Customer(first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        password=password)

        error_message=validateCustomer(customer)

        if not error_message:
         print(first_name, last_name, phone, email, password)
        customer = Customer( first_name=first_name,last_name=last_name,phone=phone, email=email, password=password)
        customer.password=make_password(customer.password)
        customer.register()
        return redirect('homepage')
        
        data = {
         'error':error_message,
      'values':value
    }
        return render(request, 'signup.html', data)

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
