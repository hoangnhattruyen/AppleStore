from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import PhoneModel, Color, Product, ProductVariant, Order, OrderItem, Review


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].label_from_instance = lambda obj: format_html(
            '<span style="display:inline-flex; align-items:center; gap:8px;">'
            '<span style="display:inline-block; width:14px; height:14px; border-radius:50%; background-color:{}; border:1px solid #aaa;"></span>'
            '{}'
            '</span>',
            obj.hex_code,
            obj.name,
        )


@admin.register(PhoneModel)
class PhoneModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'generation', 'screen_size', 'has_camera_control', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'generation')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color_preview', 'name', 'english_name', 'hex_code', 'is_dark', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'english_name', 'hex_code')

    def color_preview(self, obj):
        return format_html(
            '<span style="display:inline-block; width:22px; height:22px; border-radius:50%; background-color:{}; border:1px solid #ccc; vertical-align:middle; margin-right:8px;"></span>{}',
            obj.hex_code,
            obj.name
        )
    color_preview.short_description = "Xem màu"


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    form = ProductVariantForm
    extra = 1
    fields = ('phone_model', 'color', 'sku', 'price', 'stock', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'base_price', 'is_new', 'is_featured', 'created_at')
    list_filter = ('is_new', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    form = ProductVariantForm
    list_display = ('sku', 'product', 'phone_model', 'color_badge', 'price', 'stock', 'is_active')
    list_filter = ('phone_model', 'color', 'is_active')
    search_fields = ('sku', 'product__title', 'phone_model__name')

    def color_badge(self, obj):
        return format_html(
            '<span style="display:inline-flex; align-items:center; gap:6px;"><span style="display:inline-block; width:16px; height:16px; border-radius:50%; background-color:{}; border:1px solid #aaa;"></span>{}</span>',
            obj.color.hex_code,
            obj.color.name
        )
    color_badge.short_description = "Màu sắc"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'phone_model_name', 'color_name', 'color_preview', 'price', 'quantity', 'subtotal')

    def color_preview(self, obj):
        return format_html(
            '<span style="display:inline-block; width:16px; height:16px; border-radius:50%; background:{}; border:1px solid #999;"></span>',
            obj.color_hex
        )
    color_preview.short_description = "Màu"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'customer_name', 'customer_phone', 'total_amount_formatted', 'payment_method_badge', 'payment_status', 'status', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_code', 'customer_name', 'customer_phone', 'customer_email')
    inlines = [OrderItemInline]
    readonly_fields = ('order_code', 'created_at', 'updated_at')

    def total_amount_formatted(self, obj):
        return obj.formatted_total
    total_amount_formatted.short_description = "Tổng tiền"

    def payment_method_badge(self, obj):
        return dict(Order.PAYMENT_METHODS).get(obj.payment_method, obj.payment_method)
    payment_method_badge.short_description = "Phương thức TT"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'product', 'rating_stars', 'phone_model_bought', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified')
    search_fields = ('author_name', 'title', 'content')

    def rating_stars(self, obj):
        return '⭐' * obj.rating
    rating_stars.short_description = "Đánh giá"
