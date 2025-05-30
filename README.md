# 🐸 Pepe Bot Slack MCP Server v1.02

**jammies-frog 🐸 이모지로 Slack을 더 재미있게!**

한국어 지원 Slack MCP 서버로 **12개의 완전한 MCP 도구**와 **Pepe Bot 캐릭터** 기능을 제공합니다.

---

## 🚀 v1.02 주요 기능

### 🐸 Pepe Bot 특별 기능
- **jammies-frog 🐸 이모지** 자동 추가
- **ASCII 아트 Pepe** 캐릭터 메시지  
- **87KB Pepe 이미지** 업로드 지원
- **통합 DM + 반응** 기능

### 🎯 12개 완전한 MCP 도구들
1. **send_slack_message** - 채널 메시지 전송
2. **send_slack_direct_message** - 개인 DM 전송
3. **get_slack_channels** - 채널 목록 조회
4. **get_slack_channel_history** - 메시지 히스토리
5. **get_slack_users** - 사용자 디렉토리
6. **invite_user_to_channel** - 채널 초대
7. **add_reaction_to_message** - 🐸 이모지 반응
9. **upload_file_to_slack** - 레거시 파일 업로드
10. **upload_file_to_slack_new** - 신형 파일 업로드 (NEW!)
11. **upload_file_from_base64** - Base64 파일 업로드 (NEW!)
12. **send_pepe_message_with_reaction** - Pepe 통합 기능 (NEW!)

### 🖥️ MCP Inspector GUI 지원
- **브라우저 기반** 도구 테스트
- **실시간 JSON** 파라미터 입력
- **모든 12개 도구** GUI에서 테스트 가능

---

## 📋 요구사항

- **Python 3.10+** (필수)
- **Node.js 16+** (MCP Inspector용)
- **Slack 워크스페이스** 접근 권한
- **Slack Bot Token** (xoxb-) + **User Token** (xoxp-, 검색 기능용)

---

## 🔧 빠른 설치

### 1. 프로젝트 설정
```bash
cd slack-mcp
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 2. 의존성 설치 (uv 권장)
```bash
# uv 사용 (권장 - 빠름)
pip install uv
uv sync

# 또는 pip 사용
pip install -r requirements.txt
```

### 3. 실행 & 테스트
```bash
# MCP 서버 테스트
python slack_mcp_server.py

# MCP Inspector GUI 실행 (추천!)
npx @modelcontextprotocol/inspector python slack_mcp_server.py
```

---

## 🎯 MCP Inspector GUI 사용법

### 1. Inspector 실행
```bash
npx @modelcontextprotocol/inspector python slack_mcp_server.py
```

### 2. 브라우저에서 접속
```
http://localhost:6274
```

### 3. 12개 도구 테스트
GUI에서 JSON 파라미터로 모든 도구를 테스트할 수 있습니다:

- ✅ **send_slack_message** - 채널 메시지 전송
- ✅ **send_slack_direct_message** - 개인 DM 전송  
- ✅ **get_slack_channels** - 채널 목록 조회
- ✅ **get_slack_channel_history** - 메시지 히스토리
- ✅ **get_slack_users** - 사용자 디렉토리
- ✅ **invite_user_to_channel** - 채널 초대
- ✅ **add_reaction_to_message** - jammies-frog 🐸 이모지 반응
- ✅ **search_slack_messages** - Enterprise 검색
- ✅ **upload_file_to_slack** - 레거시 파일 업로드
- ✅ **upload_file_to_slack_new** - 신형 파일 업로드
- ✅ **upload_file_from_base64** - Base64 파일 업로드
- ✅ **send_pepe_message_with_reaction** - Pepe 통합 기능

### ⚡ 1분 빠른 테스트
```bash
1. http://localhost:6274 접속
2. get_slack_channels {} → 채널 목록 확인
3. send_slack_message {"channel": "C1234567890", "text": "🐸 Pepe 테스트"} 
4. add_reaction_to_message {"channel_id": "C1234567890", "timestamp": "받은타임스탬프"}
```

### 📁 Inspector에서 파일 업로드 테스트

#### 방법 1: 기존 Pepe 이미지 사용 (추천!)
```json
{
  "channels": "C1234567890",
  "file_path": "pepe.jpeg",
  "title": "Pepe Character",
  "initial_comment": "🐸 Pepe Bot 이미지 업로드!"
}
```

#### 방법 2: 절대 경로 사용
```json
{
  "channels": "C1234567890", 
  "file_path": "C:/python_workplace/assignment1/slack-mcp/pepe.jpeg",
  "title": "Absolute Path Test",
  "initial_comment": "절대 경로로 업로드"
}
```

#### 방법 3: 복사본 이미지 테스트
```json
{
  "channels": "C1234567890",
  "file_path": "test_pepe.jpeg",
  "title": "Test Pepe Copy", 
  "initial_comment": "복사본으로 테스트!"
}
```

#### 방법 4: Base64 직접 업로드 (🔥 최신!)
```json
{
  "channels": "C1234567890",
  "file_data": "SGVsbG8gUGVwZSEgZmVlbHMgZ29vZCBtYW4gPz8gDQo=",
  "filename": "hello_from_inspector.txt",
  "title": "Inspector Direct Upload",
  "initial_comment": "🐸 브라우저에서 직접 업로드 성공!"
}
```

#### 📋 파일 업로드 체크리스트
- [ ] `pepe.jpeg` (87KB) - ✅ 준비됨
- [ ] `test.txt` (32B) - ✅ 생성됨  
- [ ] `test_pepe.jpeg` (87KB) - ✅ 생성됨
- [ ] **Base64 데이터** - ✅ 준비됨
- [ ] 채널 ID 확인 (`get_slack_channels` 사용)
- [ ] 파일 권한 확인 (읽기 가능)
- [ ] 업로드 후 Slack에서 확인

### 🎯 완전한 파일 업로드 테스트 시나리오

#### 시나리오 1: Pepe 이미지 (87KB)
```json
{
  "channels": "C1234567890",
  "file_path": "pepe.jpeg", 
  "title": "Original Pepe",
  "initial_comment": "🐸 오리지널 Pepe 캐릭터!"
}
```

#### 시나리오 2: 테스트 텍스트 파일 (32B)
```json
{
  "channels": "C1234567890",
  "file_path": "test.txt",
  "title": "Pepe Says Hi",
  "initial_comment": "텍스트 파일로 인사드려요!"
}
```

#### 시나리오 3: 복사본 이미지 테스트
```json
{
  "channels": "C1234567890",
  "file_path": "test_pepe.jpeg",
  "title": "Test Pepe Copy", 
  "initial_comment": "복사본으로 테스트!"
}
```

#### 시나리오 4: Base64 직접 업로드 (🔥 최신!)
```json
{
  "channels": "C1234567890",
  "file_data": "SGVsbG8gUGVwZSEgZmVlbHMgZ29vZCBtYW4gPz8gDQo=",
  "filename": "hello_from_inspector.txt",
  "title": "Inspector Direct Upload",
  "initial_comment": "🐸 브라우저에서 직접 업로드 성공!"
}
```

#### 📋 파일 업로드 체크리스트
- [ ] `pepe.jpeg` (87KB) - ✅ 준비됨
- [ ] `test.txt` (32B) - ✅ 생성됨  
- [ ] `test_pepe.jpeg` (87KB) - ✅ 생성됨
- [ ] **Base64 데이터** - ✅ 준비됨
- [ ] 채널 ID 확인 (`get_slack_channels` 사용)
- [ ] 파일 권한 확인 (읽기 가능)
- [ ] 업로드 후 Slack에서 확인

---

## 🤖 MCP 클라이언트 설정

### Claude Desktop 설정

#### 설정 파일 위치
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### v1.02 설정
`claude_desktop_config.json` 파일에 다음 내용을 추가하세요:

```json
{
  "mcpServers": {
    "pepe-slack-mcp": {
      "command": "python",
      "args": ["C:/python_workplace/assignment1/slack-mcp/slack_mcp_server.py"]
    }
  }
}
```

---

## 🎮 사용 예시

### 🐸 Pepe Bot 전용 기능
```
"Pepe가 개발팀에게 DM으로 인사하고 frog 이모지를 달아줘"
"Pepe 이미지를 업로드해줘"
"ASCII 아트 Pepe로 메시지를 보내줘"
```

### 💬 메시징 기능
```
"#general 채널에 '🐸 안녕하세요 Pepe입니다!' 메시지를 보내줘"
"U0123456789 사용자에게 'Pepe Bot이 인사드립니다' DM을 보내줘"
"마지막 메시지에 jammies-frog 이모지 반응을 달아줘"
```

### 🔍 Enterprise 검색 (NEW!)
```
"지난 주 'deployment' 관련 메시지들을 검색해줘"
"'bug fix' 키워드로 최근 메시지들을 찾아줘"
"개발팀이 언급된 메시지들을 검색해줘"
```

### 📁 파일 업로드 (NEW!)
```
"pepe.jpeg 파일을 #random 채널에 업로드해줘"
"문서를 신형 API로 업로드해줘"
"파일을 업로드하고 설명을 추가해줘"
```

### 📊 관리 기능
```
"모든 Slack 채널 목록을 보여줘"
"#dev-team 채널의 최근 대화 10개를 가져와줘"
"개발자들을 #announcement 채널에 초대해줘"
```

### 💡 고급 사용법

#### 체이닝 기능
```
"채널 목록을 가져와서, 각 채널에 Pepe 인사 메시지를 보내고, frog 이모지를 달아줘"
```

#### 검색 + 업로드 조합
```
"'project update' 검색해서 관련 메시지 찾고, 결과를 파일로 저장해서 업로드해줘"
```

#### 관리자 기능
```
"모든 사용자 목록을 가져와서, 활성 사용자들을 #all-hands 채널에 초대해줘"
```

---

## 🛠️ JSON 파라미터 예시

### 필수 파라미터 체크시트

#### ✅ `send_slack_message`
```json
{
  "channel": "C1234567890",
  "text": "🐸 메시지 내용"
}
```

#### ✅ `send_slack_direct_message`
```json
{
  "user_id": "U0123456789",
  "text": "개인 메시지 내용"
}
```

#### ✅ `add_reaction_to_message`
```json
{
  "channel_id": "C1234567890",
  "timestamp": "1748594346.778619"
}
```

#### ✅ `upload_file_to_slack_new`
```json
{
  "channels": "C1234567890",
  "file_path": "test.txt",
  "title": "Pepe Test File",
  "initial_comment": "🐸 Hello Pepe! 테스트 파일"
}
```

#### ✅ `upload_file_from_base64` (NEW!)
```json
{
  "channels": "C1234567890",
  "file_data": "SGVsbG8gUGVwZSEgZmVlbHMgZ29vZCBtYW4gPz8gDQo=",
  "filename": "hello_pepe.txt",
  "title": "Base64 Test",
  "initial_comment": "🐸 Inspector에서 직접 업로드!"
}
```

#### ✅ `search_slack_messages`
```json
{
  "query": "pepe",
  "sort": "timestamp",
  "count": 10
}
```

#### ✅ `send_pepe_message_with_reaction`
```json
{
  "user_id": "U0123456789",
  "message": "feels good man! 🎉"
}
```

### 📊 응답 패턴

#### ✅ 성공 응답
```json
{
  "success": true,
  "message": "작업이 성공적으로 완료되었습니다.",
  "timestamp": "1748594346.778619",
  "channel": "C1234567890"
}
```

#### ❌ 실패 응답
```json
{
  "success": false,
  "error": "오류 코드",
  "details": { "추가 정보": "..." }
}
```

---

## 📁 주요 파일들

- `slack_mcp_server.py` - MCP 서버 (224줄)
- `slack_api.py` - Slack API 로직 (672줄)
- `pepe.jpeg` - Pepe 이미지 (87KB)
- `requirements.txt` - 의존성 목록
- `uv.lock` - 의존성 잠금 파일

---

## 🔍 문제 해결

### 🚨 자주 발생하는 오류

#### ❌ 토큰 오류
```
"error": "invalid_auth"
→ 환경변수 설정 확인
```

#### ❌ 권한 오류  
```
"error": "not_allowed_token_type"
→ User Token 필요 (검색 기능)
```

#### ❌ 파일 업로드 실패
```
"error": "method_deprecated"
→ upload_file_to_slack_new 사용
```

#### ❌ 반응 추가 실패
```
"error": "invalid_name"
→ jammies-frog 이모지만 지원
```

### Port 6277 사용중 오류
```bash
# 다른 Inspector 프로세스 종료 후 재실행
npx @modelcontextprotocol/inspector python slack_mcp_server.py
```

### 토큰 권한 오류
- Bot Token과 User Token 모두 필요
- 위 스코프들이 정확히 설정되었는지 확인

### 검색 기능 오류
- **원인**: User Token이 없거나 `search:read` 스코프 누락
- **해결**: User Token 설정 및 스코프 추가

### jammies-frog 이모지 오류
- **원인**: 워크스페이스에 custom emoji 없음
- **해결**: Slack 워크스페이스에 jammies-frog 이모지 추가

### 파일 업로드 실패
- **원인**: `files:write` 권한 없음 또는 파일 크기 초과
- **해결**: 권한 확인 및 파일 크기 체크 (10MB 제한)

### 가상환경 문제
```bash
# 가상환경 재생성
rmdir /s /q .venv  # Windows
python -m venv .venv
.venv\Scripts\activate
uv sync
```

---

## 🔧 MCP Inspector 팁

### 화면 구성
- **왼쪽**: 12개 도구 목록
- **중앙**: 파라미터 입력 폼  
- **오른쪽**: 실행 결과

### 효율적인 사용법
1. **JSON 포맷 검증**: 중괄호, 쉼표 확인
2. **타임스탬프 복사**: 결과에서 바로 복사
3. **오류 메시지 확인**: details 항목 주의 깊게 읽기
4. **재시도**: 실패 시 파라미터 수정 후 재실행

### 디버깅 순서
1. **환경변수 확인**: Bot Token, User Token
2. **네트워크 확인**: Slack API 연결 상태
3. **권한 확인**: OAuth 스코프 
4. **파라미터 확인**: 필수값 누락 여부

---

## 📋 체크리스트

설치 완료 확인:
- [ ] **Python 3.10+** 설치됨
- [ ] **Node.js 16+** 설치됨 (Inspector용)
- [ ] **가상환경** 생성 및 활성화됨
- [ ] **requirements.txt** 의존성 설치됨
- [ ] **Bot Token** (xoxb-) 발급 및 설정됨
- [ ] **User Token** (xoxp-) 발급 및 설정됨 ⭐ NEW!
- [ ] **권한(scopes)** 모두 설정됨
- [ ] **MCP 클라이언트** 설정 파일 수정됨
- [ ] **MCP Inspector** 정상 동작 확인됨
- [ ] **12개 도구** 모두 테스트됨

---

## 🛠️ 기술 스택

- **Python 3.10+** - 서버 언어
- **FastMCP 2.5.1+** - MCP 서버 프레임워크
- **Requests 2.32.3+** - HTTP 요청
- **python-dotenv 1.1.0+** - 환경변수 관리
- **Node.js 16+** - MCP Inspector

---

## 📞 지원

- 🐛 **이슈 리포트**: GitHub Issues
- 🖥️ **GUI 테스트**: MCP Inspector (http://localhost:6274)
- 📚 **Slack API**: [https://api.slack.com/](https://api.slack.com/)
- 🔗 **MCP 프로토콜**: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)

---

**🐸 Pepe Bot v1.02 - jammies-frog로 Slack을 더 재미있고 효율적으로 사용하세요!**

