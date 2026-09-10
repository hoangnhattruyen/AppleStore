from django.test import TestCase, Client
from django.urls import reverse
from shop.models import PhoneModel, Color, Product, ProductVariant, Order, OrderItem
import json


class AppleSiliconeStoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.phone_model = PhoneModel.objects.create(
            name="iPhone 16 Pro Max",
            slug="iphone-16-pro-max",
            generation="iPhone 16 Series",
            screen_size="6.9 inch",
            has_camera_control=True,
            order=1
        )
        self.color = Color.objects.create(
            name="Xanh Hồ Bơi",
            english_name="Lake Green",
            slug="lake-green",
            hex_code="#2e5b56",
            secondary_hex="#3d736c",
            is_dark=False,
            order=1
        )
        self.product = Product.objects.create(
            title="Ốp Lưng Silicon với MagSafe iPhone 16",
            slug="op-lung-silicon-magsafe-iphone-16",
            tagline="Khớp hoàn hảo",
            short_description="Mô tả ngắn",
            description="Mô tả chi tiết",
            base_price=1429000,
            badge="Mới",
            is_new=True,
            is_featured=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            phone_model=self.phone_model,
            color=self.color,
            sku="APL-TEST-SKU",
            price=1429000,
            stock=50
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse('shop:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ốp Lưng Silicon")

    def test_product_list_loads(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.title)

    def test_product_list_filter_model(self):
        response = self.client.get(reverse('shop:product_list') + '?model=iphone-16-pro-max')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.title)

    def test_product_detail_loads(self):
        url = reverse('shop:product_detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Xanh Hồ Bơi")
        self.assertContains(response, "Thêm vào Túi Hàng")

    def test_cart_operations(self):
        # Add to cart
        add_url = reverse('shop:cart_add')
        response = self.client.post(
            add_url,
            data=json.dumps({'variant_id': self.variant.id, 'quantity': 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 1)

        # Update cart
        update_url = reverse('shop:cart_update')
        response = self.client.post(
            update_url,
            data=json.dumps({'variant_id': self.variant.id, 'quantity': 2}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['cart_count'], 2)

        # Remove from cart
        remove_url = reverse('shop:cart_remove')
        response = self.client.post(
            remove_url,
            data=json.dumps({'variant_id': self.variant.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['cart_count'], 0)

    def test_checkout_flow(self):
        # Add to cart first
        self.client.post(
            reverse('shop:cart_add'),
            data=json.dumps({'variant_id': self.variant.id, 'quantity': 1}),
            content_type='application/json'
        )

        # Checkout post
        response = self.client.post(reverse('shop:checkout'), {
            'name': 'Nguyễn Văn Test',
            'email': 'test@example.com',
            'phone': '0901234567',
            'address': '123 Đường Test, Quận 1',
            'city': 'TP. Hồ Chí Minh',
            'payment_method': 'vietqr',
            'note': 'Giao nhanh'
        })
        self.assertEqual(response.status_code, 302)
        
        # Order should exist
        order = Order.objects.filter(customer_name='Nguyễn Văn Test').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.payment_method, 'vietqr')

    def test_compare_page(self):
        response = self.client.get(reverse('shop:compare'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "So sánh")

    def test_user_registration_and_login(self):
        # Register
        reg_response = self.client.post(reverse('shop:user_register'), {
            'username': 'appletestuser',
            'email': 'appletest@apple.com',
            'full_name': 'Apple Test User',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(reg_response.status_code, 302)

        # Account dashboard should be accessible
        acc_response = self.client.get(reverse('shop:user_account'))
        self.assertEqual(acc_response.status_code, 200)
        self.assertContains(acc_response, "appletestuser")

        # Logout
        logout_response = self.client.get(reverse('shop:user_logout'))
        self.assertEqual(logout_response.status_code, 302)

        # Login
        login_response = self.client.post(reverse('shop:user_login'), {
            'username': 'appletestuser',
            'password': 'password123',
        })
        self.assertEqual(login_response.status_code, 302)
