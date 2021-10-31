import django_filters
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import mixins
# from django_filters import filters
from rest_framework import filters

from shop import custompermissions
from rest_framework import views

from .models import Customer, Product, Category, UserProfile, Address, Cart, Order, Orders, OrderItem
from .serializers import UserRegisterSerializer, UserProfileSerializer, ProductSerializer, CategorySerializer, \
    CartSerializer, OrderCreateSerializer, OrdersListSerializer, UserLoginSerializer, OrderItemListSerializer, \
    OrderItemCreateSerializer


# class UserRegisterApiView(generics.ListCreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = UserRegisterSerializer


class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = UserRegisterSerializer

    filter_fields = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    ordering_fields = ('email',)

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email is None:
            email = ''
        first_name = self.request.query_params.get('first_name')
        if first_name is None:
            first_name = ''
        last_name = self.request.query_params.get('last_name')
        if last_name is None:
            last_name = ''
        result = Customer.objects.filter(
            Q(email__icontains=email) | Q(first_name__icontains=first_name) | Q(last_name__icontains=last_name))
        return result


class UserLoginApiView(APIView):

    def get(self, request):
        email = request.data['email']
        print(email)
        user = Customer.objects.get(email=email)
        token = Token.objects.get(user=user)
        print(token)
        data = {
            'user': email,
            'token': token.key
        }
        # data = JSONRenderer.render()
        return Response(data, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = Customer.objects.all()
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        users_profile = self.get_queryset()
        serializer = self.get_serializer(users_profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserProfileSerializer(instance=instance, data=request.data, context=kwargs)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(serializer.data)
        return Response(serializer.data)

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class ProductFilter(django_filters.FilterSet):
    to_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    from_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')

    class Meta:
        model = Product
        fields = (
            'to_price',
            'from_price',
            'name',
            'category',
            'label'
        )


class ProductListApiView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.AllowAny]
    # filter_backends = [DjangoFilterBackend, ]
    filter_class = ProductFilter
    filter_fields = ('name', 'category', 'label')
    search_fields = ('name', 'description')
    ordering_fields = ('name',)


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CategoryListApiView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryProductsView(APIView):

    def get(self, request, *args, **kwargs):
        category_pk = kwargs.get('pk')
        category = Category.objects.get(pk=category_pk)
        category_products = Product.objects.filter(category=category)
        serializer = ProductSerializer(category_products, many=True)
        data = {
            'category': category.name,
            'products': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


# @api_view(['GET', 'POST'])
# @permission_classes([permissions.IsAuthenticated])
# def add_product_to_cart_view(request):
#     customer = request.user
#     order, created = Order.objects


class AddToCartApiVIew(generics.CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        customer = request.user
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        cart = Cart.objects.filter(customer=customer, product=product)
        if cart.exists():
            customer_cart = cart[0]
            quantity = request.data.get('quantity')
            if quantity:
                customer_cart.quantity += int(quantity)
            else:
                customer_cart.quantity += 1
            customer_cart.save()
            return redirect('carts-list')
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CartListApiView(generics.ListAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    # def get_queryset(self):
    #     return Cart.objects.filter(customer=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderListApiView(generics.ListAPIView):
    serializer_class = OrdersListSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def filter_queryset(self, queryset):
        queryset = queryset.filter(customer=self.request.user)
        return queryset


class OrderItemListApiView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemListSerializer
    filter_fields = ('products', 'user')


class OrderItemCreateApiView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializer


