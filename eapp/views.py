from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from eapp.forms import AddressForm, ContactForm, CustomAuthenticationForm, ProfileForm, RegisterForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from eapp.models import Address, Cart, Category, Order, Product, Profile, Wishlist


def home(request):
    all_products = Product.objects.all()[0:12]
    context = {
        'all_products':all_products,
    }
    return render(request, 'home.html',context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    in_cart = False
    in_wishlist = False

    if request.user.is_authenticated:
        product_id = product.id
        in_cart = Cart.objects.filter(user=request.user, product=product_id).exists()
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product_id).exists()

    context = {
        'in_cart': in_cart,
        'in_wishlist': in_wishlist,
        'products': product,
    }
  
    return render(request, 'product_detail.html', context)


def category(request, catslug):
    query = get_object_or_404(Category, slug=catslug)
    products = Product.objects.filter(category=query)
    all_cat = Category.objects.all()
    price_lte = request.GET.get('price_lte')
    price_gte = request.GET.get('price_gte')
    

    if price_lte:
        products = products.filter(price__lte=price_lte)
    if price_gte:
        products = products.filter(price__gte=price_gte)

    context = {
        'products': products,
        'all_cats': all_cat,
        'category_search': query,
        
        
    }
    return render(request, 'category_results.html', context)


@login_required
def add_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id = product_id)
    Cart(user=user,product=product).save()
    return redirect('show_cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)       
        context = {
            'cart_items':cart_items,                  
         }

    return render(request,'cart.html',context)


def del_cart(request,pk):
    cart_item = Cart.objects.get(user=request.user, id=pk)
    cart_item.delete()
    return redirect('show_cart')


def increase_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect(reverse('show_cart'))

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect(reverse('show_cart'))


@login_required
def check_out(request):
   addresses = Address.objects.filter(user=request.user)
   cart_items = Cart.objects.filter(user = request.user)
   total_amount = sum(item.product.price * item.quantity for item in cart_items)
   shipping_charge = 70
   total_amount_with_shipping = total_amount + shipping_charge
   
   context = {
        'alladdresses': addresses,
        'total_amount':total_amount,
        'cart_items':cart_items,
        'shipping_charge':shipping_charge,
        'total_amount_with_shipping':total_amount_with_shipping,
       

    }

   return render(request, 'checkout.html',context)

@login_required
def payment_done(request):
    user = request.user
    customer_address = request.GET.get('addid')
    address = get_object_or_404(Address,id = customer_address)
    cart = Cart.objects.filter(user = user)
    for c in cart:
        Order(user=user,product=c.product,quantity=c.quantity,address=address).save()
        c.delete()
    return redirect('myorders')


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account Created Successfully!')
            form.save()
            form = RegisterForm()
            
    else:
        form = RegisterForm()
    return render(request, 'register_form.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user = authenticate(username=uname, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully!')
                return redirect('profile')

    else:
        form = CustomAuthenticationForm()
    login_messages = messages.get_messages(request)
    return render(request, 'login_form.html', {'form': form, 'login_messages': login_messages})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def create_profile(request):
    try:
        profile = request.user.profile  # Try to get the user's profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Assign the logged-in user to the profile
            profile.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')

    else:
        form = ProfileForm(instance=profile)
    profile_messages = messages.get_messages(request)
    return render(request, 'profileform.html', {'form': form, 'profile_messages': profile_messages,'profile':profile})


@login_required
def address(request):
    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Address updated!')
            return redirect('address')

    else:
        form = AddressForm()

    context = {
        'form':form,
        'alladdress':address,
    }    

    return render(request, 'addresses.html',context)

def del_add(request,pk):
    address = Address.objects.get(user = request.user,id=pk)
    address.delete()
    return redirect('address')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Mail sent succesfully!')
            form = ContactForm() 
    else:
        form = ContactForm()        
    return render(request,'contact.html',{'form':form})


def search(request):
    query = request.GET['query']
    search_result = Product.objects.filter(name__icontains=query)
    context = {
        'search_query': query,
        'search_results': search_result,

    }
    return render(request,'search_results.html',context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request,'my_orders.html',{'orders':orders})

@login_required
def add_wishlist(request):
    user = request.user
    product_id = request.GET.get('wishlist')
    product = Product.objects.get(id = product_id)
    Wishlist(user=user,product=product).save()
    return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request,'wishlist.html',{'allwishlist':wishlist})

def del_wishlist(request,pk):
    wishlist = Wishlist.objects.get(user=request.user,id = pk)
    wishlist.delete()
    return redirect('wishlist')

@login_required
def review(request) : 
    if request.method == 'POST':
        fm = ReviewForm(request.POST)
        if fm.is_valid():
            fm.save()
    else:
        fm = ReviewForm()       
  
    return render(request, 'review_form.html',{'form':fm})

def about_us(request):
    return render(request,'aboutus.html')