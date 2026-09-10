from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import PhoneModel, Color, Product, ProductVariant, Review


class Command(BaseCommand):
    help = 'Nạp dữ liệu mẫu ốp lưng silicon iPhone chuẩn Apple Store VN'

    def handle(self, *args, **kwargs):
        self.stdout.write("Bat dau nap du lieu Apple Store Viet Nam...")

        # 1. Danh sách dòng máy iPhone
        phone_models_data = [
            {"name": "iPhone 16 Pro Max", "gen": "iPhone 16 Series", "screen": "6.9 inch", "has_cc": True, "order": 1},
            {"name": "iPhone 16 Pro", "gen": "iPhone 16 Series", "screen": "6.3 inch", "has_cc": True, "order": 2},
            {"name": "iPhone 16 Plus", "gen": "iPhone 16 Series", "screen": "6.7 inch", "has_cc": True, "order": 3},
            {"name": "iPhone 16", "gen": "iPhone 16 Series", "screen": "6.1 inch", "has_cc": True, "order": 4},
            {"name": "iPhone 15 Pro Max", "gen": "iPhone 15 Series", "screen": "6.7 inch", "has_cc": False, "order": 5},
            {"name": "iPhone 15 Pro", "gen": "iPhone 15 Series", "screen": "6.1 inch", "has_cc": False, "order": 6},
            {"name": "iPhone 15 Plus", "gen": "iPhone 15 Series", "screen": "6.7 inch", "has_cc": False, "order": 7},
            {"name": "iPhone 15", "gen": "iPhone 15 Series", "screen": "6.1 inch", "has_cc": False, "order": 8},
            {"name": "iPhone 14 Pro Max", "gen": "iPhone 14 Series", "screen": "6.7 inch", "has_cc": False, "order": 9},
            {"name": "iPhone 14 Pro", "gen": "iPhone 14 Series", "screen": "6.1 inch", "has_cc": False, "order": 10},
            {"name": "iPhone 14", "gen": "iPhone 14 Series", "screen": "6.1 inch", "has_cc": False, "order": 11},
        ]

        phone_models_objs = {}
        for m in phone_models_data:
            obj, created = PhoneModel.objects.update_or_create(
                slug=slugify(m["name"]),
                defaults={
                    "name": m["name"],
                    "generation": m["gen"],
                    "screen_size": m["screen"],
                    "has_camera_control": m["has_cc"],
                    "order": m["order"]
                }
            )
            phone_models_objs[m["name"]] = obj

        self.stdout.write(f"- Da nap {len(phone_models_objs)} dong may iPhone.")

        # 2. Bộ sưu tập màu sắc Apple Silicon
        colors_data = [
            {"slug": "black15pr", "name": "Đen", "en": "Black", "hex": "#1e1e1e", "sec": "#333333", "dark": True, "order": 14},
            {"slug": "black15", "name": "Đen", "en": "Black", "hex": "#1e1e1e", "sec": "#333333", "dark": True, "order": 14},
            {"slug": "black16", "name": "Đen", "en": "Black", "hex": "#1e1e1e", "sec": "#333333", "dark": True, "order": 12},
            {"slug": "black16pr", "name": "Đen", "en": "Black", "hex": "#1e1e1e", "sec": "#333333", "dark": True, "order": 13},
            {"slug": "black", "name": "Đen", "en": "Black", "hex": "#1e1e1e", "sec": "#333333", "dark": True, "order": 1},
            {"slug": "lake-green", "name": "Xanh Hồ Bơi", "en": "Lake Green", "hex": "#2e5b56", "sec": "#3d736c", "dark": False, "order": 2},
            {"slug": "denim", "name": "Xanh Denim", "en": "Denim", "hex": "#394d68", "sec": "#4c668a", "dark": False, "order": 3},
            {"slug": "light-pink15pr", "name": "Hồng Phấn", "en": "Light Pink", "hex": "#f1c3cb", "sec": "#dca2ac", "dark": False, "order": 4},
            {"slug": "light-pink15", "name": "Hồng Phấn", "en": "Light Pink", "hex": "#f1c3cb", "sec": "#dca2ac", "dark": False, "order": 4},
            {"slug": "light-pink", "name": "Hồng Phấn", "en": "Light Pink", "hex": "#f1c3cb", "sec": "#dca2ac", "dark": False, "order": 4},
            {"slug": "plum", "name": "Mận Chín", "en": "Plum", "hex": "#4a293a", "sec": "#65374f", "dark": True, "order": 5},
            {"slug": "stone-gray", "name": "Đá Phiến", "en": "Stone Gray", "hex": "#76797d", "sec": "#8f9397", "dark": False, "order": 7},
            {"slug": "product-red", "name": "Siêu Phẩm Đỏ", "en": "PRODUCT(RED)", "hex": "#c81e26", "sec": "#e6353e", "dark": False, "order": 8},
            {"slug": "ultramarine", "name": "Xanh Siêu Âm", "en": "Ultramarine", "hex": "#264875", "sec": "#355e96", "dark": False, "order": 9},
            {"slug": "hoa-djang", "name": "Hoa Đăng", "en": "Hoa Djang", "hex": "#982f80", "sec": "#f0b98b", "dark": False, "order": 10},
            {"slug": "datset", "name": "Dat set", "en": "Light Pink", "hex": "#BDBAA2", "sec": "#dca2ac", "dark": False, "order": 4},
            {"slug": "XanhGiongTo", "name": "Blue", "en": "Light Pink", "hex": "#758DA3", "sec": "#dca2ac", "dark": False, "order": 4},
        ]
        # Nếu muốn ẩn một số màu khỏi giao diện, bỏ qua khi tạo đối tượng Color.
        # Hiện tại ẩn hai màu đầu tiên (black16, black16pr).
        hidden_slugs = {"black15","black15pr","black16", "black16pr","XanhGiongTo","datset","light-pink15pr","light-pink15"}

        color_objs = []
        for c in colors_data:
            defaults = {
                "name": c["name"],
                "english_name": c["en"],
                "hex_code": c["hex"],
                "secondary_hex": c["sec"],
                "is_dark": c["dark"],
                "order": c["order"]
            }
            # Nếu slug nằm trong hidden_slugs thì đánh dấu is_hidden=True thay vì bỏ qua hoàn toàn
            if c["slug"] in hidden_slugs:
                defaults["is_hidden"] = True

            c_obj, _ = Color.objects.update_or_create(
                slug=c["slug"],
                defaults=defaults
            )
            color_objs.append(c_obj)

        self.stdout.write(f"- Da nap {len(color_objs)} mau sac.")

        # 3. Sản phẩm chính
        products_data = [
            {
                "title": "Ốp Lưng Silicon với MagSafe và Điều Khiển Camera cho iPhone 16",
                "slug": "op-lung-silicon-magsafe-iphone-16",
                "tagline": "Khớp hoàn hảo. Cầm êm ái. Điều khiển Camera tức thì.",
                "short_description": "Được Apple thiết kế nhằm bổ trợ tuyệt đối cho iPhone 16 Series. Hoạt động liền mạch với Nút Điều Khiển Camera với kính sapphire dẫn điện siêu nhạy.",
                "description": (
                    "Được Apple thiết kế nhằm bổ trợ tuyệt đối cho iPhone 16, Ốp Lưng Silicon với MagSafe là lựa chọn tinh tế để tăng cường bảo vệ thiết bị.\n\n"
                    "Mặt ngoài bằng silicon mềm mượt tạo cảm giác cầm nắm đầm tay, êm ái tuyệt đối. Bên trong là lớp lót bằng sợi microfiber mềm mại giúp tăng cường bảo vệ cho lưng kính của chiếc iPhone.\n\n"
                    "Ốp lưng này hoạt động liền mạch với Nút Điều Khiển Camera (Camera Control). Ốp lưng được chế tác với lớp kính sapphire kết hợp cùng một lớp dẫn điện tinh vi, giúp truyền chính xác từng chuyển động nhỏ nhất từ ngón tay của bạn đến Nút Điều Khiển Camera mà không bị trễ.\n\n"
                    "Với các nam châm tích hợp tự động căn chỉnh hoàn hảo cùng iPhone, ốp lưng đem lại trải nghiệm gắn kỳ diệu cùng khả năng sạc không dây nhanh hơn mỗi lần sử dụng. Khi đến lúc cần sạc, bạn chỉ cần gắn cả iPhone đang có ốp lưng vào bộ sạc MagSafe hoặc đặt lên bộ sạc chuẩn Qi2/Qi."
                ),
                "base_price": 79000,
                "badge": "Mới",
                "is_new": True,
                "is_featured": True,
                "models": ["iPhone 16 Pro Max", "iPhone 16 Pro", "iPhone 16 Plus", "iPhone 16"]
            },
            {
                "title": "Ốp Lưng Silicon với MagSafe cho iPhone 15",
                "slug": "op-lung-silicon-magsafe-iphone-15",
                "tagline": "Bảo vệ mỏng nhẹ. Màu sắc thời thượng từ Apple.",
                "short_description": "Chất liệu silicon mịn như lụa, chống bám bụi và chống sốc hiệu quả. Tích hợp nam châm MagSafe mạnh mẽ.",
                "description": (
                    "Ốp Lưng Silicon với MagSafe được Apple sáng tạo để bảo vệ iPhone 15 của bạn một cách trọn vẹn và thời trang nhất.\n\n"
                    "Bề mặt ngoài bằng silicon êm mịn mang đến cảm giác tuyệt vời trên tay. Bên trong có lớp lót sợi nhỏ microfiber êm ái.\n\n"
                    "Các nam châm tích hợp căn chỉnh chuẩn xác theo công nghệ MagSafe của Apple, giúp việc sạc không dây trở nên nhanh chóng và dễ dàng hơn bao giờ hết."
                ),
                "base_price": 99000,
                "badge": "Bán chạy",
                "is_new": False,
                "is_featured": True,
                "models": ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15 Plus", "iPhone 15"]
            },
            {
                "title": "Ốp Lưng Silicon với MagSafe cho iPhone 14",
                "slug": "op-lung-silicon-magsafe-iphone-14",
                "tagline": "Bảo vệ tin cậy. Phong cách bền bỉ.",
                "short_description": "Trải qua hàng ngàn giờ thử nghiệm theo chuẩn phòng thí nghiệm Apple. Vẻ đẹp cổ điển nhưng trường tồn.",
                "description": (
                    "Thiết kế kinh điển của dòng ốp bảo vệ silicon Apple. Bền bỉ trước các va đập thường ngày và hạn chế trầy xước lưng kính.\n\n"
                    "Hỗ trợ trọn vẹn toàn bộ hệ sinh thái phụ kiện MagSafe từ sạc, ví kẹp thẻ đến giá treo xe hơi."
                ),
                "base_price": 99000,
                "badge": "Ưu đãi",
                "is_new": False,
                "is_featured": False,
                "models": ["iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14"]
            }
        ]

        total_variants = 0
        for p_data in products_data:
            p_obj, _ = Product.objects.update_or_create(
                slug=p_data["slug"],
                defaults={
                    "title": p_data["title"],
                    "tagline": p_data["tagline"],
                    "short_description": p_data["short_description"],
                    "description": p_data["description"],
                    "base_price": p_data["base_price"],
                    "badge": p_data["badge"],
                    "is_new": p_data["is_new"],
                    "is_featured": p_data["is_featured"],
                }
            )

            # Tạo biến thể cho các dòng máy tương thích x các màu sắc
            # Dùng URL demo thật cho các màu chính để giao diện hiển thị ảnh thực tế.
            color_image_map = {
                "black15pr":"https://down-vn.img.susercontent.com/file/sg-11134201-7rbk4-lmk3ih8qi82h52@resize_w900_nl.webp",
                "black15":"https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MT0J3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=bm5sRU4yakhNdG1UUW40VWNNbTBWd2tuVHYzMERCZURia3c5SzJFOTlPaFdPNXNCZjFUY2U4dzhjY0xjYWZIRkYwekViWm9ieXhRS1pZMWVVR3U1b2c",
                "black16pr":"https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYYT3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=bXBlZlZsUzFiRGJCaytzamZ0akR1Z2tuVHYzMERCZURia3c5SzJFOTlPZ3oveDdpQVpwS0ltY2w2UW05aU90T3Vja1hnNlRzcUJGZGVaZU5qN0t6a0E",
                "black16":"https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYY13?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=dmlrK2xBK3ZIL0RWcEZWRUx4VmNLd2tuVHYzMERCZURia3c5SzJFOTlPZ3oveDdpQVpwS0ltY2w2UW05aU90T2dOZDFJM0kzcS8rZDgybFJTRTZoK2c",
                "black": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MK8Y4?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=Y3lXQk1pbTRPeFNjbWROY0VaWitBd2tuVHYzMERCZURia3c5SzJFOTlPaW9Ta3FTNGU3WUJlRUoxOUlMR1cwK2lqTk5BQlZRcmRKcFVqL1NFbXJhQXc",
                "lake-green": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYYH3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=V3dEblFoMFFrdHRScEI0WWk4bnFSUWtuVHYzMERCZURia3c5SzJFOTlPZ3oveDdpQVpwS0ltY2w2UW05aU90T1NzbGM4MkZOUkZqZHdOMkhDaDZkdHc",
                "light-pink": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MPRX3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=QUJkNHd0QUJFMjJVeEk3dGZ6QTNCZ2tuVHYzMERCZURia3c5SzJFOTlPampWbjhveGhUMExwcENaNnJqdFZ6WDFyeFEvV0t1ZG1NakNobmVpNlZ3UkE",
                "light-pink15pr":"https://down-vn.img.susercontent.com/file/sg-11134201-7rbmc-lmk3igpbdg7fe3@resize_w900_nl.webp",
                "light-pink15": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MT0U3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=N2ZKYXgxTXkxb1ptWXNQbGZNaUJZZ2tuVHYzMERCZURia3c5SzJFOTlPaFBPR1RmQ3R0Ulg1R1NoQmo2RXhEY3hQRWV5dW1Yblkyc0x3YlZ0WTdCQmc",
                "datset":"https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MT0Q3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=aVdkbVp0OXBOeGtRd3FqMmJnbnd4UWtuVHYzMERCZURia3c5SzJFOTlPaFdPNXNCZjFUY2U4dzhjY0xjYWZIRlJydVYva1hUWkNWUG9QTVBQQlBudkE",
                "XanhGiongTo":"https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MT0N3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=ZUoyTWFicU1MN0Z6QlNDMk9LUlJNd2tuVHYzMERCZURia3c5SzJFOTlPaFdPNXNCZjFUY2U4dzhjY0xjYWZIRndUNHc3RFQ5WU9idDFINm9nOVdOQWc",
                "denim": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYYU3?wid=2000&hei=2000&fmt=jpeg&qlt=90&.v=eXY4YWRVNVdScldQQlR6RGwxOUh6R2orYzFkTG5HaE9wejd5WUxYZjRMOHoveDdpQVpwS0ltY2w2UW05aU90T0tOWjZQdFA2TEZuNWxLUHNtNjIzbnc",
                "plum": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYYW3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=RVF1WUQxZXIxK0t5UVgrL1ZXemI0QWtuVHYzMERCZURia3c5SzJFOTlPZ3oveDdpQVpwS0ltY2w2UW05aU90T3l5SkFUUWJBVnNpdGJwNTRmOTlUdVE",
                "stone-gray": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYYV3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=VnZUUDBINEI4b1ZTT0J4Rld6WGFjUWtuVHYzMERCZURia3c5SzJFOTlPZ3oveDdpQVpwS0ltY2w2UW05aU90T2d1ZEVTdkNNTEo1UEhZRjF5V2xscGc",
                "ultramarine": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYYF3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=MjRLY2thQmtHOEl5NFhZSi9YcUd2Z2tuVHYzMERCZURia3c5SzJFOTlPaVBpZElsODN6SXRvNXUyendNZGZ4SWpQSjc4Tm1pWHBZT2ZZam5uWVRaR0E",
                "product-red": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MPT63?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=NDhuaUhwQUg5SjF2ZUk2eWMvNVRZUWtuVHYzMERCZURia3c5SzJFOTlPaDk5cHI0Sk9QQ3N4N3RrQWt2VUEwNXZRNTl5ckY3VlVwNy9CNUI1Y3E5OHc",
                "hoa-djang": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYYE3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=VEs2YW53OHQxVzhITVNFZzhJY2NUd2tuVHYzMERCZURia3c5SzJFOTlPZ3oveDdpQVpwS0ltY2w2UW05aU90T3ovWVpqOFh5clQ2OWNkdkhkdzErUFE",
            }
            product_cover_map = {
                "op-lung-silicon-magsafe-iphone-16": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MYY93?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=YjBETWJveTlMYXhKelBweTdTcGtvUWtuVHYzMERCZURia3c5SzJFOTlPZ3oveDdpQVpwS0ltY2w2UW05aU90T2VlV3o2aUc2UTBlZGExYnQvOTJlcWc",
                "op-lung-silicon-magsafe-iphone-15": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MT0J3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=bm5sRU4yakhNdG1UUW40VWNNbTBWd2tuVHYzMERCZURia3c5SzJFOTlPaFdPNXNCZjFUY2U4dzhjY0xjYWZIRkYwekViWm9ieXhRS1pZMWVVR3U1b2c",
                "op-lung-silicon-magsafe-iphone-14": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MPRU3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=aitRaVpHMmNWTXNNdGdCL21aZ2pNQWtuVHYzMERCZURia3c5SzJFOTlPampWbjhveGhUMExwcENaNnJqdFZ6WFZyZjJNSnVjRnIrVVg2bGl5Vm5pOFE",
            }

            p_obj.image_url = product_cover_map.get(p_obj.slug, color_image_map.get('black', ''))
            p_obj.save(update_fields=['image_url'])

            model_color_map = {
                "iPhone 16 Pro Max": ["black16pr", "denim", "plum", "stone-gray"],
                "iPhone 16 Pro": ["black16pr", "denim", "plum", "stone-gray"],
                "iPhone 16 Plus": ["black16", "lake-green", "ultramarine", "hoa-djang"],
                "iPhone 16": ["black16", "lake-green", "ultramarine", "hoa-djang"],
                "iPhone 15 Pro Max": ["black15pr", "light-pink15pr"],
                "iPhone 15 Pro": ["black15pr", "light-pink15pr"],
                "iPhone 15 Plus": ["black15", "light-pink15", "XanhGiongTo"],
                "iPhone 15": ["black15", "light-pink15", "datset", "XanhGiongTo"],
                "iPhone 14 Pro Max": ["black", "white", "denim", "stone-gray"],
                "iPhone 14 Pro": ["black", "white", "denim", "stone-gray"],
                "iPhone 14": ["black", "white", "denim", "stone-gray"],
            }

            # Không xóa toàn bộ variants để tránh mất các variant do admin tạo.
            # Thay vào đó, sau khi tạo/update các variant do seed, ta sẽ xóa chỉ những variant
            # do seed tạo trước đó nhưng không còn trong danh sách mong muốn.

            for m_name in p_data["models"]:
                if m_name in phone_models_objs:
                    m_obj = phone_models_objs[m_name]
                    allowed_slugs = set(model_color_map.get(m_name, []))
                    eligible_colors = [c_obj for c_obj in color_objs if c_obj.slug in allowed_slugs]

                    for c_obj in eligible_colors:
                        sku = f"APL-SIL-{m_obj.slug}-{c_obj.slug}".upper()
                        image_path = color_image_map.get(c_obj.slug, f"/static/images/cases/case-{c_obj.slug}-back.png")

                        variant, created = ProductVariant.objects.update_or_create(
                            product=p_obj,
                            phone_model=m_obj,
                            color=c_obj,
                            defaults={
                                "sku": sku,
                                "price": p_obj.base_price,
                                "stock": 80,
                                "image_url": image_path,
                                "is_active": True,
                                "is_seeded": True,
                            }
                        )
                        total_variants += 1

                    # Nếu model đã có bất kỳ màu 'black*' (vd. black16, black16pr) thì không thêm 'black' nữa
                    black_color = Color.objects.filter(slug='black').first()
                    if black_color:
                        existing_slugs = {c.slug for c in eligible_colors}
                        has_model_specific_black = any(s.startswith('black') and s != 'black' for s in existing_slugs)
                        if not has_model_specific_black and 'black' not in existing_slugs:
                            sku = f"APL-SIL-{m_obj.slug}-{black_color.slug}".upper()
                            image_path = color_image_map.get(black_color.slug, f"/static/images/cases/case-{black_color.slug}-back.png")
                            v, created = ProductVariant.objects.update_or_create(
                                product=p_obj,
                                phone_model=m_obj,
                                color=black_color,
                                defaults={
                                    'sku': sku,
                                    'price': p_obj.base_price,
                                    'stock': 80,
                                    'image_url': image_path,
                                    'is_active': True,
                                }
                            )
                            if created:
                                total_variants += 1

                        # Sau khi đã tạo/update danh sách variant mong muốn cho model này,
                        # xóa các variant cũ được tạo bởi seed nhưng không còn trong danh sách mong muốn.
                        # `allowed_slugs` is a set of slug strings. Use `eligible_colors` (Color objs)
                        # to build desired (phone_model_slug, color_slug) pairs.
                        desired_pairs = {(m_obj.slug, c_obj.slug) for c_obj in eligible_colors}
                        for old_v in ProductVariant.objects.filter(product=p_obj, is_seeded=True):
                            key = (old_v.phone_model.slug, old_v.color.slug)
                            if key not in desired_pairs:
                                old_v.delete()

        

        self.stdout.write(f"- Da tao {len(products_data)} san pham va {total_variants} bien the.")

        # 4. Đánh giá khách hàng mẫu (Authentic Apple Store VN reviews)
        first_product = Product.objects.first()
        if first_product:
            sample_reviews = [
                {
                    "author": "Trần Minh Hoàng",
                    "model": "iPhone 16 Pro Max",
                    "rating": 5,
                    "title": "Phím Camera Control hoạt động quá mượt!",
                    "content": "Lớp kính sapphire ở nút Camera Control nhạy như chạm trực tiếp vào thân máy. Màu Xanh Hồ Bơi ở ngoài đẹp sang trọng hơn trên ảnh rất nhiều. Rất hài lòng với dịch vụ giao hàng nhanh của Apple."
                },
                {
                    "author": "Nguyễn Thảo Ly",
                    "model": "iPhone 16 Pro",
                    "rating": 5,
                    "title": "Màu Hồng Phấn cực kỳ xinh xắn",
                    "content": "Chất silicon cầm rất mịn tay, không hề bám bụi hay bám vân tay như các loại ốp trôi nổi. Vòng MagSafe hút cực kỳ chặt vào sạc không dây."
                },
                {
                    "author": "Lê Quốc Bảo",
                    "model": "iPhone 16",
                    "rating": 5,
                    "title": "Đúng chuẩn ốp chính hãng Apple",
                    "content": "Đóng gói cẩn thận, mở hộp đúng đẳng cấp Apple. Lớp lót nhung microfiber bên trong bảo vệ lưng máy hoàn hảo không sợ xước viền."
                },
                {
                    "author": "Đặng Tuấn Anh",
                    "model": "iPhone 15 Pro Max",
                    "rating": 4,
                    "title": "Chất lượng hoàn thiện đỉnh cao",
                    "content": "Ốp cầm đầm tay, cảm giác cao cấp. Màu Xanh Denim rất hợp với phong cách văn phòng công sở. Đánh giá 5 sao cho chất lượng hoàn thiện."
                }
            ]

            Review.objects.filter(product=first_product).delete()
            for r in sample_reviews:
                Review.objects.create(
                    product=first_product,
                    author_name=r["author"],
                    phone_model_bought=r["model"],
                    rating=r["rating"],
                    title=r["title"],
                    content=r["content"],
                    is_verified=True
                )
            self.stdout.write(f"- Da nap {len(sample_reviews)} danh gia nguoi dung.")

        self.stdout.write(self.style.SUCCESS("Nạp dữ liệu thành công 100%!"))
