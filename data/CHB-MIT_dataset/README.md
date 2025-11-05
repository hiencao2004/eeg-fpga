# Dataset: CHB-MIT Scalp EEG Database (Bản gốc)

## 1. Nguồn gốc
* **Link tải:** https://physionet.org/content/chbmit/1.0.0/
* **Loại:** Đây là bộ dữ liệu gốc và đầy đủ (classic version).

## 2. Mô tả ngắn
* Bộ dữ liệu này chứa bản ghi EEG của 22 bệnh nhi (23 ca) với các cơn động kinh khó chữa.
* Tổng cộng có 198 cơn động kinh (seizures) đã được chú thích.
* **Tổng dung lượng:** ~42.6 GB (chưa nén).

## 3. Cấu trúc dữ liệu
* **Định dạng:** .edf
* **Tần số lấy mẫu:** 256 Hz
* **Độ phân giải:** 16-bit
* **Số kênh:** Hầu hết các file có 23 kênh EEG (một số file có thể có 24 hoặc 26).
* **Chú thích (Annotation):**
    * File `.seizure`: Đánh dấu thời gian bắt đầu và kết thúc cơn động kinh.
    * File `chbnn-summary.txt`: File tóm tắt thông tin các cơn động kinh trong từng ca.
