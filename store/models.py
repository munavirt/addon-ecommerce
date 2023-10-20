from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe

from django.utils import timezone
from timeago import format


# Create your models here.

class Category(models.Model):
    category_name   = models.CharField(max_length=30)
    slug            = models.SlugField(max_length=100,unique=True)
    description     = models.TextField(max_length=255, blank=True)
    category_image  = models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
    
    def __str__(self):
        return self.category_name



class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200,unique=True)
    description     = models.TextField(max_length=500,blank=True)
    old_price       = models.FloatField()
    new_price       = models.FloatField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    
    def is_stock_zero(self):
        if self.stock == 0:
            return mark_safe('<a href="{}">{} - out of stock </a>'.format(self.get_url(),self.product_name))
        return ''
    
class Banner(models.Model):
    banner_name    = models.CharField(max_length=200, unique=True)
    b_description     = models.TextField(max_length=500,blank=True)
    price           = models.FloatField()
    b_images          = models.ImageField(upload_to='photos/banners')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    
  
    def __str__(self):
        return self.banner_name
    
    def get_related_products(self):
        if self.is_available:
            related_products = Product.objects.filter(
                product_name__startswith=self.banner_name
            )
            return related_products
        return None
    

class ContactUs(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(default='hey boii')
    sent_time = models.DateTimeField(auto_now_add=True)
    def time_ago(self):
        now = timezone.now()
        time_diff = format(self.sent_time,now)
        return time_diff

    def __str__(self):
        return self.name