# Tool Spec — Chuẩn tích hợp Tools (MCP/API)

Tools = external integrations cho agent. MCP servers, API calls, hoặc
custom scripts.

---

## Khi nào tạo Tool

| Tình huống | Tạo tool? |
|:-----------|:----------|
| Agent cần external service (database, API, cloud) | ✅ Có |
| Agent cần custom processing (data transform, automation) | ✅ Có |
| Agent cần capabilities ngoài built-in tools | ✅ Có |
| Agent chỉ cần file read/write, web search, terminal | ❌ Không (built-in) |
| Agent Tier 1, không external dependency | ❌ Không |

### Antigravity Built-in Tools (KHÔNG cần tạo MCP)
- File read/write
- Terminal commands
- Web search
- Browser automation
- Image generation

---

## Tool Types

### 1. MCP Server
Model Context Protocol — standard interface cho LLM tools.

```markdown
### [Tool Name] (MCP)
- **Server**: [mcp-server-name]
- **Setup**: [installation/config instructions]
- **Tools provided**:
  | Tool | Purpose | Parameters | Returns |
  |:-----|:--------|:-----------|:--------|
  | [name] | [1 câu] | [params] | [output] |
- **Error handling**: [khi fail]
```

### 2. API Integration
Direct API calls — khi không có MCP server.

```markdown
### [Tool Name] (API)
- **Endpoint**: [URL pattern]
- **Auth**: [method — API key, OAuth, etc.]
- **Methods**:
  | Method | Endpoint | Purpose | Params | Response |
  |:-------|:---------|:--------|:-------|:---------|
  | GET | /api/v1/... | [...] | [...] | [...] |
- **Rate limits**: [nếu có]
- **Error handling**: [status codes + recovery]
```

### 3. Custom Script
Python/Node scripts cho custom processing.

```markdown
### [Tool Name] (Script)
- **Path**: scripts/[script-name].py
- **Purpose**: [1 câu]
- **Usage**: `python scripts/[script-name].py [args]`
- **Input**: [format]
- **Output**: [format]
- **Dependencies**: [packages needed]
```

---

## Tool Description Standards

Mỗi tool cần:

1. **Purpose** — 1 câu: tool này làm gì
2. **When to use** — condition khi nào agent nên dùng tool này
3. **Parameters** — input params rõ ràng (name, type, required/optional)
4. **Returns** — output format
5. **Error handling** — khi tool fail thì agent làm gì
6. **Fallback** — nếu tool unavailable, agent có thể làm gì thay thế?

---

## Error Handling Pattern

```markdown
### Error Handling: [Tool Name]

| Error | Cause | Recovery |
|:------|:------|:---------|
| Connection timeout | Server unavailable | Retry 1 lần → nếu vẫn fail → thông báo user |
| Auth failure | Invalid credentials | Thông báo user kiểm tra credentials |
| Rate limited | Quá nhiều requests | Wait [duration] → retry |
| Invalid response | Server error | Log error → fallback hoặc thông báo user |
```

---

## Quality Checklist

```
□ Tool purpose rõ ràng (1 câu)
□ When to use — conditions cụ thể
□ Parameters có name, type, required/optional
□ Returns format defined
□ Error handling cho từng failure mode
□ Fallback khi tool unavailable
□ Không tạo tool cho built-in capabilities
□ Setup/installation instructions (nếu MCP/dependency)
```
