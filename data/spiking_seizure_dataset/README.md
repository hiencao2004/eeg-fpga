# Dataset 1: Spiking Seizure Classification Dataset

## 1. Nguồn gốc
* **Link tải:** https://zenodo.org/records/10800794
* **DOI:** 10.5281/zenodo.10800794
* **Nguồn gốc (Quan trọng):** Đây là bộ dữ liệu **đã qua xử lý**. Dữ liệu analog gốc được lấy từ "SWEC-ETHZ iEEG Database".

## 2. Mô tả ngắn
* Đây là bộ dữ liệu các tín hiệu EEG (từ SWEC-ETHZ) đã được mã hóa thành dạng **sự kiện (event-based/spikes)** để phát hiện động kinh.
* Dữ liệu chứa **10 cơn động kinh** được ghi lại từ **5 bệnh nhân**.
* Toàn bộ quá trình mã hóa được thực hiện bằng bộ xử lý thần kinh (neuromorphic processor) **DYNAP-SE2**.
* **Tổng dung lượng:** 904.9 MB (file .zip).

## 3. Phương pháp tạo (Mã hóa sang Spike)
Quá trình xử lý này là điểm mấu chốt của dataset, bao gồm 2 phần:

1.  **AFE (Analog Front End):** Tín hiệu EEG gốc (kỹ thuật số) được chuyển sang analog (qua DAC), sau đó được khuếch đại và mã hóa thành chuỗi sự kiện (spikes) bằng Bộ điều biến Delta không đồng bộ (Asynchronous Delta Modulator - ADM).
2.  **SNN (NLNG - Non-Local Non-Global):** Chuỗi sự kiện từ AFE được đưa vào một mạng SNN. Mạng SNN này sẽ trích xuất các đặc trưng của cơn động kinh (dưới dạng các cụm đồng bộ-synchronous patterns).

## 4### Nội dung file `.csv` 
Mỗi file `.csv` chứa các thông tin sau:
* **Comments (Chú thích):**
    * `# SStart: 180`: Thời gian (tính theo giây) bắt đầu cơn động kinh.
    * `# SEnd: 276.0`: Thời gian kết thúc cơn động kinh.
    * `# Pid: 2`: ID của bệnh nhân.
    * `# Sid: 1`: ID của cơn động kinh.
    * `# Channel_No: 1`: Số thứ tự kênh.

* **Các cột dữ liệu:**

| Tên cột | Mô tả |
| :--- | :--- |
| `SYS_time` | Thời gian (timestamp) từ FPGA |
| `signal_time` | Thời gian của tín hiệu (khớp với dataset SWEC ETHZ gốc) |
| `dac_value` | Giá trị tín hiệu analog gốc |
| `ADMspikes` | **Output của AFE (Spike):** `True` nếu có spike, `False` nếu không |
| `NLNGspikes` | **Output của SNN (Spike):** `True` nếu có spike, `False` nếu không |