from django.contrib import admin
from .models import (Category, SubCategory, Product, Order, OrderItem, ShippingAddress, Review)


class ShippingInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_select_related = ['category']
    list_filter = ['category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'digital']
    list_editable = ['digital']
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', ]
    inlines = [ShippingInline, OrderItemInline, ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ['user', 'product']
