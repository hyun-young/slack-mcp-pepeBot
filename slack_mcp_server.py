"""
🐸 Pepe Bot Slack MCP Server v1.02 with Complete Typing Support

FastMCP를 사용하여 Slack API와 연동되는 MCP 서버를 구현합니다.
완전한 타입 힌트와 typing 모듈을 적용한 버전입니다.
"""

from typing import Dict, List, Optional, Union, Any, Tuple
import base64
import tempfile
import os
from fastmcp import FastMCP
from slack_api import SlackAPIClient

# FastMCP 앱 생성
mcp: FastMCP = FastMCP("🐸 Pepe Bot Slack MCP Server v1.02")

# Slack API 클라이언트 인스턴스 생성
slack_client: SlackAPIClient = SlackAPIClient()


@mcp.tool()
def send_slack_message(channel: str, text: str) -> Dict[str, Any]:
    """
    지정된 Slack 채널에 메시지를 전송합니다.
    
    Args:
        channel (str): 채널 ID 또는 채널명 (예: #general, C1234567890)
        text (str): 전송할 메시지 내용 (UTF-8 인코딩 한글 지원)
    
    Returns:
        Dict[str, Any]: API 응답 결과
    """
    return slack_client.send_message(channel, text)


@mcp.tool()
def get_slack_channels() -> Dict[str, Any]:
    """
    접근 가능한 모든 Slack 채널 목록을 조회합니다.
    
    Returns:
        Dict[str, Any]: 채널 목록과 정보 (채널 ID, 이름, 공개/비공개 여부, 멤버십 상태)
    """
    return slack_client.get_channels()


@mcp.tool()
def get_slack_channel_history(channel_id: str, limit: int = 10) -> Dict[str, Any]:
    """
    지정된 채널의 최근 메시지 히스토리를 조회합니다.
    
    Args:
        channel_id (str): 조회할 채널의 ID
        limit (int): 조회할 메시지 수 (기본값: 10, 최대: 100)
    
    Returns:
        Dict[str, Any]: 메시지 히스토리 (메시지 내용, 작성자, 타임스탬프)
    """
    return slack_client.get_channel_history(channel_id, limit)


@mcp.tool()
def send_slack_direct_message(user_id: str, text: str) -> Dict[str, Any]:
    """
    특정 사용자에게 1:1 다이렉트 메시지를 전송합니다.
    
    Args:
        user_id (str): 메시지를 받을 사용자의 ID
        text (str): 전송할 메시지 내용
    
    Returns:
        Dict[str, Any]: API 응답 결과
    """
    return slack_client.send_direct_message(user_id, text)


@mcp.tool()
def invite_user_to_channel(channel_id: str, user_id: str) -> Dict[str, Any]:
    """
    지정된 채널에 사용자를 초대합니다.
    
    Args:
        channel_id (str): 초대할 채널의 ID
        user_id (str): 초대할 사용자의 ID
    
    Returns:
        Dict[str, Any]: API 응답 결과
    """
    return slack_client.invite_user_to_channel(channel_id, user_id)


@mcp.tool()
def get_slack_users() -> Dict[str, Any]:
    """
    워크스페이스의 모든 사용자 목록을 조회합니다.
    
    Returns:
        Dict[str, Any]: 사용자 목록과 정보 (사용자 ID, 이름, 이메일, 프로필 등)
    """
    return slack_client.get_users()


@mcp.tool()
def add_reaction_to_message(channel_id: str, timestamp: str) -> Dict[str, Any]:
    """
    특정 메시지에 jammies-frog 🐸 이모지 반응을 추가합니다.
    
    Args:
        channel_id (str): 메시지가 있는 채널의 ID
        timestamp (str): 메시지의 타임스탬프 (ts)
    
    Returns:
        Dict[str, Any]: API 응답 결과
    """
    return slack_client.add_reaction(channel_id, timestamp)


@mcp.tool()
def search_slack_messages(query: str, sort: str = "timestamp", count: int = 20) -> Dict[str, Any]:
    """
    키워드를 통해 워크스페이스의 메시지를 검색합니다.
    ⚠️ 이 기능은 User Token (SLACK_USER_TOKEN)과 search:read 권한이 필요합니다.
    
    Args:
        query (str): 검색할 키워드 (예: "페페", "in:#team1 페페")
        sort (str): 정렬 방식 ("timestamp", "score") 기본값: "timestamp"
        count (int): 검색할 메시지 수 (기본값: 20, 최대: 100)
    
    Returns:
        Dict[str, Any]: 검색 결과 (메시지 내용, 채널, 작성자 등)
    """
    return slack_client.search_messages(query, sort, count)


@mcp.tool()
def upload_file_to_slack(channels: str, file_path: str, title: str = "", 
                        initial_comment: str = "", filetype: Optional[str] = None) -> Dict[str, Any]:
    """
    채널에 파일을 업로드합니다 (레거시 API 방식).
    ⚠️ 이 방식은 deprecated되었습니다. upload_file_to_slack_new를 사용하세요.
    
    Args:
        channels (str): 파일을 업로드할 채널 ID (쉼표로 구분하여 여러 채널 가능)
        file_path (str): 업로드할 파일의 경로
        title (str): 파일 제목 (선택사항)
        initial_comment (str): 파일과 함께 보낼 코멘트 (선택사항)
        filetype (Optional[str]): 파일 타입 (선택사항, 자동 감지됨)
    
    Returns:
        Dict[str, Any]: API 응답 결과
    """
    return slack_client.upload_file(channels, file_path, title, initial_comment, filetype)


@mcp.tool()
def upload_file_to_slack_new(channels: str, file_path: str, title: str = "", 
                            initial_comment: str = "", filetype: Optional[str] = None) -> Dict[str, Any]:
    """
    새로운 Slack API를 사용하여 채널에 파일을 업로드합니다.
    (files.getUploadURLExternal + files.completeUploadExternal)
    
    Args:
        channels (str): 파일을 업로드할 채널 ID (쉼표로 구분하여 여러 채널 가능)
        file_path (str): 업로드할 파일의 경로
        title (str): 파일 제목 (선택사항)
        initial_comment (str): 파일과 함께 보낼 코멘트 (선택사항)
        filetype (Optional[str]): 파일 타입 (선택사항, 자동 감지됨)
    
    Returns:
        Dict[str, Any]: API 응답 결과
    """
    return slack_client.upload_file_new(channels, file_path, title, initial_comment, filetype)


@mcp.tool()
def upload_file_from_base64(channels: str, file_data: str, filename: str, 
                           title: str = "", initial_comment: str = "") -> Dict[str, Any]:
    """
    Base64로 인코딩된 파일 데이터를 받아서 Slack에 업로드합니다.
    Inspector에서 파일 내용을 직접 입력할 때 유용합니다.
    
    Args:
        channels (str): 파일을 업로드할 채널 ID
        file_data (str): Base64로 인코딩된 파일 데이터
        filename (str): 파일명 (확장자 포함)
        title (str): 파일 제목 (선택사항)
        initial_comment (str): 파일과 함께 보낼 코멘트 (선택사항)
    
    Returns:
        Dict[str, Any]: API 응답 결과
        
    Example:
        file_data: "SGVsbG8gUGVwZSEgZmVlbHMgZ29vZCBtYW4g8J+QuA=="
        filename: "hello_pepe.txt"
    """
    try:
        # Base64 데이터 디코딩
        file_bytes: bytes = base64.b64decode(file_data)
        
        # 임시 파일 생성
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as temp_file:
            temp_file.write(file_bytes)
            temp_file_path: str = temp_file.name
        
        try:
            # 새로운 API로 파일 업로드
            result: Dict[str, Any] = slack_client.upload_file_new(
                channels, temp_file_path, title, initial_comment
            )
            return result
        finally:
            # 임시 파일 정리
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        return {
            "success": False,
            "error": f"Base64 파일 업로드 실패: {str(e)}"
        }


@mcp.tool()
def send_pepe_message_with_reaction(user_id: str, message: str) -> Dict[str, Any]:
    """
    🐸 Pepe Bot 전용 기능: 사용자에게 DM을 보내고 자동으로 jammies-frog 반응을 추가합니다.
    
    Args:
        user_id (str): 메시지를 받을 사용자의 ID
        message (str): 전송할 Pepe 메시지 내용
    
    Returns:
        Dict[str, Any]: DM 전송 및 반응 추가 결과
    """
    # ASCII 아트 Pepe 메시지 추가
    pepe_art: str = """
```
    ∩───∩
   （  ･×･  ）
  ○_   "   _○  feels good man!
     ¯¯¯¯¯¯¯
```
"""
    
    full_message: str = f"🐸 {message}\n{pepe_art}"
    
    # DM 전송
    dm_result: Dict[str, Any] = slack_client.send_direct_message(user_id, full_message)
    
    if not dm_result.get("success"):
        return dm_result
    
    # DM 채널 정보 가져오기
    timestamp: Optional[str] = dm_result.get("timestamp")
    channel_id: Optional[str] = dm_result.get("channel")
    
    if timestamp and channel_id:
        # jammies-frog 반응 추가
        reaction_result: Dict[str, Any] = slack_client.add_reaction(channel_id, timestamp)
        
        return {
            "success": True,
            "message": "🐸 Pepe DM과 frog 반응이 성공적으로 추가되었습니다!",
            "dm_result": dm_result,
            "reaction_result": reaction_result
        }
    else:
        return {
            "success": True,
            "message": "DM은 전송되었지만 반응 추가에 필요한 정보가 부족합니다.",
            "dm_result": dm_result
        }


def main() -> None:
    """
    MCP 서버를 실행합니다.
    """
    print("🐸 Pepe Bot Slack MCP Server v1.02 starting...")
    print("📡 12개의 완전한 타입 힌트 적용 MCP 도구 준비 완료!")
    mcp.run()


if __name__ == "__main__":
    main() 