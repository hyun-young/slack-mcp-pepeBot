"""
Slack MCP 서버 구현

FastMCP를 사용하여 Slack API와 연동되는 MCP 서버를 구현합니다.
"""

from fastmcp import FastMCP
from slack_api import SlackAPIClient

# FastMCP 앱 생성
mcp = FastMCP("Slack MCP Server")

# Slack API 클라이언트 인스턴스 생성
slack_client = SlackAPIClient()


@mcp.tool()
def send_slack_message(channel: str, text: str) -> dict:
    """
    지정된 Slack 채널에 메시지를 전송합니다.
    
    Args:
        channel: 채널 ID 또는 채널명 (예: #general, C1234567890)
        text: 전송할 메시지 내용 (UTF-8 인코딩 한글 지원)
    
    Returns:
        dict: API 응답 결과
    """
    return slack_client.send_message(channel, text)


@mcp.tool()
def get_slack_channels() -> dict:
    """
    접근 가능한 모든 Slack 채널 목록을 조회합니다.
    
    Returns:
        dict: 채널 목록과 정보 (채널 ID, 이름, 공개/비공개 여부, 멤버십 상태)
    """
    return slack_client.get_channels()


@mcp.tool()
def get_slack_channel_history(channel_id: str, limit: int = 10) -> dict:
    """
    지정된 채널의 최근 메시지 히스토리를 조회합니다.
    
    Args:
        channel_id: 조회할 채널의 ID
        limit: 조회할 메시지 수 (기본값: 10, 최대: 100)
    
    Returns:
        dict: 메시지 히스토리 (메시지 내용, 작성자, 타임스탬프)
    """
    return slack_client.get_channel_history(channel_id, limit)


@mcp.tool()
def send_slack_direct_message(user_id: str, text: str) -> dict:
    """
    특정 사용자에게 1:1 다이렉트 메시지를 전송합니다.
    
    Args:
        user_id: 메시지를 받을 사용자의 ID
        text: 전송할 메시지 내용
    
    Returns:
        dict: API 응답 결과
    """
    return slack_client.send_direct_message(user_id, text)


@mcp.tool()
def invite_user_to_channel(channel_id: str, user_id: str) -> dict:
    """
    지정된 채널에 사용자를 초대합니다.
    
    Args:
        channel_id: 초대할 채널의 ID
        user_id: 초대할 사용자의 ID
    
    Returns:
        dict: API 응답 결과
    """
    return slack_client.invite_user_to_channel(channel_id, user_id)


@mcp.tool()
def get_slack_users() -> dict:
    """
    워크스페이스의 모든 사용자 목록을 조회합니다.
    
    Returns:
        dict: 사용자 목록과 정보 (사용자 ID, 이름, 이메일, 프로필 등)
    """
    return slack_client.get_users()


@mcp.tool()
def add_reaction_to_message(channel_id: str, timestamp: str) -> dict:
    """
    특정 메시지에 jammies-frog 🐸 이모지 반응을 추가합니다.
    
    Args:
        channel_id: 메시지가 있는 채널의 ID
        timestamp: 메시지의 타임스탬프 (ts)
    
    Returns:
        dict: API 응답 결과
    """
    return slack_client.add_reaction(channel_id, timestamp)


@mcp.tool()
def search_slack_messages(query: str, sort: str = "timestamp", count: int = 20) -> dict:
    """
    키워드를 통해 워크스페이스의 메시지를 검색합니다.
    ⚠️ 이 기능은 User Token (SLACK_USER_TOKEN)과 search:read 권한이 필요합니다.
    
    Args:
        query: 검색할 키워드 (예: "페페", "in:#team1 페페")
        sort: 정렬 방식 ("timestamp", "score") 기본값: "timestamp"
        count: 검색할 메시지 수 (기본값: 20, 최대: 100)
    
    Returns:
        dict: 검색 결과 (메시지 내용, 채널, 작성자 등)
    """
    return slack_client.search_messages(query, sort, count)


@mcp.tool()
def upload_file_to_slack(channels: str, file_path: str, title: str = "", 
                        initial_comment: str = "", filetype: str = None) -> dict:
    """
    채널에 파일을 업로드합니다 (레거시 API 방식).
    ⚠️ 이 방식은 deprecated되었습니다. upload_file_to_slack_new를 사용하세요.
    
    Args:
        channels: 파일을 업로드할 채널 ID (쉼표로 구분하여 여러 채널 가능)
        file_path: 업로드할 파일의 경로
        title: 파일 제목 (선택사항)
        initial_comment: 파일과 함께 보낼 코멘트 (선택사항)
        filetype: 파일 타입 (선택사항, 자동 감지됨)
    
    Returns:
        dict: API 응답 결과
    """
    return slack_client.upload_file(channels, file_path, title, initial_comment, filetype)


@mcp.tool()
def upload_file_to_slack_new(channels: str, file_path: str, title: str = "", 
                            initial_comment: str = "", filetype: str = None) -> dict:
    """
    새로운 Slack API를 사용하여 채널에 파일을 업로드합니다.
    (files.getUploadURLExternal + files.completeUploadExternal)
    
    Args:
        channels: 파일을 업로드할 채널 ID (쉼표로 구분하여 여러 채널 가능)
        file_path: 업로드할 파일의 경로
        title: 파일 제목 (선택사항)
        initial_comment: 파일과 함께 보낼 코멘트 (선택사항)
        filetype: 파일 타입 (선택사항, 자동 감지됨)
    
    Returns:
        dict: API 응답 결과
    """
    return slack_client.upload_file_new(channels, file_path, title, initial_comment, filetype)


@mcp.tool()
def upload_file_from_base64(channels: str, file_data: str, filename: str, 
                           title: str = "", initial_comment: str = "") -> dict:
    """
    Base64로 인코딩된 파일 데이터를 받아서 Slack에 업로드합니다.
    Inspector에서 파일 내용을 직접 입력할 때 유용합니다.
    
    Args:
        channels: 파일을 업로드할 채널 ID
        file_data: Base64로 인코딩된 파일 데이터
        filename: 파일명 (확장자 포함)
        title: 파일 제목 (선택사항)
        initial_comment: 파일과 함께 보낼 코멘트 (선택사항)
    
    Returns:
        dict: API 응답 결과
        
    Example:
        file_data: "SGVsbG8gUGVwZSEgZmVlbHMgZ29vZCBtYW4g8J+QuA=="
        filename: "hello_pepe.txt"
    """
    import base64
    import tempfile
    import os
    
    try:
        # Base64 데이터 디코딩
        file_bytes = base64.b64decode(file_data)
        
        # 임시 파일 생성
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name
        
        # 파일 업로드
        result = slack_client.upload_file_new(channels, temp_path, title, initial_comment)
        
        # 임시 파일 삭제
        os.unlink(temp_path)
        
        return {
            **result,
            "upload_method": "base64",
            "original_filename": filename
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": "base64_upload_failed",
            "details": str(e)
        }


@mcp.tool()
def send_pepe_message_with_reaction(channel: str, text: str) -> dict:
    """
    페페 스타일로 메시지를 보내고 자동으로 🐸 jammies-frog 이모지 반응을 추가합니다.
    
    Args:
        channel: 채널 ID 또는 채널명
        text: 전송할 메시지 내용
    
    Returns:
        dict: 메시지 전송 및 이모지 반응 결과
    """
    # 메시지 전송
    message_result = slack_client.send_message(channel, text)
    
    if message_result.get("success"):
        # 이모지 반응 추가
        reaction_result = slack_client.add_reaction(
            message_result.get("channel"), 
            message_result.get("timestamp")
        )
        
        return {
            "success": True,
            "message": "페페 스타일 메시지 전송 및 이모지 반응 완료! 🐸",
            "message_result": message_result,
            "reaction_result": reaction_result
        }
    else:
        return message_result


def main():
    """MCP 서버 실행"""
    print("Slack MCP 서버가 시작되었습니다!")
    print("사용 가능한 도구들:")
    print("  - send_slack_message: 채널에 메시지 전송")
    print("  - get_slack_channels: 채널 목록 조회")
    print("  - get_slack_channel_history: 채널 메시지 히스토리 조회")
    print("  - send_slack_direct_message: 다이렉트 메시지 전송")
    print("  - invite_user_to_channel: 채널에 사용자 초대")
    print("  - get_slack_users: 사용자 목록 조회")
    print("  - add_reaction_to_message: 메시지에 jammies-frog 이모지 반응 추가")
    print("  - search_slack_messages: 메시지 검색 (User Token 필요)")
    print("  - upload_file_to_slack: 파일 업로드 (레거시)")
    print("  - upload_file_to_slack_new: 파일 업로드 (새로운 API)")
    print("  - upload_file_from_base64: 파일 업로드 (Base64 데이터 받기)")
    print("  - send_pepe_message_with_reaction: 페페 스타일 메시지 + 자동 이모지")
    
    # MCP 서버 실행
    mcp.run()


if __name__ == "__main__":
    main() 