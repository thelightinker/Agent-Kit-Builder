---
name: tiering-complexity
description: "Use when analyzing agent requirements to classify the system into a complexity tier (Micro, Multi-state, or System) and determine the necessary components."
when_to_use: "Kích hoạt khi cần năng lực tiering-complexity trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Tiering Complexity

## Overview
Phân loại yêu cầu của Agent Kit thành 3 mức độ phức tạp (Tier) để quyết định cấu trúc và số lượng components cần sinh, tránh over-engineering.

## When to Use
- Khi bắt đầu phân tích yêu cầu từ user (New Build hoặc Refactor).
- Khi cần quyết định xem agent chỉ cần 1 System Prompt duy nhất hay cần cả bộ nhớ, skills, workflow.

### When NOT to use
- Khi hệ thống đã được phân loại Tier từ trước và không có thay đổi về scope.

## Core Pattern
Phân cấp thiết kế dựa trên các tiêu chí sau:

### Tier 1 — Micro-agent
- **Đặc trưng**: 1 tác vụ đơn lẻ, không lưu trạng thái (stateless), input đơn giản.
- **Component**: Chỉ cần 1 file `Agent` (system prompt < 300 từ).
- **Ví dụ**: Bot tóm tắt email, Bot chuyển đổi nhiệt độ.

### Tier 2 — Multi-state Agent
- **Đặc trưng**: Nhiều chế độ hoạt động, cần lưu giữ context động hoặc style profile.
- **Component**: `Agent` + `Memory` (file-based).
- **Ví dụ**: Bot viết sách (cần giữ giọng văn tác giả), Bot hỗ trợ khách hàng cá nhân.

### Tier 3 — Agent System (SUITE_BUILD)
- **Đặc trưng**: Phối hợp nhiều vai trò, workflow phức tạp, cần gọi API/MCP tools.
- **Component**: `Agent` + `Workflow` + `Skills` + `Memory` + `Tools`.
- **Ví dụ**: Hệ thống xuất bản tự động, Pipeline phân tích dữ liệu và báo cáo.

## Quick Reference
- **YAGNI (You Aren't Gonna Need It)**: Nếu Tier 1 đủ giải quyết, tuyệt đối không lên Tier 2 hay Tier 3.
- Càng nhiều component, độ trễ và chi phí token càng tăng.

## Common Mistakes
- **Lỗi**: Thiết kế workflow và cấu trúc thư mục phức tạp cho một tác vụ dịch thuật đơn giản (Tier 1).
  - *Khắc phục*: Gộp tất cả vào 1 prompt tinh gọn.
- **Lỗi**: Thiết kế 1 prompt khổng lồ cho hệ thống pipeline gồm 3 bước phức tạp.
  - *Khắc phục*: Tách thành Tier 3 với Workflow rõ ràng.
