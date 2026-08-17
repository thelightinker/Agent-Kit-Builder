---
name: building-component-specs
description: "Use when defining specifications for non-prompt components such as Memory files, Workflow state transitions, and Tool integration parameters based on AGENT WORKFLOW MASTER FRAMEWORK."
when_to_use: "Kích hoạt khi cần thiết kế thông số kỹ thuật (specs) cho Memory schema, Workflow states (Node Anatomy 5 phần), hoặc Tool integration contracts."
requires_templates: ["templates/memory-template.md", "templates/workflow-template.md"]
requires_references: ["references/workflow-master-framework.md", "references/component-specs/memory-spec.md"]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.2.0
---

# Building Component Specs

## Overview
Thiết kế thông số kỹ thuật (specifications) cho các thành phần phi văn bản trong bộ Agent Kit như Memory schema, Workflow State Machines (theo chuẩn `AGENT WORKFLOW MASTER FRAMEWORK`), và Tool integration contract.

## When to Use
- Khi Kit Generator hoặc Kit Architect thiết kế các workflows, memory structures, hoặc tool interfaces.
- Khi refactor hoặc tối ưu hóa workflow từ dạng free-text sang dạng State Machine khép kín.

## Core Reference
- **Workflow Master Framework**: Tham khảo tài liệu [references/workflow_master_framework.md](references/workflow_master_framework.md) chứa toàn bộ nguyên tắc Topology Tree, 5-part Node Anatomy, 3-Check DoD, Long-running Sessions, và Guardrails.

---

## Pattern Implementation Guide

### 1. Workflow Spec (Master State Machine Pattern)
Khi xây dựng hoặc sửa đổi bất kỳ workflow `.md` nào:
1. **Frontmatter YAML (Compile-time)**: Khai báo `topology`, `trigger`, `permissions`, `tools_allowed`, và `safe_outputs` (Ràng buộc quyền ghi).
2. **Node Anatomy (5 Phần Bắt Buộc)**:
   - `[STATE: <tên>]`: Tên node đại diện cho trạng thái.
   - `[Input Artifacts]`: Chỉ danh sách khóa dữ liệu node được đọc (Artifacts Isolation).
   - `[Output Artifacts]`: Khóa dữ liệu node ghi vào.
   - `[DoD]`: 3 kiểm định nhị phân (Pass/Fail, đo được từ output, 0 dùng tính từ sáo ngữ).
   - `[Evaluation Loop]`: Phân nhánh Pass/Fail, Retry limit và `[ESCALATE_HUMAN]`.

### 2. Memory Spec
- Quản lý persistent memory dựa trên `MEMORY.md` index và các topic files.
- Hỗ trợ Long-running Session bằng cách tích hợp nghi thức đầu phiên (`pwd` ➔ Read progress/git log ➔ Read feature list ➔ Run `init.sh`).

### 3. Tool & ACI Spec
- Áp dụng Tool Namespacing (`service_resource_action`).
- Tool Consolidation: Gộp các operation hay đi cùng nhau thành 1 tool duy nhất để tránh gây nhầm lẫn cho Agent.

---

## Pre-Publish Audit Checklist (11 Bước)
Trước khi hoàn tất thiết kế Workflow:
- [ ] Topology đã qua Complexity Ladder (không dùng multi-agent nếu single-agent giải quyết tốt hơn).
- [ ] Mọi Node có đủ 5 phần `[STATE]`, `[Input Artifacts]`, `[Output Artifacts]`, `[DoD]`, `[Evaluation Loop]`.
- [ ] DoD có tính nhị phân 100%.
- [ ] Safe outputs được khai báo rõ ràng trong Frontmatter.
