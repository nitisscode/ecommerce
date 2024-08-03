from django.shortcuts import render, redirect
from . serializers import categorySerializer, usersignupSerializer, ProductSerializer, userloginSerializer, OrderItemSerializer, OrderSerializer, CartSerializer, CartItemSerializer, addProductSerializer
from rest_framework import viewsets,generics, status, mixins
from rest_framework.views import APIView
from . models import category, CustomUser, Product, Order, OrderItem, Cart, CartItem
from django.contrib.auth import authenticate,login,logout
#from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, user_passes_test
from .permissions import IsSeller
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
#from rest_framework.renderers import JSONRenderer
# Create your views here.

# def is_seller(user):
#     return user.user_type == 'Seller'


class categoryViewSet(generics.ListCreateAPIView):
    queryset=category.objects.all()
    serializer_class=categorySerializer


class category_details(generics.RetrieveUpdateDestroyAPIView):
    queryset=category.objects.all()
    serializer_class=categorySerializer

class user_signup(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=usersignupSerializer
    #return redirect("login")

class user_login(APIView):
    serializer_class=userloginSerializer
    def post(self, request):
         username = request.data.get('username')
         password = request.data.get('password')
         
         user = CustomUser.objects.filter(username=username).first()
         print(username,password,user)
         if user is None:
             return Response({'message':'User not Regitsered, Please Signup'}, status=status.HTTP_404_NOT_FOUND)
         
         if not user.check_password(password):
             return Response({'message':'wrong password, Please try again'}, status=status.HTTP_400_BAD_REQUEST)
         # i will create a token here, where i will hide the information of logged in user
         login(request,user)
         print(user)
         return redirect("add_category")

class user_logout(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        logout(request)

        return Response(status=status.HTTP_200_OK)
        
#@user_passes_test(is_seller)
class create_product(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticated]
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class edit_product(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticated]
    permission_classes = [IsSeller]

    def perform_create(self,request, serializer):
        serializer.save(seller=self.request.user)

class show_products(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

class add_product_cart(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=addProductSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartItemCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    #queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
        
# class CartItemCreateView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Product.objects.all()
#     serializer_class = addProductSerializer
#     #renderer_classes = [JSONRenderer]

#     def get(self, request, *args, **kwargs):
#         product = self.get_object()
#         serializer = self.get_serializer(product)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         product = self.get_object()
#         cart, created = Cart.objects.get_or_create(user=self.request.user)
#         data = {
#             "product": product.id,
#             "quantity": request.data.get("quantity", 1)
#         }
#         serializer = CartItemSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save(cart=cart, product=product)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)