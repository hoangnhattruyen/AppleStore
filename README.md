# Apple iPhone Silicone Cases Store (Apple VN Style)

Trang web thương mại điện tử chuyên bán các mẫu **Ốp Lưng Silicon Apple chính hãng** với trải nghiệm tối giản, tinh tế mô phỏng chuẩn giao diện Apple Store Việt Nam.

- **Front-end**: HTML5, CSS3 (Apple Design System, San Francisco font, Glassmorphism, Micro-interactions), JavaScript ES6+ (Túi hàng slide-over, live color swatches, dynamic SVG case rendering, preview khắc tên).
- **Back-end**: Python Django 4.2+, SQLite, Django ORM, Session Cart, VietQR Payment Gateway, Django Admin.

---

## 🌟 Các Tính Năng Nổi Bật

1. **Giao diện & Hình ảnh sản phẩm thực tế chuẩn Apple Store**:
   - Thay thế toàn bộ thiết kế giả lập bằng **bộ ảnh sản phẩm SVG/Vector độ phân giải cao** cho từng màu sắc (Mặt lưng hoàn thiện tinh xảo, cụm 3 camera sapphire, nút Camera Control và mặt trong lớp nhung microfiber kèm vòng nam châm MagSafe).
   - Nút chuyển góc nhìn tức thì: **Mặt Sau (Camera & Phím Sapphire)** ⇄ **Mặt Trong (Vòng MagSafe)**.
2. **Menu lựa chọn dòng máy chuyên biệt (Apple Device Subnav)**:
   - **Thanh Subnav thiết bị Apple**: Hiển thị biểu tượng và tên đầy đủ từng dòng máy (iPhone 16 Pro Max, 16 Pro, 16 Plus, 16, 15 Pro Max, 15 Pro, 15, 14).
   - **Menu Dropdown trên thanh Navigation**: Bấm "Chọn Dòng Máy" mở menu phân nhóm theo thế hệ (iPhone 16 Series, 15 Series, Thế hệ trước).
3. **Hệ thống Quản lý Tài Khoản & Đăng Nhập (Apple ID Style)**:
   - **Đăng ký tài khoản (`/register/`)**: Tạo tài khoản Apple Store cá nhân nhanh chóng.
   - **Đăng nhập (`/login/`)**: Hỗ trợ đăng nhập linh hoạt bằng Tên tài khoản hoặc Email.
   - **Trang quản lý cá nhân (`/account/`)**: Theo dõi thông tin cá nhân và toàn bộ lịch sử đơn hàng đã đặt kèm trạng thái xử lý/vận chuyển.
   - Tự động liên kết đơn hàng khi mua sắm và điền sẵn thông tin khi thanh toán.
4. **Bộ chọn màu tương tác (Live Swatches)**:
   - 10 màu sắc chính thức của Apple (Xanh Hồ Bơi, Xanh Denim, Hồng Phấn, Mận Chín, Vàng Khế, Đá Phiến, Đen, Siêu Phẩm Đỏ...).
   - Đổi ảnh ốp lưng tức thì ngay khi click vào chấm màu không cần reload trang.
3. **Trang chi tiết sản phẩm tương tác cao**:
   - Chuyển màu và thay đổi dòng máy mượt mà không cần reload trang.
   - Mô phỏng chi tiết phím **Điều Khiển Camera (Camera Control)** bằng kính sapphire cho thế hệ iPhone 16.
   - Hiệu ứng bật/tắt hiển thị vòng nam châm **MagSafe**.
   - **Khắc tên miễn phí (Apple Engraving)**: Gõ chữ và xem trước chữ khắc trực tiếp trên lưng ốp silicon.
4. **Túi hàng Apple (Slide-over Cart Drawer)**:
   - Thêm vào túi với micro-animation.
   - Tăng/giảm số lượng, xóa sản phẩm, tính tổng tiền tự động qua AJAX.
5. **Quy trình Thanh toán & Tích hợp VietQR**:
   - Form thông tin giao hàng tại Việt Nam (Tỉnh/Thành phố, SĐT, Email).
   - Tự động sinh mã đơn hàng chuẩn Apple (`AP-VN-XXXXXX`).
   - Tự động hiển thị mã **VietQR** chuẩn ngân hàng kèm số tiền và nội dung thanh toán để khách hàng quét app chuyển khoản tức thì.
6. **Tra cứu đơn hàng**:
   - Khách hàng có thể tra cứu tình trạng đơn hàng bất cứ lúc nào qua Mã đơn và Số điện thoại.
7. **Bảng so sánh ốp lưng (Compare Tool)**:
   - So sánh thông số chi tiết giữa các thế hệ iPhone 16, iPhone 15 và iPhone 14.
8. **Đánh giá khách hàng**:
   - Xem đánh giá thực tế và gửi review trực tiếp.
9. **Trang quản trị Django Admin**:
   - Quản lý sản phẩm, biến thể (Dòng máy x Màu sắc), đơn hàng và doanh thu trực quan.

---

## 🚀 Hướng Dẫn Chạy Dự Án

### 1. Di chuyển vào thư mục dự án
```powershell
cd "C:\Users\Nhat Truyen\.gemini\antigravity\scratch\apple_silicone_store"
```

### 2. Khởi động máy chủ Django
```powershell
python manage.py runserver 8000
```

### 3. Mở trình duyệt
- Trang chủ cửa hàng: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Danh sách ốp silicon: [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
- Bảng so sánh ốp lưng: [http://127.0.0.1:8000/compare/](http://127.0.0.1:8000/compare/)
- Tra cứu đơn hàng: [http://127.0.0.1:8000/order-lookup/](http://127.0.0.1:8000/order-lookup/)
- Trang quản trị (Django Admin): [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  - Tài khoản: `admin`
  - Mật khẩu: `admin123`
