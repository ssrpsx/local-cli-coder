# Local CLI Coder: End-to-End Plan

เอกสารนี้เป็นแผนสร้าง Local Coding Agent ด้วย Python ตั้งแต่ศูนย์จนถึงระดับใช้งานจริงระดับ 3 โดยเน้นการเขียน logic เองเพื่อฝึกทักษะ ไม่ใช้ agent framework สำเร็จรูปในช่วงแกนหลัก

## วิธีใช้ Checkpoint

ผู้เรียนเป็นผู้ลงมือเขียนโค้ดและติ๊ก `[x]` ด้วยตนเองเมื่อทำเสร็จ ส่วน Agent ทำหน้าที่อ่าน ตรวจ และทดสอบเท่านั้น โดยห้ามแก้ไขไฟล์นี้หรือทำเครื่องหมายแทนผู้เรียน

สถานะที่ใช้:

- `[ ]` ยังไม่ทำ
- `[x]` ผู้เรียนทำเสร็จและมีหลักฐานแล้ว
- `PASS` Agent ตรวจแล้วผ่าน
- `PARTIAL` ผ่านบางส่วน ต้องแก้หรือเพิ่มหลักฐาน
- `FAIL` ไม่ผ่านเงื่อนไข
- `BLOCKED` ตรวจไม่ได้เพราะ environment หรือข้อมูลไม่พร้อม

ทุก checkpoint ต้องมีครบ 4 อย่าง:

1. โค้ดหรือเอกสารที่เกี่ยวข้อง
2. test command ที่ระบุใน milestone
3. ผลลัพธ์ที่คาดหวัง
4. หลักฐานจาก test output, diff หรือ manual verification

ห้ามติ๊ก `[x]` เพียงเพราะเขียนโค้ดเสร็จ ต้องทดสอบ behavior จริงก่อน

## 1. เป้าหมายโครงการ

สร้าง CLI ที่ผู้ใช้สามารถสั่งงานด้วยภาษาธรรมชาติ แล้ว agent สามารถ:

1. เข้าใจ project ที่กำลังทำงานอยู่
2. ค้นหาและอ่าน source code ที่เกี่ยวข้อง
3. อธิบายปัญหาและวางแผนการแก้ไข
4. สร้าง patch และขออนุมัติก่อนแก้ไฟล์
5. รัน test, lint หรือ command ที่ได้รับอนุญาต
6. อ่าน error แล้วแก้ไขซ้ำได้จำนวนรอบจำกัด
7. แสดง git status และ diff
8. ป้องกัน path, command และ secret ที่อันตราย
9. เก็บ session เพื่อกลับมาทำงานต่อได้

ตัวอย่างการใช้งานที่ต้องรองรับเมื่อจบ:

```bash
coder
coder ask "หาสาเหตุที่ test ล้มเหลว"
coder ask "เพิ่ม validation ให้ฟังก์ชันนี้ แล้วรัน test ที่เกี่ยวข้อง"
coder status
coder resume <session-id>
```

## 2. ขอบเขต

### อยู่ในขอบเขต

- Python CLI
- Ollama เป็น local provider หลัก
- OpenAI-compatible provider ในภายหลัง
- อ่าน ค้นหา และแก้ไข source code
- รัน test/lint แบบมี permission
- git status และ diff
- context management
- session persistence
- unit/integration tests
- Windows เป็น platform หลัก และควรรองรับ macOS/Linux ด้วย

### ยังไม่อยู่ในขอบเขต

- multi-agent ที่ซับซ้อน
- autonomous mode ที่ไม่มี confirmation
- browser automation
- distributed execution
- vector database/RAG ตั้งแต่เริ่มต้น
- plugin marketplace
- automatic commit/push
- sandbox ระดับ production ตั้งแต่วันแรก

## 3. หลักการพัฒนา

1. เริ่มจาก standard library ก่อนเพิ่ม dependency
2. เขียน agent loop และ tool execution เอง
3. แยก LLM provider ออกจาก agent logic
4. ทุก side effect ต้องผ่าน permission policy
5. ทุกการแก้ไฟล์ต้องเห็น diff ก่อน apply
6. ทุก command ต้องมี timeout และจำกัด output
7. ทุก milestone ต้องมีสิ่งที่รันและทดสอบได้
8. เพิ่ม abstraction เมื่อมี use case จริง ไม่สร้าง framework ล่วงหน้า
9. เก็บ decision log เมื่อเลือกแนวทางสำคัญ
10. ไม่ส่ง secret หรือไฟล์ที่ไม่เกี่ยวข้องเข้า LLM

## 4. Technology Stack

### ต้องใช้ช่วงแรก

| งาน | เครื่องมือ |
|---|---|
| Python environment | `uv` |
| CLI | `Typer` |
| Terminal output | `Rich` |
| HTTP | `httpx` |
| Schema validation | `Pydantic v2` |
| Local model | Ollama |
| Tests | `pytest` |
| Lint/format | `Ruff` |
| Type checking | `Pyright` |

### เพิ่มตาม milestone

| งาน | เครื่องมือ |
|---|---|
| Interactive input | `prompt-toolkit` |
| Retry | `tenacity` |
| Async compatibility | `anyio` |
| Ignore rules | `pathspec` |
| Patch parsing | `unidiff` หรือ `patch-ng` |
| Async tests | `pytest-asyncio` |
| HTTP mocking | `respx` |
| Syntax parsing | `tree-sitter` และ language packages |
| Multiple LLM providers | `LiteLLM` หรือ official SDKs |
| External tool protocol | MCP Python SDK |

### ไม่ควรใช้ในช่วงเริ่มต้น

- LangChain
- LangGraph
- agent framework สำเร็จรูป
- vector database
- embedding pipeline
- multi-agent orchestration

เหตุผลคือโปรเจกต์นี้ต้องการฝึกเข้าใจ state, tool calling, context, permission และ retry loop โดยตรงก่อน

## 5. สถาปัตยกรรมเป้าหมาย

```text
CLI / Interactive UI
        |
        v
Application Service
        |
        v
Agent Loop <----> Context Manager
        |
        +------> LLM Provider
        |
        +------> Tool Registry
                         |
                         +--> Files / Search
                         +--> Patch / Edit
                         +--> Shell / Tests
                         +--> Git
        |
        v
Permission Policy
        |
        v
Session Store / Logs
```

หลักการสำคัญ:

```text
LLM เสนอ action
Python ตรวจสอบ action
Python รัน action
ผลลัพธ์ถูกส่งกลับให้ LLM
```

LLM ต้องไม่สามารถอ่านไฟล์ เขียนไฟล์ หรือรัน shell ได้โดยตรง

## 6. โครงสร้างโปรเจกต์เป้าหมาย

```text
local-cli-coder/
├── README.md
├── Plan.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── src/
│   └── local_coder/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── errors.py
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── loop.py
│       │   ├── state.py
│       │   ├── context.py
│       │   └── planner.py
│       ├── llm/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── models.py
│       │   └── ollama.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   ├── files.py
│       │   ├── search.py
│       │   ├── patch.py
│       │   ├── shell.py
│       │   └── git.py
│       ├── security/
│       │   ├── __init__.py
│       │   ├── paths.py
│       │   ├── commands.py
│       │   └── permissions.py
│       ├── sessions/
│       │   ├── __init__.py
│       │   └── store.py
│       └── ui/
│           ├── __init__.py
│           └── terminal.py
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

ไม่ต้องสร้างทุกไฟล์ตั้งแต่ต้น ให้เพิ่มเมื่อถึง milestone ที่เกี่ยวข้อง

## 7. Agent Loop เป้าหมาย

```text
รับ user prompt
  -> สร้างหรือโหลด AgentState
  -> เพิ่ม prompt ใน message history
  -> สร้าง context ตาม budget
  -> เรียก LLM
  -> validate response
  -> ถ้าเป็น final: แสดงผลและจบ
  -> ถ้าเป็น tool call:
       validate tool และ arguments
       ตรวจ permission
       execute tool
       จำกัดผลลัพธ์
       เพิ่ม tool result ลง state
       วนต่อ
  -> หยุดเมื่อครบ max iterations หรือผู้ใช้ยกเลิก
```

Agent ต้องมี `max_iterations` ตั้งแต่แรก เพื่อป้องกัน loop ไม่จบ

## 8. Checkpoint Summary

ตารางนี้ใช้เป็นภาพรวมสำหรับ Agent และผู้เรียน ห้ามใช้แทน checklist รายละเอียดของแต่ละ milestone

| สถานะ | Major Checkpoint | Milestone | จุดตรวจหลัก | คำสั่งตรวจหลัก |
|---|---|---|---|---|
| [ ] | MC-00 | 0 | Environment และ package import | `uv run pytest` |
| [ ] | MC-01 | 1 | CLI และ error handling | `uv run coder --help` |
| [ ] | MC-02 | 2 | Config และ logging | `uv run pytest tests/unit/test_config.py -q` |
| [ ] | MC-03 | 3 | Ollama provider | `uv run pytest tests/unit/test_ollama.py -q` |
| [ ] | MC-04 | 4 | Read-only tools | `uv run pytest tests/unit/test_tools.py -q` |
| [ ] | MC-05 | 5 | Agent loop | `uv run pytest tests/unit/test_agent_loop.py -q` |
| [ ] | MC-06 | 6 | Context management | `uv run pytest tests/unit/test_context.py -q` |
| [ ] | MC-07 | 7 | Patch และ file editing | `uv run pytest tests/unit/test_patch.py -q` |
| [ ] | MC-08 | 8 | Shell และ verification | `uv run pytest tests/unit/test_shell.py -q` |
| [ ] | MC-09 | 9 | Permission และ security | `uv run pytest tests/security -q` |
| [ ] | MC-10 | 10 | Git integration | `uv run pytest tests/unit/test_git.py -q` |
| [ ] | MC-11 | 11 | Session persistence | `uv run pytest tests/unit/test_sessions.py -q` |
| [ ] | MC-12 | 12 | Quality และ release | `uv run pytest` |

## 9. Milestones

## Milestone 0: Environment และ Python Foundation

### เป้าหมาย

เตรียม environment และทบทวน Python ที่จำเป็น

### ต้องเรียน

- function, class และ module
- list, dict, set และ tuple
- type hints และ `Protocol`
- exceptions และ custom exceptions
- `pathlib`, `json`, `dataclasses`
- `subprocess`
- `async`/`await`
- virtual environment และ package management
- Git พื้นฐาน

### งานที่ต้องทำ

1. ติดตั้ง Python เวอร์ชันที่โปรเจกต์กำหนด
2. ติดตั้ง `uv`
3. สร้าง `pyproject.toml`
4. ตั้ง `src` layout
5. ตั้ง `.gitignore`
6. สร้างคำสั่ง test และ lint เบื้องต้น

### ผ่านเมื่อ

- `uv run python -m local_coder` ทำงานได้
- `uv run pytest` ทำงานได้
- `uv run ruff check .` ทำงานได้
- โค้ดแยก package และ import ได้ถูกต้อง

### Student Checkpoint

- [X] ติดตั้ง Python และ `uv`
- [X] สร้าง `pyproject.toml` และ `src` layout
- [X] สร้าง `.gitignore`
- [X] คำสั่งเริ่มต้นทำงานได้
- [X] มี test อย่างน้อยหนึ่ง test
- [X] มีหลักฐานคำสั่ง test ผ่าน

### วิธีทดสอบ

```powershell
uv run python -m local_coder
uv run pytest
uv run ruff check .
```

### Expected Result

- โปรแกรมเริ่มต้นโดยไม่เกิด import error
- pytest ผ่านทั้งหมด
- Ruff ไม่พบ error
- ไม่มี secret หรือไฟล์ environment ถูก track ใน Git

## Milestone 1: CLI Skeleton

### เป้าหมาย

สร้าง CLI ที่รับคำสั่งและแสดงผลได้ โดยยังไม่เรียก LLM

### คำสั่ง

```bash
coder
coder ask "ข้อความ"
coder --project .
coder --help
```

### ต้องทำ

- ใช้ Typer
- รองรับ `--project`
- ตรวจ project root
- รองรับ interactive prompt
- แสดง error ที่อ่านง่ายด้วย Rich
- รองรับ Ctrl+C

### ต้องทดสอบ

- ไม่มี prompt
- project path ไม่มีอยู่จริง
- project path เป็นไฟล์
- path มีช่องว่าง
- Ctrl+C

### ผ่านเมื่อ

CLI เรียกใช้ได้บน Windows และไม่พิมพ์ traceback ที่ไม่จำเป็นให้ผู้ใช้

### Student Checkpoint

- [ ] คำสั่ง `coder --help` ทำงาน
- [ ] คำสั่ง `coder ask "ข้อความ"` รับ prompt ได้
- [ ] `--project` ตรวจสอบ project root ได้
- [ ] จัดการ path ที่ไม่มีอยู่จริง
- [ ] จัดการ path ที่เป็นไฟล์
- [ ] จัดการ path ที่มีช่องว่าง
- [ ] จัดการ Ctrl+C
- [ ] มี test สำหรับ failure cases

### วิธีทดสอบ

```powershell
uv run coder --help
uv run coder --project .
uv run pytest tests/unit/test_cli.py -q
```

ทดสอบเพิ่มเติมด้วย path ที่ไม่มีอยู่จริง, path ที่เป็นไฟล์ และกด `Ctrl+C` ระหว่าง interactive mode

### Expected Result

- help แสดงคำสั่งครบ
- project path ถูก resolve และ validate
- invalid path แสดง error ที่เข้าใจได้
- Ctrl+C จบการทำงานโดยไม่แสดง traceback ที่ไม่จำเป็น

## Milestone 2: Configuration และ Logging

### เป้าหมาย

ทำให้ค่าต่างๆ ไม่ hard-code ใน source code

### Config ที่ต้องมี

```text
project_root
llm_provider
ollama_url
model
request_timeout
max_iterations
max_file_size
max_tool_output
permission_mode
session_database
```

### ต้องทำ

- config object ด้วย Pydantic หรือ dataclass
- ค่า default ที่ปลอดภัย
- environment variables
- CLI options override config
- log ระดับ debug/info/error
- ไม่ log secret หรือ prompt ที่มี secret

### ผ่านเมื่อ

เปลี่ยน model และ Ollama endpoint ได้โดยไม่แก้ source code

### Student Checkpoint

- [ ] สร้าง config object
- [ ] มีค่า default ที่ปลอดภัย
- [ ] อ่านค่าจาก environment variables
- [ ] CLI options override config ได้
- [ ] มี debug/info/error logging
- [ ] log ไม่แสดง secret
- [ ] มี test ลำดับความสำคัญของ config

### วิธีทดสอบ

```powershell
$env:CODER_MODEL = "test-model"
$env:CODER_OLLAMA_URL = "http://localhost:11434"
uv run coder config --show
uv run pytest tests/unit/test_config.py -q
```

### Expected Result

- ค่า environment ถูกอ่านได้
- CLI override environment ได้ตามที่ออกแบบ
- ค่า invalid ถูก reject พร้อมข้อความชัดเจน
- secret ไม่ปรากฏใน log

## Milestone 3: Ollama Provider

### เป้าหมาย

เรียก local LLM ได้ โดยแยก provider ออกจาก agent

### ต้องทำ

- `LLMProvider` interface
- Ollama implementation ด้วย `httpx`
- normal response
- streaming response
- timeout
- connection error
- retry เฉพาะ error ที่ retry ได้
- parse response เป็น Pydantic model

### Response ที่ต้องรองรับ

```text
final answer
tool call
invalid response
provider error
```

### ต้องทดสอบ

- mock success response
- malformed JSON
- timeout
- HTTP 4xx/5xx
- Ollama unavailable

### ผ่านเมื่อ

เรียก local model ได้และเปลี่ยน provider ภายหลังได้โดยไม่ต้องแก้ agent loop

### Student Checkpoint

- [ ] มี `LLMProvider` interface
- [ ] Ollama provider เรียก API ได้
- [ ] รองรับ normal response
- [ ] รองรับ streaming response
- [ ] validate response ด้วย schema
- [ ] จัดการ timeout และ connection error
- [ ] retry เฉพาะ error ที่เหมาะสม
- [ ] มี mock tests โดยไม่ต้องเปิด Ollama
- [ ] มี integration test กับ Ollama จริงถ้าสภาพแวดล้อมพร้อม

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_ollama.py -q
uv run pytest tests/integration/test_ollama_live.py -q
```

ถ้าไม่มี Ollama ให้รันเฉพาะ unit tests และรายงานสถานะ `BLOCKED` สำหรับ live test ห้ามนับเป็น `PASS`

### Expected Result

- mock success ผ่าน
- malformed response ถูก reject
- timeout ไม่ทำให้โปรแกรมค้าง
- Ollama unavailable แสดง error ที่เข้าใจได้
- agent layer ไม่ผูกกับ implementation ของ Ollama

## Milestone 4: Tool Contract และ Read-only Tools

### เป้าหมาย

ให้ agent สำรวจ project ได้อย่างปลอดภัย

### Tools

```text
list_files
read_file
search_code
git_status
git_diff
```

### Tool contract

ทุก tool ต้องมี:

- name
- description
- argument schema
- execute method
- timeout ที่เหมาะสม
- output limit
- error result ที่ model เข้าใจได้

### `list_files`

- ไม่รวม `.git`
- เคารพ `.gitignore`
- ไม่รวม binary ตามค่าเริ่มต้น
- จำกัดจำนวนผลลัพธ์

### `read_file`

- ตรวจ path ให้อยู่ใน project
- จำกัดขนาดไฟล์
- รองรับ line range
- แจ้ง encoding error อย่างปลอดภัย
- block secret files ตาม policy

### `search_code`

- ใช้ `rg` ถ้ามี
- มี Python fallback สำหรับ portability
- จำกัดจำนวนผลลัพธ์
- แสดง path และ line number

### ผ่านเมื่อ

Agent ตอบคำถามจาก project จริงได้โดยไม่ต้องอ่านทุกไฟล์

### Student Checkpoint

- [ ] มี tool registry และ tool contract
- [ ] `list_files` ทำงาน
- [ ] `read_file` ทำงาน
- [ ] `search_code` ทำงาน
- [ ] `git_status` ทำงาน
- [ ] `git_diff` ทำงาน
- [ ] จำกัดขนาดไฟล์และจำนวนผลลัพธ์
- [ ] เคารพ `.gitignore`
- [ ] block binary และ secret files ตาม policy
- [ ] มี unit tests ของทุก tool

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_tools.py -q
uv run coder ask "แสดงโครงสร้าง project และค้นหา TODO"
```

### Expected Result

- tools คืนผลลัพธ์ตาม schema
- path นอก project ถูกปฏิเสธ
- output ใหญ่ถูกตัดอย่างปลอดภัย
- agent ค้นหาไฟล์ที่เกี่ยวข้องได้โดยไม่อ่านทั้ง project

## Milestone 5: Agent Loop และ State

### เป้าหมาย

สร้าง reasoning/tool loop ด้วยตัวเอง

### State ที่ต้องมี

```text
messages
iteration
tool_call_count
files_read
changed_files
last_error
started_at
```

### ต้องทำ

- tool registry
- dispatch tool
- validate arguments
- ส่ง tool result กลับ model
- `max_iterations`
- unknown tool handling
- duplicate tool call detection แบบง่าย
- cancellation ด้วย Ctrl+C
- debug trace ของแต่ละรอบ

### ผ่านเมื่อ

คำสั่งต่อไปนี้ทำงานได้:

```bash
coder ask "ค้นหา bug ในระบบคำนวณภาษีและอธิบายสาเหตุ"
```

Agent ต้องตัดสินใจเองว่าจะ list, search และ read ไฟล์ใด

### Student Checkpoint

- [ ] มี `AgentState`
- [ ] เพิ่ม user message เข้า state
- [ ] เรียก LLM และ parse response
- [ ] dispatch tool call ได้
- [ ] ส่ง tool result กลับ LLM
- [ ] รองรับ final response
- [ ] จำกัด `max_iterations`
- [ ] จัดการ unknown tool
- [ ] จัดการ malformed arguments
- [ ] รองรับ Ctrl+C
- [ ] มี trace สำหรับ debug

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_agent_loop.py -q
uv run pytest tests/integration/test_agent_read_only.py -q
uv run coder ask "ค้นหา bug ในระบบคำนวณภาษีและอธิบายสาเหตุ"
```

### Expected Result

- tool call ถูก execute ตามลำดับ
- tool result ถูกส่งกลับไปยัง model
- agent จบด้วย final response
- agent หยุดเมื่อครบ iteration limit
- unknown tool ไม่ทำให้โปรแกรม crash

## Milestone 6: Context Management

### เป้าหมาย

ส่งเฉพาะข้อมูลที่จำเป็นให้ model และรับมือกับ context limit

### Context sources

```text
system prompt
project instructions
user request
recent conversation
relevant file content
tool results
git diff
test errors
```

### ต้องทำ

- context budget
- จำกัดขนาด tool output
- ตัดข้อความเก่าตามลำดับความสำคัญ
- สรุป history เมื่อยาวเกินไป
- อ่าน project instruction files
- เคารพ `.gitignore`
- filter secret และ sensitive files
- ป้องกัน instruction ใน source code ไม่ให้ override system rules

### ผ่านเมื่อ

- project ใหญ่ขึ้นแล้วไม่ส่งทุกไฟล์เข้า context
- context เต็มแล้ว agent ยังตอบได้
- source code ที่มีข้อความหลอก model ไม่สามารถเปลี่ยน policy ได้

### Student Checkpoint

- [ ] กำหนด context budget
- [ ] จำกัด tool output
- [ ] เลือก recent messages ตาม priority
- [ ] มี truncation behavior
- [ ] มี summarization behavior เมื่อจำเป็น
- [ ] อ่าน project instructions ได้อย่างมีลำดับความสำคัญ
- [ ] filter secret และ sensitive files
- [ ] ทดสอบ prompt injection จาก source file

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_context.py -q
uv run pytest tests/integration/test_large_context.py -q
```

### Expected Result

- context ไม่เกิน budget ที่กำหนด
- ข้อมูลสำคัญล่าสุดยังอยู่หลัง truncation
- output ขนาดใหญ่ถูกย่ออย่างมีข้อความแจ้ง
- instruction ใน source code ไม่สามารถเปลี่ยน system policy

## Milestone 7: Patch และ File Editing

### เป้าหมาย

แก้ไฟล์แบบตรวจสอบได้และไม่ทำลายการแก้ไขเดิมของผู้ใช้

### Flow

```text
อ่านไฟล์ปัจจุบัน
  -> model เสนอ patch
  -> validate patch
  -> ตรวจ target path
  -> สร้าง diff preview
  -> ขอ confirmation
  -> apply patch
  -> ตรวจผลหลัง apply
```

### ต้องทำ

- patch schema
- path validation
- reject absolute path
- reject `..` traversal
- ตรวจ source context ก่อน apply
- แสดง diff
- confirmation
- ปฏิเสธแล้วไม่เปลี่ยนไฟล์
- patch failure feedback
- ตรวจ git diff หลัง apply

### Library

เริ่มด้วย `difflib` และ standard library ก่อน แล้วค่อยทดลอง `unidiff` หรือ `patch-ng`

### ผ่านเมื่อ

```bash
coder ask "เพิ่ม validation ให้ฟังก์ชันนี้ แล้วแสดง diff ให้ฉันตรวจ"
```

ไม่มีไฟล์ถูกแก้จนกว่าผู้ใช้จะอนุมัติ

### Student Checkpoint

- [ ] model ส่ง patch ตาม schema
- [ ] reject absolute path
- [ ] reject `..` traversal
- [ ] ตรวจ source context ก่อน apply
- [ ] แสดง diff preview
- [ ] ขอ confirmation
- [ ] ปฏิเสธแล้วไฟล์ไม่เปลี่ยน
- [ ] patch failure ถูกส่งกลับเป็น tool error
- [ ] ตรวจผลหลัง apply
- [ ] มี tests ป้องกันการแก้ไฟล์นอก project

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_patch.py -q
uv run pytest tests/integration/test_file_editing.py -q
uv run coder ask "เพิ่ม validation ให้ฟังก์ชันนี้ แล้วแสดง diff ให้ฉันตรวจ"
```

### Expected Result

- diff แสดงก่อนแก้ไขจริง
- ตอบปฏิเสธแล้วไม่มีไฟล์เปลี่ยน
- patch ที่ target นอก project ถูก reject
- patch ที่ source ไม่ตรงถูก reject หรือขออ่านไฟล์ใหม่

## Milestone 8: Shell, Tests และ Verification Loop

### เป้าหมาย

ให้ agent ตรวจสอบงานหลังแก้ไขและแก้ error ได้จำกัดจำนวนรอบ

### Tools

```text
run_test
run_lint
run_formatter
run_command
```

แยก tools ที่รู้จักและปลอดภัยออกจาก arbitrary shell command

### ต้องทำ

- `subprocess.run` ที่กำหนด `cwd`
- timeout
- stdout/stderr capture
- output truncation
- exit code
- process cancellation
- command policy
- confirmation policy
- retry loop สูงสุด 3 รอบในช่วงแรก

### Verification loop

```text
apply patch
  -> run test
  -> ถ้าผ่าน: สรุปผล
  -> ถ้า fail: ส่ง error ให้ model
  -> ขอ patch ใหม่
  -> วนจนผ่านหรือครบจำนวนรอบ
```

### ผ่านเมื่อ

Agent แก้ bug เล็กๆ และทำให้ test ผ่านได้ โดยไม่วนไม่จบและไม่รันคำสั่งนอก project

### Student Checkpoint

- [ ] `run_test` ทำงาน
- [ ] `run_lint` ทำงาน
- [ ] `run_formatter` ทำงาน
- [ ] `run_command` มี timeout
- [ ] capture stdout/stderr ได้
- [ ] จำกัด output ได้
- [ ] รองรับ non-zero exit code
- [ ] รองรับ process cancellation
- [ ] มี command policy
- [ ] verification loop จำกัดจำนวนรอบ
- [ ] มี test สำหรับ timeout และ failing command

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_shell.py -q
uv run pytest tests/integration/test_verification_loop.py -q
```

ทดสอบกับ project ที่มี test ผ่าน, test fail, command timeout และ command ที่ไม่อนุญาต

### Expected Result

- command timeout ไม่ทำให้ agent ค้าง
- output ถูกตัดเมื่อเกิน limit
- test fail ถูกส่งกลับให้ model วิเคราะห์
- verification loop หยุดเมื่อ test ผ่านหรือครบ retry limit

## Milestone 9: Permission และ Security

### เป้าหมาย

ทำให้ human-in-the-loop เป็นส่วนหนึ่งของ architecture ไม่ใช่ code เฉพาะกิจ

### ระดับ permission

```text
allow  อนุญาตอัตโนมัติ
ask    ถามผู้ใช้
deny   ปฏิเสธ
```

### Default policy

| Action | Default |
|---|---|
| อ่าน source file | allow |
| search code | allow |
| git status/diff | allow |
| อ่าน `.env`, key, credential | deny |
| แก้ source file | ask |
| รัน test | ask ครั้งแรก |
| รัน arbitrary shell | ask |
| ลบไฟล์ | ask หรือ deny |
| เขียนนอก project | deny |
| network access | ask |

### ต้องป้องกัน

- path traversal
- command injection
- secret leakage
- arbitrary file deletion
- symlink escape
- shell command ที่อันตราย
- output ที่มี credential
- prompt injection จากไฟล์
- process ที่รันไม่จบ

### หมายเหตุ

บน Windows ต้องทดสอบ path separator, drive letter, PowerShell และ `cmd.exe` โดยเฉพาะ ไม่ควรสมมติว่า shell เป็น Unix

### ผ่านเมื่อ

ผู้ใช้เห็น action, target, arguments และผลกระทบก่อนทุก side effect

### Student Checkpoint

- [ ] มี permission levels: allow, ask, deny
- [ ] read-only action มี policy ชัดเจน
- [ ] file write ต้องถามผู้ใช้
- [ ] shell command ต้องถามผู้ใช้
- [ ] secret files ถูก deny
- [ ] path traversal ถูก deny
- [ ] symlink escape ถูกตรวจ
- [ ] dangerous command ถูก block หรือถาม
- [ ] network access มี policy
- [ ] มี audit log ของ permission decision
- [ ] มี security tests

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_permissions.py -q
uv run pytest tests/security -q
```

ทดสอบ path traversal, absolute path, symlink, `.env`, command อันตราย และการตอบปฏิเสธของผู้ใช้

### Expected Result

- ไม่มี side effect โดยไม่มี policy decision
- action ที่ deny ไม่ถูก execute
- target และ arguments แสดงก่อน action ที่ต้องถาม
- security tests ผ่านทั้งหมด

## Milestone 10: Git Integration

### เป้าหมาย

ทำงานร่วมกับ working tree จริงโดยไม่ทำลายการแก้ไขเดิม

### ต้องทำ

- ตรวจว่าอยู่ใน git repository หรือไม่
- `git status --short`
- `git diff`
- แสดง changed files ก่อนและหลัง agent ทำงาน
- ตรวจ uncommitted changes ก่อนแก้ไฟล์
- ไม่ reset, checkout หรือ commit อัตโนมัติ
- แจ้งผู้ใช้หากไฟล์มีการแก้ไขจากภายนอกระหว่าง session

### ผ่านเมื่อ

ผู้ใช้สามารถตรวจสอบการเปลี่ยนแปลงทั้งหมดผ่าน git diff และ agent ไม่ลบงานเดิม

### Student Checkpoint

- [ ] ตรวจว่า project เป็น Git repository
- [ ] แสดง `git status --short`
- [ ] แสดง `git diff`
- [ ] แสดง changed files ก่อนและหลังงาน
- [ ] ตรวจ uncommitted changes เดิม
- [ ] ไม่ทำ automatic reset/checkout/commit
- [ ] ตรวจ external file changes
- [ ] มี tests กับ clean และ dirty working tree

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_git.py -q
uv run pytest tests/integration/test_git_safety.py -q
uv run coder status
git status --short
git diff
```

### Expected Result

- status และ diff ตรงกับ Git จริง
- งานเดิมของผู้ใช้ไม่ถูกลบ
- project ที่ไม่ใช่ Git แสดง warning ที่เหมาะสม
- agent ไม่ commit หรือ reset เอง

## Milestone 11: Session Persistence

### เป้าหมาย

กลับมาทำงานต่อได้หลังปิด CLI

### Storage

ใช้ `sqlite3` ที่มากับ Python ก่อน ไม่ต้องใช้ database server

### เก็บข้อมูล

```text
session id
project root
model/provider
messages
tool calls
permission decisions
changed files
errors
timestamps
```

### คำสั่ง

```bash
coder sessions
coder resume <session-id>
coder delete-session <session-id>
```

### ผ่านเมื่อ

ปิดโปรแกรมแล้ว resume session ได้ และ context ที่สำคัญยังอยู่ครบ

### Student Checkpoint

- [ ] สร้าง SQLite schema
- [ ] บันทึก session metadata
- [ ] บันทึก messages
- [ ] บันทึก tool calls
- [ ] บันทึก permission decisions
- [ ] list sessions ได้
- [ ] resume session ได้
- [ ] delete session ได้
- [ ] จัดการ database corruption/error อย่างปลอดภัย
- [ ] มี persistence tests

### วิธีทดสอบ

```powershell
uv run pytest tests/unit/test_sessions.py -q
uv run pytest tests/integration/test_session_resume.py -q
uv run coder sessions
```

### Expected Result

- session ที่บันทึกไว้ resume ได้
- messages และ tool history สำคัญยังอยู่
- delete session ไม่ลบ project files
- database error แสดงอย่างเข้าใจได้

## Milestone 12: Quality, Evaluation และ Release

### Testing layers

#### Unit tests

- path validation
- command validation
- context trimming
- response parsing
- tool registry
- patch validation
- permission policy

#### Integration tests

- agent เรียก tool ตามลำดับ
- mock LLM response
- patch แล้วรัน test
- session save/resume
- provider timeout/retry

#### Manual evaluation

สร้าง benchmark project ขนาดเล็กที่มี:

- bug ที่รู้คำตอบ
- test ที่ fail
- หลายไฟล์ที่ชื่อคล้ายกัน
- secret file ที่ต้องห้ามอ่าน
- uncommitted changes เดิม
- project ที่มีทั้ง Python และ JavaScript

วัดผล:

```text
task success rate
จำนวน tool calls
จำนวนรอบแก้ไข
เวลาที่ใช้
จำนวน false tool calls
จำนวน permission violations
จำนวน test ที่ผ่านหลังแก้
```

### Quality tools

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

### Release checklist

- [ ] `pyproject.toml` มี metadata ครบ
- [ ] มี README สำหรับติดตั้งและใช้งาน
- [ ] มี config example
- [ ] ไม่มี secret ใน repository
- [ ] มี test บน Windows
- [ ] error message อ่านเข้าใจได้
- [ ] มี version command
- [ ] มี changelog หรือ decision log

### Student Checkpoint

- [ ] Unit tests ครอบคลุม security, parsing, tools, patch และ session
- [ ] Integration tests ครอบคลุม agent flow และ provider failure
- [ ] Manual benchmark project ถูกสร้างและมี known expected results
- [ ] วัด task success rate และจำนวน tool calls
- [ ] รัน quality checks ครบ
- [ ] ทดสอบ clean installation
- [ ] ทดสอบบน Windows
- [ ] ตรวจว่าไม่มี secret ใน repository
- [ ] มี README สำหรับผู้ใช้งาน
- [ ] มี decision log หรือ changelog

### วิธีทดสอบ

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

### Expected Result

- quality checks ผ่านทั้งหมด
- test suite ผ่านทั้งหมด
- package ติดตั้งใน clean environment ได้
- manual benchmark report มี task success rate และ known limitations

## 10. Definition of Done ระดับ 3

โปรเจกต์ถือว่าถึงเป้าหมายเมื่อทำได้ครบ:

- [ ] เปิด project ได้อย่างปลอดภัย
- [ ] ใช้ local LLM ผ่าน provider abstraction
- [ ] อ่านและค้นหา source code ได้
- [ ] ทำ agent loop ที่มี tool calls ได้
- [ ] จัดการ context ที่ใหญ่เกินได้
- [ ] สร้างและ apply patch ได้
- [ ] แสดง diff และขอ confirmation
- [ ] รัน test/lint พร้อม timeout
- [ ] อ่าน error และแก้ซ้ำได้จำกัดรอบ
- [ ] มี path/command/secret protection
- [ ] แสดง git status และ diff
- [ ] resume session ได้
- [ ] มี unit และ integration tests
- [ ] ผ่าน Ruff, Pyright และ Pytest
- [ ] ใช้งานบน Windows ได้โดยไม่พึ่ง Unix-only behavior

### วิธีตรวจ Final Checkpoint

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
uv run coder --help
uv run coder status
```

นอกจากคำสั่งข้างต้น ต้องมี manual evaluation report จาก benchmark projects ใน Milestone 12 และต้องตรวจ security cases แบบ read-only ให้ครบ

## 11. ทักษะที่ต้องสะสมระหว่างทาง

### Python

- modules และ package design
- type hints และ protocols
- dataclass และ Pydantic models
- sync/async I/O
- subprocess
- filesystem security
- exception design
- testing และ mocking
- packaging ด้วย `pyproject.toml`

### AI Engineering

- prompt design
- structured output
- tool calling
- context engineering
- token budget
- retry/fallback
- prompt injection defense
- model evaluation
- local inference

### Software Engineering

- API abstraction
- state machine
- permission boundary
- process management
- git integration
- logging/observability
- test-driven development
- cross-platform behavior

## 12. Definition of Done ของแต่ละ Milestone

ห้ามขึ้น milestone ถัดไปจนกว่าจะมีครบ:

1. โค้ดรันได้
2. มี test ของ behavior หลัก
3. มี README หรือ note สั้นๆ ว่าทำงานอย่างไร
4. ทดลอง failure case อย่างน้อยหนึ่งแบบ
5. ตรวจ `git diff` แล้วเข้าใจการเปลี่ยนแปลงทั้งหมด
6. เขียนสิ่งที่เรียนรู้และปัญหาที่พบลง decision log

## 13. Decision Log Template

เมื่อเลือกแนวทางสำคัญ ให้บันทึกในรูปแบบนี้:

```text
วันที่:
หัวข้อ:
ตัวเลือก:
ตัวเลือกที่เลือก:
เหตุผล:
ข้อเสียที่ยอมรับ:
เงื่อนไขที่อาจทำให้เปลี่ยนใจ:
```

หัวข้อที่ควรบันทึก:

- ทำไมใช้ Ollama
- ทำไมไม่ใช้ agent framework
- ทำไมใช้ subprocess แทน GitPython ในช่วงแรก
- policy ของ shell command
- รูปแบบ patch
- context truncation strategy
- SQLite schema

## 14. ลำดับการลงมือทำแบบสั้น

```text
1. ตั้ง Python project ด้วย uv
2. ทำ CLI รับ prompt
3. เชื่อม Ollama
4. ทำ read_file
5. ทำ search_code และ list_files
6. ทำ tool registry
7. ทำ agent loop
8. ทำ context budget
9. ทำ patch preview และ confirmation
10. ทำ run_test และ verification loop
11. ทำ permission policy
12. ทำ git status/diff
13. ทำ SQLite session
14. เพิ่ม tests, Ruff, Pyright และ CI
15. ทดสอบกับ benchmark projects
```

## 15. สิ่งที่ไม่ควรทำ

- อย่าให้ model เขียนไฟล์โดยตรงโดยไม่มี diff
- อย่าให้ model รัน shell โดยไม่มี permission
- อย่าส่งทั้ง project เข้า context
- อย่าใช้ `shell=True` โดยไม่มี policy และ timeout
- อย่าเก็บ API key หรือ secret ใน log
- อย่าเพิ่ม vector database ก่อนมีปัญหา context จริง
- อย่าเพิ่ม multi-agent ก่อน single-agent loop เสถียร
- อย่าเชื่อ output ของ model โดยไม่ validate schema
- อย่า reset หรือ checkout งานของผู้ใช้โดยอัตโนมัติ
- อย่าแก้ปัญหาโดยเพิ่ม dependency ก่อนเข้าใจ root cause

## 16. ผลลัพธ์สุดท้ายที่คาดหวัง

เมื่อทำตามแผนนี้จนจบ จะได้ทั้ง:

1. Local CLI Coding Agent ที่ใช้งานได้จริงระดับหนึ่ง
2. ความเข้าใจ Python สำหรับระบบที่มี I/O และ state ซับซ้อน
3. ประสบการณ์สร้าง tool-using agent ตั้งแต่ระดับ protocol ถึง execution
4. ประสบการณ์ด้าน security และ human-in-the-loop
5. ความเข้าใจ context engineering และ LLM failure modes
6. ประสบการณ์ testing, packaging, Git และ cross-platform CLI
7. พื้นฐานพร้อมต่อยอดไป MCP, plugins, subagents และ sandbox ในระดับ 4
