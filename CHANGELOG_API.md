# API Changelog - Full Data Serialization Update

## 🎉 Version 0.2.0 - Complete Data Export

### ✨ Summary
Backend API hiện đã trả về **100% dữ liệu** mà thư viện lasotuvi cung cấp, tăng từ ~60% lên 100%.

---

## 📊 Changes Overview

### 1. **HouseInfo Schema** (11 fields)
Đã bổ sung 4 fields mới:

#### ✅ Existing Fields:
- `branch` (str) - Tên chi: Tý, Sửu, Dần...
- `name` (str) - Tên cung chủ: Mệnh, Phụ Mẫu, Phúc Đức...
- `element` (str) - Ngũ hành: Kim, Mộc, Thủy, Hỏa, Thổ
- `is_body_house` (bool) - Cung Thân
- `major_period` (int | null) - Đại hạn
- `minor_period` (str | null) - Tiểu hạn
- `stars` (List[StarInfo]) - Danh sách sao

#### 🆕 New Fields:
- **`house_number`** (int) - Số thứ tự cung (1-12) từ `cungSo`
- **`am_duong`** (int) - Âm dương của cung (1 = Dương, -1 = Âm)
- **`tuan_trung`** (bool) - Có Tuần Triệt hay không
- **`triet_lo`** (bool) - Có Triệt Lộ hay không

---

### 2. **StarInfo Schema** (9 fields)
Đã bổ sung 5 fields mới:

#### ✅ Existing Fields:
- `name` (str) - Tên sao: Tử Vi, Tham Lang...
- `element` (str) - Ngũ hành: K, M, T, H, O
- `category` (int) - Loại sao (1=Chính, 2=Phụ, 3=Quý...)
- `strength` (str | null) - Đặc tính: Vượng, Miếu, Đắc, Bình, Hãm

#### 🆕 New Fields:
- **`star_id`** (int) - ID của sao (số duy nhất)
- **`direction`** (str | null) - Phương vị: "Bắc đẩu tinh", "Nam đẩu tinh"
- **`am_duong`** (int | null) - Âm dương của sao (1/-1)
- **`trang_sinh`** (int) - Thuộc vòng Tràng sinh (0=không, 1=có)
- **`css_class`** (str | null) - CSS class cho styling (hanhKim, hanhMoc...)

---

### 3. **Extra Info** (21 fields)
Đã bổ sung 11 fields mới:

#### ✅ Existing Fields:
- `gender` (str) - "Nam"/"Nữ"
- `hour` (str) - Giờ sinh (Can Chi)
- `solar_date` (str) - Ngày dương lịch
- `lunar_date` (str) - Ngày âm lịch
- `stem_branch` (dict) - Can Chi năm/tháng/ngày/giờ (tên)
- `cuc` (str) - Tên cục: Thủy 2 cục, Mộc 3 cục...
- `menh` (str) - Bản mệnh: Đại Lâm Mộc...
- `menh_vs_cuc` (str) - Quan hệ Mệnh và Cục

#### 🆕 New Fields:
- **`name`** (str) - Tên người (từ request)
- **`gender_value`** (int) - Giá trị giới tính (1/-1)
- **`thang_nhuan`** (int | null) - Tháng nhuận (0=không, số tháng nếu có)
- **`stem_branch_numbers`** (dict) - Can Chi dạng số:
  - `can_nam`, `chi_nam` - Số can chi năm
  - `can_thang`, `chi_thang` - Số can chi tháng
  - `can_ngay`, `chi_ngay` - Số can chi ngày
  - `can_gio_sinh` - Số can giờ sinh
- **`hour_can_chi`** (str) - Chi giờ sinh riêng
- **`hanh_cuc`** (int) - ID ngũ hành của cục (1-5)
- **`menh_id`** (int) - ID ngũ hành năm sinh
- **`menh_chu`** (str) - Mệnh chủ (sao chủ mệnh)
- **`than_chu`** (str) - Thân chủ (sao chủ thân)
- **`am_duong_nam_sinh`** (str) - "Dương"/"Âm" năm sinh
- **`am_duong_menh`** (str) - "Âm dương thuận lý"/"Âm dương nghịch lý"
- **`timezone`** (int) - Múi giờ
- **`today`** (str) - Ngày lập lá số

---

## 📝 Example Response

### Houses:
```json
{
  "house_number": 1,
  "branch": "Tý",
  "name": "Phu thê",
  "element": "Thủy",
  "am_duong": 1,
  "is_body_house": false,
  "tuan_trung": false,
  "triet_lo": false,
  "major_period": 105,
  "minor_period": "Dần",
  "stars": [...]
}
```

### Stars:
```json
{
  "star_id": 9,
  "name": "Tham lang",
  "element": "T",
  "category": 1,
  "strength": "H",
  "direction": "Bắc đẩu tinh",
  "am_duong": -1,
  "trang_sinh": 0,
  "css_class": "hanhThuy"
}
```

### Extra:
```json
{
  "name": "Test User",
  "gender": "Nam",
  "gender_value": 1,
  "menh_chu": "Vũ khúc",
  "than_chu": "Thiên cơ",
  "am_duong_menh": "Âm dương thuận lý",
  "am_duong_nam_sinh": "Âm",
  "thang_nhuan": 0,
  "today": "21/10/2025",
  "stem_branch_numbers": {
    "can_nam": 6,
    "chi_nam": 6,
    "can_thang": 4,
    "chi_thang": 12,
    "can_ngay": 3,
    "chi_ngay": 3,
    "can_gio_sinh": 5
  },
  ...
}
```

---

## 🔄 Migration Guide

### Backward Compatibility
✅ **Tất cả existing fields vẫn giữ nguyên tên và cấu trúc.**
✅ **Chỉ bổ sung thêm fields mới, không breaking changes.**

### Updated Clients
Nếu bạn đang sử dụng API client cũ:
- Client cũ **vẫn hoạt động bình thường** (backward compatible)
- Cập nhật models để nhận thêm fields mới
- Sử dụng Optional typing cho các fields mới nếu cần support cả data cũ lẫn mới

---

## 🧪 Testing

Chạy test script để xem dữ liệu đầy đủ:

```bash
python test_full_data.py
```

Output sẽ hiển thị:
- Số lượng fields trong mỗi house
- Sample data từ house và star
- Toàn bộ extra info
- JSON file: `test_full_data_output.json`

---

## 📚 Files Changed

- ✏️ `lasotuvi/api/schemas.py` - Updated models
- ✏️ `lasotuvi/api/services.py` - Enhanced serialization
- ➕ `test_full_data.py` - Test script
- ➕ `CHANGELOG_API.md` - This file
- 📝 `data_analysis.md` - Data structure analysis

---

## 🎯 Benefits

1. **Đầy đủ thông tin** - Frontend có đủ data để hiển thị chi tiết
2. **Flexible UI** - Có thể tùy chỉnh hiển thị theo nhiều cách khác nhau
3. **Tử Vi chuyên nghiệp** - Hiển thị đúng Âm/Dương, Mệnh chủ, Thân chủ...
4. **Sorting & Filtering** - Có house_number và star_id để sắp xếp
5. **Styling** - Có css_class sẵn để styling theo ngũ hành

---

## 🚀 Next Steps

1. Update UI để hiển thị các fields mới (optional)
2. Thêm filtering/sorting dựa trên house_number
3. Hiển thị Mệnh chủ, Thân chủ trong UI
4. Styling sao theo css_class
5. Đánh dấu cung đặc biệt (Tuần Triệt, Triệt Lộ)

---

**Date**: October 21, 2025  
**Author**: Factory AI Assistant
