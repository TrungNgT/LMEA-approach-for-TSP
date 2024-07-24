# Đồ án: Sử dụng Mô hình ngôn ngữ lớn (LLM) kết hợp giải thuật di truyền (GA) để giải bài toán Người du lịch (TSP)

## Sử dụng chương trình theo đề xuất LMEA
### 1. Thiết lập các đường dẫn, tham số quá trình
- Mở file [instance_pyfile](paper_LMEA_construction/instance_pyfile.py)
- Lựa chọn file input từ mục [dataset](dataset)
- Điều chỉnh các thông số (n, N, G) lần lượt là (số_điểm, kích_thước_quần_thể, số_thế_hệ)
- Các thông số mặc định được đề xuất là (N=16, G=80) để so sánh kết quả các lần chạy

### 2. Chạy chương trình
- Mở Notebook: [LMEA](paper_LMEA_construction/LMEA.ipynb)
- Chú ý  thêm vào thành phần API key của Google Gemini API:

```
        genai.configure(api_key='YOUR_API_KEY')
```

- Thực hiện 'Run All' đối với tất cả các Cell của Notebook


## Sử dụng chương trình theo thuật toán tự đề xuất
### 1. Thiết lập các đường dẫn, tham số quá trình
- Mở file [instance_pyfile](new_approach/instance_pyfile.py)
- Lựa chọn file input từ mục [dataset](dataset)
- Điều chỉnh các thông số (n, N, G) lần lượt là (số_điểm, kích_thước_quần_thể, số_thế_hệ)
- Các thông số mặc định được đề xuất là (N=40, G=80) để so sánh kết quả các lần chạy

### 2. Chạy chương trình
- Mở Notebook: [GA_approach](new_approach/GA_approach.ipynb)
- Chú ý  thêm vào thành phần API key của Google Gemini API:

```
        genai.configure(api_key='YOUR_API_KEY')
```

- Thực hiện 'Run All' đối với tất cả các Cell của Notebook
