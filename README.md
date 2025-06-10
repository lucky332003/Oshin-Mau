# Oshin-Mau
# 🤖 Bot Discord Chọn Màu Role

Một bot Discord đơn giản cho phép thành viên trong server tự chọn một màu sắc riêng cho tên của mình bằng mã màu HEX. Bot cũng có tính năng tự động dọn dẹp các role màu không còn ai sử dụng.

**Tác giả:** Thành (HADES)

## ✨ Tính năng

* 🎨 **20 Màu Đặt Sẵn**: Cung cấp danh sách 20 màu phổ biến để người dùng lựa chọn nhanh.
* 💡 **Màu Tùy Chỉnh**: Cho phép người dùng nhập mã màu HEX bất kỳ để tạo màu sắc cá nhân.
* 🗑️ **Xóa Role Cũ**: Tự động xóa role màu cũ của người dùng khi họ chọn một màu mới.
* 🧹 **Tự Động Dọn Dẹp**: Lệnh `/tudongxoarole` (yêu cầu quyền *Manage Roles*) để xóa các role màu không ai dùng, giữ server gọn gàng.
* 🚀 **Dễ Triển Khai**: Cấu hình sẵn để triển khai 24/7 trên nền tảng **Render**.

## ⚙️ Cài đặt & Chạy ở Máy cá nhân (Local)

1.  **Clone repository về máy:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Tạo và kích hoạt môi trường ảo:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Thiết lập token:**
    Bot lấy token từ biến môi trường tên là `DISCORD_TOKEN`. Bạn có thể tạo file `.env` để chạy local.
    ```
    DISCORD_TOKEN=your_super_secret_discord_bot_token
    ```
    *Lưu ý: Tệp `.gitignore` đã được cấu hình để bỏ qua file `.env`, đảm bảo bạn không đưa token lên GitHub.*

5.  **Chạy bot:**
    ```bash
    python main.py
    ```

## 🚀 Hướng dẫn Triển khai 24/7 lên Render

Bạn có thể host bot này miễn phí và hoạt động 24/7 trên [Render](https://render.com/).

1.  **Đăng ký tài khoản:**
    Tạo một tài khoản trên Render, bạn có thể liên kết trực tiếp với tài khoản GitHub của mình cho tiện.

2.  **Tạo một "Background Worker" mới:**
    * Trên trang Dashboard của Render, nhấn **"New +"** và chọn **"Background Worker"**.
    * Kết nối với kho GitHub (repository) mà bạn vừa đăng tải code lên.

3.  **Cấu hình dịch vụ:**
    * **Name**: Đặt tên cho dịch vụ của bạn (ví dụ: `discord-color-bot`).
    * **Region**: Chọn khu vực gần bạn nhất (ví dụ: `Singapore`).
    * **Build Command**: Để mặc định là `pip install -r requirements.txt`.
    * **Start Command**: `python main.py`.
    * **Instance Type**: Chọn **Free** (Miễn phí).

4.  **Thêm Biến Môi Trường (Quan trọng):**
    * Cuộn xuống phần **"Advanced"**.
    * Nhấn **"Add Environment Variable"**.
    * Nhập vào 2 ô:
        * **Key**: `DISCORD_TOKEN`
        * **Value**: `dán_token_bot_của_bạn_vào_đây`

5.  **Triển khai:**
    * Nhấn nút **"Create Background Worker"** ở cuối trang.
    * Render sẽ tự động cài đặt và chạy bot của bạn. Bạn có thể xem log để theo dõi quá trình khởi động.

Bot của bạn giờ đã hoạt động trực tuyến 24/7!
