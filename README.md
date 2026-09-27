# Bảng điều khiển phát hiện xu hướng tin tức

## Giới thiệu

Đây là ứng dụng Streamlit để khám phá các xu hướng tin tức đã được lưu trong `trends.json`. Dashboard trình bày tổng quan dữ liệu, phân tích EDA, biểu đồ embedding UMAP, phân tích các cụm xu hướng và thông tin chi tiết của từng cụm. Điểm khởi chạy là `app.py`.

## Cài đặt

Từ thư mục gốc của repository:

```bash
git clone https://github.com/trumcodelord/new_trends_demo.git
cd new_trends_demo
python -m venv .venv
```

Kích hoạt môi trường ảo:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Cài các thư viện được khai báo trong `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## Chạy Streamlit

Chạy lệnh sau tại thư mục gốc, nơi có `app.py` và `trends.json`:

```bash
streamlit run app.py
```

Mở địa chỉ do Streamlit hiển thị trong terminal (thường là `http://localhost:8501`).

## Dữ liệu đầu vào

- `trends.json` là tệp đầu vào mà `app.py` đọc từ thư mục làm việc hiện tại. Repository hiện có sẵn tệp này.
- `data.loader.load_payload` đọc JSON. Nếu gốc là object, ứng dụng lấy `trends`, `metrics`, `model` và `generated_at`; các khóa tùy chọn còn thiếu lần lượt nhận giá trị mặc định là danh sách rỗng, object rỗng, object rỗng và chuỗi rỗng. Loader cũng chấp nhận danh sách xu hướng trực tiếp ở gốc JSON.
- Mỗi xu hướng cần có dữ liệu bài viết trong `articles`; bước tiền xử lý dùng trực tiếp `cluster_id`, `rank` và `coherence` của xu hướng. Với mỗi bài viết, bước này dùng `title`, `description`, `published` và `topic`; các biểu đồ còn dùng các trường như `source`, `umap_x` và `umap_y`. Tệp mẫu trong repository cho thấy cấu trúc dữ liệu thực tế.
- Nếu không tìm thấy `trends.json`, ứng dụng hiển thị lỗi rồi dừng. Nếu danh sách `trends` rỗng, ứng dụng hiển thị cảnh báo rồi dừng. Mã hiện tại không có bước kiểm tra đầy đủ mọi trường của từng bản ghi; dữ liệu sai cấu trúc có thể gây lỗi trong lúc xử lý.
- `clusters.xlsx` không phải đầu vào của `app.py` và không có trong repository hiện tại.

## Cấu trúc thư mục

```text
new_trends_demo/
├── app.py                       # Điểm khởi chạy, ghép các thành phần dashboard
├── trends.json                  # Dữ liệu xu hướng và bài viết
├── requirements.txt             # Thư viện Python
├── README.md
├── news-trend-detection.ipynb   # Notebook có trong repository
├── assets/                      # CSS theo giao diện sáng/tối, danh sách stopwords
├── data/                        # Đọc JSON và chuẩn hóa DataFrame
├── general/                     # Sidebar, header, các chỉ số
├── dataset_overview/            # Tổng quan tập dữ liệu
├── eda_analysis/                # Phân tích khám phá dữ liệu
├── embedding_anslysis/          # Biểu đồ UMAP (giữ đúng tên thư mục trong mã)
├── trends_analysis/             # Biểu đồ và bảng xu hướng
└── trend_detail_analysis/       # Thông tin, bài viết và biểu đồ chi tiết xu hướng
```

## Luồng hoạt động

1. `app.py` thiết lập trang, kiểm tra `trends.json` và nạp CSS theo giao diện sáng hoặc tối từ `assets/`.
2. `data.loader` đọc JSON; ứng dụng dừng nếu không có xu hướng.
3. `data.preprocess` tạo bảng xu hướng và bảng bài viết, bổ sung số từ/ký tự, thời điểm đăng và tên chủ đề tiếng Việt.
4. `general.sidebar` tạo bộ lọc và lọc bảng xu hướng; `general.header` và `general.metrics` hiển thị phần đầu trang.
5. Năm tab lần lượt hiển thị **Tổng quan dữ liệu**, **Phân tích EDA**, **Phân tích embedding**, **Phân tích cụm** và **Phân tích chi tiết cụm**. Tab phân tích cụm gồm heatmap nguồn tin, biểu đồ kích thước/độ kết dính cụm, biểu đồ cột và bảng xu hướng; tab cuối hiển thị chi tiết xu hướng.

## Checklist bàn giao

- [ ] Có `app.py`, `requirements.txt`, các thư mục module và `assets/` như cấu trúc trên.
- [ ] Đặt `trends.json` cùng thư mục làm việc khi chạy lệnh Streamlit; xác nhận danh sách xu hướng không rỗng.
- [ ] Xác nhận dữ liệu xu hướng và bài viết có các trường mà bước tiền xử lý và biểu đồ sử dụng.
- [ ] Cài thư viện bằng `python -m pip install -r requirements.txt`.
- [ ] Chạy `streamlit run app.py` từ thư mục gốc và kiểm tra năm tab cùng bộ lọc trên sidebar.
