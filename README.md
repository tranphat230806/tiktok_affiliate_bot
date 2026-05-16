# 🤖 TikTok Affiliate Bot

**Vietnamese Version | [English Version](#english-version)**

---

## 📌 Mô Tả Dự Án

TikTok Affiliate Bot là một công cụ tự động hóa Python tiên tiến dành cho các affiliate marketer. Nó giúp tự động scrape sản phẩm bán chạy từ Shopee, tạo video marketing chuyên nghiệp, và đăng tải tự động lên TikTok cùng với affiliate link - giúp tối ưu hóa quá trình kiếm thụ hưởng tiếp thị.

**Tính năng chính:**
- ✅ Scrape sản phẩm THẬT từ Shopee API (không hardcode)
- ✅ Tạo video marketing 1080x1920 (TikTok format)
- ✅ Tự động đăng video lên TikTok với caption hấp dẫn
- ✅ Quản lý affiliate links tự động
- ✅ Theo dõi sản phẩm đã đăng (tránh trùng lặp)
- ✅ Cơ chế retry tự động khi upload thất bại
- ✅ Logging chi tiết cho mỗi job

---

## 🏗️ Kiến Trúc Dự Án

### Luồng Hoạt Động Chính

```
┌─────────────────────────────────────────────────────┐
│  MAIN JOB LOOP (run_job)                            │
└─────────────────────────────────────────────────────┘
           │
           ├─────────────┬──────────────┬───────────────┐
           ▼             ▼              ▼               ▼
    ┌──────────┐   ┌──────────┐  ┌─────────┐  ┌─────────────┐
    │ Scraper  │   │ Validator│  │ Generate│  │ Video       │
    │ (Get)    │   │(Check if │  │ Caption │  │ Creator     │
    │Products  │   │ Posted)  │  │         │  │             │
    └──────────┘   └──────────┘  └─────────┘  └─────────────┘
           │             │              │               │
           └─────────────┴──────────────┴───────────────┘
                         │
                         ▼
                   ┌──────────────┐
                   │   Uploader   │
                   │ (TikTok API) │
                   └──────────────┘
                         │
                    ┌────┴────┐
                    ▼         ▼
              ┌──────────┐ ┌─────────────┐
              │Save Log  │ │Track Product│
              └──────────┘ └─────────────┘
```

### Thành Phần Chính

| Module | Mục Đích | Đặc Điểm |
|--------|----------|----------|
| `main.py` | Orchestrator chính | Điều phối toàn bộ workflow, có check config |
| `real_shopee_api.py` | Scraper Shopee | Lấy sản phẩm thật từ Shopee, fallback graceful |
| `shopee_scraper.py` | Alternative Scraper | Có thể gọi real Shopee API với retry logic |
| `tiktok_uploader.py` | TikTok Uploader | Upload video sử dụng tiktokautouploader lib |
| `config.py` | Configuration | 2 cấu hình bắt buộc: Affiliate ID + Session ID |

---

## 📁 Cấu Trúc Thư Mục

```
tiktok_affiliate_bot/
├── main.py                      # Script chính (entry point)
├── config.py                    # Cấu hình (⚠️ được ignore bởi .gitignore)
├── requirements.txt             # Dependencies
│
├── tiktok_uploader.py          # Module upload TikTok
├── real_shopee_api.py          # Scraper sản phẩm thật
├── shopee_scraper.py           # Alternative scraper (API call)
├── free_api_scraper.py         # TODO: Module scraper khác
├── test_scraper.py             # Kiểm tra scraper
│
├── data/
│   ├── products_posted.json    # Danh sách sản phẩm đã đăng (tracking)
│   └── upload_log.txt          # Log chi tiết mỗi lần upload
│
├── videos/                      # Thư mục tạm cho video/frame
│   ├── temp_video.mp4          # Video tạm thời
│   └── product_image.jpg       # Ảnh sản phẩm
│
├── .gitignore                  # Ignore config, cookies, env
└── README.md                   # Documentation (this file)
```

**⚠️ Lưu ý Bảo Mật:**
- `config.py` được ignore (chứa sensitive data)
- `TK_cookies_default.json` được ignore
- `.env` files được ignore
- Session ID không được commit lên repo

---

## 🚀 Hướng Dẫn Cài Đặt

### 1. Yêu Cầu Hệ Thống
- Python 3.8+
- pip (package manager)
- FFmpeg (cho moviepy, tùy chọn)

### 2. Clone Repository
```bash
git clone <repo-url>
cd tiktok_affiliate_bot
```

### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies chính:**
- `Pillow>=10.0.0` - Xử lý hình ảnh
- `moviepy>=1.0.3` - Tạo video từ ảnh
- `requests>=2.31.0` - HTTP requests
- `schedule>=1.2.0` - Scheduling jobs
- `TikTokLive>=1.0.0` - TikTok API
- `tiktokautouploader` - Upload TikTok (install riêng)

### 4. Cài Đặt Optional (TikTok Uploader)
```bash
pip install tiktokautouploader
```

---

## ⚙️ Hướng Dẫn Cấu Hình

### Bước 1: Lấy Affiliate ID từ Shopee

1. Truy cập [Shopee Affiliate](https://affiliate.shopee.vn)
2. Đăng nhập tài khoản
3. Copy **Affiliate ID** từ dashboard
4. Ví dụ: `17395550452`

### Bước 2: Lấy TikTok Session ID

#### Phương Pháp 1: Từ TikTok Web
1. Mở TikTok.com và đăng nhập
2. Mở DevTools (F12)
3. Vào tab **Application** → **Cookies**
4. Tìm cookie tên `sessionid`
5. Copy value của nó

#### Phương Pháp 2: Từ TikTok Auto Uploader
Lần đầu chạy, thư viện sẽ tự động mở trình duyệt để bạn đăng nhập, session sẽ được lưu tự động.

### Bước 3: Cập Nhật Config

Mở file `config.py` và cập nhật:

```python
# 1. AFFILIATE ID của bạn trên Shopee
AFFILIATE_ID = "17395550452"  # <--- THAY VÀO ĐÂY

# 2. SESSION ID từ TikTok
TIKTOK_SESSION_ID = "7c460458088cb7f504ce503f96418bbc"  # <--- DÁN VÀO ĐÂY

# (Tùy chọn) Cấu hình khác:
SCHEDULE_TIMES = ["07:00", "12:00", "19:00"]  # 3 bài/ngày
VIDEO_DURATION = 10  # giây (5-60s an toàn)
```

---

## 🎯 Cách Chạy Dự Án

### Chạy Một Lần (Test)
```bash
python main.py
```

**Output mong đợi:**
```
🐍 TIKTOK AFFILIATE BOT
🔑 Affiliate ID: 17395550452
📱 TikTok Session: 7c460458088cb7...
-----------
🟢 Chạy thử 1 lần...

🚀 BẮT ĐẦU JOB lúc: 2026-05-16 10:30:45
==============================================
🔄 Đang lấy sản phẩm thật từ Shopee...
📦 Chọn sản phẩm THẬT: Tai nghe Bluetooth True Wireless
💰 Giá: 399,000đ
⭐ Đánh giá: 4.8/5

🎬 Đang tạo video...
📸 Dùng ảnh sản phẩm thật
📤 Bắt đầu upload...
✅ UPLOAD THÀNH CÔNG!
🎉 THÀNH CÔNG! Đã đăng: Tai nghe Bluetooth True Wireless
```

### Chạy Định Kỳ (Scheduling)

**Option 1: Chạy 3 lần/ngày (07:00, 12:00, 19:00)**
```bash
# Lưu code này vào file `scheduler.py`
import schedule
import time
from main import run_job

schedule.every().day.at("07:00").do(run_job)
schedule.every().day.at("12:00").do(run_job)
schedule.every().day.at("19:00").do(run_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Chạy: `python scheduler.py`

**Option 2: Chạy mỗi N giờ**
```bash
# Mỗi 4 giờ chạy 1 lần
python -c "import schedule, time; from main import run_job; schedule.every(4).hours.do(run_job); [schedule.run_pending() or time.sleep(60) for _ in iter(int, 1)]"
```

---

## 🔄 Luồng Hoạt Động Chi Tiết

### 1️⃣ Scraping Sản Phẩm

```python
# real_shopee_api.py - Cách hoạt động
scraper = RealShopeeAPI("17395550452")
products = scraper.get_hot_products(limit=20)

# Output:
# - Lấy 20 sản phẩm hot từ Shopee
# - Các sản phẩm có: id, name, price, image_url, rating_star, sold
# - Tự động tạo affiliate link: https://shope.ee/aff_{ID}_{PRODUCT_ID}
# - Nếu lỗi → fallback tới sản phẩm mẫu (graceful degradation)
```

**Sản phẩm Mẫu (Fallback):**
- Tai nghe Bluetooth (399,000đ)
- Sạc dự phòng (299,000đ)
- Chuột không dây (249,000đ)
- Bàn phím cơ (1,290,000đ)
- etc.

### 2️⃣ Tạo Video

```python
# main.py - create_video()
# 1. Resize ảnh về 1080x1920 (TikTok vertical format)
# 2. Vẽ text overlay:
#    - Tiêu đề: "🌟 SIÊU PHẨM HOT 🌟"
#    - Tên sản phẩm
#    - Giá bán
#    - Mô tả
#    - Link affiliate + "CLICK ĐẶT HÀNG"
#    - Logo Shopee
# 3. Chuyển ảnh thành video 10 giây (mp4 format)
# 4. Xóa file tạm
```

**Output Video:** `videos/temp_video.mp4`

### 3️⃣ Upload TikTok

```python
# tiktok_uploader.py - upload_with_retry()
# 1. Kiểm tra file video tồn tại
# 2. Gọi tiktokautouploader library
# 3. Nếu lần 1 thất bại → retry lần 2 (sau 10 giây)
# 4. Trả về video_id nếu thành công
# 5. Log kết quả vào upload_log.txt
```

### 4️⃣ Tracking Sản Phẩm

```python
# main.py - load_posted_products() / save_posted_products()
# File: data/products_posted.json
# Format: ["product_id_1", "product_id_2", ...]
# Tác dụng: Tránh đăng sản phẩm bị lặp lại
```

**Ví dụ:**
```json
[
  "25648021334",
  "18945612378",
  "34567891234"
]
```

---

## 📊 Workflow Upload TikTok

### Trạng Thái Workflow

```
START
  │
  ├─► [Load Config] ──────────► Kiểm tra AFFILIATE_ID, SESSION_ID
  │        │
  │        ▼
  ├─► [Get Product] ──────────► Scrape từ Shopee API
  │        │
  │        ▼
  ├─► [Check Duplicate] ──────► Xem sản phẩm đã posted chưa?
  │        │                          │
  │        │                      (Nếu yes) → SKIP
  │        │
  │        ▼
  ├─► [Generate Caption] ─────► Random caption template
  │        │
  │        ▼
  ├─► [Create Video] ─────────► PIL + moviepy
  │        │
  │        ▼
  ├─► [Upload TikTok] ────────► tiktokautouploader
  │        │
  │        ├─► [Retry Logic] ──► Nếu lỗi, thử 2 lần
  │        │
  │        ▼
  ├─► [Save Tracking] ────────► Ghi product_id vào JSON
  │        │
  │        ▼
  ├─► [Log Result] ───────────► Ghi vào upload_log.txt
  │        │
  │        ▼
  └─► END
```

### Log Files

**data/upload_log.txt:**
```
2026-05-16 10:30:45.123456|uploaded_success|Tai nghe Bluetooth True Wireless
2026-05-16 12:15:32.654321|uploaded_success|Sạc dự phòng Polymer 20000mAh
2026-05-16 14:45:10.987654|upload_failed|Chuột không dây Logitech (retry quá hạn)
```

**data/products_posted.json:**
```json
[
  "25648021334",
  "18945612378",
  "34567891234",
  "45678912345"
]
```

---

## 🛠️ Công Nghệ & Dependencies

| Package | Phiên Bản | Mục Đích |
|---------|-----------|----------|
| **Pillow** | >=10.0.0 | Image processing, text rendering, gradient creation |
| **moviepy** | >=1.0.3 | Video creation from frames, codec support (libx264) |
| **requests** | >=2.31.0 | HTTP requests tới Shopee API, image download |
| **schedule** | >=1.2.0 | Job scheduling (daily times) |
| **TikTokLive** | >=1.0.0 | TikTok API integration |
| **tiktokautouploader** | Latest | TikTok video upload automation |

### Công Nghệ Chính

- **Python 3.8+** - Runtime
- **FFmpeg** - Video codec support (optional, but recommended)
- **PIL/Pillow** - Graphics pipeline
- **moviepy** - Video composition (ffmpeg wrapper)

---

## ⚠️ Lưu Ý Bảo Mật & Luật Pháp

### 1. Ethical Automation
- ✅ Tuân thủ [Shopee ToS](https://shopee.vn/terms)
- ✅ Tuân thủ [TikTok ToS](https://www.tiktok.com/legal/page/row/terms-of-service/)
- ✅ Không spam, không misleading content
- ✅ Affiliate link rõ ràng & transparent

### 2. Bảo Mật
- 🔐 **Giữ kín Affiliate ID & Session ID**
  - Không commit vào Git (đã .gitignore)
  - Không chia sẻ publicly
  - Rotate regularly
  
- 🔐 **TikTok Session**
  - Session sẽ hết hạn sau vài tuần
  - Cần refresh session định kỳ
  - Lần đầu upload sẽ cần đăng nhập

### 3. Scraping Policy
- ⚠️ Shopee API này là public endpoint, không "hack"
- ⚠️ Thêm rate limiting nếu scrape quá nhiều (tránh bị IP ban)
- ⚠️ Respect robots.txt & API rate limits

### 4. Content Policy
- ⚠️ Chỉ share genuine reviews/recommendations
- ⚠️ Không fake testimonials
- ⚠️ Affiliate disclosure rõ ràng
- ⚠️ Comply với quốc gia của bạn (FTC, ASA, etc.)

### 5. Files Được Ignore
```
# .gitignore
config.py                    # Chứa Affiliate ID, Session ID
TK_cookies_default.json     # TikTok cookies
.env                        # Environment variables
.env.local
credentials.json
data/upload_log.txt         # Logs có thể chứa sensitive data
videos/                     # Temporary files
__pycache__/
```

---

## 📈 Hướng Phát Triển (Roadmap)

### Phase 1: MVP (✅ Done)
- [x] Scrape sản phẩm từ Shopee
- [x] Tạo video marketing
- [x] Upload TikTok
- [x] Tracking products

### Phase 2: Enhancement (🚧 In Progress)
- [ ] Multiple account support (round-robin posting)
- [ ] AI caption generation (GPT-based)
- [ ] Advanced video effects & transitions
- [ ] Product analytics (view, like, conversion tracking)
- [ ] Webhook for external triggers
- [ ] Database migration (JSON → SQLite/PostgreSQL)

### Phase 3: Scaling (📋 Planned)
- [ ] Support multiple affiliate programs (Lazada, Tiki, Shopee)
- [ ] Batch video generation
- [ ] Distributed uploading (multiple TikTok accounts)
- [ ] Dashboard UI for monitoring
- [ ] Email/Slack notifications
- [ ] Performance metrics & ROI tracking

### Phase 4: Optimization (💡 Ideas)
- [ ] ML-based optimal posting time detection
- [ ] Trending hashtag integration
- [ ] Competitor product monitoring
- [ ] Dynamic pricing updates
- [ ] A/B testing captions
- [ ] Video CDN caching

---

## 🤝 Contribution

Contributions welcome! Bạn có thể:
1. Report bugs via GitHub Issues
2. Submit feature requests
3. Fork & create Pull Requests
4. Improve documentation

**Chuẩn code:**
- Follow PEP 8 style guide
- Add docstrings cho hàm mới
- Test trước khi submit PR

---

## 📝 License

MIT License - Xem file [LICENSE](LICENSE) để chi tiết

---

## 📞 Support

- 📧 Email: [your-email@example.com]
- 🐛 Issues: https://github.com/your-repo/issues
- 💬 Discussions: https://github.com/your-repo/discussions

---

---

## English Version

# 🤖 TikTok Affiliate Bot

**[Vietnamese Version](#vietnamese-version) | English Version**

---

## 📌 Project Description

TikTok Affiliate Bot is an advanced Python automation tool for affiliate marketers. It automatically scrapes trending products from Shopee, creates professional marketing videos, and uploads them to TikTok with affiliate links - optimizing your affiliate marketing workflow.

**Key Features:**
- ✅ Scrape REAL products from Shopee API (no hardcoding)
- ✅ Generate marketing videos in 1080x1920 (TikTok format)
- ✅ Auto-post videos to TikTok with compelling captions
- ✅ Automatic affiliate link management
- ✅ Posted product tracking (prevent duplicates)
- ✅ Automatic retry mechanism for uploads
- ✅ Detailed logging for each job

---

## 🏗️ Project Architecture

### Main Workflow

```
┌─────────────────────────────────────────────────────┐
│  MAIN JOB LOOP (run_job)                            │
└─────────────────────────────────────────────────────┘
           │
           ├─────────────┬──────────────┬───────────────┐
           ▼             ▼              ▼               ▼
    ┌──────────┐   ┌──────────┐  ┌─────────┐  ┌─────────────┐
    │ Scraper  │   │ Validator│  │ Generate│  │ Video       │
    │ (Get)    │   │(Check if │  │ Caption │  │ Creator     │
    │Products  │   │ Posted)  │  │         │  │             │
    └──────────┘   └──────────┘  └─────────┘  └─────────────┘
           │             │              │               │
           └─────────────┴──────────────┴───────────────┘
                         │
                         ▼
                   ┌──────────────┐
                   │   Uploader   │
                   │ (TikTok API) │
                   └──────────────┘
                         │
                    ┌────┴────┐
                    ▼         ▼
              ┌──────────┐ ┌─────────────┐
              │Save Log  │ │Track Product│
              └──────────┘ └─────────────┘
```

### Main Components

| Module | Purpose | Features |
|--------|---------|----------|
| `main.py` | Main orchestrator | Coordinates full workflow, config validation |
| `real_shopee_api.py` | Shopee Scraper | Fetch real products, graceful fallback |
| `shopee_scraper.py` | Alternative Scraper | Can call real Shopee API with retry logic |
| `tiktok_uploader.py` | TikTok Uploader | Upload videos using tiktokautouploader lib |
| `config.py` | Configuration | 2 required settings: Affiliate ID + Session ID |

---

## 📁 Directory Structure

```
tiktok_affiliate_bot/
├── main.py                      # Main script (entry point)
├── config.py                    # Configuration (⚠️ ignored by .gitignore)
├── requirements.txt             # Dependencies
│
├── tiktok_uploader.py          # TikTok upload module
├── real_shopee_api.py          # Real product scraper
├── shopee_scraper.py           # Alternative scraper (API calls)
├── free_api_scraper.py         # TODO: Other scraper module
├── test_scraper.py             # Scraper tests
│
├── data/
│   ├── products_posted.json    # List of posted products (tracking)
│   └── upload_log.txt          # Detailed upload logs
│
├── videos/                      # Temporary video/frame directory
│   ├── temp_video.mp4          # Temporary video file
│   └── product_image.jpg       # Product image
│
├── .gitignore                  # Ignore config, cookies, env
└── README.md                   # Documentation (this file)
```

**⚠️ Security Notes:**
- `config.py` is ignored (contains sensitive data)
- `TK_cookies_default.json` is ignored
- `.env` files are ignored
- Session IDs are never committed to repo

---

## 🚀 Installation Guide

### 1. System Requirements
- Python 3.8+
- pip (package manager)
- FFmpeg (for moviepy, optional)

### 2. Clone Repository
```bash
git clone <repo-url>
cd tiktok_affiliate_bot
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Main Dependencies:**
- `Pillow>=10.0.0` - Image processing
- `moviepy>=1.0.3` - Video creation from images
- `requests>=2.31.0` - HTTP requests
- `schedule>=1.2.0` - Job scheduling
- `TikTokLive>=1.0.0` - TikTok API
- `tiktokautouploader` - TikTok upload (install separately)

### 4. Install Optional TikTok Uploader
```bash
pip install tiktokautouploader
```

---

## ⚙️ Configuration Guide

### Step 1: Get Affiliate ID from Shopee

1. Visit [Shopee Affiliate](https://affiliate.shopee.vn)
2. Login with your account
3. Copy **Affiliate ID** from dashboard
4. Example: `17395550452`

### Step 2: Get TikTok Session ID

#### Method 1: From TikTok Web
1. Open TikTok.com and login
2. Open DevTools (F12)
3. Go to **Application** tab → **Cookies**
4. Find cookie named `sessionid`
5. Copy its value

#### Method 2: From TikTok Auto Uploader
On first run, the library will automatically open a browser for login, and session will be saved automatically.

### Step 3: Update Config

Open `config.py` and update:

```python
# 1. Your Shopee Affiliate ID
AFFILIATE_ID = "17395550452"  # <--- REPLACE HERE

# 2. TikTok Session ID
TIKTOK_SESSION_ID = "7c460458088cb7f504ce503f96418bbc"  # <--- PASTE HERE

# (Optional) Other configuration:
SCHEDULE_TIMES = ["07:00", "12:00", "19:00"]  # 3 posts/day
VIDEO_DURATION = 10  # seconds (5-60s is safe)
```

---

## 🎯 Running the Project

### Run Once (Test)
```bash
python main.py
```

**Expected Output:**
```
🐍 TIKTOK AFFILIATE BOT
🔑 Affiliate ID: 17395550452
📱 TikTok Session: 7c460458088cb7...
-----------
🟢 Running test once...

🚀 JOB START at: 2026-05-16 10:30:45
==============================================
🔄 Fetching real products from Shopee...
📦 Selected product: Bluetooth True Wireless Earbuds
💰 Price: 399,000đ
⭐ Rating: 4.8/5

🎬 Creating video...
📸 Using real product image
📤 Starting upload...
✅ UPLOAD SUCCESS!
🎉 SUCCESS! Posted: Bluetooth True Wireless Earbuds
```

### Run Periodically (Scheduling)

**Option 1: Run 3 times/day (07:00, 12:00, 19:00)**
```bash
# Save this to `scheduler.py`
import schedule
import time
from main import run_job

schedule.every().day.at("07:00").do(run_job)
schedule.every().day.at("12:00").do(run_job)
schedule.every().day.at("19:00").do(run_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Run: `python scheduler.py`

**Option 2: Run every N hours**
```bash
# Run every 4 hours
python -c "import schedule, time; from main import run_job; schedule.every(4).hours.do(run_job); [schedule.run_pending() or time.sleep(60) for _ in iter(int, 1)]"
```

---

## 🔄 Detailed Workflow

### 1️⃣ Product Scraping

```python
# real_shopee_api.py - How it works
scraper = RealShopeeAPI("17395550452")
products = scraper.get_hot_products(limit=20)

# Output:
# - Fetches 20 trending products from Shopee
# - Each product has: id, name, price, image_url, rating_star, sold
# - Auto-generates affiliate link: https://shope.ee/aff_{ID}_{PRODUCT_ID}
# - On error → fallback to sample products (graceful degradation)
```

**Sample Products (Fallback):**
- Bluetooth Earbuds (399,000đ)
- Power Bank (299,000đ)
- Wireless Mouse (249,000đ)
- Mechanical Keyboard (1,290,000đ)
- etc.

### 2️⃣ Video Creation

```python
# main.py - create_video()
# 1. Resize image to 1080x1920 (TikTok vertical format)
# 2. Draw text overlays:
#    - Title: "🌟 SUPER PRODUCT 🌟"
#    - Product name
#    - Price
#    - Description
#    - Affiliate link + "CLICK TO ORDER"
#    - Shopee logo
# 3. Convert image to 10-second video (mp4 format)
# 4. Delete temporary files
```

**Output Video:** `videos/temp_video.mp4`

### 3️⃣ TikTok Upload

```python
# tiktok_uploader.py - upload_with_retry()
# 1. Verify video file exists
# 2. Call tiktokautouploader library
# 3. If first attempt fails → retry second time (after 10 sec)
# 4. Return video_id if successful
# 5. Log result to upload_log.txt
```

### 4️⃣ Product Tracking

```python
# main.py - load_posted_products() / save_posted_products()
# File: data/products_posted.json
# Format: ["product_id_1", "product_id_2", ...]
# Purpose: Prevent posting duplicate products
```

**Example:**
```json
[
  "25648021334",
  "18945612378",
  "34567891234"
]
```

---

## 📊 TikTok Upload Workflow

### Workflow States

```
START
  │
  ├─► [Load Config] ──────────► Validate AFFILIATE_ID, SESSION_ID
  │        │
  │        ▼
  ├─► [Get Product] ──────────► Scrape from Shopee API
  │        │
  │        ▼
  ├─► [Check Duplicate] ──────► Is product already posted?
  │        │                          │
  │        │                      (If yes) → SKIP
  │        │
  │        ▼
  ├─► [Generate Caption] ─────► Random caption template
  │        │
  │        ▼
  ├─► [Create Video] ─────────► Pillow + moviepy
  │        │
  │        ▼
  ├─► [Upload TikTok] ────────► tiktokautouploader
  │        │
  │        ├─► [Retry Logic] ──► If error, try 2 times
  │        │
  │        ▼
  ├─► [Save Tracking] ────────► Write product_id to JSON
  │        │
  │        ▼
  ├─► [Log Result] ───────────► Write to upload_log.txt
  │        │
  │        ▼
  └─► END
```

### Log Files

**data/upload_log.txt:**
```
2026-05-16 10:30:45.123456|uploaded_success|Bluetooth True Wireless Earbuds
2026-05-16 12:15:32.654321|uploaded_success|Polymer Power Bank 20000mAh
2026-05-16 14:45:10.987654|upload_failed|Logitech Wireless Mouse (max retries exceeded)
```

**data/products_posted.json:**
```json
[
  "25648021334",
  "18945612378",
  "34567891234",
  "45678912345"
]
```

---

## 🛠️ Technology Stack & Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **Pillow** | >=10.0.0 | Image processing, text rendering, gradient creation |
| **moviepy** | >=1.0.3 | Video creation from frames, codec support (libx264) |
| **requests** | >=2.31.0 | HTTP requests to Shopee API, image download |
| **schedule** | >=1.2.0 | Job scheduling (daily times) |
| **TikTokLive** | >=1.0.0 | TikTok API integration |
| **tiktokautouploader** | Latest | TikTok video upload automation |

### Main Technologies

- **Python 3.8+** - Runtime
- **FFmpeg** - Video codec support (optional, but recommended)
- **PIL/Pillow** - Graphics pipeline
- **moviepy** - Video composition (ffmpeg wrapper)

---

## ⚠️ Security & Legal Notes

### 1. Ethical Automation
- ✅ Comply with [Shopee ToS](https://shopee.vn/terms)
- ✅ Comply with [TikTok ToS](https://www.tiktok.com/legal/page/row/terms-of-service/)
- ✅ No spam, no misleading content
- ✅ Affiliate links are clear & transparent

### 2. Security
- 🔐 **Keep Affiliate ID & Session ID secret**
  - Never commit to Git (already .gitignored)
  - Don't share publicly
  - Rotate regularly
  
- 🔐 **TikTok Session**
  - Sessions expire after a few weeks
  - Need to refresh session regularly
  - First upload will require login

### 3. Scraping Policy
- ⚠️ This Shopee API is a public endpoint, not "hacked"
- ⚠️ Add rate limiting if scraping too much (prevent IP ban)
- ⚠️ Respect robots.txt & API rate limits

### 4. Content Policy
- ⚠️ Only share genuine reviews/recommendations
- ⚠️ No fake testimonials
- ⚠️ Clear affiliate disclosure
- ⚠️ Comply with your country's regulations (FTC, ASA, etc.)

### 5. Ignored Files
```
# .gitignore
config.py                    # Contains Affiliate ID, Session ID
TK_cookies_default.json     # TikTok cookies
.env                        # Environment variables
.env.local
credentials.json
data/upload_log.txt         # Logs may contain sensitive data
videos/                     # Temporary files
__pycache__/
```

---

## 📈 Development Roadmap

### Phase 1: MVP (✅ Done)
- [x] Scrape products from Shopee
- [x] Create marketing videos
- [x] Upload to TikTok
- [x] Product tracking

### Phase 2: Enhancement (🚧 In Progress)
- [ ] Multiple account support (round-robin posting)
- [ ] AI caption generation (GPT-based)
- [ ] Advanced video effects & transitions
- [ ] Product analytics (view, like, conversion tracking)
- [ ] Webhook for external triggers
- [ ] Database migration (JSON → SQLite/PostgreSQL)

### Phase 3: Scaling (📋 Planned)
- [ ] Support multiple affiliate programs (Lazada, Tiki, Shopee)
- [ ] Batch video generation
- [ ] Distributed uploading (multiple TikTok accounts)
- [ ] Monitoring dashboard UI
- [ ] Email/Slack notifications
- [ ] Performance metrics & ROI tracking

### Phase 4: Optimization (💡 Ideas)
- [ ] ML-based optimal posting time detection
- [ ] Trending hashtag integration
- [ ] Competitor product monitoring
- [ ] Dynamic pricing updates
- [ ] A/B testing captions
- [ ] Video CDN caching

---

## 🤝 Contributing

Contributions welcome! You can:
1. Report bugs via GitHub Issues
2. Submit feature requests
3. Fork & create Pull Requests
4. Improve documentation

**Code Standards:**
- Follow PEP 8 style guide
- Add docstrings for new functions
- Test before submitting PR

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 📞 Support

- 📧 Email: [your-email@example.com]
- 🐛 Issues: https://github.com/your-repo/issues
- 💬 Discussions: https://github.com/your-repo/discussions

---

**Last Updated:** 2026-05-16  
**Status:** ✅ Active Development
