from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate,login
from .models import *
def homeView(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request=request, template_name='home.html', context=context)

def signInView(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all()
        }
        return render(request=request, template_name='sign_in.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return render(request=request, template_name='home.html', context={'message': 'Successfully logged in!'})
        return render(request=request, template_name='sign_in.html', context={'error': 'Wrong email or password!'})

def signUpView(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all()
        }
        return render(request=request, template_name='sign_up.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('name')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        birth_date = request.POST.get('birthdate')
        try:
            Customer.object.get(email=email)
        except Customer.DoesNotExist:
            customer = Customer(email=email, first_name=first_name, last_name=last_name,phone=phone, birth_date=birth_date)
            customer.set_password(password)
            customer.save()
            return redirect('sign_in_url')
        else:
            context={
                'error':'This email is already taken!',
                'name': first_name,
                'last_name': last_name,
                'phone': phone,
                'birthdate': birth_date,
                'categories': Category.objects.all()
            }
            return render(request=request, template_name='sign_up.html', context=context)

def signOutView(request):
    logout(request)
    return redirect('home_url')


def productsView(request):
    context = {
        'products': Product.objects.all(),
        'categories': Category.objects.all(),
        'category': 'All Products'
    }
    return render(request=request, template_name='products.html', context=context)
def addToCartView(request, product_id):
    if 'cart' not in request.session.keys():
        request.session['cart'] = [product_id]
    else:
        request.session['cart'].append(product_id)
        request.session.modified = True
    return HttpResponse()

def cartDetailView(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all(),
        }
        total_sum = 0
        if 'cart' in request.session.keys():
            context['cart'] = []
            count = 1
            for product_id in request.session['cart']:
                product = Product.objects.get(id=product_id)
                product.count = count
                context['cart'].append(product)
                count += 1
                total_sum += product.price
        context['total'] = total_sum
        return render(request=request, template_name='cart.html', context=context)
    elif request.method == 'POST':
        total_sum = int(request.POST.get('total'))
        if request.user.wallet >= total_sum:
            request.user.wallet -= total_sum
            request.user.save()
            request.session.pop('cart')
            return redirect('profile_url')
        else:
            context = {
                'categories': Category.objects.all(),
                'error': 'You do not have enough balance in your Wallet!'
            }
        if 'cart' in request.session.keys():
            context['cart'] = []
            count = 1
            total_sum = 0
            for product_id in request.session['cart']:
                product = Product.objects.get(id=product_id)
                product.count = count
                context['cart'].append(product)
                count += 1
                total_sum += product.price
            context['total'] = total_sum
        return render(request=request, template_name='cart.html', context=context)

def profileView(request):
    if request.user.is_authenticated:
        context = {
            'categories': Category.objects.all(),
        }
        return render(request=request, template_name='profile.html', context=context)
    return redirect('sign_in_url')

def productsByCategoryView(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'categories': Category.objects.all(),
        'products': products,
        'category': category.name,
    }
    return render(request=request, template_name='products.html', context=context)

def productDetailView(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'categories': Category.objects.all(),
        'product_name': product.name,
        'product_description': product.description,
        'product_category': product.category,
        'product_manufacturer': product.manufacturer,
        'product_price': product.price,
        'product_value': product.value,
        'product_unit': product.unit,
        'product_manufacturing_date': product.manufacturing_date,
        'expired_date': product.expired_date,
        'product_image_url': product.image.url,
    }
    return render(request=request, template_name='single_product.html', context=context)


