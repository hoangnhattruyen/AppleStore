import json
import uuid
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.db.models import Q
from .models import PhoneModel, Color, Product, ProductVariant, Order, OrderItem, Review
from .cart import Cart


def index(request):
    featured_products = Product.objects.filter(is_featured=True).prefetch_related('variants__color', 'variants__phone_model')
    hero_product = Product.objects.filter(slug='op-lung-silicon-magsafe-iphone-16').first() or featured_products.first()
    
    phone_models = PhoneModel.objects.all().order_by('order')
    colors = Color.objects.filter(is_hidden=False).order_by('order')
    reviews = Review.objects.all().order_by('-created_at')[:6]

    context = {
        'hero_product': hero_product,
        'featured_products': featured_products,
        'phone_models': phone_models,
        'colors': colors,
        'reviews': reviews,
    }
    return render(request, 'shop/index.html', context)


def product_list(request):
    selected_model_slug = request.GET.get('model', '')
    selected_color_slug = request.GET.get('color', '')
    search_query = request.GET.get('q', '').strip()

    products = Product.objects.all().prefetch_related('variants__color', 'variants__phone_model')
    phone_models = PhoneModel.objects.all().order_by('order')

    selected_model = None
    if selected_model_slug:
        selected_model = get_object_or_404(PhoneModel, slug=selected_model_slug)
        products = products.filter(variants__phone_model=selected_model).distinct()

    if selected_color_slug:
        products = products.filter(variants__color__slug=selected_color_slug).distinct()

    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(tagline__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()

    color_ids = ProductVariant.objects.filter(product__in=products, is_active=True).values_list('color_id', flat=True)
    colors = Color.objects.filter(id__in=color_ids).distinct().order_by('order')

    context = {
        'products': products,
        'phone_models': phone_models,
        'colors': colors,
        'selected_model': selected_model,
        'selected_model_slug': selected_model_slug,
        'selected_color_slug': selected_color_slug,
        'search_query': search_query,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    all_variants = product.variants.filter(is_active=True).select_related('phone_model', 'color')

    # Lấy danh sách các dòng máy tương thích
    compatible_models = PhoneModel.objects.filter(variants__product=product).distinct().order_by('order')

    selected_model_slug = request.GET.get('model', '')
    if selected_model_slug:
        selected_model = compatible_models.filter(slug=selected_model_slug).first() or compatible_models.first()
    else:
        selected_model = compatible_models.first()

    variants = all_variants.filter(phone_model=selected_model)
    colors = Color.objects.filter(
        variants__product=product,
        variants__phone_model=selected_model,
        variants__is_active=True,
    ).distinct().order_by('order')

    selected_color_slug = request.GET.get('color', '')
    if selected_color_slug:
        selected_color = colors.filter(slug=selected_color_slug).first() or colors.first()
    else:
        selected_color = colors.first()

    # Active variant
    active_variant = variants.filter(color=selected_color).first()
    if not active_variant and variants.exists():
        active_variant = variants.first()
        selected_color = active_variant.color

    # Xây dựng bảng tra cứu JS variant_matrix để chuyển đổi nhanh trên client
    variant_matrix = {}
    for v in all_variants:
        key = f"{v.phone_model.slug}_{v.color.slug}"
        variant_matrix[key] = {
            'id': v.id,
            'sku': v.sku,
            'price': int(v.price),
            'formatted_price': v.formatted_price,
            'stock': v.stock,
            'model_name': v.phone_model.name,
            'model_slug': v.phone_model.slug,
            'color_name': v.color.name,
            'color_en': v.color.english_name,
            'color_slug': v.color.slug,
            'hex': v.color.hex_code,
            'secondary_hex': v.color.secondary_hex,
            'image_url': v.normalized_image_url,
            'image_inside_url': v.normalized_inside_image_url,
            'has_camera_control': v.phone_model.has_camera_control,
        }

    reviews = product.reviews.all().order_by('-created_at')
    related_products = Product.objects.exclude(id=product.id)[:2]

    context = {
        'product': product,
        'compatible_models': compatible_models,
        'colors': colors,
        'selected_model': selected_model,
        'selected_color': selected_color,
        'active_variant': active_variant,
        'variant_matrix_json': json.dumps(variant_matrix),
        'reviews': reviews,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


@require_POST
def cart_add(request):
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        variant_id = data.get('variant_id')
        quantity = int(data.get('quantity', 1))

        if not variant_id:
            return JsonResponse({'success': False, 'error': 'Thiếu mã sản phẩm'}, status=400)

        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart = Cart(request)
        cart.add(variant=variant, quantity=quantity)

        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'total_price': int(cart.get_total_price()),
            'formatted_total_price': cart.formatted_total_price,
            'items': cart.get_items_json(),
            'message': f'Đã thêm {variant.product.title} ({variant.color.name} - {variant.phone_model.name}) vào túi.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def cart_update(request):
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        variant_id = data.get('variant_id')
        quantity = int(data.get('quantity', 1))

        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart = Cart(request)
        if quantity > 0:
            cart.add(variant=variant, quantity=quantity, override_quantity=True)
        else:
            cart.remove(variant)

        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'total_price': int(cart.get_total_price()),
            'formatted_total_price': cart.formatted_total_price,
            'items': cart.get_items_json(),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def cart_remove(request):
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        variant_id = data.get('variant_id')

        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart = Cart(request)
        cart.remove(variant)

        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'total_price': int(cart.get_total_price()),
            'formatted_total_price': cart.formatted_total_price,
            'items': cart.get_items_json(),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_GET
def cart_json(request):
    cart = Cart(request)
    return JsonResponse({
        'cart_count': len(cart),
        'total_price': int(cart.get_total_price()),
        'formatted_total_price': cart.formatted_total_price,
        'items': cart.get_items_json(),
    })


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Túi hàng của bạn đang trống. Hãy chọn một chiếc ốp lưng ưng ý!")
        return redirect('shop:index')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        payment_method = request.POST.get('payment_method', 'vietqr')
        note = request.POST.get('note', '').strip()

        if not (name and email and phone and address and city):
            messages.error(request, "Vui lòng điền đầy đủ tất cả thông tin nhận hàng.")
            return render(request, 'shop/checkout.html', {'cart': cart})

        # Tạo mã đơn hàng độc quyền kiểu Apple: AP-VN-XXXXXX
        order_code = f"AP-VN-{uuid.uuid4().hex[:6].upper()}"

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_code=order_code,
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            shipping_address=address,
            province_city=city,
            payment_method=payment_method,
            payment_status='pending',
            status='processing',
            shipping_fee=0, # Miễn phí giao hàng như Apple Store
            total_amount=cart.get_total_price(),
            note=note,
        )

        for item in cart:
            variant = item['variant']
            OrderItem.objects.create(
                order=order,
                variant=variant,
                product_name=variant.product.title,
                phone_model_name=variant.phone_model.name,
                color_name=variant.color.name,
                color_hex=variant.color.hex_code,
                price=item['price'],
                quantity=item['quantity'],
            )

        # Xóa giỏ hàng sau khi đặt thành công
        cart.clear()
        return redirect('shop:order_success', order_code=order.order_code)

    return render(request, 'shop/checkout.html', {'cart': cart})


def order_success(request, order_code):
    order = get_object_or_404(Order, order_code=order_code)
    
    # Sinh URL VietQR nhanh
    account_no = "03399998888"
    bank_bin = "970422" # MBBank
    account_name = "APPLE VIETNAM AUTHORIZED"
    amount = int(order.total_amount)
    desc = f"THANH TOAN DON {order.order_code}"
    vietqr_url = f"https://img.vietqr.io/image/MB-{account_no}-compact2.png?amount={amount}&addInfo={desc}&accountName={account_name}"

    context = {
        'order': order,
        'vietqr_url': vietqr_url,
        'account_no': account_no,
        'account_name': account_name,
        'bank_name': 'MB Bank (Ngân Hàng Quân Đội)',
    }
    return render(request, 'shop/order_success.html', context)


def order_lookup(request):
    order = None
    searched = False
    if request.method == 'POST':
        order_code = request.POST.get('order_code', '').strip().upper()
        phone = request.POST.get('phone', '').strip()
        searched = True
        if order_code and phone:
            order = Order.objects.filter(order_code=order_code, customer_phone=phone).first()

    return render(request, 'shop/order_lookup.html', {'order': order, 'searched': searched})


def compare_cases(request):
    phone_models = PhoneModel.objects.all().order_by('order')
    products = Product.objects.all()
    return render(request, 'shop/compare.html', {
        'phone_models': phone_models,
        'products': products
    })


@require_POST
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    author_name = request.POST.get('author_name', '').strip()
    phone_model_bought = request.POST.get('phone_model_bought', '').strip()
    rating = int(request.POST.get('rating', 5))
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()

    if author_name and content and title:
        Review.objects.create(
            product=product,
            author_name=author_name,
            phone_model_bought=phone_model_bought,
            rating=max(1, min(5, rating)),
            title=title,
            content=content,
            is_verified=True
        )
        messages.success(request, "Cảm ơn bạn! Đánh giá của bạn đã được gửi thành công.")
    else:
        messages.error(request, "Vui lòng điền đầy đủ tiêu đề và nội dung đánh giá.")

    return redirect('shop:product_detail', slug=product.slug)


# --- User Authentication & Account Views ---
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def user_register(request):
    if request.user.is_authenticated:
        return redirect('shop:user_account')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        full_name = request.POST.get('full_name', '').strip()

        if not (username and email and password):
            messages.error(request, "Vui lòng điền đầy đủ các thông tin bắt buộc.")
            return render(request, 'shop/register.html')

        if password != confirm_password:
            messages.error(request, "Mật khẩu nhập lại không khớp.")
            return render(request, 'shop/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập này đã được sử dụng.")
            return render(request, 'shop/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email này đã được đăng ký tài khoản.")
            return render(request, 'shop/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        if full_name:
            names = full_name.split()
            user.first_name = names[0]
            user.last_name = " ".join(names[1:]) if len(names) > 1 else ""
            user.save()

        login(request, user)
        messages.success(request, f"Chào mừng {user.username}! Bạn đã tạo tài khoản Apple Store thành công.")
        return redirect('shop:user_account')

    return render(request, 'shop/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('shop:user_account')

    next_url = request.GET.get('next', 'shop:user_account')

    if request.method == 'POST':
        login_id = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Cho phép đăng nhập bằng username hoặc email
        user = authenticate(request, username=login_id, password=password)
        if not user and '@' in login_id:
            user_obj = User.objects.filter(email=login_id).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Đăng nhập thành công. Chào mừng {user.first_name or user.username}!")
            return redirect(next_url if next_url.startswith('/') else 'shop:user_account')
        else:
            messages.error(request, "Tên tài khoản hoặc mật khẩu không chính xác.")

    return render(request, 'shop/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Bạn đã đăng xuất tài khoản Apple ID an toàn.")
    return redirect('shop:index')


@login_required(login_url='shop:user_login')
def user_account(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/account.html', {
        'orders': user_orders,
    })
