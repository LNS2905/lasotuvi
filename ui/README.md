# Hướng dẫn sử dụng UI Lá Số Tử Vi

## Các file UI có sẵn

1. **index.html** - UI test đơn giản (tiếng Anh)
2. **tuvichart.html** - UI hiển thị lá số với form input (tiếng Việt)
3. **lasotu_traditional.html** - UI hiển thị lá số kiểu truyền thống (Layout 4x4 giống ảnh mẫu) ⭐ **MỚI**

## Cách chạy

### 1. Khởi động Backend API

Từ thư mục gốc của project:

```bash
# Cài đặt dependencies (nếu chưa có)
pip install -r requirements.txt

# Chạy API server
python -m uvicorn lasotuvi.api.main:app --reload
```

API sẽ chạy tại: `http://localhost:8000`

### 2. Mở UI trong trình duyệt

Mở trực tiếp file HTML trong trình duyệt:

- **Đơn giản nhất**: Mở file `lasotu_traditional.html` bằng trình duyệt (Chrome, Firefox, Edge)
- Hoặc sử dụng Live Server extension trong VS Code

### 3. Nhập thông tin và lập lá số

Trong form nhập:
- **Họ Tên**: Tên người xem (không bắt buộc)
- **Ngày/Tháng/Năm Sinh**: Ngày tháng năm sinh
- **Giờ Sinh**: Từ 1-12 (theo địa chi)
- **Giới Tính**: Nam (1) hoặc Nữ (-1)
- **Loại Lịch**: Dương lịch hoặc Âm lịch
- **Múi Giờ**: Mặc định là 7 (GMT+7 - Việt Nam)

Nhấn **LẬP LÁ SỐ** để xem kết quả.

## Layout Lá Số Truyền Thống

File `lasotu_traditional.html` hiển thị lá số theo bố cục truyền thống:

```
┌─────────┬─────────┬─────────┬─────────┐
│  Dần    │  Mão    │  Thìn   │  Tỵ     │
│ (Cung)  │ (Cung)  │ (Cung)  │ (Cung)  │
├─────────┼─────────┴─────────┼─────────┤
│  Sửu    │                   │  Ngọ    │
│ (Cung)  │   THÔNG TIN      │ (Cung)  │
├─────────┤   TRUNG TÂM      ├─────────┤
│  Tý     │                   │  Mùi    │
│ (Cung)  │   (Tên, Mệnh,    │ (Cung)  │
├─────────┼─────────┬─────────┤  Cục..)  │
│  Hợi    │  Tuất   │  Dậu    │  Thân   │
│ (Cung)  │ (Cung)  │ (Cung)  │ (Cung)  │
└─────────┴─────────┴─────────┴─────────┘
```

### Thông tin hiển thị trong mỗi cung:

- **Chi** (góc phải trên): Tý, Sửu, Dần, Mão...
- **Tên Cung** (đỏ, in đậm): Mệnh, Phụ Mẫu, Phúc Đức...
- **Ngũ Hành**: Kim, Mộc, Thủy, Hỏa, Thổ
- **Các Sao**: Hiển thị với màu theo ngũ hành
- **Đại Hạn/Tiểu Hạn**: Nếu có

### Thông tin trung tâm:

- Họ tên
- Năm sinh, Giới tính
- Ngày Dương lịch / Âm lịch
- Can Chi (Năm)
- Mệnh
- Cục
- Mệnh vs Cục (Sinh/Khắc)

## API Endpoints

Backend cung cấp các endpoints:

- `POST /charts` - Tạo lá số mới
- `GET /charts/{id}` - Lấy lá số theo ID
- `GET /charts?limit=20` - Danh sách các lá số gần đây

## Cấu trúc dữ liệu Response

> **🎉 Update v0.2.0**: Backend hiện trả về 100% dữ liệu đầy đủ từ thư viện lasotuvi!
> 
> Xem chi tiết: [CHANGELOG_API.md](../CHANGELOG_API.md)

### Houses (11 fields):
```json
{
  "house_number": 1,        // NEW: Số thứ tự cung (1-12)
  "branch": "Tý",           // Tên chi
  "name": "Mệnh",           // Tên cung chủ
  "element": "Thủy",        // Ngũ hành
  "am_duong": 1,            // NEW: Âm dương (1/-1)
  "is_body_house": false,   // Cung Thân
  "tuan_trung": false,      // NEW: Tuần Triệt
  "triet_lo": false,        // NEW: Triệt Lộ
  "major_period": 82,       // Đại hạn
  "minor_period": "Dần",    // Tiểu hạn
  "stars": [...]            // Danh sách sao (xem bên dưới)
}
```

### Stars (9 fields):
```json
{
  "star_id": 1,                  // NEW: ID sao
  "name": "Tử Vi",               // Tên sao
  "element": "O",                // Ngũ hành (K/M/T/H/O)
  "category": 1,                 // Loại sao
  "strength": "Đắc",             // Đặc tính: Vượng/Miếu/Đắc/Bình/Hãm
  "direction": "Đế tinh",        // NEW: Bắc đẩu/Nam đẩu tinh
  "am_duong": 1,                 // NEW: Âm dương (1/-1)
  "trang_sinh": 0,               // NEW: Vòng Tràng sinh (0/1)
  "css_class": "hanhTho"         // NEW: CSS class
}
```

### Extra (21 fields):
```json
{
  "name": "Nguyễn Văn A",                    // NEW: Tên người
  "gender": "Nam",                           // Giới tính (text)
  "gender_value": 1,                         // NEW: Giới tính (số)
  "hour": "Mậu Tý",                          // Giờ sinh (Can Chi)
  "solar_date": "1/1/1990",                  // Ngày dương lịch
  "lunar_date": "5/12/1989",                 // Ngày âm lịch
  "thang_nhuan": 0,                          // NEW: Tháng nhuận
  "stem_branch": {                           // Can Chi (tên)
    "year": "Kỷ Tỵ",
    "month": "Bính Tý",
    "day": "Giáp Dần",
    "hour": "Mậu Tý"
  },
  "stem_branch_numbers": {                   // NEW: Can Chi (số)
    "can_nam": 6, "chi_nam": 6,
    "can_thang": 3, "chi_thang": 1,
    "can_ngay": 3, "chi_ngay": 3,
    "can_gio_sinh": 5
  },
  "hour_can_chi": "Tý",                      // NEW: Chi giờ sinh
  "cuc": "Thổ 5 cục",                        // Tên cục
  "hanh_cuc": 5,                             // NEW: ID ngũ hành cục
  "menh": "Đại Lâm Mộc",                     // Bản mệnh
  "menh_id": 2,                              // NEW: ID mệnh
  "menh_chu": "Vũ khúc",                     // NEW: Mệnh chủ ⭐
  "than_chu": "Thiên cơ",                    // NEW: Thân chủ ⭐
  "menh_vs_cuc": "Cục Khắc Mệnh",           // Quan hệ Mệnh-Cục
  "am_duong_nam_sinh": "Âm",                 // NEW: Âm/Dương năm sinh
  "am_duong_menh": "Âm dương thuận lý",      // NEW: Thuận/Nghịch lý ⭐
  "timezone": 7,                             // NEW: Múi giờ
  "today": "21/10/2025"                      // NEW: Ngày lập lá số
}
```

## Troubleshooting

### UI không kết nối được với API

1. Kiểm tra API server đang chạy: mở `http://localhost:8000/docs` trong trình duyệt
2. Kiểm tra console trong DevTools (F12) xem có lỗi CORS không
3. Đảm bảo URL trong HTML đúng: `http://localhost:8000` (không phải 127.0.0.1 nếu có vấn đề)

### Layout bị lệch

1. Đảm bảo trình duyệt hỗ trợ CSS Grid
2. Thử zoom in/out để xem rõ hơn
3. Resize cửa sổ trình duyệt

### Không thấy sao trong cung

- Backend có thể chưa tính đủ sao
- Kiểm tra response data trong Network tab (F12)

## Cập nhật từ version cũ

Nếu đã có dữ liệu từ API cũ (chỉ có `name` field), cần:

1. Cập nhật backend API (đã được sửa trong commit này)
2. Restart API server
3. Tạo lá số mới để có đầy đủ field `branch` và `name`
