from decimal import Context
from rest_framework import status 
from rest_framework.filters import SearchFilter
from django.http import request, response
from django.urls.conf import include
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.serializers import Serializer

from store.paginations import LargeResultsSetPagination
from .models import BestSellingProduct, LastProduct, Product as ProductModel, SpesialProduct
from rest_framework import generics,viewsets
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated , AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Category , Product
from .serializers import *
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from zeep import Client
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_json_api import django_filters,filters
import re
from rest_framework_json_api.filters import QueryParameterValidationFilter,OrderingFilter
MERCHANT = 'bdae3de6-ef15-49e6-903b-34cc18e656cb'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 5000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://127.0.0.1:4200' # Important: need to edit for realy server.
class MyQPValidator(QueryParameterValidationFilter):
    query_regex = re.compile(r'^(sort|include|page|page_size)$|^(filter|fields|page)(\[[\w\.\-]+\])?$')
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.DjangoFilterBackend , SearchFilter,OrderingFilter )
    filterset_fields = {
        'brand__name': ('exact', 'in'),
        'productSpecificationValue__value':('exact', 'in'),
        'regular_price':('gte','lte','in')
    }
    search_fields = ['title' ,'description', 'category__name', 'category__slug']
    pagination_class = LargeResultsSetPagination
    ordering_fields = ['regular_price', 'updated_at']

class Product(generics.RetrieveAPIView,generics.RetrieveUpdateAPIView):
    http_method_names = ['get' , 'patch' ]
    lookup_field = "slug"
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateProductSerializer     
        return ProductSerializer
    # serializer_class= ProductSerializer

class ProductType(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = ProductType.objects.all()
    serializer_class= ProductTypeSerializer

class CategoryItemView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (django_filters.DjangoFilterBackend ,SearchFilter,OrderingFilter)
    pagination_class = LargeResultsSetPagination
    filterset_fields = {
        'brand__name': ('exact', 'in'),
        'productSpecificationValue__value':('exact', 'in'),
        'regular_price':('gte','lte','in')
    }
    search_fields = ['description','productSpecificationValue__value','brand__name','category__slug']
    ordering_fields = ['regular_price', 'updated_at']
    def get_queryset(self):
        return ProductModel.objects.filter(category__in = Category.objects.get(slug =self.kwargs["slug"]).get_descendants(include_self = True)
        )
  

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(level = 1)
    serializer_class = CategorySerializer

class SpesialProductViewSet(ModelViewSet):

    http_method_names = ['get']
    queryset = SpesialProduct.objects.all()
    serializer_class = SpesialProdutSerializer

class BestSellingProductViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = BestSellingProduct.objects.all()
    serializer_class = SpesialProdutSerializer

class LastProductViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = LastProduct.objects.all()
    serializer_class = SpesialProdutSerializer

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItamViewSet(ModelViewSet):
    http_method_names = ['get' , 'post', 'patch' , 'delete']

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return AddCartItemSerializer 
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id = self.kwargs['cart_pk'])\
                .select_related('product')


class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail= False , methods=['GET','PUT'])
    def me(self,request):
        (customer,created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer  = CustomerSerializer(customer)
            return Response(serializer.data)  
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)  

class OrderViewSet(ModelViewSet):

    http_method_names = ['patch','get','post','delete','head','options']

    def get_permissions(self):
        if self.request.method == ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context = {'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        # result = client.service.PaymentRequest(MERCHANT, order.get_total_price(), description, email, mobile, CallbackURL)
        # if result.Status != 100:
        order.Authority = "A10000"
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        # serializer  = zarinpallSerializer(result)
        # return Response(serializer.data) 
  



    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
            
        return OrderSerializer
    


    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        (customer_id , created) = Customer.objects.only('id').get_or_create(user_id = user.id)
        return Order.objects.filter(customer_id = customer_id)

    # @action(detail= False , methods=['POST'])
    # def verify(self,request):
    #     order = UpdateOrderSerializer(data = request.data)
    #     order.is_valid(raise_exception=True)
    #     # result = client.service.PaymentVerification(MERCHANT, serializer.Authority, serializer.get_total_price())
    #     # if result.Status != 100:
    #     return Response(status=status.HTTP_200_OK)
    #     # serializer = OrderSerializer(order)
    #     # return Response(serializer.data)


        