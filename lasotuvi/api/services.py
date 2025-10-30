"""Service layer for generating astrology charts."""

from typing import Dict, List, Tuple

from lasotuvi.App import lapDiaBan
from lasotuvi.DiaBan import diaBan
from lasotuvi.ThienBan import lapThienBan


def build_chart(
    day: int,
    month: int,
    year: int,
    hour_branch: int,
    gender: int,
    name: str | None,
    solar_calendar: bool,
    timezone: int,
) -> Tuple[diaBan, lapThienBan]:
    """Create diaBan and thienBan objects."""

    board = lapDiaBan(
        diaBan,
        nn=day,
        tt=month,
        nnnn=year,
        gioSinh=hour_branch,
        gioiTinh=gender,
        duongLich=1 if solar_calendar else 0,
        timeZone=timezone,
    )
    overview = lapThienBan(
        day,
        month,
        year,
        hour_branch,
        gender,
        name or "",
        board,
        duongLich=solar_calendar,
        timeZone=timezone,
    )
    return board, overview


def serialize_board(board: diaBan) -> List[Dict[str, object]]:
    houses: List[Dict[str, object]] = []
    for house in board.thapNhiCung[1:]:
        stars = [
            {
                "star_id": star.get("saoID"),
                "name": star.get("saoTen"),
                "element": star.get("saoNguHanh"),
                "category": star.get("saoLoai"),
                "strength": star.get("saoDacTinh") or None,
                "direction": star.get("saoPhuongVi") or None,
                "am_duong": star.get("saoAmDuong"),
                "trang_sinh": star.get("vongTrangSinh", 0),
                "css_class": star.get("cssSao"),
            }
            for star in house.cungSao
        ]
        houses.append(
            {
                "house_number": house.cungSo,
                "branch": house.cungTen,
                "name": getattr(house, "cungChu", house.cungTen),
                "element": house.hanhCung,
                "am_duong": house.cungAmDuong,
                "is_body_house": bool(house.cungThan),
                "tuan_trung": getattr(house, "tuanTrung", False),
                "triet_lo": getattr(house, "trietLo", False),
                "major_period": getattr(house, "cungDaiHan", None),
                "minor_period": getattr(house, "cungTieuHan", None),
                "stars": stars,
            }
        )
    return houses


def extract_overview_info(overview: lapThienBan) -> Dict[str, object]:
    return {
        "name": overview.ten,
        "gender": overview.namNu,
        "gender_value": overview.gioiTinh,
        "hour": overview.gioSinh,
        "solar_date": f"{overview.ngayDuong}/{overview.thangDuong}/{overview.namDuong}",
        "lunar_date": f"{overview.ngayAm}/{overview.thangAm}/{overview.namAm}",
        "thang_nhuan": getattr(overview, "thangNhuan", None),
        "stem_branch": {
            "year": f"{overview.canNamTen} {overview.chiNamTen}",
            "month": f"{overview.canThangTen} {overview.chiThangTen}",
            "day": f"{overview.canNgayTen} {overview.chiNgayTen}",
            "hour": overview.gioSinh,
        },
        "stem_branch_numbers": {
            "can_nam": overview.canNam,
            "chi_nam": overview.chiNam,
            "can_thang": overview.canThang,
            "chi_thang": overview.chiThang,
            "can_ngay": overview.canNgay,
            "chi_ngay": overview.chiNgay,
            "can_gio_sinh": overview.canGioSinh,
        },
        "hour_can_chi": f"{overview.chiGioSinh['tenChi']}",
        "cuc": overview.tenCuc,
        "hanh_cuc": overview.hanhCuc,
        "menh": overview.banMenh,
        "menh_id": overview.menh,
        "menh_chu": overview.menhChu,
        "than_chu": overview.thanChu,
        "menh_vs_cuc": overview.sinhKhac,
        "am_duong_nam_sinh": overview.amDuongNamSinh,
        "am_duong_menh": overview.amDuongMenh,
        "timezone": overview.timeZone,
        "today": overview.today,
    }
