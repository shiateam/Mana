from django.contrib.admin.decorators import register
from django.db import  models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import SlugField
from django.db.models.manager import ManagerDescriptor
from django.db.models.signals import ModelSignal
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from uuid import uuid4
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib import admin


class Category(MPTTModel):
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )

    slug = models.SlugField(verbose_name=_("Category safe Url"),max_length=255,unique=True)
    parent = TreeForeignKey("self",on_delete=models.CASCADE, null=True,blank=True,related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertaion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args= [self.slug])
    
    def __str__(self):
        return self.name
    
class ProductType(models.Model):
    name = models.CharField(verbose_name=_("Product Name"),help_text=_("Required"),max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product type")

    def __str__(self):
        return self.name
    
    
class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType,related_name='typeSpecification', on_delete= models.RESTRICT)
    name = models.CharField(verbose_name= _("name"),help_text=_("Required"),max_length=255 )

    class Meta:
        verbose_name = _("product Specification")
        verbose_name_plural = _("product Specification")
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    product_type = models.ForeignKey(ProductType,related_name='brandType', on_delete= models.RESTRICT)
    name = models.CharField(verbose_name= _("name"),help_text=_("Required"),max_length=255 )

    class Meta:
        verbose_name = _("product Brand")
        verbose_name_plural = _("product Brand")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    product_type = models.ForeignKey(ProductType,on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
      verbose_name=_("title"),help_text=_("Required"), max_length=255,
    )
    brand = models.ForeignKey(Brand,on_delete=models.RESTRICT)

    description = models.TextField(
      verbose_name=_("description"),help_text=_("Not Required"), blank=True 
    )
    slug = SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("Maximum 999.99"),
        error_messages= {
            "name":{
                "max_length":_("The price must be between 0 and 999.99."),
            },
        },
        max_digits= 5,
        decimal_places=2,
    )
    is_active = models.BooleanField(
      verbose_name=_("Product Visibility"),help_text=_("Change Product Visibility"), default=True,  
    )
    inventory = models.IntegerField(validators=[MinValueValidator(0)] ,default=1)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True , editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now = True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title
    
class ProductSpecificationValue(models.Model):

    product = models.ForeignKey(Product , related_name='productSpecificationValue',on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification,related_name='specificationValue',on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name= _("value"),
        help_text=_("Product specification value (maximum of 255 words"),
        max_length=255 
    )

    class Meta:
        verbose_name = _("Product specification value")
        verbose_name_plural = _("Product specification values")
    
    def __str__(self):
        return self.value
    

class ProductImage(models.Model):
    porduct = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_image")
    image = models.ImageField (
        verbose_name= _("image"),
        help_text=_("Upload a product image"),
        upload_to = "images/",
        default = "images/default.png",
    )
    alt_text = models.CharField(
        verbose_name= _("Alturnative text"),
        help_text=_("please add alturnative text"),
        max_length=255 ,
        null=True,
        blank=True
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField( auto_now_add=True , editable=False)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

class Cart(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    send_price = models.DecimalField(verbose_name=_("Send Price"),
        help_text=_("Maximum 999.999"),
        error_messages= {
            "name":{
                "max_length":_("The price must be between 0 and 999.999."),
            },
        },
        max_digits= 6,
        decimal_places=3,
        default=380.000)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators = [MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart','product']]

class Customer(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    city = models.CharField(max_length=225)
    address = models.CharField(max_length=550)
    province = models.CharField(max_length=225)
    post = models.CharField(max_length=225)



    def __str__(self):
        return f'{self.user.username}'


    # @admin.display(ordering='first_name')
    # def first_name(self):
    #     return self.first_name

    # @admin.display(ordering='last_name')
    # def last_name(self):
    #     return self.last_name
    

    class Meta:
        ordering = ['user__username']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'در حال پرداخت'
    PAYMENT_STATUS_COMPLETE = 'پرداخت شده'
    PAYMENT_STATUS_FAILED = 'پرداخت نشده'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
        (PAYMENT_STATUS_FAILED,'Failed'),

    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=13,choices=PAYMENT_STATUS_CHOICES,default= PAYMENT_STATUS_FAILED,

    )
    customer = models.ForeignKey(Customer,on_delete= models.PROTECT,related_name='order')
    Authority = models.CharField(max_length=1100 , default=0)

    def get_total_price(self):
       return sum([item.quantity * item.unit_price for item in self.items.all()]) 
    
    def __str__(self):
        return f'{self.customer.first_name} {self.customer.last_name}'

class OrderItem (models.Model):
    order = models.ForeignKey(Order,on_delete=PROTECT , related_name='items')
    product = models.ForeignKey(Product,on_delete=PROTECT , related_name= 'orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=3)

    def __str__(self):
        return f'{self.product.title}'

class SpesialProduct (models.Model):
    product = models.ForeignKey(Product,on_delete=PROTECT )

    def __str__(self):
        return f'{self.product.title}'

class BestSellingProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=PROTECT )

class LastProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=PROTECT )

class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=PROTECT,related_name="product_comment" )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255)
    text = models.TextField()

class Slider(models.Model):
    image_1 = models.ImageField(
        verbose_name= _("slider1"),
        help_text=_("Upload a product image"),
        upload_to = "images/",
        default = "images/default.png",
    )
    image_2 = models.ImageField(
        verbose_name= _("slider2"),
        help_text=_("Upload a product image"),
        upload_to = "images/",
        default = "images/default.png",
    )
    image_3 = models.ImageField(
        verbose_name= _("slider3"),
        help_text=_("Upload a product image"),
        upload_to = "images/",
        default = "images/default.png",
    )


