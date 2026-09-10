from django.db import models
from django.utils.text import slugify
import uuid


class PhoneModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên dòng máy")
    slug = models.SlugField(max_length=100, unique=True)
    generation = models.CharField(max_length=50, verbose_name="Thế hệ", default="iPhone 16 Series")
    screen_size = models.CharField(max_length=50, verbose_name="Kích thước màn hình", default="6.1 inch")
    has_camera_control = models.BooleanField(default=False, verbose_name="Có Nút Điều Khiển Camera")
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Dòng máy iPhone"
        verbose_name_plural = "Dòng máy iPhone"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên màu (Tiếng Việt)")
    english_name = models.CharField(max_length=100, verbose_name="Tên tiếng Anh", blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    hex_code = models.CharField(max_length=20, verbose_name="Mã màu HEX")
    secondary_hex = models.CharField(max_length=20, verbose_name="Mã viền/bóng", blank=True)
    is_dark = models.BooleanField(default=False, verbose_name="Màu tối")
    is_hidden = models.BooleanField(default=False, verbose_name="Ẩn khỏi giao diện")
    order = models.IntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Màu sắc"
        verbose_name_plural = "Màu sắc"

    def __str__(self):
        return f"{self.name} ({self.english_name})" if self.english_name else self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=255, unique=True)
    tagline = models.CharField(max_length=255, verbose_name="Khẩu hiệu", blank=True)
    short_description = models.CharField(max_length=500, verbose_name="Mô tả ngắn")
    description = models.TextField(verbose_name="Mô tả chi tiết")
    base_price = models.DecimalField(max_digits=12, decimal_places=0, default=1429000, verbose_name="Giá gốc (VNĐ)")
    image_url = models.CharField(max_length=500, blank=True, verbose_name="Ảnh đại diện sản phẩm")
    badge = models.CharField(max_length=50, blank=True, default="Mới", verbose_name="Huy hiệu")
    is_new = models.BooleanField(default=True, verbose_name="Sản phẩm mới")
    is_featured = models.BooleanField(default=True, verbose_name="Nổi bật")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

    def __str__(self):
        return self.title

    @property
    def formatted_price(self):
        return f"{int(self.base_price):,}đ".replace(",", ".")

    @property
    def display_image_url(self):
        if self.image_url:
            return self.image_url
        first_variant = self.variants.filter(is_active=True).order_by('id').first()
        if first_variant:
            return first_variant.normalized_image_url
        return "/static/images/cases/case-lake-green-back.png"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    phone_model = models.ForeignKey(PhoneModel, on_delete=models.CASCADE, related_name="variants")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Mã SKU")
    price = models.DecimalField(max_digits=12, decimal_places=0, default=1429000, verbose_name="Giá bán (VNĐ)")
    stock = models.IntegerField(default=100, verbose_name="Tồn kho")
    image_url = models.CharField(max_length=500, blank=True, verbose_name="https://shopdunk.com/images/thumbs/0020896_black.jpeg")
    is_active = models.BooleanField(default=True, verbose_name="Đang kinh doanh")
    is_seeded = models.BooleanField(default=False, verbose_name="Tạo bởi seed (không xóa khi admin thêm)")

    class Meta:
        unique_together = ('product', 'phone_model', 'color')
        verbose_name = "Biến thể sản phẩm"
        verbose_name_plural = "Biến thể sản phẩm"

    def __str__(self):
        return f"{self.product.title} - {self.phone_model.name} - {self.color.name}"

    @property
    def formatted_price(self):
        return f"{int(self.price):,}đ".replace(",", ".")

    @property
    def normalized_image_url(self):
        if not self.image_url:
            return f"/static/images/cases/case-{self.color.slug}-back.png"
        if self.image_url.startswith('/static/images/cases/') and self.image_url.endswith('.svg'):
            return self.image_url.replace('.svg', '.png')
        return self.image_url

    @property
    def normalized_inside_image_url(self):
        if not self.image_url:
            return f"/static/images/cases/case-{self.color.slug}-inside.png"
        if self.image_url.startswith('/static/images/cases/') and self.image_url.endswith('.svg'):
            return self.image_url.replace('.svg', '.png').replace('-back.png', '-inside.png')
        return self.image_url


class Order(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('vietqr', 'Chuyển khoản VietQR tức thì'),
        ('apple_pay', 'Apple Pay / Thẻ Quốc Tế'),
        ('momo', 'Ví MoMo'),
    ]

    STATUS_CHOICES = [
        ('processing', 'Đang xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao thành công'),
        ('cancelled', 'Đã hủy'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('failed', 'Thất bại'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Tài khoản")
    order_code = models.CharField(max_length=32, unique=True, verbose_name="Mã đơn hàng")
    customer_name = models.CharField(max_length=150, verbose_name="Họ và tên khách hàng")
    customer_email = models.EmailField(verbose_name="Email nhận hóa đơn")
    customer_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    shipping_address = models.CharField(max_length=255, verbose_name="Địa chỉ giao hàng")
    province_city = models.CharField(max_length=100, verbose_name="Tỉnh / Thành phố")
    district = models.CharField(max_length=100, blank=True, verbose_name="Quận / Huyện")
    note = models.TextField(blank=True, verbose_name="Ghi chú đơn hàng")
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='vietqr', verbose_name="Phương thức thanh toán")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name="Trạng thái thanh toán")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name="Trạng thái đơn")
    
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Phí vận chuyển")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Tổng tiền (VNĐ)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian đặt")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"

    def __str__(self):
        return f"Đơn hàng #{self.order_code} - {self.customer_name}"

    @property
    def formatted_total(self):
        return f"{int(self.total_amount):,}đ".replace(",", ".")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    phone_model_name = models.CharField(max_length=100)
    color_name = models.CharField(max_length=100)
    color_hex = models.CharField(max_length=20, default="#000000")
    price = models.DecimalField(max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Mục đơn hàng"
        verbose_name_plural = "Mục đơn hàng"

    @property
    def subtotal(self):
        return self.price * self.quantity

    @property
    def formatted_subtotal(self):
        return f"{int(self.subtotal):,}đ".replace(",", ".")


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author_name = models.CharField(max_length=100, verbose_name="Tên người đánh giá")
    phone_model_bought = models.CharField(max_length=100, blank=True, verbose_name="Dòng máy đã mua")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Số sao (1-5)")
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    content = models.TextField(verbose_name="Nội dung đánh giá")
    is_verified = models.BooleanField(default=True, verbose_name="Đã mua hàng")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"

    def __str__(self):
        return f"{self.author_name} - {self.rating} sao - {self.title}"
