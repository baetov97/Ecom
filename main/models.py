from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.utils.translation import get_language, gettext_lazy as _
from django_resized import ResizedImageField
from django.contrib.contenttypes.models import ContentType


class Category(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=256)
    image = ResizedImageField(verbose_name=_('image'), upload_to="category/", size=[400, 250], quality=100)
    slug = models.SlugField(verbose_name=_('slug field'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        unique_together = ('name', 'slug')


class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('subcategory'), on_delete=models.CASCADE,
                                 related_name='subcategories')
    image = ResizedImageField(verbose_name=_('image'), upload_to="subcategory/", size=[400, 250], quality=100)
    name = models.CharField(verbose_name=_('name of subcategory'), max_length=256)
    slug = models.SlugField(verbose_name=_('slug field'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subcategory'
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')


class Product(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=200, null=True)
    description = models.TextField(verbose_name=_('description'))
    price = models.DecimalField(verbose_name=_('price'), max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, verbose_name=_('digital of product'))
    image = models.ImageField(upload_to='images', verbose_name=_('image'), null=True, blank=True)
    slug = models.SlugField(verbose_name=_('slug field'), max_length=256, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        unique_together = ('name', 'slug')

    def __str__(self):
        return self.name

    @property
    def imageURl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.SET_NULL, null=True,
                                 blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name=_('date ordered'))
    complete = models.BooleanField(default=False, null=True, blank=False, verbose_name='completed')
    transaction_id = models.CharField(verbose_name=_('transaction'), max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, verbose_name=_('order'), blank=True, null=True)
    quantity = models.IntegerField(default=0, verbose_name=_('quantity of product in the order'), null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('date added'))

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.SET_NULL,
                                 blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, verbose_name=_('order'), blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name=_('address'), null=True)
    city = models.CharField(max_length=200, verbose_name=_('city'), null=True)
    state = models.CharField(max_length=200, verbose_name=_('state'), null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('date added'))

    def __str__(self):
        return self.address


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name="reviews",
                             on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name="reviews", on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('text'))
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', on_delete=models.SET_NULL,
                               blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'review'
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
