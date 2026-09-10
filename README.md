# 🎙️ Ứng Dụng Chuyển Đổi & Nhân Bản Giọng Nói AI (TTS & Voice Cloning)

Ứng dụng đọc văn bản thành giọng nói AI chất lượng cao, **hoàn toàn miễn phí 100%**, không cần API Key, không giới hạn độ dài ký tự, phong phú phong cách giọng đọc và hỗ trợ sẵn sàng cho **Nhân bản giọng mẫu (Voice Cloning)**.

---

## 🌟 Tính Năng Nổi Bật Vừa Được Nâng Cấp

### 1. Bộ lọc phong cách giọng đọc (Voice Presets)
- 🎬 **Review phim / Kể chuyện ma:** Tông trầm lắng, chậm rãi, bí ẩn, lôi cuốn.
- 📻 **Phát thanh viên / Thời sự:** Dứt khoát, rành mạch, tốc độ chuẩn.
- 🎧 **Sách nói thư giãn (Audiobook Calm):** Nhẹ nhàng, từ tốn, thích hợp nghe đêm khuya.
- 🧸 **Hoạt hình / Trẻ con vui nhộn:** Tông giọng cao, trong trẻo, vui tươi.
- 👴 **Người lớn tuổi / Trầm ấm:** Sâu lắng, từng trải.
- ⚡ **Tóm tắt siêu tốc:** Đọc nhanh +35% để lướt nội dung nhanh.
- 🎛️ **Tùy chỉnh tự do:** Tự tay kéo các thanh trượt Speed, Pitch, Volume theo sở thích.

### 2. Mở khóa hơn 300+ Giọng đọc toàn cầu
- Tự động lấy danh mục hơn 300 giọng AI từ Microsoft Edge trên toàn thế giới.
- Lọc theo Quốc gia / Ngôn ngữ: Việt Nam, Mỹ, Anh, Nhật Bản, Hàn Quốc, Trung Quốc, Pháp, Đức, Thái Lan...

### 3. Sẵn sàng tính năng Thêm giọng mẫu (Voice Cloning)
- **Tự động nhận diện phần cứng máy tính:** Kiểm tra xem máy hiện tại có Card đồ họa rời NVIDIA (CUDA) hay đang dùng card tích hợp (Intel UHD Graphics).
- **Phương án Cloud (Dùng được ngay):** Cho phép nạp API Key miễn phí (ElevenLabs) để clone giọng từ file âm thanh 10-60 giây mà không cần card rời.
- **Phương án Local GPU (Khi đổi sang máy có Card rời):** Đã tích hợp sẵn cấu trúc để chạy mô hình AI Offline mã nguồn mở (như F5-TTS, Coqui XTTS-v2) siêu tốc khi bạn chuyển sang máy mới có card NVIDIA.

### 4. Không giới hạn ký tự (Unlimited Length)
- Tự động chia nhỏ văn bản dài thành các đoạn an toàn (~1.800 ký tự) và ghép nối tự động thành **1 file MP3 liên tục duy nhất**.

---

## 🚀 Cách Chạy Ứng Dụng

### Cách 1: Chạy bằng file bấm đúp chuột (Khuyên dùng)
Mở thư mục này và **bấm đúp vào file `run_app.bat`**. Trình duyệt web sẽ tự động mở ứng dụng lên!

### Cách 2: Chạy bằng dòng lệnh Terminal / PowerShell
Mở PowerShell tại thư mục này và gõ:
```bash
python -m streamlit run app.py
```
Sau đó truy cập vào địa chỉ: `http://localhost:8501` trên trình duyệt web của bạn.
