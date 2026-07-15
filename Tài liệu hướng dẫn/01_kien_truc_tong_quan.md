# TÀI LIỆU HƯỚNG DẪN 01: KIẾN TRÚC TỔNG QUAN HỆ THỐNG

Tài liệu này dựa trên **Tài liệu Thiết kế Kỹ thuật gốc** nhằm giúp các bạn lập trình viên Intern hình dung toàn bộ luồng đi của dữ liệu từ khi thu thập cho đến khi đưa ra màn hình duyệt và báo cáo.

---

## 1. Nguyên lý phễu lọc chi phí (Cost Funnel)

Để tránh lãng phí tiền gọi API AI (Gemini) cho tất cả bài viết quét được trên mạng xã hội, hệ thống được thiết kế theo hình một chiếc **phễu lọc chi phí**:

1.  **Tầng Sàng lọc (M2):** Chạy trên **100%** dữ liệu thô. Sử dụng các quy tắc văn phong (Regular Expression) và mô hình AI nhỏ tiếng Việt chạy cục bộ (PhoBERT/ViSoBERT) để lọc rác và chấm điểm nghi ngờ. **Tuyệt đối không gọi Gemini ở bước này**.
2.  **Tầng Bộ nhớ đệm (M3):** Chỉ chạy trên các bài viết đáng nghi (1 - 2%). Hệ thống so sánh vector ngữ nghĩa bài viết mới với kho tin giả đã biết (lưu trong ChromaDB). Nếu trùng, trả kết quả kiểm chứng ngay lập tức.
3.  **Tầng Kiểm chứng sâu (M4):** Chỉ chạy khi **bị trượt bộ nhớ đệm** (Cache Miss). Lúc này hệ thống mới dùng Gemini để bóc tách mệnh đề, cào tìm bằng chứng trực tiếp trên Internet và ra phán quyết.

---

## 2. Sơ đồ luồng dữ liệu 7 Mô-đun (Architecture Flowchart)

Dưới đây là sơ đồ Mermaid trực quan hóa đường đi của một bài đăng (`post`) qua các mô-đun:

```mermaid
flowchart TD
    %% Nguồn dữ liệu đầu vào
    Sub1["Kênh Telegram"] --> M1["Mô-đun 1: Thu thập <br/> Collection"]
    Sub2["RSS Báo chí"] --> M1
    Sub3["YouTube API"] --> M1

    %% Khử trùng & Lưu trữ thô
    M1 -->|Khử trùng bằng ID & Lưu posts| DB_Posts[("CSDL SQLite/Postgres")]
    M1 -->|Đẩy sự kiện to_screen| Queue_Screen["Hàng đợi to_screen"]

    %% Sàng lọc thô
    Queue_Screen --> M2["Mô-đun 2: Sàng lọc <br/> Screening"]
    M2 -->|1. Phân loại chủ đề| M2_Eval
    M2 -->|2. Tính điểm giật gân| M2_Eval
    M2_Eval{"Điểm nghi ngờ <br/> vượt ngưỡng?"} 
    M2_Eval -->|Không: Kết thúc sớm| Exit1(["Dừng xử lý - Bài viết bình thường"])
    M2_Eval -->|Có: Đẩy to_memory| Queue_Mem["Hàng đợi to_memory"]

    %% Tra cứu bộ nhớ đệm
    Queue_Mem --> M3["Mô-đun 3: Bộ nhớ cache <br/> Memory Cache"]
    M3 -->|Truy vấn vector| VectorDB[("CSDL ChromaDB")]
    VectorDB --> Match{"Có khớp tin giả cũ?"}

    %% Nhánh Cache Hit
    Match -->|Khớp > 85%| M3_Stance["Kiểm tra Lập trường Stance <br/> ASSERT / REFUTE"]
    M3_Stance --> Stance_Eval{"Lập trường gì?"}
    Stance_Eval -->|REFUTE: Bài đính chính| Exit2(["Dừng xử lý - Bài tin tốt"])
    Stance_Eval -->|ASSERT: Lan truyền tin giả| M6_Quick["Mô-đun 6: Gán kết luận nhanh"]

    %% Nhánh Cache Miss
    Match -->|Không khớp| Queue_Verify["Hàng đợi to_verify"]
    
    %% Kiểm chứng sâu (Deep RAG)
    Queue_Verify --> M4["Mô-đun 4: Kiểm chứng <br/> Verification"]
    M4 -->|1. Tách mệnh đề bằng LLM| M4_Query["2. Tạo Query"]
    M4_Query -->|3. Tìm Google/Serper| M4_Search["4. Cào toàn văn trang nguồn"]
    M4_Search -->|5. Đối soát chữ bằng rapidfuzz| M4_Ground["Chỉ giữ bằng chứng thật"]
    M4_Ground -->|6. LLM hội đồng ra phán quyết| Queue_Alert["Hàng đợi to_alert"]

    %% Con người duyệt
    M6_Quick --> Queue_Alert
    Queue_Alert --> M5["Mô-đun 5: Con người duyệt <br/> Human-in-the-loop"]
    DB_Posts -.->|Hiển thị hồ sơ đầy đủ| M5
    M5 -->|Cán bộ bấm Duyệt/Bác bỏ| Decision{"Quyết định?"}
    
    %% Vòng phản hồi ghi nhận tin giả
    Decision -->|Đồng ý gán nhãn Tin giả| DB_Verified[("Ghi nhận vào ChromaDB")]
    DB_Verified -.->|Cập nhật dữ liệu bộ nhớ| VectorDB
    Decision -->|Bác bỏ| Exit3(["Dừng xử lý"])

    %% Báo cáo & Dashboard
    M5 -->|Xuất báo cáo & Đẩy thống kê| M6["Mô-đun 6: Báo cáo & Cảnh báo"]

    %% Phát hiện botnet chạy song song
    DB_Posts -.->|Đọc lịch sử co-link| MR["Mô-đun R: Phát hiện phối hợp"]
    MR -->|Vẽ đồ thị mạng lưới tài khoản| M6
```

---

## 3. Bản đồ vai trò của 7 Mô-đun (Dành cho Intern)

*   **M1 (Thu thập):** Đóng vai trò làm "người đi chợ", lấy dữ liệu từ các kênh mạng xã hội, làm sạch định dạng thô và lưu vào bảng `posts`.
*   **M2 (Sàng lọc):** Làm "người phân loại sơ bộ", dùng các bộ lọc Regex và model PhoBERT chạy CPU cục bộ cực nhanh để vứt bỏ các bài viết rác (quảng cáo, chào hỏi, tin thường).
*   **M3 (Bộ nhớ cache):** Làm "người ghi nhớ", xem câu này ai nói chưa. Nếu là tin giả cũ được copy-paste lại thì dùng luôn kết luận cũ, tránh tốn tiền gọi Gemini.
*   **M4 (Kiểm chứng):** Làm "thám tử điều tra", khi gặp tin hoàn toàn mới thì bóc tách từng ý, lên Google tìm thông tin từ cổng chính phủ, tải trang báo về đối chiếu từ chữ một để đưa ra phán quyết chuẩn xác.
*   **M5 (Cán bộ duyệt):** Làm "quan tòa", máy chỉ dọn sẵn hồ sơ bằng chứng, cán bộ đọc và bấm nút kết án. Quyết định của cán bộ sẽ được nạp ngược lại kho M3 để cỗ máy thông minh hơn.
*   **M6 (Báo cáo):** Trực quan hóa số liệu lên Dashboard.
*   **MR (Phát hiện phối hợp):** Chạy ngầm gom các bài viết đăng cùng link trong thời gian ngắn để chỉ điểm mạng lưới botnet.
