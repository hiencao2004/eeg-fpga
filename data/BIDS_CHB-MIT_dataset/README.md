# Dataset: BIDS CHB-MIT Scalp EEG Database

## 1. Nguồn gốc
* **Link tải:** https://zenodo.org/records/10259996
* **Loại:** Đây là phiên bản BIDS-compatible (đã qua xử lý) của bộ CHB-MIT gốc.

## 2. Mô tả ngắn
* Bộ dữ liệu này chứa bản ghi EEG của 23 bệnh nhi tại Bệnh viện Nhi Boston.
* **Khác biệt chính:** Dữ liệu đã được chỉnh sửa để chỉ giữ lại **18 kênh** theo montage "double banana". Các chú thích (annotation) được định dạng lại thành file `.tsv`.
* **Tổng dung lượng:** ~21.7 GB (file .zip).

## 3. Cấu trúc dữ liệu
* **Định dạng:** .edf
* **Tần số lấy mẫu:** 256 Hz
* **Độ phân giải:** 16-bit
* **Số kênh:** 18 kênh (theo montage double banana)
* **Chú thích (Annotation):** Dạng file `.tsv`, tương thích với BIDS.

* Script tiền xử lý : `process_bids_chbmit.py`
* Script này sẽ đọc file `.edf` và file `.tsv` để chuyển sang file pickle .pkl
Cấu trúc trong file:

pos_array.pkl (seizure): shape (N_pos, 18, 256)
neg_array.pkl (non-seizure): shape (N_neg, 18, 256)

N epoch, 18 kênh, 256 mẫu (FREQ=64 và WINDOW_SIZE=4)