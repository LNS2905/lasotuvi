# Phân tích dữ liệu Backend API vs Thư viện lasotuvi

## 1. Dữ liệu từ cungDiaBan (DiaBan.py)

### ✅ Đã có trong API:
- `branch` (cungTen - tên chi: Tý, Sửu, Dần...)
- `name` (cungChu - tên cung chủ: Mệnh, Phụ Mẫu...)
- `element` (hanhCung - ngũ hành: Kim, Mộc, Thủy, Hỏa, Thổ)
- `is_body_house` (cungThan - boolean)
- `major_period` (cungDaiHan - đại hạn)
- `minor_period` (cungTieuHan - tiểu hạn)
- `stars` (cungSao - danh sách sao)

### ❌ THIẾU trong API:
- `cungSo` - Số thứ tự cung (1-12)
- `cungAmDuong` - Âm dương của cung (1/-1)
- `tuanTrung` - Có Tuần Triệt hay không (boolean)
- `trietLo` - Có Triệt Lộ hay không (boolean)

---

## 2. Dữ liệu từ Sao (Sao.py)

### ✅ Đã có trong API:
- `name` (saoTen - tên sao: Tử Vi, Tham Lang...)
- `element` (saoNguHanh - ngũ hành: K, M, T, H, O)
- `category` (saoLoai - loại sao: 1-chính, 2-phụ, 3-quý...)
- `strength` (saoDacTinh - đặc tính: Vượng, Miếu, Đắc, Bình, Hãm)

### ❌ THIẾU trong API:
- `saoID` - ID của sao (số)
- `saoPhuongVi` - Phương vị: "Bắc đẩu tinh", "Nam đẩu tinh"
- `saoAmDuong` - Âm dương của sao (1/-1)
- `vongTrangSinh` - Thuộc vòng Tràng sinh hay không (0/1)
- `cssSao` - CSS class cho ngũ hành
- `saoViTriCung` - Vị trí cung của sao

---

## 3. Dữ liệu từ lapThienBan (ThienBan.py)

### ✅ Đã có trong API (extra):
- `gender` (namNu: "Nam"/"Nữ")
- `hour` (gioSinh)
- `solar_date` (ngày dương lịch)
- `lunar_date` (ngày âm lịch)
- `stem_branch.year` (canNamTen + chiNamTen)
- `stem_branch.month` (canThangTen + chiThangTen)
- `stem_branch.day` (canNgayTen + chiNgayTen)
- `cuc` (tenCuc - tên cục: Thủy 2 cục, Mộc 3 cục...)
- `menh` (banMenh - bản mệnh: Đại Lâm Mộc...)
- `menh_vs_cuc` (sinhKhac - quan hệ mệnh và cục)

### ❌ THIẾU trong API:
- `gioiTinh` (1/-1 numeric)
- `chiGioSinh` - Chi giờ sinh (object)
- `canGioSinh` - Can giờ sinh (số)
- `timeZone` - Múi giờ
- `today` - Ngày lập lá số
- `ten` - Tên người (có trong request nhưng không trong extra)
- `thangNhuan` - Tháng nhuận (nếu có)
- `canThang`, `chiThang` (số thay vì tên)
- `canNam`, `chiNam` (số thay vì tên)
- `canNgay`, `chiNgay` (số thay vì tên)
- `amDuongNamSinh` - "Dương"/"Âm"
- `amDuongMenh` - "Âm dương thuận lý"/"nghịch lý"
- `hanhCuc` - Ngũ hành của cục (ID số)
- `menhChu` - Mệnh chủ
- `thanChu` - Thân chủ
- `menh` - Ngũ hành năm sinh (số)

---

## 4. Thuộc tính quan trọng còn thiếu cho UI đẹp

### Ưu tiên cao (cần cho UI truyền thống):
1. **cungSo** - để sort đúng thứ tự 1-12
2. **saoPhuongVi** - để hiển thị Bắc/Nam đẩu
3. **saoAmDuong** - để phân biệt sao Âm/Dương
4. **tuanTrung, trietLo** - để đánh dấu cung đặc biệt
5. **cungAmDuong** - âm dương của cung
6. **menhChu, thanChu** - thông tin quan trọng trong tử vi
7. **amDuongMenh** - thuận/nghịch lý
8. **thangNhuan** - nếu sinh vào tháng nhuận
9. **today** - ngày lập lá số
10. **Can/Chi giờ sinh** (riêng biệt)

### Ưu tiên trung bình:
- saoID
- cssSao
- vongTrangSinh
- hanhCuc (ID số)
- canNgay, chiNgay (số)

### Ưu tiên thấp:
- saoViTriCung (đã biết qua house)

---

## 5. Khuyến nghị

### Bổ sung vào `HouseInfo`:
```python
class HouseInfo(BaseModel):
    # Existing
    branch: str
    name: str
    element: str
    is_body_house: bool
    major_period: Optional[int] = None
    minor_period: Optional[str] = None
    stars: List[StarInfo]
    
    # NEW
    house_number: int  # cungSo (1-12)
    am_duong: int  # cungAmDuong (1/-1)
    tuan_trung: bool  # có Tuần Triệt
    triet_lo: bool  # có Triệt Lộ
```

### Bổ sung vào `StarInfo`:
```python
class StarInfo(BaseModel):
    # Existing
    name: str
    element: str
    category: int
    strength: Optional[str] = None
    
    # NEW
    star_id: int  # saoID
    direction: str  # saoPhuongVi (Bắc đẩu, Nam đẩu)
    am_duong: int  # saoAmDuong (1/-1)
    trang_sinh: int  # vongTrangSinh (0/1)
```

### Bổ sung vào `extra`:
```python
{
    # Existing...
    
    # NEW
    "menh_chu": str,  # Mệnh chủ
    "than_chu": str,  # Thân chủ
    "am_duong_nam_sinh": str,  # "Dương"/"Âm"
    "am_duong_menh": str,  # "Âm dương thuận lý"/"nghịch lý"
    "thang_nhuan": bool,  # Tháng nhuận
    "today": str,  # Ngày lập lá số
    "hour_can_chi": str,  # Can Chi giờ sinh
}
```

---

## 6. Tổng kết

**Tỷ lệ dữ liệu đã có**: ~60%
- ✅ Houses: 7/11 fields (64%)
- ✅ Stars: 4/10 fields (40%)
- ✅ Extra: 10/22 fields (45%)

**Cần bổ sung thêm**: ~40% dữ liệu để đầy đủ và chính xác hơn.
