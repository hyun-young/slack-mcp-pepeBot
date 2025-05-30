"""
🐸 Pepe Bot Slack API Client v1.02 with Complete Typing Support

Slack API와 상호작용하기 위한 완전한 타입 힌트가 적용된 클라이언트입니다.
typing 모듈을 활용하여 모든 메서드와 변수에 타입 정보를 제공합니다.
"""

import os
import mimetypes
from typing import Dict, List, Optional, Any, Union, Tuple, BinaryIO
import requests
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv(".env")


class SlackAPIClient:
    """
    Slack API와 상호작용하기 위한 완전한 타입 힌트가 적용된 클라이언트 클래스
    """
    
    def __init__(self) -> None:
        """
        SlackAPIClient를 초기화합니다.
        
        Raises:
            ValueError: SLACK_BOT_TOKEN 환경변수가 설정되지 않은 경우
        """
        self.bot_token: Optional[str] = os.getenv("SLACK_BOT_TOKEN")
        self.user_token: Optional[str] = os.getenv("SLACK_USER_TOKEN")
        
        if not self.bot_token:
            raise ValueError("SLACK_BOT_TOKEN 환경변수가 설정되지 않았습니다.")
        
        self.base_url: str = "https://slack.com/api"
        
        # Bot Token용 헤더 (기본)
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        # User Token용 헤더 (검색 기능용)
        self.user_headers: Optional[Dict[str, str]] = None
        if self.user_token:
            self.user_headers = {
                "Authorization": f"Bearer {self.user_token}",
                "Content-Type": "application/json"
            }
    
    def make_request(
        self, 
        endpoint: str, 
        method: str = "GET", 
        data: Optional[Dict[str, Any]] = None, 
        use_user_token: bool = False
    ) -> Dict[str, Any]:
        """
        Slack API 요청을 위한 헬퍼 메서드
        
        Args:
            endpoint (str): API 엔드포인트
            method (str): HTTP 메서드 (GET 또는 POST)
            data (Optional[Dict[str, Any]]): 요청 데이터
            use_user_token (bool): User Token 사용 여부 (검색 기능용)
        
        Returns:
            Dict[str, Any]: API 응답 결과
        """
        url: str = f"{self.base_url}/{endpoint}"
        
        # User Token 사용 시
        if use_user_token:
            if not self.user_headers:
                return {
                    "ok": False,
                    "error": "SLACK_USER_TOKEN 환경변수가 설정되지 않았습니다."
                }
            headers: Dict[str, str] = self.user_headers
        else:
            headers = self.headers
        
        try:
            response: requests.Response
            if method == "GET":
                response = requests.get(url, headers=headers, params=data)
            else:
                response = requests.post(url, headers=headers, json=data)
            
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "ok": False,
                "error": f"HTTP 요청 오류: {str(e)}"
            }
    
    def send_message(self, channel: str, text: str) -> Dict[str, Any]:
        """
        지정된 Slack 채널에 메시지를 전송합니다.
        
        Args:
            channel (str): 채널 ID 또는 채널명 (예: #general, C1234567890)
            text (str): 전송할 메시지 내용 (UTF-8 인코딩 한글 지원)
        
        Returns:
            Dict[str, Any]: API 응답 결과
        """
        data: Dict[str, str] = {
            "channel": channel,
            "text": text
        }
        
        result: Dict[str, Any] = self.make_request("chat.postMessage", method="POST", data=data)
        
        if result.get("ok"):
            return {
                "success": True,
                "message": "메시지가 성공적으로 전송되었습니다.",
                "timestamp": result.get("ts"),
                "channel": result.get("channel")
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "알 수 없는 오류가 발생했습니다."),
                "details": result
            }
    
    def get_channels(self) -> Dict[str, Any]:
        """
        접근 가능한 모든 Slack 채널 목록을 조회합니다.
        
        Returns:
            Dict[str, Any]: 채널 목록과 정보 (채널 ID, 이름, 공개/비공개 여부, 멤버십 상태)
        """
        # 공개 채널 조회
        public_channels: Dict[str, Any] = self.make_request(
            "conversations.list", 
            data={"types": "public_channel"}
        )
        
        # 비공개 채널 조회  
        private_channels: Dict[str, Any] = self.make_request(
            "conversations.list", 
            data={"types": "private_channel"}
        )
        
        channels: List[Dict[str, Any]] = []
        
        # 공개 채널 처리
        if public_channels.get("ok"):
            for channel in public_channels.get("channels", []):
                channels.append({
                    "id": channel["id"],
                    "name": channel["name"],
                    "is_private": False,
                    "is_member": channel.get("is_member", False),
                    "topic": channel.get("topic", {}).get("value", ""),
                    "purpose": channel.get("purpose", {}).get("value", "")
                })
        
        # 비공개 채널 처리
        if private_channels.get("ok"):
            for channel in private_channels.get("channels", []):
                channels.append({
                    "id": channel["id"],
                    "name": channel["name"],
                    "is_private": True,
                    "is_member": channel.get("is_member", False),
                    "topic": channel.get("topic", {}).get("value", ""),
                    "purpose": channel.get("purpose", {}).get("value", "")
                })
        
        return {
            "success": True,
            "total_channels": len(channels),
            "channels": channels
        }
    
    def get_channel_history(self, channel_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        지정된 채널의 최근 메시지 히스토리를 조회합니다.
        
        Args:
            channel_id (str): 조회할 채널의 ID
            limit (int): 조회할 메시지 수 (기본값: 10, 최대: 100)
        
        Returns:
            Dict[str, Any]: 메시지 히스토리 (메시지 내용, 작성자, 타임스탬프)
        """
        # limit 값 검증
        if limit > 100:
            limit = 100
        elif limit < 1:
            limit = 1
        
        data: Dict[str, Union[str, int]] = {
            "channel": channel_id,
            "limit": limit
        }
        
        result: Dict[str, Any] = self.make_request("conversations.history", data=data)
        
        if not result.get("ok"):
            return {
                "success": False,
                "error": result.get("error", "메시지 히스토리를 가져올 수 없습니다."),
                "details": result
            }
        
        messages: List[Dict[str, Any]] = []
        for msg in result.get("messages", []):
            # 사용자 정보 조회
            user_info: Optional[Dict[str, Any]] = None
            if msg.get("user"):
                user_response: Dict[str, Any] = self.make_request("users.info", data={"user": msg["user"]})
                if user_response.get("ok"):
                    user_info = user_response.get("user", {})
            
            message_data: Dict[str, Any] = {
                "text": msg.get("text", ""),
                "user_id": msg.get("user", ""),
                "user_name": user_info.get("real_name", "") if user_info else "",
                "timestamp": msg.get("ts", ""),
                "type": msg.get("type", ""),
                "subtype": msg.get("subtype", "")
            }
            
            # 스레드 정보가 있는 경우
            if msg.get("thread_ts"):
                message_data["is_thread_reply"] = True
                message_data["thread_timestamp"] = msg.get("thread_ts")
            
            messages.append(message_data)
        
        return {
            "success": True,
            "channel_id": channel_id,
            "message_count": len(messages),
            "messages": messages
        }
    
    def send_direct_message(self, user_id: str, text: str) -> Dict[str, Any]:
        """
        특정 사용자에게 1:1 다이렉트 메시지를 전송합니다.
        
        Args:
            user_id (str): 메시지를 받을 사용자의 ID
            text (str): 전송할 메시지 내용
        
        Returns:
            Dict[str, Any]: API 응답 결과
        """
        # DM 채널 열기
        dm_open_data: Dict[str, str] = {"users": user_id}
        dm_channel_result: Dict[str, Any] = self.make_request("conversations.open", method="POST", data=dm_open_data)
        
        if not dm_channel_result.get("ok"):
            return {
                "success": False,
                "error": f"DM 채널을 열 수 없습니다: {dm_channel_result.get('error', '알 수 없는 오류')}",
                "details": dm_channel_result
            }
        
        # DM 채널 ID 가져오기
        dm_channel_id: str = dm_channel_result.get("channel", {}).get("id", "")
        
        if not dm_channel_id:
            return {
                "success": False,
                "error": "DM 채널 ID를 가져올 수 없습니다.",
                "details": dm_channel_result
            }
        
        # 메시지 전송
        return self.send_message(dm_channel_id, text)
    
    def invite_user_to_channel(self, channel_id: str, user_id: str) -> Dict[str, Any]:
        """
        지정된 채널에 사용자를 초대합니다.
        
        Args:
            channel_id (str): 초대할 채널의 ID
            user_id (str): 초대할 사용자의 ID
        
        Returns:
            Dict[str, Any]: API 응답 결과
        """
        data: Dict[str, str] = {
            "channel": channel_id,
            "users": user_id
        }
        
        result: Dict[str, Any] = self.make_request("conversations.invite", method="POST", data=data)
        
        if result.get("ok"):
            return {
                "success": True,
                "message": "사용자가 성공적으로 채널에 초대되었습니다.",
                "channel": channel_id,
                "user": user_id
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "사용자 초대에 실패했습니다."),
                "details": result
            }
    
    def get_users(self) -> Dict[str, Any]:
        """
        워크스페이스의 모든 사용자 목록을 조회합니다.
        
        Returns:
            Dict[str, Any]: 사용자 목록과 정보 (사용자 ID, 이름, 이메일, 프로필 등)
        """
        result: Dict[str, Any] = self.make_request("users.list")
        
        if not result.get("ok"):
            return {
                "success": False,
                "error": result.get("error", "사용자 목록을 가져올 수 없습니다."),
                "details": result
            }
        
        users: List[Dict[str, Any]] = []
        for user in result.get("members", []):
            # 삭제된 사용자나 봇은 제외 (선택적)
            if user.get("deleted", False):
                continue
            
            user_data: Dict[str, Any] = {
                "id": user["id"],
                "name": user.get("name", ""),
                "real_name": user.get("real_name", ""),
                "display_name": user.get("profile", {}).get("display_name", ""),
                "email": user.get("profile", {}).get("email", ""),
                "is_bot": user.get("is_bot", False),
                "is_admin": user.get("is_admin", False),
                "is_owner": user.get("is_owner", False),
                "status": user.get("profile", {}).get("status_text", ""),
                "timezone": user.get("tz", ""),
                "image_url": user.get("profile", {}).get("image_72", "")
            }
            
            users.append(user_data)
        
        return {
            "success": True,
            "total_users": len(users),
            "users": users
        }
    
    def add_reaction(self, channel_id: str, timestamp: str, emoji: str = "jammies-frog") -> Dict[str, Any]:
        """
        특정 메시지에 이모지 반응을 추가합니다.
        
        Args:
            channel_id (str): 메시지가 있는 채널의 ID
            timestamp (str): 메시지의 타임스탬프 (ts)
            emoji (str): 추가할 이모지 이름 (기본값: "jammies-frog")
        
        Returns:
            Dict[str, Any]: API 응답 결과
        """
        data: Dict[str, str] = {
            "channel": channel_id,
            "timestamp": timestamp,
            "name": emoji
        }
        
        result: Dict[str, Any] = self.make_request("reactions.add", method="POST", data=data)
        
        if result.get("ok"):
            return {
                "success": True,
                "message": f"🐸 {emoji} 이모지 반응이 성공적으로 추가되었습니다!",
                "channel": channel_id,
                "timestamp": timestamp,
                "emoji": emoji
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "이모지 반응 추가에 실패했습니다."),
                "details": result
            }
    
    def search_messages(self, query: str, sort: str = "timestamp", count: int = 20) -> Dict[str, Any]:
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
        # count 값 검증
        if count > 100:
            count = 100
        elif count < 1:
            count = 1
        
        data: Dict[str, Union[str, int]] = {
            "query": query,
            "sort": sort,
            "count": count
        }
        
        result: Dict[str, Any] = self.make_request("search.messages", data=data, use_user_token=True)
        
        if not result.get("ok"):
            return {
                "success": False,
                "error": result.get("error", "메시지 검색에 실패했습니다."),
                "details": result
            }
        
        messages: List[Dict[str, Any]] = []
        search_results: Dict[str, Any] = result.get("messages", {})
        
        for match in search_results.get("matches", []):
            # 채널 정보 가져오기 (Bot Token 사용)
            channel_info: Optional[Dict[str, Any]] = None
            if match.get("channel", {}).get("id"):
                channel_response: Dict[str, Any] = self.make_request("conversations.info", 
                                                   data={"channel": match["channel"]["id"]})
                if channel_response.get("ok"):
                    channel_info = channel_response.get("channel", {})
            
            # 사용자 정보 가져오기 (Bot Token 사용)
            user_info: Optional[Dict[str, Any]] = None
            if match.get("user"):
                user_response: Dict[str, Any] = self.make_request("users.info", data={"user": match["user"]})
                if user_response.get("ok"):
                    user_info = user_response.get("user", {})
            
            message_data: Dict[str, Any] = {
                "text": match.get("text", ""),
                "user_id": match.get("user", ""),
                "user_name": user_info.get("real_name", "") if user_info else "",
                "channel_id": match.get("channel", {}).get("id", ""),
                "channel_name": channel_info.get("name", "") if channel_info else "",
                "timestamp": match.get("ts", ""),
                "permalink": match.get("permalink", ""),
                "score": match.get("score", 0)
            }
            
            messages.append(message_data)
        
        return {
            "success": True,
            "query": query,
            "total_results": search_results.get("total", 0),
            "message_count": len(messages),
            "messages": messages
        }
    
    def upload_file(
        self, 
        channels: str, 
        file_path: str, 
        title: str = "", 
        initial_comment: str = "", 
        filetype: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        채널에 파일을 업로드합니다 (레거시 API 방식).
        ⚠️ 이 방식은 deprecated되었습니다. upload_file_new를 사용하세요.
        
        Args:
            channels (str): 파일을 업로드할 채널 ID (쉼표로 구분하여 여러 채널 가능)
            file_path (str): 업로드할 파일의 경로
            title (str): 파일 제목 (선택사항)
            initial_comment (str): 파일과 함께 보낼 코멘트 (선택사항)
            filetype (Optional[str]): 파일 타입 (선택사항, 자동 감지됨)
        
        Returns:
            Dict[str, Any]: API 응답 결과
        """
        try:
            # 파일 존재 여부 확인
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"파일을 찾을 수 없습니다: {file_path}"
                }
            
            # 파일 타입 자동 감지
            if not filetype:
                guessed_type, _ = mimetypes.guess_type(file_path)
                filetype = guessed_type or "application/octet-stream"
            
            # 파일 업로드 요청
            url: str = f"{self.base_url}/files.upload"
            
            data: Dict[str, str] = {
                "channels": channels,
                "title": title,
                "initial_comment": initial_comment,
                "filetype": filetype
            }
            
            headers_without_content_type: Dict[str, str] = {
                "Authorization": f"Bearer {self.bot_token}"
            }
            
            with open(file_path, 'rb') as file_content:
                files: Dict[str, Tuple[str, BinaryIO, str]] = {
                    'file': (os.path.basename(file_path), file_content, filetype)
                }
                
                response: requests.Response = requests.post(
                    url, 
                    headers=headers_without_content_type, 
                    data=data, 
                    files=files
                )
                result: Dict[str, Any] = response.json()
            
            if result.get("ok"):
                return {
                    "success": True,
                    "message": "파일이 성공적으로 업로드되었습니다. (레거시 API)",
                    "file_id": result.get("file", {}).get("id"),
                    "file_url": result.get("file", {}).get("url_private"),
                    "channels": channels
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "파일 업로드에 실패했습니다."),
                    "details": result
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"파일 업로드 중 오류가 발생했습니다: {str(e)}"
            }
    
    def upload_file_new(
        self, 
        channels: str, 
        file_path: str, 
        title: str = "", 
        initial_comment: str = "", 
        filetype: Optional[str] = None
    ) -> Dict[str, Any]:
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
        try:
            # 파일 존재 여부 확인
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"파일을 찾을 수 없습니다: {file_path}"
                }
            
            # 파일 정보 가져오기
            file_size: int = os.path.getsize(file_path)
            filename: str = os.path.basename(file_path)
            
            # 파일 타입 자동 감지
            if not filetype:
                guessed_type, _ = mimetypes.guess_type(file_path)
                filetype = guessed_type or "application/octet-stream"
            
            # 1단계: 업로드 URL 가져오기
            upload_url_data: Dict[str, Union[str, int]] = {
                "filename": filename,
                "length": file_size
            }
            
            upload_url_result: Dict[str, Any] = self.make_request(
                "files.getUploadURLExternal", 
                method="POST", 
                data=upload_url_data
            )
            
            if not upload_url_result.get("ok"):
                return {
                    "success": False,
                    "error": "업로드 URL을 가져올 수 없습니다.",
                    "details": upload_url_result
                }
            
            upload_url: str = upload_url_result.get("upload_url", "")
            file_id: str = upload_url_result.get("file_id", "")
            
            # 2단계: 파일 업로드
            with open(file_path, 'rb') as file_content:
                upload_response: requests.Response = requests.post(upload_url, files={'file': file_content})
                
                if upload_response.status_code != 200:
                    return {
                        "success": False,
                        "error": f"파일 업로드 실패: HTTP {upload_response.status_code}"
                    }
            
            # 3단계: 업로드 완료 및 채널에 공유
            complete_data: Dict[str, str] = {
                "files": file_id,
                "channels": channels,
                "title": title,
                "initial_comment": initial_comment
            }
            
            complete_result: Dict[str, Any] = self.make_request(
                "files.completeUploadExternal", 
                method="POST", 
                data=complete_data
            )
            
            if complete_result.get("ok"):
                return {
                    "success": True,
                    "message": "파일이 성공적으로 업로드되었습니다. (새로운 API)",
                    "file_id": file_id,
                    "channels": channels,
                    "filename": filename,
                    "file_size": file_size
                }
            else:
                return {
                    "success": False,
                    "error": complete_result.get("error", "파일 업로드 완료에 실패했습니다."),
                    "details": complete_result
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"새로운 API 파일 업로드 중 오류가 발생했습니다: {str(e)}"
            } 