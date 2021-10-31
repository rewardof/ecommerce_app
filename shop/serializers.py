from rest_framework import serializers
from .models import Customer, Product, Category, UserProfile, Address, Cart, Order, Orders, OrderItem
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=20, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'password2', 'date_joined')
        # fields = '__all__'

    def create(self, validated_data):
        password = validated_data.get('password')
        print(password)
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        user = super(UserRegisterSerializer, self).create(validated_data)
        UserProfile.objects.create(user=user)
        return user

    def to_representation(self, instance):
        data = super(UserRegisterSerializer, self).to_representation(instance)
        email = data.get('email')
        return {
            'id': data.get('id'),
            'email': data.get('email'),
            'phone_number': data.get('phone_number'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'date_joined': data.get('date_joined'),
        }


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, )

    # url = serializers.HyperlinkedIdentityField(lookup_field='pk', view_name='')

    class Meta:
        model = UserProfile
        fields = ('image',)

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    # id = serializers.HyperlinkedIdentityField(view_name='customer_profile-detail')

    class Meta:
        model = Customer
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'profile')

    def update(self, instance, validated_data):
        print('updateda kirdi')
        # print(self.context)
        profile = validated_data.pop('profile')
        pk = self.context
        print(pk)
        user_profile = UserProfile.objects.update(image=profile.get('image'))
        return super(UserProfileSerializer, self).update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')

    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'label', 'discount_price', 'slug', 'image', 'description')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    # customer = serializers.SlugRelatedField(queryset=Customer.objects.all(), slug_field='first_name')

    class Meta:
        model = Cart
        fields = '__all__'

    # def create(self, validated_data):
    #     # customer = validated_data.get('customer')
    #     request = self.context.get('request')
    #     print(request.session)
    #     customer = self.context.get('request').user
    #     customer_carts = Cart.objects.filter(customer=customer)
    #     products = validated_data.get('products')
    #     for cart in customer_carts:
    #         print('for')
    #         if products == cart.products:
    #             print('if')
    #             serializers.ValidationError('This product is already in carts')
    #     data = super(CartSerializer, self).create(validated_data)
    #     return data

    # def to_representation(self, instance):
    #     data = super(CartSerializer, self).to_representation(instance)
    #     return {
    #         'customer': data.get('customer')
    #     }


class OrderCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        print('create')
        return super(OrderCreateListSerializer, self).create(validated_data)


class OrderListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        list = []
        for order in validated_data:
            order['prize'] = order.get('products').price
            list.append(order)
        validated_data = list
        order = [Order(**item) for item in validated_data]
        return Order.objects.bulk_create(order)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('customer', 'products', 'prize', 'quantity',)
        list_serializer_class = OrderListSerializer


class OrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ('user', 'products', 'shipping_address', 'delivered', 'created')


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


