from django.contrib import admin

from eapp.models import Address, Cart, Category, Contact, Order, Product, Profile, Review, Wishlist


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'user', )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'phone', 'street', 'city',
                    'zipcode', 'state',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug', 'description', 'image', 'price', )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'review', 'product',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'product', 'quantity', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product',
                    'ordered_date', 'quantity', 'order_status', )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','message')

@admin.register(Wishlist)    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user','product')