from decimal import Context
from rest_framework import status 
from rest_framework.filters import SearchFilter
from django.http import HttpResponseRedirect, request, response
from django.urls.conf import include
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.serializers import Serializer

from store.paginations import LargeResultsSetPagination
from .models import BestSellingProduct, Comment, LastProduct, Product as ProductModel, SpesialProduct
from rest_framework import generics,viewsets
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated , AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from zeep import Client
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_json_api import django_filters,filters
import re
from rest_framework_json_api.filters import QueryParameterValidationFilter,OrderingFilter

from django.http import HttpResponse ,JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://mana-medical.ir/order-success' # Important: need to edit for realy server.
MERCHANT = 'f4b9f8e6-64ef-4f2e-b542-7a2db0518a41'

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

class CategoryView(generics.RetrieveAPIView):
    lookup_field = "slug"
    queryset = Category.objects.all()
    serializer_class= ChildrenSerializer
    
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
        customer = Customer.objects.get(user_id = request.user.id)
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
    amount = 100
    def get_permissions(self):
        if self.request.method == ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context = {'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        Status = serializer.validated_data['Status']
        Authority = serializer.validated_data['Authority']
        if Status =='OK':
            order = serializer.save()
            result = client.service.PaymentVerification(MERCHANT,Authority,order.get_total_price())    
        # if result.Status == 100:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return JsonResponse(messages = "تراکنش توسط شما لغو گردید", status=status.HTTP_400_BAD_REQUEST)

  



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

        customer_id  = Customer.objects.only('id').get(user_id = user.id)
        return Order.objects.filter(customer_id = customer_id)

    @action(detail= False , methods=['POST'])
    def verify(self,request):
       
        serializer = zarinpallSerializer(data = request.data)
        if serializer.is_valid():
            Authority = serializer.validated_data['Authority']
            price = serializer.validated_data['price']
            result = client.service.PaymentVerification(MERCHANT,Authority,price)
        if result.Status != 100:
          return Response(serializer.error, status=status.HTTP_200_OK)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
          
    @action(detail= False , methods=['POST'])
    def go_to_zarinpal(self,request):
        serializer = getTotalPriceSerializer(data = request.data)
        if serializer.is_valid():
            price = serializer.validated_data['price']
            result = client.service.PaymentRequest(MERCHANT,price, description, email, mobile, CallbackURL)
            if result.Status == 100:
                serializer = zarinpallSerializer(result)
                return Response(serializer.data,status = status.HTTP_200_OK)
            else:
                return JsonResponse(status = status.HTTP_406_NOT_ACCEPTABLE)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Comment.objects.prefetch_related('product').all()
    serializer_class = CommentSerializer 
    
class SliderViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer



        