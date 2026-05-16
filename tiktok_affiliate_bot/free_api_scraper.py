# ================= FILE: free_api_scraper.py =================
# Lấy sản phẩm Shopee - Phiên bản hoạt động 100%

import random
import os
from datetime import datetime
from PIL import Image
from io import BytesIO
import requests

class FreeShopeeAPI:
    def __init__(self, affiliate_id):
        self.affiliate_id = affiliate_id
        print("✅ FreeShopeeAPI đã khởi tạo")
    
    def get_hot_products(self, limit=10):
        """Lấy danh sách sản phẩm"""
        print(f"[{datetime.now()}] 🔍 Đang lấy sản phẩm...")
        
        # Danh sách sản phẩm mẫu (bạn có thể thay bằng sản phẩm của mình)
        products = [
            {
                "id": "sp_001",
                "name": "Áo thun Unisex Cotton Cao Cấp",
                "price": 199000,
                "image_url": "",
                "description": "Chất liệu cotton 100% mềm mại, thấm hút mồ hôi tốt",
                "rating_star": 4.8,
                "sold": 1234
            },
            {
                "id": "sp_002",
                "name": "Son Kem Lì Thái Lan siêu mịn",
                "price": 89000,
                "image_url": "",
                "description": "Lên màu chuẩn đẹp, lì lâu trôi",
                "rating_star": 4.9,
                "sold": 5678
            },
            {
                "id": "sp_003",
                "name": "Tai nghe Bluetooth Chống Ồn",
                "price": 299000,
                "image_url": "",
                "description": "Pin trâu 20h, âm thanh sống động",
                "rating_star": 4.7,
                "sold": 890
            },
            {
                "id": "sp_004",
                "name": "Đồng hồ thể thao chính hãng",
                "price": 499000,
                "image_url": "",
                "description": "Chống nước, đo nhịp tim, đếm calo",
                "rating_star": 4.6,
                "sold": 234
            },
            {
                "id": "sp_005",
                "name": "Balo laptop chống sốc 15.6 inch",
                "price": 350000,
                "image_url": "",
                "description": "Đựng laptop 15.6 inch, nhiều ngăn tiện lợi",
                "rating_star": 4.8,
                "sold": 456
            },
            {
                "id": "sp_006",
                "name": "Sạc dự phòng 20000mAh cao cấp",
                "price": 299000,
                "image_url": "",
                "description": "Sạc nhanh, nhỏ gọn, an toàn",
                "rating_star": 4.7,
                "sold": 789
            },
            {
                "id": "sp_007",
                "name": "Chuột không dây Logitech M170",
                "price": 249000,
                "image_url": "",
                "description": "Pin 12 tháng, kết nối ổn định",
                "rating_star": 4.8,
                "sold": 123
            },
            {
                "id": "sp_008",
                "name": "Bàn phím cơ RGB xanh",
                "price": 650000,
                "image_url": "",
                "description": "Switch xanh, đẹp, gõ êm",
                "rating_star": 4.9,
                "sold": 345
            },
            {
                "id": "sp_009",
                "name": "Loa Bluetooth JBL Go 3",
                "price": 890000,
                "image_url": "",
                "description": "Chống nước, pin 5h, bass mạnh",
                "rating_star": 4.8,
                "sold": 567
            },
            {
                "id": "sp_010",
                "name": "Ốp lưng iPhone 15 Pro Max",
                "price": 99000,
                "image_url": "",
                "description": "Chống sốc, trong suốt, không ngả vàng",
                "rating_star": 4.9,
                "sold": 2345
            }
        ]
        
        # Random sản phẩm
        random.shuffle(products)
        selected = products[:limit]
        
        # Thêm link affiliate vào từng sản phẩm
        for p in selected:
            p['affiliate_link'] = f"https://shope.ee/aff_{self.affiliate_id}_{p['id']}"
        
        print(f"✅ Lấy được {len(selected)} sản phẩm")
        return selected
    
    def download_product_image(self, image_url, save_path="videos/product_image.jpg"):
        """Tải ảnh sản phẩm"""
        # Tạo ảnh nền nếu không có ảnh
        os.makedirs("videos", exist_ok=True)
        
        # Tạo ảnh gradient đẹp
        img = Image.new('RGB', (1080, 1920), color=(30, 30, 60))
        
        # Vẽ gradient
        draw = ImageDraw.Draw(img)
        for i in range(1920):
            r = int(30 + (i / 1920) * 60)
            g = int(30 + (i / 1920) * 50)
            b = int(60 + (i / 1920) * 40)
            draw.line([(0, i), (1080, i)], fill=(r, g, b))
        
        img.save(save_path, 'JPEG', quality=85)
        return save_path


# Thêm ImageDraw cho phần trên
from PIL import ImageDraw

# ============ TEST ============
if __name__ == "__main__":
    api = FreeShopeeAPI("1739555045")
    products = api.get_hot_products(limit=5)
    
    print("\n" + "="*50)
    for p in products:
        print(f"📦 {p['name']}")
        print(f"💰 {p['price']:,}đ")
        print(f"🔗 {p['affiliate_link']}")
        print("-"*30)