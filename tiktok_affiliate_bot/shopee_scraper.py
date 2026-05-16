# ================= FILE: shopee_scraper.py =================
# Lấy sản phẩm thật từ Shopee - PHIÊN BẢN HOẠT ĐỘNG CHẮC CHẮN

import requests
import json
import random
import time
import os
from datetime import datetime
from PIL import Image
from io import BytesIO

class ShopeeScraper:
    def __init__(self, affiliate_id):
        self.affiliate_id = affiliate_id
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'Referer': 'https://shopee.vn/',
            'Origin': 'https://shopee.vn',
            'Connection': 'keep-alive'
        }
    
    def get_hot_products(self, limit=10):
        """Lấy sản phẩm hot từ Shopee"""
        print(f"[{datetime.now()}] 🔍 Đang lấy sản phẩm thật từ Shopee...")
        
        # Dùng API search của Shopee với từ khóa phổ biến
        search_keywords = ["áo thun", "son", "tai nghe", "balo", "đồng hồ", "giày", "túi xách"]
        
        all_products = []
        
        for keyword in random.sample(search_keywords, 3):
            try:
                url = "https://shopee.vn/api/v4/search/search_items"
                params = {
                    "by": "pop",
                    "keyword": keyword,
                    "limit": limit,
                    "newest": 0,
                    "order": "desc",
                    "page_type": "search",
                    "version": 2
                }
                
                print(f"   🔍 Tìm kiếm: {keyword}")
                response = requests.get(url, headers=self.headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    
                    for item in items:
                        item_data = item.get('item_basic', {})
                        
                        if not item_data:
                            continue
                        
                        # Lấy giá
                        price = item_data.get('price', 0)
                        if price:
                            price = int(price) // 100000  # Chuyển về đồng
                        
                        product = {
                            'id': str(item_data.get('itemid', '')),
                            'shop_id': str(item_data.get('shopid', '')),
                            'name': item_data.get('name', keyword)[:80],
                            'price': price if price > 0 else 100000,
                            'image_url': item_data.get('image', ''),
                            'sold': item_data.get('sold', 0),
                            'rating_star': item_data.get('item_rating', {}).get('rating_star', 0),
                            'likes': item_data.get('likes', 0)
                        }
                        
                        # Tạo mô tả
                        product['description'] = self._get_desc_from_name(product['name'])
                        
                        # Tạo link affiliate
                        product['full_url'] = f"https://shopee.vn/product/{product['shop_id']}/{product['id']}/"
                        product['affiliate_link'] = f"https://shope.ee/{self.affiliate_id}_{product['id']}"
                        
                        all_products.append(product)
                    
                    print(f"   ✅ Tìm thấy {len(items)} sản phẩm cho '{keyword}'")
                    time.sleep(1)  # Tránh bị chặn
                    
                else:
                    print(f"   ⚠️ Lỗi HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ⚠️ Lỗi: {e}")
                continue
        
        # Loại bỏ trùng lặp
        seen = set()
        unique_products = []
        for p in all_products:
            if p['id'] not in seen:
                seen.add(p['id'])
                unique_products.append(p)
        
        print(f"✅ Tổng cộng: {len(unique_products)} sản phẩm thật")
        
        if not unique_products:
            # Fallback: trả về sản phẩm mẫu nếu không lấy được
            print("⚠️ Không lấy được sản phẩm thật, dùng sản phẩm mẫu")
            return self._get_mock_products()
        
        return unique_products[:limit]
    
    def _get_desc_from_name(self, name):
        """Tạo mô tả từ tên sản phẩm"""
        templates = [
            f"{name} chất lượng cao, giao nhanh, giá tốt nhất",
            f"{name} - Hàng chính hãng, đổi trả trong 7 ngày",
            f"🔥 HOT: {name} đang được săn đón, số lượng có hạn",
            f"{name} - Mua ngay kẻo lỡ, free ship cho đơn hàng đầu tiên",
            f"✨ {name} - Sản phẩm được yêu thích nhất tuần qua"
        ]
        return random.choice(templates)
    
    def _get_mock_products(self):
        """Sản phẩm mẫu dự phòng"""
        return [
            {
                "id": "mock_001",
                "name": "Áo thun Unisex Cotton",
                "price": 199000,
                "image_url": "",
                "affiliate_link": f"https://shope.ee/aff_{self.affiliate_id}_mock_001",
                "description": "Chất liệu mềm mại, thấm hút mồ hôi",
                "rating_star": 4.8,
                "sold": 1234
            },
            {
                "id": "mock_002",
                "name": "Son Kem Lì Siêu Mịn",
                "price": 89000,
                "image_url": "",
                "affiliate_link": f"https://shope.ee/aff_{self.affiliate_id}_mock_002",
                "description": "Lên màu chuẩn, lì siêu đẹp",
                "rating_star": 4.9,
                "sold": 5678
            }
        ]
    
    def download_product_image(self, image_id, save_path="videos/product_image.jpg"):
        """Tải ảnh sản phẩm từ Shopee"""
        if not image_id:
            print("   ⚠️ Không có ID ảnh")
            return None
        
        # Tạo URL ảnh đúng định dạng Shopee
        if image_id.startswith('http'):
            image_url = image_id
        else:
            # Định dạng ảnh Shopee: https://cf.shopee.vn/file/{image_id}
            image_url = f"https://cf.shopee.vn/file/{image_id}"
        
        os.makedirs("videos", exist_ok=True)
        
        try:
            print(f"   📸 Đang tải ảnh...")
            response = requests.get(image_url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                # Resize về kích thước phù hợp
                img = img.resize((1080, 1920))
                img.save(save_path, 'JPEG', quality=85)
                print(f"   ✅ Đã tải ảnh: {save_path}")
                return save_path
            else:
                print(f"   ⚠️ Lỗi tải ảnh: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ⚠️ Lỗi tải ảnh: {e}")
            return None


# ============ TEST ============
if __name__ == "__main__":
    scraper = ShopeeScraper("1739555045")
    products = scraper.get_hot_products(limit=5)
    
    print("\n" + "="*50)
    print("KẾT QUẢ:")
    for p in products:
        print(f"\n📦 {p['name']}")
        print(f"💰 Giá: {p['price']:,}đ")
        print(f"⭐ Đánh giá: {p.get('rating_star', 'N/A')}")
        print(f"📦 Đã bán: {p.get('sold', 'N/A')}")
        print(f"🔗 Link: {p['affiliate_link']}")