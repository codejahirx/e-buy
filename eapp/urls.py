from .import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'), 
    path('product/<slug:slug>/',views.product_detail, name='product-detail'),
    path('category/<slug:catslug>/', views.category, name='category'),
    path('add-cart/', views.add_cart, name='add_cart'),
    path('cart/',views.show_cart, name = 'show_cart'),
    path('<int:pk>/',views.del_cart,name = 'del_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),  
    path('checkout/', views.check_out, name='check_out'),
    path('paymentdone/', views.payment_done, name='payment_done'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('profile/', views.create_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('addresses/', views.address, name='address'),
    path('address/<int:pk>/',views.del_add,name = 'del_add'),
    path('contact-us/',views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('my-orders/',views.my_orders,name='myorders'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlist/<int:pk>/',views.del_wishlist,name = 'del_wishlist'),
    path('add-to-wishlist/', views.add_wishlist, name='add_wishlist'),
    path('write-your-review/',views.review,name='review'), 
    path('about-us/',views.about_us, name = 'aboutus')  
]
