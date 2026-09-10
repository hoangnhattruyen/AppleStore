from django.core.management.base import BaseCommand
from shop.models import Product, ProductVariant, Color, PhoneModel


class Command(BaseCommand):
    help = 'Tạo hoặc cập nhật ProductVariant màu black cho product hoặc tất cả products'

    def add_arguments(self, parser):
        parser.add_argument('--slug', help='Slug của product cần tạo variant (nếu bỏ qua sẽ xử lý tất cả)')

    def handle(self, *args, **options):
        slug = options.get('slug')
        black = Color.objects.filter(slug='black').first()
        if not black:
            self.stdout.write(self.style.ERROR('Không tìm thấy Color slug="black". Hãy tạo màu trước.'))
            return

        products = Product.objects.all()
        if slug:
            products = products.filter(slug=slug)

        total_created = 0
        total_updated = 0

        for p in products:
            # lấy các phone_model đã có variant cho product (các màu khác)
            phone_model_ids = ProductVariant.objects.filter(product=p).values_list('phone_model', flat=True).distinct()
            phone_models = PhoneModel.objects.filter(id__in=phone_model_ids)

            # nếu không có phone_models nào (sản phẩm mới), bỏ qua
            if not phone_models.exists():
                self.stdout.write(f'Bỏ qua {p.slug} — không tìm thấy phone models liên quan.')
                continue

            for m in phone_models:
                sku = f"APL-SIL-{m.slug}-{black.slug}".upper()
                defaults = {
                    'sku': sku,
                    'price': p.base_price,
                    'stock': 80,
                    'image_url': f'/static/images/cases/case-{black.slug}-back.png',
                    'is_active': True,
                }
                variant, created = ProductVariant.objects.update_or_create(
                    product=p,
                    phone_model=m,
                    color=black,
                    defaults=defaults
                )
                if created:
                    total_created += 1
                    self.stdout.write(self.style.SUCCESS(f'Created black variant for {p.slug} / {m.slug} (id={variant.id})'))
                else:
                    total_updated += 1
                    self.stdout.write(self.style.NOTICE(f'Updated black variant for {p.slug} / {m.slug} (id={variant.id})'))

        self.stdout.write(self.style.SUCCESS(f'Done. Created: {total_created}, Updated: {total_updated}'))
