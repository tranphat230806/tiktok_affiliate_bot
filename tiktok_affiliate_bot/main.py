import os
import json
import random
import time
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# Import cấu hình và module
from config import *
from tiktok_uploader import TikTokUploader

from real_shopee_api import RealShopeeAPI 
# ================= TẠO THƯ MỤC =================
os.makedirs("data", exist_ok=True)
os.makedirs("videos", exist_ok=True)

# ================= KHỞI TẠO SCRAPER =================

scraper = RealShopeeAPI(AFFILIATE_ID)
# ================= HÀM LẤY SẢN PHẨM THẬT =================
def get_product():
    """Lấy 1 sản phẩm ngẫu nhiên từ Shopee THẬT"""
    print("🔄 Đang lấy sản phẩm thật từ Shopee...")
    products = scraper.get_hot_products(limit=20)
    
    if products and len(products) > 0:
        product = random.choice(products)
        
        # Tải ảnh sản phẩm về
        if product.get('image_url'):
            img_path = scraper.download_product_image(
                product['image_url'],
                save_path="videos/product_image.jpg"
            )
            if img_path:
                product['image_url'] = img_path
            else:
                product['image_url'] = ""  # Sẽ dùng ảnh nền sau
        
        # Đảm bảo có description
        if not product.get('description'):
            product['description'] = f"Sản phẩm {product['name']} chất lượng cao, giá tốt nhất"
        
        print(f"📦 Chọn sản phẩm THẬT: {product['name']}")
        print(f"💰 Giá: {product['price']:,}đ")
        if product.get('rating_star'):
            print(f"⭐ Đánh giá: {product['rating_star']}/5")
        if product.get('sold'):
            print(f"📦 Đã bán: {product['sold']}")
        
        return product
    else:
        print("⚠️ Không lấy được sản phẩm thật, dùng mẫu dự phòng")
        return {
            "id": "sp_fallback",
            "name": "Áo thun Unisex Cotton",
            "price": 199000,
            "image_url": "",
            "affiliate_link": f"https://shope.ee/aff_{AFFILIATE_ID}_fallback",
            "description": "Sản phẩm chất lượng cao, giao hàng nhanh chóng"
        }

# ================= TẠO CAPTION =================
def generate_caption(product):
    """Tạo caption hấp dẫn với link clickable"""
    templates = [
        f"🔥 {product['name']} - {product['description']}\n💰 Giá CHỈ {product['price']:,}đ\n🛒 Đặt ngay: {product['affiliate_link']}\n#Sale #Shopee #FYP",
        
        f"📦 REVIEW: {product['name']}\n⭐ {product['description']}\n💸 {product['price']:,}đ\n👉 {product['affiliate_link']}\n#Affiliate #MuaSam",
        
        f"Cả nhà ơi! Em vừa săn được {product['name']} giá {product['price']:,}đ\n{product['description']}\nLink đây ạ 👇\n{product['affiliate_link']}\n#SaleOff #GiamGia",
        
        f"✨ SIÊU PHẨM {product['name']} ✨\n{product['description']}\n💝 Giá sốc: {product['price']:,}đ\n🔗 {product['affiliate_link']}\n#TikTokShop #FYP"
    ]
    return random.choice(templates)

# ================= TẠO VIDEO =================
def create_video(product, caption):
    """Tạo video từ ảnh sản phẩm"""
    print("🎬 Đang tạo video...")
    
    # Thử dùng ảnh sản phẩm nếu có
    img_path = product.get('image_url', '')
    
    if img_path and os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            img = img.resize((1080, 1920))
            print("   📸 Dùng ảnh sản phẩm thật")
        except:
            img = Image.new('RGB', (1080, 1920), color=(30, 30, 50))
            print("   🎨 Không mở được ảnh, dùng ảnh nền")
    else:
        # Tạo ảnh nền gradient đẹp
        img = Image.new('RGB', (1080, 1920), color=(30, 30, 50))
        draw = ImageDraw.Draw(img)
        
        # Vẽ gradient đơn giản
        for i in range(1920):
            color_value = int(30 + (i / 1920) * 50)
            draw.line([(0, i), (1080, i)], fill=(color_value, color_value, 70))
        
        print("   🎨 Tạo ảnh nền gradient")
    
    draw = ImageDraw.Draw(img)
    
    # Font chữ
    try:
        font_title = ImageFont.truetype("arial.ttf", 70)
        font_price = ImageFont.truetype("arial.ttf", 55)
        font_desc = ImageFont.truetype("arial.ttf", 40)
        font_link = ImageFont.truetype("arial.ttf", 35)
    except:
        font_title = font_price = font_desc = font_link = ImageFont.load_default()
    
    # Vẽ khung viền
    draw.rectangle([(30, 30), (1050, 1890)], outline=(255, 100, 100), width=4)
    
    # Tiêu đề
    draw.text((540, 200), "🌟 SIÊU PHẨM HOT 🌟", fill=(255, 215, 0), font=font_title, anchor="mm")
    
    # Tên sản phẩm
    name = product['name'][:35]
    draw.text((540, 500), name, fill=(255, 255, 255), font=font_title, anchor="mm")
    
    # Đường kẻ ngang
    draw.line([(200, 600), (880, 600)], fill=(255, 100, 100), width=3)
    
    # Giá
    price_text = f"{product['price']:,}đ"
    draw.text((540, 750), price_text, fill=(255, 100, 100), font=font_price, anchor="mm")
    
    # Mô tả
    desc = product.get('description', '')[:50]
    draw.text((540, 950), desc, fill=(220, 220, 220), font=font_desc, anchor="mm")
    
    # Link
    draw.text((540, 1300), "⬇️ CLICK LINK ĐẶT HÀNG ⬇️", fill=(100, 255, 100), font=font_desc, anchor="mm")
    
    link_text = product['affiliate_link'][:45]
    draw.text((540, 1420), link_text, fill=(255, 255, 255), font=font_link, anchor="mm")
    
    # Logo Shopee
    draw.rectangle([(440, 1650), (640, 1750)], fill=(255, 80, 50))
    draw.text((540, 1700), "SHOPEE", fill=(255, 255, 255), font=font_desc, anchor="mm")
    
    # Lưu ảnh
    frame_path = "videos/frame.jpg"
    img.save(frame_path, 'JPEG', quality=90)
    print(f"   💾 Đã tạo ảnh: {frame_path}")
    
    # Tạo video
    try:
        clip = ImageClip(frame_path, duration=VIDEO_DURATION)
        clip = clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))
        
        video_path = TEMP_VIDEO_PATH
        clip.write_videofile(
            video_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        print(f"✅ Video đã tạo: {video_path}")
        
        # Xóa ảnh tạm
        if os.path.exists(frame_path):
            os.remove(frame_path)
        
        return video_path
        
    except Exception as e:
        print(f"⚠️ Lỗi tạo video: {e}")
        print(f"📸 Ảnh đã lưu tại: {frame_path}")
        return frame_path

# ================= QUẢN LÝ SẢN PHẨM ĐÃ ĐĂNG =================
def load_posted_products():
    """Đọc danh sách sản phẩm đã đăng"""
    if os.path.exists(PRODUCTS_DB):
        with open(PRODUCTS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_posted_products(posted_list):
    """Lưu danh sách sản phẩm đã đăng"""
    with open(PRODUCTS_DB, 'w', encoding='utf-8') as f:
        json.dump(posted_list, f, ensure_ascii=False, indent=4)

def log_upload(video_id, product_name):
    """Ghi log upload thành công"""
    with open(UPLOAD_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()}|{video_id}|{product_name}\n")

# ================= JOB CHÍNH =================
def run_job():
    """Chạy 1 job: Lấy sản phẩm -> Tạo video -> Đăng TikTok"""
    print("\n" + "="*60)
    print(f"🚀 BẮT ĐẦU JOB lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 1. Lấy sản phẩm thật
    product = get_product()
    
    # 2. Kiểm tra đã đăng chưa
    posted = load_posted_products()
    if product['id'] in posted:
        print(f"⚠️ Sản phẩm '{product['name']}' đã đăng rồi, bỏ qua")
        return
    
    # 3. Tạo caption
    caption = generate_caption(product)
    print(f"📝 Caption: {caption[:80]}...")
    
    # 4. Tạo video
    try:
        video_path = create_video(product, caption)
        if not video_path or not os.path.exists(video_path):
            print("❌ Tạo video thất bại")
            return
    except Exception as e:
        print(f"❌ Lỗi tạo video: {e}")
        return
    
    # 5. Upload TikTok
    try:
        uploader = TikTokUploader(TIKTOK_SESSION_ID)
        video_id = uploader.upload_with_retry(video_path, caption, max_retries=2)
        
        if video_id:
            posted.append(product['id'])
            save_posted_products(posted)
            log_upload(video_id, product['name'])
            print(f"\n🎉 THÀNH CÔNG! Đã đăng: {product['name']}")
        else:
            print(f"\n❌ THẤT BẠI! Không đăng được: {product['name']}")
    except Exception as e:
        print(f"❌ Lỗi upload: {e}")
    
    # Dọn dẹp
    if os.path.exists(TEMP_VIDEO_PATH):
        try:
            os.remove(TEMP_VIDEO_PATH)
        except:
            pass
    
    print("="*60 + "\n")

# ================= MAIN =================
def main():
    print("🐍 TIKTOK AFFILIATE BOT")
    print(f"🔑 Affiliate ID: {AFFILIATE_ID}")
    print(f"📱 TikTok Session: {TIKTOK_SESSION_ID[:20]}...")
    print("-"*40)
    
    # Kiểm tra cấu hình
    if AFFILIATE_ID == "YOUR_AFFILIATE_ID_HERE":
        print("⚠️ CẢNH BÁO: Bạn chưa sửa AFFILIATE_ID trong config.py!")
        print("👉 Mở file config.py và thay YOUR_AFFILIATE_ID_HERE bằng ID thật")
        return
    
    # Chạy 1 lần để test
    print("🟢 Chạy thử 1 lần...\n")
    run_job()

if __name__ == "__main__":
    main()  