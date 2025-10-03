# Quy Tắc Vận Hành Bắt Buộc cho AI Agent

Tài liệu này quy định các quy tắc, tiêu chuẩn và quy trình làm việc bắt buộc mà AI Agent phải tuân thủ trong suốt vòng đời phát triển dự án.

## 1. Nguyên Tắc Cốt Lõi

Đây là những nguyên tắc nền tảng, áp dụng cho mọi khía cạnh của dự án.

- **Ưu tiên Kiến trúc Module (Modular-First)**: Mọi logic phải được chia thành các module/component nhỏ, có trách nhiệm duy nhất và khả năng tái sử dụng cao.
- **Phát triển Hướng Kiểm thử (Test-Driven)**: Luôn viết và xác thực các bài kiểm thử (test) **trước khi** triển khai mã nguồn cho một tính năng mới.
- **Phát triển Tịnh tiến (Incremental Generation)**: Agent phải hoạt động theo từng bước, mỗi lần chỉ tạo ra một module hoặc hoàn thành một tác vụ duy nhất.
- **Quản lý Dependencies Ổn định**: Chỉ sử dụng các dependencies (thư viện, gói) đã được xác minh, có phiên bản ổn định và chính thức.
- **Nhận thức Ngữ cảnh (Context-Aware)**: Agent phải ghi nhớ các quyết định và mã nguồn đã tạo trước đó để đảm bảo tính nhất quán, tránh trùng lặp hoặc xung đột.
- **Tài liệu Hóa Toàn diện**: Mỗi module được tạo ra phải đi kèm tài liệu mô tả rõ ràng:
    - Mục đích (Purpose)
    - Đầu vào & Đầu ra (Inputs/Outputs)
    - Dependencies và phiên bản
    - Kết quả kiểm thử (Test Results)
- **Bảo mật & Hiệu năng là Mặc định**: Các yếu tố về bảo mật và hiệu năng phải được tích hợp ngay từ giai đoạn thiết kế và phát triển, không phải là một bước xử lý sau cùng.

---

## 2. Tiêu Chuẩn Viết Mã Nguồn & Cấu Trúc Dự Án

Để đảm bảo code luôn chính xác, dễ đọc, và dễ bảo trì, AI Agent phải tuân thủ các tiêu chuẩn sau:

### 2.1. Chất Lượng và Độ Chính Xác Của Mã Nguồn

- **Nguyên tắc Đơn trách nhiệm (Single Responsibility Principle - SRP)**: Mỗi hàm (function), lớp (class), hoặc module chỉ nên thực hiện **một** công việc duy nhất. Điều này giúp code không phức tạp và dễ kiểm thử.
- **Tránh Lặp Code (Don't Repeat Yourself - DRY)**: Không sao chép và dán code. Thay vào đó, hãy tạo các hàm hoặc thành phần có thể tái sử dụng.
- **Giữ Mọi Thứ Đơn Giản (Keep It Simple, Stupid - KISS)**: Luôn ưu tiên giải pháp đơn giản và dễ hiểu nhất. Tránh các giải pháp phức tạp hoặc tối ưu hóa sớm khi không cần thiết.
- **Tên gọi Rõ ràng, có ý nghĩa**: Tên biến, hàm, lớp phải mô tả rõ ràng chức năng của chúng. Ví dụ: `getUserData` thay vì `getData`.
- **Xử lý Lỗi Tường minh (Explicit Error Handling)**: Không để lỗi xảy ra một cách âm thầm. Luôn sử dụng `try-catch`, `Promise.catch()` hoặc các cơ chế xử lý lỗi khác để quản lý các trường hợp ngoại lệ một cách rõ ràng.
- **Logging có Chủ đích**: Thêm logging tại các điểm quan trọng (ví dụ: xử lý lỗi, các bước nghiệp vụ chính) để dễ dàng gỡ lỗi và theo dõi hệ thống.

### 2.2. Cấu Trúc File và Module

- **Cấu trúc Thư mục Nhất quán**: Áp dụng một cấu trúc thư mục logic và nhất quán trong toàn bộ dự án (ví dụ: chia theo tính năng `features` hoặc theo loại `components`, `services`, `hooks`).
- **Điểm Truy cập Module (Module Entry Points)**: Mỗi thư mục/module nên có một file `index.js` (hoặc `index.ts`) làm điểm truy cập duy nhất. File này sẽ `export` ra những thành phần mà các module khác được phép truy cập, tạo ra một "public API" rõ ràng cho module đó.
- **Quy tắc Import/Export**:
    - Ưu tiên sử dụng `named export` thay vì `export default` để tăng tính tường minh và tránh xung đột tên.
    - Sử dụng alias path (ví dụ: `@/components/Button`) để tránh các đường dẫn tương đối phức tạp (`../../../components/Button`).
    - **Nghiêm cấm** tạo ra các phụ thuộc vòng (circular dependencies) giữa các module.
- **Tách biệt Cấu hình (Configuration Separation)**: Không bao giờ hardcode các giá trị cấu hình (API keys, connection strings, port...) trực tiếp trong mã nguồn. Các giá trị này phải được lưu trong các file biến môi trường (`.env`) hoặc file cấu hình riêng biệt (`config.js`).

---

## 3. Tiêu Chuẩn Kỹ Thuật theo Từng Lĩnh Vực

### Frontend
- **Functional Components**: Tất cả các component giao diện người dùng phải được triển khai dưới dạng functional component.
- **Tách biệt Logic Phức tạp**: Sử dụng custom hooks (React) hoặc services (Angular/Vue) để xử lý các logic nghiệp vụ.
- **Hệ thống Styling nhất quán**: Áp dụng nhất quán hệ thống styling đã chọn (ví dụ: Tailwind CSS, CSS Modules).
- **Đảm bảo Type Safety**: Ưu tiên sử dụng TypeScript để đảm bảo an toàn kiểu dữ liệu.

### Backend
- **API Contract Rõ ràng**: Tất cả API phải có schema đầu vào và đầu ra được định nghĩa chặt chẽ.
- **Service Module hóa**: Các service phải được thiết kế theo dạng module, dễ dàng kiểm thử độc lập.
- **Bảo mật Tích hợp**: Luôn thực hiện các biện pháp kiểm tra bảo mật cần thiết (Input Validation, XSS, SQL Injection).

### Database
- **Schema có Phiên bản**: Schema của cơ sở dữ liệu phải được quản lý phiên bản và đồng bộ trên mọi môi trường.
- **Truy vấn Tham số hóa**: Mọi truy vấn cơ sở dữ liệu phải sử dụng tham số hóa (parameterized queries).
- **Xác thực Migration**: Các script migration phải được kiểm tra và xác nhận kỹ lưỡng trước khi thực thi.

## 4. Đảm bảo Chất lượng & Kiểm thử

- **Unit Testing**: Mọi module **phải** có bộ unit test tương ứng để xác minh logic cốt lõi.
- **Integration Testing**: Thực hiện integration test **trước khi** tích hợp các module vào nhánh chính.
- **Tự động hóa qua CI/CD**: Hệ thống CI/CD **phải** tự động chạy toàn bộ các bài test trước khi cho phép merge code.

## 5. Quản lý Phiên bản & Dependencies

- **Khai báo Phiên bản Rõ ràng**: Luôn khai báo và "ghim" (pin) phiên bản cụ thể cho môi trường runtime và tất cả các thư viện.
- **Kiểm tra Tương thích**: **Trước khi** thêm một dependency mới, phải xác minh tính tương thích của nó với hệ thống hiện tại.

## 6. Quy Trình Làm Việc Bắt Buộc

AI Agent phải tuân thủ nghiêm ngặt quy trình 7 bước sau đây. **Không được bỏ qua bất kỳ bước nào.**

1.  **Phân tích Yêu cầu (Requirement Analysis)**: Tiếp nhận và làm rõ yêu cầu.
2.  **Xác thực Tài liệu & Phiên bản (Pre-generation Validation)**: Tra cứu tài liệu chính thức của các công nghệ liên quan.
3.  **Lập kế hoạch Module/Tác vụ (Module/Task Planning)**: Thiết kế cấu trúc và phạm vi của module/tác vụ.
4.  **Tạo Mã nguồn (Code Generation)**: Viết mã nguồn tuân thủ **tất cả** các tiêu chuẩn đã định.
5.  **Kiểm thử Đơn vị (Unit Testing)**: Viết và chạy unit test cho mã nguồn vừa tạo.
6.  **Tài liệu hóa & Cập nhật Ngữ cảnh (Documentation & Context Update)**: Tạo tài liệu cho module và ghi nhớ kết quả.
7.  **Tích hợp và Kiểm thử Tích hợp (Integration & Testing)**: Tích hợp module mới và chạy integration test.

---

### Nguyên Tắc Vận Hành Quy Trình

* **Tuân thủ Tuyệt đối**: Quy trình này là bắt buộc và không được phép bỏ qua bước.
* **Cổng Chất lượng (Quality Gate)**: Mã nguồn chỉ được phép tích hợp khi đã vượt qua tất cả các tiêu chuẩn về chất lượng, kiểm thử và tài liệu.
* **Áp dụng Phổ quát**: Các quy tắc và quy trình này được áp dụng cho mọi ngôn ngữ lập trình, runtime và framework được sử dụng trong dự án.
