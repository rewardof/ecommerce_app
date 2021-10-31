from django.urls import path, include
from shop import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', views.UserRegisterViewSet, basename='register')
router.register('profile', views.UserProfileViewSet, basename='customer_profile')

urlpatterns = [
    path('djoser/', include('djoser.urls')),
    path('djoser/', include('djoser.urls.authtoken')),
    # path('customer/register/', views.UserRegisterViewSet, name='register'),
    path('customer/', include(router.urls)),
    path('auth/login/', views.UserLoginApiView.as_view(), name='login'),
    path('products-list/', views.ProductListApiView.as_view(), name='products-list'),
    path('products-detail/<int:pk>/', views.ProductDetailApiView.as_view(), name='products-detail'),
    path('categories/', views.CategoryListApiView.as_view(), name='categories-list'),
    path('categories/<int:pk>/products/', views.CategoryProductsView.as_view(), name='category-products'),
    path('carts/carts-list/', views.CartListApiView.as_view(), name='carts-list'),
    path('product-detail/add-to-cart/', views.AddToCartApiVIew.as_view(), name='add-to-cart'),
    path('order/order-create/', views.OrderCreateView.as_view(), name='order-create'),
    path('order/orders-list/', views.OrderListApiView.as_view(), name='orders-list'),
    path('carts/order-item-list/', views.OrderItemListApiView.as_view(), name='order-item-list'),
    path('carts/order-item-create/', views.OrderItemCreateApiView.as_view(), name='order-item-create')
]
