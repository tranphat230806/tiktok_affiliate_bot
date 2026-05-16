from config import AFFILIATE_ID
from real_shopee_api import RealShopeeAPI

# Khởi tạo scraper
print("="*50)
print("KIỂM TRA LẤY SẢN PHẨM THẬT TỪ SHOPEE")
print("="*50)

scraper = RealShopeeAPI(AFFILIATE_ID)

# Lấy sản phẩm thật
products = scraper.get_hot_products(limit=5)

print("\n" + "="*50)
print(f"KẾT QUẢ: Tìm thấy {len(products)} sản phẩm")
print("="*50)

for i, p in enumerate(products, 1):
    print(f"\n{i}. 📦 Tên: {p['name']}")
    print(f"   💰 Giá: {p['price']:,}đ")
    print(f"   ⭐ Đánh giá: {p.get('rating_star', 'N/A')}")
    print(f"   📦 Đã bán: {p.get('sold', 'N/A')}")
    print(f"   🔗 Link Affiliate: {p['affiliate_link']}")
    print(f"   🖼️ Ảnh: {p.get('image_url', 'Không có')[:60]}...")
    print("-"*40)

print("\n✅ Test hoàn tất!")