# ================= FILE: tiktok_uploader.py =================
# Module upload video lên TikTok dùng session ID

import os
import time
from datetime import datetime

# Import thư viện đúng
try:
    from tiktokautouploader import upload_tiktok
    UPLOADER_AVAILABLE = True
    print("✅ Đã tìm thấy tiktokautouploader")
except ImportError:
    UPLOADER_AVAILABLE = False
    print("⚠️ Chưa cài tiktokautouploader")
    print("👉 Chạy lệnh: pip install tiktokautouploader")


class TikTokUploader:
    """
    Upload video lên TikTok bằng session_id
    """
    
    def __init__(self, session_id):
        """
        Khởi tạo uploader với session_id
        """
        self.session_id = session_id
        self.account_name = "default"  # Bạn có thể đặt tên tài khoản
        
        if not self.session_id or len(self.session_id) < 5:
            raise Exception("❌ Session ID không hợp lệ!")
        
        print(f"✅ Đã nạp session TikTok: {self.session_id[:15]}...")
        
        if not UPLOADER_AVAILABLE:
            print("⚠️ CẢNH BÁO: tiktokautouploader chưa được cài đặt!")
            print("👉 Chạy lệnh: pip install tiktokautouploader")
    
    def upload_video(self, video_path, caption, allow_comments=True, allow_duet=True):
        """
        Đăng video lên TikTok
        """
        print("\n" + "="*50)
        print(f"📤 [{datetime.now().strftime('%H:%M:%S')}] Bắt đầu upload...")
        
        # Kiểm tra file
        if not os.path.exists(video_path):
            print(f"❌ Không tìm thấy file: {video_path}")
            return None
        
        if not UPLOADER_AVAILABLE:
            print("❌ tiktokautouploader chưa được cài đặt!")
            return None
        
        # Kiểm tra dung lượng
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"📹 File: {os.path.basename(video_path)} ({file_size_mb:.1f} MB)")
        print(f"📝 Caption: {caption[:80]}...")
        
        # Upload với session ID
        # Thư viện này sẽ tự động lưu session sau lần đăng nhập đầu
        try:
            print("⏳ Đang upload lên TikTok...")
            print("⚠️ Lần đầu chạy sẽ mở trình duyệt để bạn đăng nhập. Sau đó session sẽ được lưu lại.")
            
            # Upload video
            result = upload_tiktok(
                video=video_path,
                description=caption,
                accountname=self.account_name,
                headless=False,  # Lần đầu nên để False để đăng nhập
                suppressprint=False
            )
            
            if result:
                print(f"\n✅ UPLOAD THÀNH CÔNG!")
                return "uploaded_success"
            else:
                print("❌ Upload thất bại")
                return None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Lỗi: {error_msg}")
            
            if "login" in error_msg.lower() or "session" in error_msg.lower():
                print("\n🔧 Bạn cần đăng nhập lần đầu!")
                print("👉 Lần chạy đầu tiên, trình duyệt sẽ mở ra, hãy đăng nhập TikTok.")
                print("👉 Sau khi đăng nhập thành công, session sẽ được lưu lại.")
            
            return None
    
    def upload_with_retry(self, video_path, caption, max_retries=2):
        """Upload với cơ chế thử lại"""
        for attempt in range(max_retries):
            if attempt > 0:
                wait_time = 10 * attempt
                print(f"\n⏳ Chờ {wait_time} giây trước khi thử lại lần {attempt + 1}...")
                time.sleep(wait_time)
            
            result = self.upload_video(video_path, caption)
            if result:
                return result
        
        print("\n❌ Đã thử hết số lần, upload thất bại!")
        return None


# ================= HÀM TEST =================
def test_uploader():
    """Kiểm tra uploader có hoạt động không"""
    print("🔍 Kiểm tra tiktokautouploader...")
    
    if UPLOADER_AVAILABLE:
        print("✅ tiktokautouploader đã sẵn sàng")
        return True
    else:
        print("❌ Chưa cài tiktokautouploader")
        print("\n📌 Cài đặt bằng lệnh:")
        print("   pip install tiktokautouploader")
        return False

if __name__ == "__main__":
    test_uploader()