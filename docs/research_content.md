PHẦN 1: GIẢI QUYẾT VẤN ĐỀ ẢO GIÁC, THIÊN KIẾN VÀ SỰ ĐỒNG THUẬN DỄ DÃI
1. Vấn đề: Sự xu nịnh và Thiên kiến xác nhận (Sycophancy & Confirmation Bias)
Thực trạng: Các LLM hiện đại được huấn luyện bằng RLHF (Reinforcement Learning from Human Feedback) để trở nên "hữu ích" và "thân thiện". Điều này tạo ra một tác dụng phụ nguy hiểm: Mô hình có xu hướng đồng ý với quan điểm của người dùng (Sycophancy) hoặc né tránh xung đột thay vì nói lên sự thật mất lòng.
Giải pháp của FailSafe: Kiến trúc Tranh biện Đa tác nhân (Multi-Agent Debate).
Tại sao chọn kiến trúc này (Thay vì 1 mô hình "khủng")?
Một mô hình đơn lẻ (Single Agent), dù thông minh đến đâu, cũng chỉ có một "luồng tư duy" (single stream of thought). Nó dễ bị rơi vào bẫy Mode Collapse (sụp đổ điểm hội tụ) - tức là nhanh chóng kết luận mà không xét đến các góc nhìn ngoại lai.
Cơ sở nghiên cứu & Biện luận lựa chọn:
 “Improving Factuality and Reasoning in Language Models through Multiagent Debate” (Du et al., 2023)và các nghiên cứu tiếp nối như “More Agents Is All You Need” (2024).
Luận điểm: Các nghiên cứu này chứng minh rằng độ chính xác của sự thật không tăng tuyến tính theo kích thước mô hình, mà tăng theo độ đa dạng của các góc nhìn (Cognitive Diversity).
Áp dụng: FailSafe thiết kế 3 nhân cách xung khắc (Logician vs. Skeptic vs. Researcher). Việc ép buộc xung đột quan điểm (Forced conflict) giúp phá vỡ sự "đồng thuận dễ dãi" của mô hình ngôn ngữ.
Bổ sung mới đây: Nghiên cứu: "H-Neurons: On the Existence, Impact, and Origin of Hallucination-Associated Neurons in LLMs" (Gao et al., Tsinghua University, 12/2025).
Phát hiện: Các nhà nghiên cứu đã tìm ra "H-Neurons" - một nhóm neuron chiếm chưa tới 0.1% nhưng chịu trách nhiệm chính cho việc sinh ra ảo giác. Quan trọng hơn, chúng hình thành ngay từ giai đoạn Tiền huấn luyện (Pre-training).
Áp dụng: Đây là bằng chứng thép cho việc cần thiết phải có Agent Skeptic (Kẻ hoài nghi) trong hệ thống FailSafe. Vai trò của Skeptic chính là cơ chế "ức chế" (suppress) hoạt động của các H-Neurons, buộc mô hình phải thoát khỏi trạng thái "dễ dãi" để quay về thực tế.
		
“Sycophancy in Large Language Models” (Wei et al., Google DeepMind, 2024).
Luận điểm: Bài báo chỉ ra rằng cách duy nhất để loại bỏ sự xu nịnh là tách rời vai trò "người đánh giá" khỏi "người trả lời".
Áp dụng: Đây là lý do FailSafe tách riêng module ClaimVerify (đánh giá) khỏi module Reporting (trả lời người dùng).
2. Vấn đề: Ảo giác "Tuyết lăn" (Snowball Hallucination)
Thực trạng: Khi LLM mắc một lỗi nhỏ ở đầu câu, nó có xu hướng bịa đặt thêm các chi tiết tiếp theo để hợp lý hóa lỗi sai đó (Self-consistency hallucination).
Giải pháp của FailSafe: Quy trình Chuỗi xác thực (Chain-of-Verification - CoVe) có sửa đổi.
Tại sao chọn CoVe (Thay vì Chain-of-Thought - CoT)?
CoT ("Hãy suy nghĩ từng bước") vẫn diễn ra trong một lần chạy (single pass). Nếu bước 1 sai, bước 2 sẽ sai theo. CoVe chia cắt quá trình thành các bước độc lập, ngăn chặn sự lây lan của lỗi.
Cơ sở nghiên cứu & Biện luận lựa chọn:
“Chain-of-Verification Reduces Hallucination in Large Language Models” (Dhuliawala et al., Meta AI, 2023) - Đây là bài báo nền tảng (Seminal paper).
Luận điểm: Việc tách bước "Lập kế hoạch kiểm tra" và bước "Thực thi kiểm tra" giúp giảm ảo giác vì mô hình không bị áp lực phải giữ thể diện cho câu trả lời ban đầu.
“Self-Refine: Iterative Refinement with Self-Feedback” (Madaan et al., 2024).
Luận điểm: Khả năng tự sửa lỗi (Self-correction) của LLM tăng mạnh khi được cung cấp ngữ cảnh bên ngoài.
Áp dụng: Trong FailSafe, Lớp 1 (Decomposition) sử dụng CoVe không phải để trả lời, mà để trích xuất. Tại sao? Vì nếu trích xuất sai (bịa ra một câu Elon Musk không nói), cả hệ thống sẽ sụp đổ. CoVe ở đây đóng vai trò là "Van an toàn" (Safety Valve) đầu tiên.
3. Vấn đề: Suy luận Logic kém trong các mô hình tổng quát
Thực trạng: Các mô hình LLM rất giỏi ngôn ngữ nhưng kém về Logic hình thức (Formal Logic) và nhận thức thời gian (Temporal reasoning). Ví dụ: Chúng không nhận ra sự vô lý khi nói "Vua Quang Trung gọi điện thoại".
Giải pháp của FailSafe: Kỹ thuật Persona Prompting chuyên biệt hóa (Role-based Reasoning).
Tại sao dùng Persona (Logician/Skeptic)?
Thay vì dùng một mô hình to để làm tất cả (Generalist), hệ thống FailSafe sử dụng các "Chuyên gia ảo" (Specialists). Việc gán vai trò (Role) hoạt động như một cơ chế Attention Masking (Che phủ sự chú ý) - hướng sự tập trung của mô hình vào một khía cạnh duy nhất (Logic hoặc Bằng chứng), bỏ qua các yếu tố nhiễu khác.
Cơ sở nghiên cứu & Biện luận lựa chọn:
“Unleashing Cognitive Synergy in Large Language Models” (2024).
Luận điểm: Việc thiết lập các "Persona" chuyên biệt giúp kích hoạt các vùng tiềm năng khác nhau trong không gian tham số của mô hình (Latent Space).
Áp dụng: Agent "The Logician" được thiết kế dựa trên nghiên cứu về Logical Fallacy Detection (Phát hiện ngụy biện), tập trung vào cấu trúc câu thay vì nội dung. Agent "The Skeptic" được thiết kế dựa trên nguyên lý Parsimony (Tiết kiệm giả thuyết - Dao cạo Occam), giúp hệ thống không bị sa đà vào các thuyết âm mưu phức tạp.
PHẦN 2: TỐI ƯU HÓA HỆ THỐNG BẰNG CÁC MÔ HÌNH CHUYÊN BIỆT CỤC BỘ
Mục tiêu: Giải quyết bài toán về Hiệu năng (Performance) và Chi phí (Cost). Việc gọi LLM cho mọi tác vụ nhỏ (như tìm câu trùng lặp, giải quyết đại từ) là cực kỳ lãng phí và chậm chạp. Do đó, FailSafe tích hợp các mô hình Deep Learning nhỏ gọn, chuyên biệt (Specialized Local Models) chạy trực tiếp trên máy chủ Worker.
1. Vấn đề: Sự mơ hồ về Ngữ cảnh do Đồng tham chiếu (Contextual Ambiguity from Coreferences)
Thực trạng: Các LLM hiện đại, mặc dù mạnh, vẫn có thể hiểu sai ngữ cảnh khi một văn bản dài sử dụng nhiều đại từ ("ông ấy", "nó", "công ty này"). Nếu tách các câu chứa đại từ này ra độc lập, chúng sẽ mất hoàn toàn ý nghĩa, dẫn đến việc kiểm chứng sai.
Giải pháp của FailSafe: Tiền xử lý bằng mô hình chuyên biệt.
Mô hình lựa chọn: FastCoref.
Tại sao chọn mô hình này?
Cơ sở đánh giá: Bộ dữ liệu chuẩn OntoNotes 5.0 là thước đo vàng cho bài toán Coreference Resolution.
Biện luận lựa chọn: Đến năm 2025, có thể có các mô hình lớn hơn với F1-score cao hơn, nhưng chúng thường quá nặng (vài GB) và chậm. FastCoref (dựa trên kiến trúc DistilRoBERTa) đạt F1-score 81.5%, đây là điểm "ngọt" (sweet spot) giữa độ chính xác và hiệu năng. Việc xử lý một văn bản vài trăm từ chỉ mất vài mili giây. Việc gọi một LLM lớn để làm tác vụ này có thể mất vài giây và tốn chi phí không cần thiết.
Cơ sở khoa học: Dựa trên nguyên lý Phân rã bài toán (Task Decomposition).
Luận điểm: Một hệ thống AI hiệu quả không nên dùng một "con dao Thụy Sĩ" (LLM) cho mọi việc. Thay vào đó, hãy dùng "con dao mổ" chuyên dụng (FastCoref) cho các tác vụ đã được định nghĩa rõ ràng.
2. Vấn đề: Hiệu năng của Tìm kiếm Ngữ nghĩa và Khử trùng lặp
Thực trạng: Hệ thống cần thực hiện hàng nghìn phép so sánh ngữ nghĩa mỗi giây trong các tác vụ:
Khử trùng lặp (Lớp 1): So sánh chéo các tuyên bố vừa được tách ra.
Kiểm tra Cache (Lớp 2): So sánh tuyên bố mới với toàn bộ kho kiến thức đã lưu.
Giải pháp của FailSafe: Sử dụng các mô hình Embedding hiệu năng cao.
Mô hình lựa chọn: all-MiniLM-L6-v2 và intfloat/e5-base-v2.
Tại sao không dùng các model mới nhất/mạnh nhất (ví dụ: 
Cơ sở đánh giá: Bảng xếp hạng MTEB (Massive Text Embedding Benchmark) được cập nhật liên tục.
Biện luận lựa chọn:
Tốc độ là Vua: Các mô hình như all-MiniLM-L6-v2 được tối ưu cho tốc độ suy luận hàng loạt (batch inference), đạt 14,200 câu/giây. Các model lớn hơn dù có điểm MTEB cao hơn một chút (ví dụ: 65 so với 58) nhưng tốc độ có thể chậm hơn 10-100 lần. Đối với một hệ thống tương tác, độ trễ vài giây chỉ để khử trùng lặp là không thể chấp nhận.
Chi phí Lưu trữ & Tính toán: MiniLM tạo ra vector 384 chiều. Các model mới hơn thường tạo vector 1024 hoặc 4096 chiều. Việc lưu trữ và tính toán khoảng cách Cosine trên vector lớn hơn sẽ tốn kém hơn theo cấp số nhân (về cả RAM và thời gian CPU).
"Đủ tốt" (Good Enough): Với tác vụ khử trùng lặp và tìm kiếm cache, độ chính xác của MiniLM và e5-base đã vượt ngưỡng "đủ tốt". Việc tăng độ chính xác thêm 5% nhưng phải trả giá bằng việc chậm đi 10 lần là một sự đánh đổi không hiệu quả về mặt kỹ thuật.
Cơ sở khoa học: Nguyên lý Cân bằng Hiệu năng-Chi phí (Performance-Cost Trade-off).
Luận điểm: Dựa trên "Efficiently Scaling Transformer Based Models" (Google Research, 2024), việc chọn kiến trúc mô hình phù hợp với tài nguyên phần cứng và yêu cầu độ trễ của ứng dụng là yếu tố sống còn. MiniLM là một ví dụ điển hình của việc chưng cất tri thức (Knowledge Distillation) để tạo ra các mô hình nhỏ nhưng mạnh mẽ.
3. Vấn đề: Cần một đơn vị đo lường sự thật khách quan
Thực trạng: Làm sao để biết một tuyên bố đã được phân rã đủ nhỏ và có thể kiểm chứng được?
Giải pháp của FailSafe: Áp dụng khái niệm "Sự thật Nguyên tử" (Atomic Facts).
Cơ sở khoa học: "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation" (Min et al., 2023).
Tại sao khái niệm này vẫn quan trọng vào năm 2025?
Luận điểm: Bài báo này đã thiết lập một tiêu chuẩn công nghiệp. Dù các LLM ngày nay có thể xử lý các câu phức tốt hơn, nhưng nguyên tắc cơ bản về tính đúng/sai vẫn không thay đổi: Một đơn vị thông tin chỉ có thể là Đúng hoặc Sai, không thể vừa đúng vừa sai.
Áp dụng: FailSafe sử dụng khái niệm này làm "hợp đồng" (contract) giữa các lớp. Lớp 1 có nhiệm vụ phải tạo ra các Atomic Facts. Lớp 4 chỉ nhận đầu vào là các Atomic Facts. Điều này giúp hệ thống trở nên module hóa, dễ kiểm thử và đáng tin cậy.
4. Vấn đề: Lọc nhiễu trong kết quả tìm kiếm
Thực trạng: Google trả về 10 kết quả, nhưng có thể chỉ 1-2 kết quả thực sự chứa câu trả lời. Làm sao để chọn ra đoạn văn bản tốt nhất?
Giải pháp của FailSafe: Kiến trúc Reranking hai bước.
Cơ sở khoa học: Dựa trên các kiến trúc tìm kiếm thông tin tiêu chuẩn (Information Retrieval Architectures) đã được kiểm chứng qua thời gian.
Biện luận lựa chọn kiến trúc:
Bước 1 - Bi-Encoder (MiniLM/e5): Tìm kiếm nhanh (Fast Retrieval). Quăng một lưới rộng để tìm ra 10-20 ứng viên tiềm năng.
Bước 2 - Cross-Encoder: Xếp hạng lại chính xác (Precise Reranking). Dùng một mô hình chậm hơn nhưng thông minh hơn để "đọc kỹ" từng ứng viên và chấm điểm.
Tại sao không dùng Cross-Encoder ngay từ đầu? Vì nó quá chậm. Nó phải so sánh câu hỏi với toàn bộ kho dữ liệu. Kiến trúc 2 bước này là tiêu chuẩn công nghiệp để cân bằng giữa Tốc độ (Recall) và Độ chính xác (Precision). Chỉ số MRR@10 0.39 trên MS MARCO cho thấy Cross-Encoder vẫn là lựa chọn hàng đầu cho tác vụ Reranking chuyên sâu, ngay cả khi các mô hình LLM tổng quát đã phát triển.
PHẦN 3: CƠ CHẾ PHÒNG THỦ CHIỀU SÂU BẰNG THỐNG KÊ (STYLOMETRY)
Trong một thế giới mà AI tạo sinh có thể viết văn bản mượt mà như người thật, làm sao để phân biệt được tin giả hoặc văn bản do máy tạo ra một cách nhanh chóng và rẻ tiền nhất?
1. Vấn đề: Chi phí của việc kiểm chứng mọi thứ
Thực trạng: Nếu hệ thống cứ nhận được bất kỳ văn bản nào cũng đem đi hỏi Google và LLM (Deep Verification), chi phí vận hành sẽ cực lớn. Có những văn bản rõ ràng là rác (spam) hoặc tin giật gân (clickbait) cần phải bị loại bỏ ngay từ đầu.
Giải pháp của FailSafe: Chiến lược "Dừng sớm" (Early Exit) bằng Phân tích Văn phong.
Tại sao dùng các thuật toán "cổ lỗ sĩ" (Classic ML) thay vì AI hiện đại?
Luận điểm: Các thuật toán thống kê (Statistical Methods) có chi phí tính toán gần như bằng 0 (Zero-cost). Chúng chạy trong vài mili giây.
Hiệu quả: Chúng hoạt động như một bộ lọc thô (Coarse Filter). Nếu một văn bản không vượt qua được bộ lọc này, nó không xứng đáng tiêu tốn tài nguyên của các lớp sau.
2. Các chỉ số đo lường cụ thể và Cơ sở khoa học
A. Shannon Entropy (Lý thuyết Thông tin)
Cơ sở khoa học: Lý thuyết thông tin (Information Theory) ra đời từ thế kỷ 20, nhưng vẫn là nền tảng của mọi hệ thống nén và mã hóa dữ liệu ngày nay.
Tại sao chọn nó cho hệ thống FailSafe?
Phát hiện sự lặp lại (Repetitiveness): Tin rác, tin spam, hoặc văn bản lỗi của bot thường có xu hướng lặp lại từ ngữ một cách bất thường. Điều này làm giảm độ hỗn loạn (Entropy) của văn bản.
Tính khách quan: Entropy là một con số toán học thuần túy, không bị ảnh hưởng bởi ngữ nghĩa hay thiên kiến chính trị. Nó là một thước đo trung lập và đáng tin cậy để phát hiện sự bất thường trong cấu trúc văn bản.
B. TF-IDF trên nền tảng dữ liệu chuẩn (Benchmarking)
Cơ sở khoa học: Dựa trên các nghiên cứu về phát hiện bất thường trong văn bản (Text Anomaly Detection).
Tại sao dùng tập dữ liệu 
Lý do hệ thống: Để biết một văn bản có "bất thường" hay không, hệ thống cần một "thước đo chuẩn" (Baseline). ag_news với hơn 120.000 bài báo chính thống đóng vai trò như một chuẩn mực về văn phong báo chí.
Ứng dụng: Khi hệ thống so sánh văn bản đầu vào với chuẩn mực này, nếu phát hiện sự chênh lệch lớn về tần suất từ khóa (ví dụ: từ "mua ngay" xuất hiện quá nhiều so với mức trung bình của ag_news), đó là dấu hiệu của việc nhồi nhét từ khóa (Keyword Stuffing) - một đặc trưng của tin rác SEO hoặc lừa đảo.
PHẦN 4: BIỂU DIỄN TRI THỨC VÀ SUY LUẬN LOGIC (KNOWLEDGE REPRESENTATION)
Để máy tính không chỉ "đọc" mà còn "hiểu" và "suy luận" được như con người, chúng ta cần chuyển đổi văn bản sang một định dạng có cấu trúc chặt chẽ hơn.
1. Vấn đề: Giới hạn của văn bản tuyến tính (Linear Text)
Thực trạng: Văn bản thông thường là một chuỗi tuyến tính các từ. Máy tính rất khó nhận ra mối quan hệ logic phức tạp (như "A gây ra B", "C phủ định A") nếu chỉ đọc lần lượt từ trái sang phải. Các mô hình LLM đôi khi bị "lạc trôi" trong các văn bản dài và quên mất các mối liên kết logic.
Giải pháp của FailSafe: Mô hình hóa dữ liệu dưới dạng Đồ thị Lập luận Cấu trúc (SAG).
Cơ sở khoa học: Lĩnh vực Argumentation Mining (Khai phá lập luận) và Knowledge Graphs (Đồ thị tri thức).
Tại sao chọn chuẩn JSON-LD?
Tiêu chuẩn công nghiệp: JSON-LD là chuẩn của W3C cho Dữ liệu liên kết (Linked Data). Nó được hỗ trợ rộng rãi bởi Google, Bing và các công cụ tìm kiếm lớn.
Tính tương thích: Sử dụng chuẩn này giúp dữ liệu của FailSafe dễ dàng tích hợp với các hệ thống tri thức khác trong tương lai, hoặc hiển thị trực quan lên giao diện người dùng.
Tại sao chọn cấu trúc Đồ thị (Graph)?
Lý do hệ thống: Đồ thị cho phép biểu diễn rõ ràng các mối quan hệ: Hỗ trợ (Support), Tấn công (Attack), Giải thích (Explain). Nhờ đó, module "Hội đồng thẩm định" (Lớp 4) có thể dễ dàng truy vết logic: Nếu luận điểm A bị bác bỏ, thì luận điểm B (dựa trên A) cũng sẽ sụp đổ theo. Đây là khả năng suy luận nhân quả mà các phương pháp xử lý văn bản thông thường không làm được.
2. Vấn đề: Đo lường sự tương đồng về ý nghĩa
Thực trạng: Trong Lớp 2 (Bộ nhớ đệm) và Lớp 3 (Tìm kiếm), hệ thống cần biết hai câu văn viết khác nhau có cùng nghĩa hay không.
Giải pháp của FailSafe: Sử dụng độ đo Cosine Similarity.
Cơ sở toán học: Đại số tuyến tính trong không gian Vector nhiều chiều.
Tại sao chọn Cosine Similarity (thay vì Euclidean Distance)?
Đặc tính quan trọng: Cosine Similarity đo góc giữa hai vector, không phụ thuộc vào độ dài (magnitude) của vector. Điều này cực kỳ quan trọng trong xử lý ngôn ngữ, vì một câu ngắn ("Trái đất tròn") và một câu dài ("Hành tinh của chúng ta có hình cầu") có thể có cùng ý nghĩa (cùng hướng vector) dù độ dài văn bản khác nhau.
Hiệu quả: Đây là tiêu chuẩn vàng (Gold Standard) cho các tác vụ tìm kiếm ngữ nghĩa, đảm bảo độ chính xác cao khi truy hồi kiến thức từ bộ nhớ.


L0
1. Mục tiêu cốt lõi
Nhiệm vụ: "Dừng sớm" (Early Exit).
Hệ thống sẽ từ chối xử lý nếu văn bản đầu vào thỏa mãn điều kiện logic AND:
Nguồn tin kém uy tín (Trust Level = LOW).
Phong cách viết giật gân/kém chất lượng (Sensationalism Score > 0.5).
2. Phân rã Kỹ thuật
Lớp này gồm 3 module con chạy song song và tuần tự:
Module A: Phân tích Metadata (Nguồn tin)
File code: factcheck/core/Screening.py (Class MetadataAnalyzer).
Input: URL hoặc Văn bản.
Quy trình:
Trích xuất Domain: Dùng regex/urllib để lấy domain (ví dụ: cnn.com từ https://cnn.com/article.).
Danh sách đen/trắng (Allow/Blocklist) : Kiểm tra nhanh danh sách cứng. Nếu là trang chính phủ/giáo dục -> High Trust Allow hoặc các trang chắc chắn lừa đảo đã biết thì Block List..
Tra cứu nhanh (O(1)): Kiểm tra trong SQLite (data/sources.db). Đây là database chứa dữ liệu từ Media Bias/Fact Check (MBFC).
                        Query: SELECT credibility, bias FROM sources WHERE domain = ?
Dự phòng (Fallback): Nếu không tìm thấy trong DB (gặp domain lạ), hệ thống gọi Gemini Flash (model rẻ, nhanh) để đánh giá "nóng" (On-the-fly evaluation).
Output: Nhãn độ tin cậy (High, Mixed, Low).
Module B: Bộ cố vấn (The Advisor - Memory)
File code: factcheck/core/Screening.py (Class ScreeningAdvisor).
Quy trình:
Input: Người dùng gửi một bài viết giả.
Vector Embedding: Hệ thống gọi model e5-base-v2 để biến câu trên thành vectơ V.new (gồm 768 số).
Query (Truy vấn Ký ức) Hệ thống mang vectơ V.new này đi so sánh với hàng nghìn vectơ V.old đang được lưu trong ChromaDB (nơi chứa các bài viết đã từng bị đánh dấu là tin giả trước đây).
Tính toán khoảng cách (Cosine Similarity). Hệ thống dùng công thức Cosine để đo góc giữa 2 vectơ:
similarity=cos(θ)= (V.new x V.old) / (||V.new|| ||V.old||)
Kết quả chạy từ -1 đến 1 lấy ngưỡng mặc định là distance < 0.5 .
Nếu Similarity > 0.85 (distance  < 0.15), nghĩa là bài viết mới này cực kỳ giống một bài tin giả đã biết trong quá khứ.
Ra quyết định: Advisor hét lên: "Đừng tốn công kiểm tra nữa! Bài này nội dung y hệt bài lừa đảo tuần trước, chỉ đổi tiêu đề thôi!".
-> Hệ thống Skip luôn, trả về kết quả FAKE ngay lập tức.
Module C: Phân tích Văn phong (Stylometry Analysis) 
File code: factcheck/core/Screening.py (Class StylometryAnalyzer).
Mục đích: Phát hiện "mùi" tin giả thông qua thống kê từ ngữ mà không cần hiểu nghĩa sâu.
Đây là phần phức tạp nhất, được mô tả trong sơ đồ "Bộ máy thống kê (Statistical Engine)". Điểm số giật gân (Score) được tính bằng tổng có trọng số (Weighted Sum) của 4 đặc trưng.
Công thức tổng quát:
Score=1.5⋅R.cap+3.0⋅S.words+1.0⋅Z.Entropy+0.35⋅S.TFIDF
Chúng ta hãy đi sâu vào từng biến số:
Tỷ lệ in hoa (R.cap - Uppercase Ratio)
Ý nghĩa: Tin giả hoặc tin câu view thường hay "HÉT VÀO MẶT" người đọc bằng cách viết hoa toàn bộ (CAPSLOCK).
R.cap=Số ký tự in hoa / Tổng số ký tự chữ cái
Trọng số (1.5): Mức độ quan trọng trung bình.
Từ ngữ giật gân (S.words - Sensationalism)
Ý nghĩa: Đếm tần suất các từ kích động cảm xúc (ví dụ: shocking, exposed, secret, miracle, hoax...).
S.words=Tổng giật gân tìm thấy / Tổng số từ trong văn bản
Trọng số (3.0): Cao nhất. Đây là dấu hiệu rõ ràng nhất của Clickbait/Fake News. Chỉ cần vài từ này xuất hiện, điểm số sẽ tăng vọt.
Độ hỗn loạn thông tin (Z.entrophy - Shannon Entropy)
Đây là phần tinh vi nhất, dựa trên Lý thuyết thông tin (Information Theory).
Khái niệm: Entropy đo lường lượng tin tức trung bình hoặc độ "ngẫu nhiên" của văn bản.
Văn bản Spam (copy-paste lặp lại): Entropy rất thấp.
Văn bản Bot dởm (sinh từ ngẫu nhiên): Entropy rất cao hoặc bất thường.
Văn bản Tin tức chuẩn: Có mức Entropy ổn định (khoảng 4.5 - 6.0 bit/từ).
Công thức Shannon Entropy:

 (Trong đó  p(xi) là tần suất xuất hiện của từ (xi)).
Chuẩn hóa Z-Score: Hệ thống không dùng Entropy thô. Nó so sánh Entropy của văn bản hiện tại (H) với mức trung bình của tập dữ liệu tin tức chuẩn (ag_news - μ (120.000 bài báo)):
Z=H−μ / σ    
 (Nếu Z quá lệch so với 0, tức là văn bản này rất "dị").
Code thực tế: Trong file build_stylometry_corpus.py, hệ thống đã tính trước μ(mean) và σ(std) của tập ag_news để làm chuẩn so sánh.
Nhồi nhét từ khó (S.TFIDFS - Keyword Stuffing)
Ý nghĩa: Tin rác SEO thường lặp lại một vài từ khóa vô nghĩa để lên top tìm kiếm.
Kỹ thuật: Sử dụng mô hình TF-IDF (Term Frequency - Inverse Document Frequency).
Nếu một từ xuất hiện quá nhiều trong bài này (TF cao) nhưng hiếm gặp ở chỗ khác (IDF cao) -> Điểm TF-IDF vọt lên.
Hệ thống lấy trung bình cộng điểm TF-IDF của 5 từ khóa cao nhất trong bài.
Công thức:
TF-IDF=TF×IDF
Trọng số (0.35): Thấp nhất, dùng để bổ trợ.

Sau khi có các chỉ số, hệ thống đi qua một cổng logic AND:
Nếu nguồn tin là Unknown hoặc Low Trust và Sensationalism Score > 0.5 :
KÍCH HOẠT EARLY EXIT.
Trả về ngay: "Hệ thống từ chối xử lý vì phát hiện nội dung Spam/Giật gân từ nguồn không uy tín."
Nếu nguồn tin là High Trust:
Vẫn cho đi tiếp vào Lớp 1, nhưng gắn cờ cảnh báo.
Tiêu chí:
Chi phí bằng 0 (Zero-cost)
Phòng thủ chiều sâu (Defense in Depth)
L1
1. Mục tiêu cốt lõi
Đây là lớp chuyển đổi dữ liệu từ dạng "Văn bản thô" (Unstructured) sang dạng "Tri thức có cấu trúc" (Structured Knowledge) để máy tính có thể hiểu và xử lý logic được.
2. Phân rã Kỹ thuật
Lớp này gồm 3 bước xử lý tuần tự (Pipeline):
Giải quyết đồng tham chiếu (Coreference Resolution)
File code: factcheck/core/Coreference.py (Class ReferenceResolver).
Mô hình: FastCoref (DistilRoBERTa based).
Vấn đề: Văn bản thường dùng đại từ (he, she, it, they, ông ấy, nó...) thay vì lặp lại tên riêng. Nếu tách câu ra mà giữ nguyên "Ông ấy", câu đó trở nên vô nghĩa.
Kỹ thuật:
Mô hình tìm các cụm từ (Clusters) cùng chỉ một thực thể.
Ví dụ: {Elon Musk, CEO Tesla, Ông ấy}.
Thay thế (Replace): Thay tất cả các từ phụ (mentions) bằng từ chính (head mention).
Hiệu năng: Chạy cục bộ trên CPU/GPU, F1-Score ~81.5%.
Xây dựng Đồ thị lập luận (SAG Construction)
File code: factcheck/core/Decompose.py (Class Decompose).
Engine: Sử dụng LLM (Gemini-Flash) để hiểu ngữ nghĩa.
Phương pháp: CoVe Baseline (Chain-of-Verification for Draft ,Plan ,Execute ,Revise ).
Ánh xạ Ψ:D^→G(V,E)
Nhiệm vụ:
Tách văn bản thành các câu đơn (Atomic Claims).
Xác định mối quan hệ giữa các câu (Support/Attack).
Chuẩn đầu ra: JSON-LD (Linked Data).
Đây là định dạng chuẩn để biểu diễn Đồ thị tri thức (Knowledge Graph).
Gồm: Nodes (Câu) và Edges (Quan hệ).
Khử trùng lặp (Deduplication)
File code: factcheck/core/Decompose.py.
Mô hình: Sentence-Transformers (Model: all-MiniLM-L6-v2 với 384 chiều với 14.200 câu/giây).
Embedding Φ:ci→vi ​∈ R384
Vấn đề: LLM có thể tách ra 2 câu giống hệt nhau về ý nghĩa: "Elon Musk mua Twitter" và "Twitter được bán cho Elon Musk". Cần gộp lại để đỡ tốn tiền kiểm chứng 2 lần.
Thuật toán cố lõi (Độ tương đồng cặp):
S(i,j)=cos⁡(θ)=(vi x vj) / (∥vi∥∥vj∥)
vi⋅vj: Tích vô hướng (Dot product).
∥v∥: Độ dài (Norm) của vector.
Quy tắc: Nếu S>0.85 → Gộp (Discard câu ngắn hơn).
Kết quả: Tập hợp cuối (Cfinal) gồm các luận điểm đơn nhất.


L2
1. Mục tiêu cốt lõi
Thay vì lao ngay đi tìm kiếm trên Internet (tốn tiền API, tốn thời gian ~30s), hệ thống kiểm tra xem: "Câu này mình đã từng kiểm chứng chưa?". Nếu có rồi -> Trả kết quả ngay lập tức (độ trễ ~10ms).
2. Phân rã Kỹ thuật
Đánh giá Kiểm chứng (Verifiability Check)
Model: LLM (Gemini-Flash) và Logic phân loại.
Ánh xạ ci→y∈{0,1}
y=1: Có thể kiểm chứng (Fact).
y=0: Ý kiến chủ quan, cảm thán, câu hỏi (Opinion/Spam).
Logic:
Nếu y= 0 (Opinion) -> LOẠI BỎ (DISCARD). Hệ thống không fact-check câu "Cô ấy thật xinh đẹp".
Nếu y=1 (Fact) -> Đi tiếp sang bước 2.
Output: Tập hợp đã lọc C.filtered
Ánh xạ Không gian Vector (Semantic Mapping)
Model: intfloat/e5-base-v2 (768 chiều) để chính xác hơn về ngữ nghĩa.
Toán học (Encoder):
Φ(ci)→q∈R768)
(Biến câu ci thành vector truy vấn q).
Thuật toán Tìm kiếm: k-NN (k-Nearest Neighbors) trong không gian Vector V.cache
Collection: verified_facts (trong ChromaDB)
Quyết định Thuật toán (Algorithmic Decision)
Metric (Độ đo): Cosine Distance (d).
Công thức:
d=1−CosineSimilarity=1−(q⋅vcached / ∥q∥∥v.cached∥)
Ngưỡng (Threshold τ): 0.2
Đây là con số "tử huyệt".
Nếu d≤0.2: Hai câu giống nhau y hệt -> CACHE HIT.
Nếu d>0.2: Hai câu khác nhau -> CACHE MISS.
Luồng xử lý (Workflow)
Nhánh 1: CACHE HIT
Điều kiện: 
d≤0.2
d≤0.2
Hành động: Truy xuất kết quả cũ (Reasoning + Verdict) từ DB.
Độ trễ: ~10ms (Tức thời).
Kết quả: Return Result ngay lập tức, bỏ qua các lớp sau.
Nhánh 2: CACHE MISS
Điều kiện: 
d>0.2
d>0.2
Hành động: Đẩy vào Hàng đợi xử lý lô (Batch Processing Queue).
Logic gom lô: Batch size = 5. Thay vì xử lý từng câu lẻ tẻ, hệ thống gom 5 câu lại để gửi đi tìm kiếm một lần cho tối ưu.
Chuyển tiếp sang Lớp 3 (Tìm kiếm & Đọc sâu).

LƯU Ý về Vòng lặp phản hồi (Feedback Loop)
Sau khi Lớp 5 xử lý xong một câu mới (Cache Miss), kết quả đó sẽ được Nạp kiến thức mới ngược trở lại vào Không gian Vector của Lớp 2.
Lần sau gặp lại câu đó -> Nó sẽ thành Cache Hit.

L3:
1. Mục tiêu cốt lõi
Tìm kiếm các bằng chứng (Evidences) có độ tin cậy cao nhất và sát nghĩa nhất với câu tuyên bố cần kiểm tra.
2.Phân rã Kỹ thuật
Lớp này gồm 5 bước xử lý tuần tự (Pipeline):
Sinh Truy vấn (Query Generation)
Vấn đề: "Vocabulary Mismatch" (Lệch từ vựng). Người dùng viết "Musk thâu tóm Chim xanh", nhưng Google chỉ hiểu "Elon Musk mua Twitter".
Mục tiêu: Maximize Recall (Tăng tối đa khả năng tìm thấy).
Kỹ thuật: Dùng LLM để biến 1 câu tuyên bố (Q) thành danh sách các từ khóa tìm kiếm tối ưu 
{q1,q2,…,qk}
Tìm kiếm Ứng viên (Candidate Retrieval)
Kho dữ liệu: Corpus C (Google Index) / ChromaDB (nạp).
Hành động: Gửi query lên Google (qua Serper API).
Output: Lấy Top-K kết quả đầu tiên (thường là 10).
Tập ứng viên: Dcand={d1,…,d10} (Danh sách các URL thô).
Lọc Nguồn tin (Trust Filtering)
Logic: Không phải cứ lên Google là đúng. Cần lọc bỏ trang web rác.
Hàm tin cậy: 
T(url)∈[0,1]
Hệ thống tra cứu Database MBFC (từ Lớp 0).
Ngưỡng quyết định (Decision Boundary): 
τ=0.5
.Nếu 
T(url)<0.5 (Low Trust) → Skip Deep (Bỏ qua, không đọc sâu, chỉ lấy snippet).
Nếu 
T(url)≥0.5 (High Trust) → Đi tiếp sang Bước 4.
Trích xuất Nội dung Sâu (Deep Scraping)
Thư viện: Trafilatura.
Tại sao cần? Google chỉ trả về một đoạn tóm tắt (Snippet) ngắn tí. Để fact-check kỹ, cần đọc cả bài báo.
Kỹ thuật:
Parsing DOM Tree →Text.
Noise Removal: Loại bỏ quảng cáo, menu điều hướng, footer, popup.
Kết quả: Văn bản sạch (Clean Text) từ các trang uy tín.
Xếp hạng lại bằng Neural (Neural Reranking)
Kiến trúc: Cross-Encoder.
Khác với Bi-Encoder (như e5/MiniLM ở các lớp trước tách rời 2 câu), Cross-Encoder nhét cả Câu hỏi và Đoạn văn vào cùng một mô hình để "đọc" mối quan hệ sâu sắc hơn.
Input: [CLS] + Query + [SEP] + Passage + [SEP] (Cấu trúc chuẩn của BERT).
Hàm tính điểm:
Score(q,p)=σ(W⋅BERT(q,p)+b)
(Trong đó σ là hàm Sigmoid đưa về xác suất 0-1).
Xác suất: 
P(Relevant∣q,p)
Output: Danh sách đã sắp xếp lại (Dsorted). Chọn ra Top-3 đoạn văn có điểm cao nhất làm Bằng chứng cuối cùng (Final Context).






Dưới đây là phân tích chi tiết:

1. Lớp 4: Hội đồng thẩm định (Multi-Agent Debate)
Đây là "bộ não" phản biện của hệ thống. Thay vì tin vào một kết quả duy nhất, FailSafe tạo ra một cuộc tranh luận giữa các tác giả ảo (Agents) có tính cách đối lập nhau:



Nhân sự của Hội đồng:

The Logician (Nhà Logic học): Chuyên tìm kiếm các lỗi ngụy biện, kiểm tra tính nhất quán về mặt thời gian và sự kiện giữa các bằng chứng.

The Skeptic (Người hoài nghi): Đóng vai "luật sư của quỷ", luôn đặt câu hỏi ngược lại, chống lại các thuyết âm mưu và giả khoa học.

The Researcher (Nhà nghiên cứu): Tập trung vào việc đối chiếu với các nguồn tài liệu uy tín đã thu thập được ở Lớp 3 để tìm điểm tương đồng (Consensus).


Cơ chế hoạt động: Các Agent này sẽ tranh luận dựa trên Đồ thị Lập luận (SAG) được tạo ra từ Lớp 1. Nếu một luận điểm A bị bác bỏ, mọi hệ quả dựa trên A cũng sẽ bị loại bỏ theo (truy vết nhân quả).

Mục tiêu: Phá vỡ sự "xu nịnh" (Sycophancy) của AI – tức là thói quen đồng ý vô điều kiện với người dùng.


2. Lớp 5: Tổng hợp & Phán quyết (Executive Synthesis)
Lớp này đóng vai trò như một Tổng biên tập, người có quyền năng cao nhất để đưa ra kết luận cuối cùng dựa trên kết quả của cuộc tranh luận ở Lớp 4.



Tổng hợp điểm số: Hệ thống sử dụng thuật toán để tính toán trọng số từ các ý kiến của Hội đồng thẩm định.

Áp dụng Quy tắc cứng (Hard Rules): * Nếu tỷ lệ bằng chứng phản đối vượt quá một ngưỡng nhất định, tuyên bố sẽ bị dán nhãn là "Sai sự thật" (False).

Nếu bằng chứng không đủ để kết luận, hệ thống sẽ trả về trạng thái "Chưa thể xác minh" (Unverified) thay vì đoán mò.


Xuất báo cáo điều tra (Investigation Report): Không chỉ đưa ra câu trả lời Đúng/Sai, Lớp 5 còn xuất ra một báo cáo chi tiết bao gồm:

Phán quyết: (Đúng, Sai, Gây tranh cãi, hoặc Không đủ dữ liệu).

Trích dẫn (Citations): Liệt kê chính xác nguồn tin nào ủng hộ hoặc phản đối.

Giải thích logic: Tóm tắt tại sao hệ thống lại đưa ra kết luận đó.



