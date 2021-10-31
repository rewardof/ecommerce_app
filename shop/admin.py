from django.contrib import admin
from .models import Customer, Product, Category, UserProfile, Address, Cart, Order, OrderItem, Orders, ProductsGroup

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductsGroup)


