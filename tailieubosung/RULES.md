# AI Agent Rules – Comprehensive Guide for Code Base Standards

## 1. Mục tiêu

Đảm bảo mọi code AI sinh ra:

- Tuân thủ coding standards của dự án.
- Modular, dễ bảo trì, dễ test.
- Sử dụng dependency và version ổn định.
- Tài liệu và context đầy đủ.
- Không làm hỏng code base hiện tại.

---

## 2. Nguyên tắc chung

1. **Dữ liệu chuẩn**
   - Luôn sử dụng docs chính thức, release notes, GitHub releases.
   - Không dùng alpha, beta, deprecated hoặc package không tồn tại.
   - Kiểm tra tương thích giữa các thư viện và runtime.

2. **Modular-first**
   - Tách code thành module nhỏ, reusable.
   - Không viết monolithic code.
   - Complex logic phải tách ra custom module/hook/service.

3. **Test-driven**
   - Viết test trước khi sinh logic mới.
   - Kiểm tra module độc lập trước khi tích hợp.

4. **Incremental**
   - Một task/module mỗi lần.
   - AI phải chờ xác nhận trước khi tạo task tiếp theo.

5. **Version & Dependency**
   - Luôn ghi rõ version của runtime, thư viện.
   - Kiểm tra compatibility trước khi sinh code.
   - Không tự thêm dependency mới nếu không xác nhận.

6. **Documentation**
   - Ghi purpose, inputs/outputs, dependency/version.
   - Test result, integration notes.
   - Mỗi module AI sinh ra phải kèm tài liệu.

7. **Context Recall**
   - AI nhớ lại decisions trước đó (module, types, hooks, services).
   - Tránh duplicate, conflict hoặc inconsistency.

---

## 3. Quy tắc chi tiết theo loại module

### 3.1 Frontend (React / Vue / Angular / Svelte)

- Components: functional, reusable, state management rõ ràng.
- Hooks / Services: logic tách riêng, testable.
- Styling: sử dụng system đã chọn (Tailwind / CSS Modules / Styled Components), version xác định.
- Props & State: luôn type-safe (TS nếu có).

### 3.2 Backend (Python / Node / Java / Go)

- APIs: input/output rõ ràng, type safe nếu có.
- Services: modular, testable.
- Dependency: stable version, check compatibility.
- Security: validate input, escape output, chống injection/XSS.

### 3.3 Database

- Schema: versioned, consistent.
- Query: parameterized, tránh hardcode.
- Migration: chỉ tạo khi đã xác nhận.

### 3.4 Testing

- Unit test: mỗi module phải có.
- Integration test: khi tích hợp nhiều module.
- CI/CD: chạy test trước merge code.

---

## 4. Template file `.aiagentrules.md`

```markdown
# AI Agent Rules for Project

## General Rules
- Use only stable, verified dependencies.
- Modular-first: break logic into small, reusable components/modules.
- Test-driven: write tests before implementing features.
- Incremental: generate one module/task at a time.
- Document: purpose, inputs/outputs, dependency, version, test results.
- Context-aware: recall previous decisions and avoid conflicts.

## Frontend
- Components must be functional (React, Vue, Angular, Svelte).
- Custom hooks/services for complex logic.
- Styling via chosen system (Tailwind / CSS Modules / Styled Components).
- Ensure type safety where possible.

## Backend
- APIs: clearly defined inputs/outputs.
- Services: modular, testable.
- Dependency versions must be stable.
- Security checks (input validation, XSS, SQL injection).

## Database
- Schemas versioned and consistent.
- Queries parameterized, no hardcoded values.
- Migrations confirmed before execution.

## Testing
- Each module must have unit tests.
- Integration tests before merging multiple modules.
- CI/CD must run tests before merge.

## Versioning & Dependency
- Always declare runtime and library versions.
- Confirm compatibility before adding new dependencies.


5. Best Practices
	•	Trước khi sinh module, AI phải check docs chính thức & version.
	•	Mỗi module sinh ra phải có test và tài liệu đi kèm.
	•	Sử dụng context recall để tránh duplicate hoặc conflict.
	•	Tuân thủ modular-first và incremental: mỗi lần sinh 1 task/module.
	•	Security & performance phải được kiểm tra trước khi merge code.

⸻

6. Workflow tích hợp rules

[Requirement] → [Validate docs/version] → [Plan module/task] → [AI generate code] → [Test module] → [Document & context] → [Integration] → [Next module]

•	AI không được skip bước nào.
	•	Luôn đảm bảo code chuẩn trước khi tích hợp.
	•	Áp dụng cho tất cả ngôn ngữ, runtime, framework.

