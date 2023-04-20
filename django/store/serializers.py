from pickle import TRUE
import re
from django.db import models
from django.db.models import fields
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import server_error

from .models import Brand, Cart, CartItem, Comment, Customer, Order, OrderItem, Product , Category, ProductImage, ProductSpecification, ProductSpecificationValue, ProductType, SpesialProduct

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ["image", "alt_text"]

class BrandSerializer(serializers.ModelSerializer):


    class Meta:
        model = Brand
        fields = ["name"]
class CommentSerializer(serializers.ModelSerializer):

   

    class Meta:
        model = Comment
        fields = ['product','author','text']
class ProductSpecificationValueSerializer(serializers.ModelSerializer):

    specification = serializers.CharField()
    class Meta:
        model =  ProductSpecificationValue
        fields = ["value","specification"]

class ProductSpecificationSerializer(serializers.ModelSerializer):
    specificationValue = ProductSpecificationValueSerializer(many=True)
    class Meta:
            model = ProductSpecification
            fields = ["name","specificationValue"]

class ProductTypeSerializer(serializers.ModelSerializer):

    typeSpecification = ProductSpecificationSerializer(many=True)
    brandType = BrandSerializer(many=True)
    class Meta:
        model = ProductType
        fields = ["name", "is_active", "typeSpecification","brandType"]






class ChildrenSerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ["name","slug"]

class CategoryItemSerializer(serializers.ModelSerializer):

    children = ChildrenSerializer(many = True)
    class Meta:
        model = Category
        fields = ["name","slug","children"]

class CategorySerializer(serializers.ModelSerializer):

    children = CategoryItemSerializer(many = True)

    class Meta:
        model = Category
        fields = ["name","slug","children"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    productSpecificationValue = ProductSpecificationValueSerializer(many = True)
    brand = serializers.CharField()
    product_image =ImageSerializer(many =True)
    product_comment = CommentSerializer(many = True)
    class Meta:
        model = Product
        fields = ["id","title","category","brand","product_type", "description","slug","regular_price","productSpecificationValue","inventory","product_image", "product_comment"]

class SpesialProdutSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = SpesialProduct
        fields = ['product']

class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['inventory']
    

class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.regular_price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']


class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many = True ,read_only = True )
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart):
       return sum([item.quantity * item.product.regular_price for item in cart.items.all()]) 

    class Meta:
        model = Cart
        fields = ['id','items','send_price','total_price']

class AddCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('No Product with this id')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id , product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
           self.instance =  CartItem.objects.create(cart_id = cart_id , **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=CartItem
        fields = ['quantity']




class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','unit_price','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many  = True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,order):
       return sum([item.quantity * item.unit_price for item in order.items.all()]) 

    class Meta:
        model = Order
        fields = ['id','customer', 'placed_at','payment_status','items','Authority','total_price']

class UpdateOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):

    cart_id = serializers.UUIDField()
    Status = serializers.CharField()
    Authority = serializers.CharField()

    def validate_cart_id (self,cart_id):
        if not Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError('no cart with the given Id')
        if CartItem.objects.filter(cart_id = cart_id).count()==0:
            raise serializers.ValidationError('the cart is empty')
        return cart_id



    def save(self, **kwargs):

        with transaction.atomic():

            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id = self.context['user_id'])
            order = Order.objects.create(customer = customer)

            cart_items =  CartItem.objects.select_related('product').filter(cart_id = cart_id)

            order_items =[

                OrderItem(
                    order = order,
                    product = item.product,
                    unit_price = item.product.regular_price,
                    quantity = item.quantity

                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk = cart_id).delete()
            return order
    
class zarinpallSerializer(serializers.Serializer):
    Status = serializers.IntegerField()
    Authority = serializers.CharField()

class getTotalPriceSerializer(serializers.Serializer):
    price = serializers.IntegerField()

class CustomerSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(read_only = True)
    order = OrderSerializer(many = True)

    class Meta:
        model = Customer
        fields = ['id','first_name' ,'last_name','city','address','province','user_username','post','order']
