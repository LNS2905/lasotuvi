"""Test script to verify full data serialization"""
import json
import sys
from lasotuvi.api.services import build_chart, serialize_board, extract_overview_info

# Set console encoding to UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Build a chart
board, overview = build_chart(
    day=1,
    month=1,
    year=1990,
    hour_branch=1,
    gender=1,
    name='Test User',
    solar_calendar=True,
    timezone=7
)

# Serialize data
houses = serialize_board(board)
extra = extract_overview_info(overview)

# Print summary
print("="*60)
print("DATA SERIALIZATION TEST")
print("="*60)

print(f"\n[OK] Total houses: {len(houses)}")
print(f"[OK] Fields per house: {len(houses[0].keys())}")
print(f"[OK] Fields in extra: {len(extra.keys())}")

print("\n" + "="*60)
print("SAMPLE HOUSE (First house):")
print("="*60)
print(f"House Number: {houses[0]['house_number']}")
print(f"Branch: {houses[0]['branch']}")
print(f"Name: {houses[0]['name']}")
print(f"Element: {houses[0]['element']}")
print(f"Am Duong: {houses[0]['am_duong']}")
print(f"Is Body House: {houses[0]['is_body_house']}")
print(f"Tuan Trung: {houses[0]['tuan_trung']}")
print(f"Triet Lo: {houses[0]['triet_lo']}")
print(f"Major Period: {houses[0]['major_period']}")
print(f"Minor Period: {houses[0]['minor_period']}")
print(f"Number of Stars: {len(houses[0]['stars'])}")

if houses[0]['stars']:
    print("\n" + "="*60)
    print("SAMPLE STAR (First star in first house):")
    print("="*60)
    star = houses[0]['stars'][0]
    print(f"Star ID: {star['star_id']}")
    print(f"Name: {star['name']}")
    print(f"Element: {star['element']}")
    print(f"Category: {star['category']}")
    print(f"Strength: {star['strength']}")
    print(f"Direction: {star['direction']}")
    print(f"Am Duong: {star['am_duong']}")
    print(f"Trang Sinh: {star['trang_sinh']}")
    print(f"CSS Class: {star['css_class']}")

print("\n" + "="*60)
print("EXTRA INFO (First 10 keys):")
print("="*60)
for key in list(extra.keys())[:10]:
    print(f"{key}: {extra[key]}")

print("\n" + "="*60)
print("IMPORTANT EXTRA FIELDS:")
print("="*60)
print(f"Menh Chu: {extra.get('menh_chu')}")
print(f"Than Chu: {extra.get('than_chu')}")
print(f"Am Duong Menh: {extra.get('am_duong_menh')}")
print(f"Am Duong Nam Sinh: {extra.get('am_duong_nam_sinh')}")
print(f"Thang Nhuan: {extra.get('thang_nhuan')}")
print(f"Today: {extra.get('today')}")

# Save to JSON file for inspection
output = {
    "houses": houses,
    "extra": extra
}

with open('test_full_data_output.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("[OK] Full data saved to: test_full_data_output.json")
print("="*60)
