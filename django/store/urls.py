from django.db import router
from django.urls import path
from rest_framework import routers
from rest_framework_nested import routers
from . import views

app_name = "store"
router = routers.DefaultRouter()
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)
router.register('orders',views.OrderViewSet,basename='orders')
router.register('spesial',views.SpesialProductViewSet)
router.register('best-selling',views.BestSellingProductViewSet)
router.register('last',views.LastProductViewSet)
router.register('comment',views.CommentViewSet)
carts_router = routers.NestedDefaultRouter(router ,'carts',lookup = 'cart')
carts_router.register('items',views.CartItamViewSet, basename = 'cart-items-detail')

urlpatterns = [
    path("api/",views.ProductListView.as_view(),name="store_home"),
    path("api/category",views.CategoryListView.as_view(),name="categories"),
    path("api/<slug:slug>/",views.Product.as_view(),name="product"),
    path("api/category/<slug:slug>/",views.CategoryItemView.as_view(),name="category_items"),
    path("api/type/<int:id>",views.ProductType.as_view(),name="product_types"),
    

] + router.urls + carts_router.urls
