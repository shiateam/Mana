from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *

admin.site.register(Category,MPTTModelAdmin)

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification

class BrandInline(admin.TabularInline):
    model = Brand

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,BrandInline
    ]
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
   model= Brand
   
class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline
    ]

class CartItemInline(admin.TabularInline):
    model = CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

class OrderInline(admin.TabularInline):
    model = Order 

class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # list_display = ['first_name' , 'last_name']
    list_per_page = 10
    inlines = [OrderInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = ['first_name' , 'last_name']
    list_per_page = 10
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    # list_display = ['first_name' , 'last_name']
    list_per_page = 10
    # inlines = [OrderItemInline] 

@admin.register(SpesialProduct)
class SpesialProductAdmin(admin.ModelAdmin):
   model: SpesialProduct

@admin.register(BestSellingProduct)
class BestSellingProductAdmin(admin.ModelAdmin):
  model: BestSellingProduct

@admin.register(LastProduct)
class LastProductAdmin(admin.ModelAdmin):
    model: LastProduct