from rest_framework import serializers
from . models import category, Product, CustomUser, Order, OrderItem, Cart, CartItem
from django.contrib.auth.password_validation import validate_password
#from . models import 



class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model= category
        fields='__all__'

class usersignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2=serializers.CharField(write_only=True, required=True)
    user_type = serializers.ChoiceField(choices=[('Seller', 'Seller'), ('User', 'User')])

    class Meta:
        model=CustomUser
        fields=["username","email","first_name","last_name","user_type","password","password2"]

    def validate(self,attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password":"password fields does not match"})
        return attrs

    def create(self,validated_data):
        user_type = validated_data.pop('user_type')
        user=CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        print(user)
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=("name","description","price","category","stock","image")

class addProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=("name","description","price","image")

class userloginSerializer(serializers.ModelSerializer):
    # username=serializers.CharField()
    # password=serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields=["username","password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Product
#         fields=["quantity"]
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product','product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items']
        read_only_fields = ['user', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=OrderItem
        fields=['product','quantity','price']


class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    
    class Meta:
        model=Order
        fields=["id","created_at","updated_at","is_completed","items"]
        read_only_fields=["created_at","updated_at"]

    def create(self,validated_data):
        items_data=validated_data.pop('items')
        order=Order.objects.create()
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


