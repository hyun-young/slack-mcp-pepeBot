import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv(".env")


class SlackAPIClient:
    """Slack API와 상호작용하기 위한 클라이언트 클래스"""
    
    def __init__(self):
        """SlackAPIClient 초기화"""
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.user_token = os.getenv("SLACK_USER_TOKEN")
        
        if not self.bot_token:
            raise ValueError("SLACK_BOT_TOKEN 환경변수가 설정되지 않았습니다.")
        
        self.base_url = "https://slack.com/api"
        
        # Bot Token용 헤더 (기본)
        self.headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        # User Token용 헤더 (검색 기능용)
        self.user_headers = None
        if self.user_token:
            self.user_headers = {
                "Authorization": f"Bearer {self.user_token}",
                "Content-Type": "application/json"
            }
    
    def make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None, use_user_token: bool = False) -> Dict:
        """
        Slack API 요청을 위한 헬퍼 메서드
        
        Args:
            endpoint: API 엔드포인트
            method: HTTP 메서드 (GET 또는 POST)
            data: 요청 데이터
            use_user_token: User Token 사용 여부 (검색 기능용)
        
        Returns:
            Dict: API 응답 결과
        """
        url = f"{self.base_url}/{endpoint}"
        
        # User Token 사용 시
        if use_user_token:
            if not self.user_headers:
                return {
                    "ok": False,
                    "error": "SLACK_USER_TOKEN 환경변수가 설정되지 않았습니다."
                }
            headers = self.user_headers
        else:
            headers = self.headers
        
        try:
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
    
    def send_message(self, channel: str, text: str) -> Dict:
        """
        지정된 Slack 채널에 메시지를 전송합니다.
        
        Args:
            channel: 채널 ID 또는 채널명 (예: #general, C1234567890)
            text: 전송할 메시지 내용 (UTF-8 인코딩 한글 지원)
        
        Returns:
            Dict: API 응답 결과
        """
        data = {
            "channel": channel,
            "text": text
        }
        
        result = self.make_request("chat.postMessage", method="POST", data=data)
        
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
    
    def get_channels(self) -> Dict:
        """
        접근 가능한 모든 Slack 채널 목록을 조회합니다.
        
        Returns:
            Dict: 채널 목록과 정보 (채널 ID, 이름, 공개/비공개 여부, 멤버십 상태)
        """
        # 공개 채널 조회
        public_channels = self.make_request("conversations.list", data={"types": "public_channel"})
        
        # 비공개 채널 조회  
        private_channels = self.make_request("conversations.list", data={"types": "private_channel"})
        
        channels = []
        
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
    
    def get_channel_history(self, channel_id: str, limit: int = 10) -> Dict:
        """
        지정된 채널의 최근 메시지 히스토리를 조회합니다.
        
        Args:
            channel_id: 조회할 채널의 ID
            limit: 조회할 메시지 수 (기본값: 10, 최대: 100)
        
        Returns:
            Dict: 메시지 히스토리 (메시지 내용, 작성자, 타임스탬프)
        """
        # limit 값 검증
        if limit > 100:
            limit = 100
        elif limit < 1:
            limit = 1
        
        data = {
            "channel": channel_id,
            "limit": limit
        }
        
        result = self.make_request("conversations.history", data=data)
        
        if not result.get("ok"):
            return {
                "success": False,
                "error": result.get("error", "메시지 히스토리를 가져올 수 없습니다."),
                "details": result
            }
        
        messages = []
        for msg in result.get("messages", []):
            # 사용자 정보 조회
            user_info = None
            if msg.get("user"):
                user_response = self.make_request("users.info", data={"user": msg["user"]})
                if user_response.get("ok"):
                    user_info = user_response.get("user", {})
            
            message_data = {
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
    
    def send_direct_message(self, user_id: str, text: str) -> Dict:
        """
        특정 사용자에게 1:1 다이렉트 메시지를 전송합니다.
        
        Args:
            user_id: 메시지를 받을 사용자의 ID
            text: 전송할 메시지 내용
        
        Returns:
            Dict: API 응답 결과
        """
        # DM 채널 열기
        dm_open_result = self.make_request("conversations.open", method="POST", data={"users": user_id})
        
        if not dm_open_result.get("ok"):
            return {
                "success": False,
                "error": f"DM 채널을 열 수 없습니다: {dm_open_result.get('error', '알 수 없는 오류')}",
                "details": dm_open_result
            }
        
        # DM 채널 ID 가져오기
        dm_channel_id = dm_open_result.get("channel", {}).get("id")
        
        if not dm_channel_id:
            return {
                "success": False,
                "error": "DM 채널 ID를 가져올 수 없습니다.",
                "details": dm_open_result
            }
        
        # 메시지 전송
        data = {
            "channel": dm_channel_id,
            "text": text
        }
        
        result = self.make_request("chat.postMessage", method="POST", data=data)
        
        if result.get("ok"):
            return {
                "success": True,
                "message": "다이렉트 메시지가 성공적으로 전송되었습니다.",
                "timestamp": result.get("ts"),
                "channel": result.get("channel"),
                "user_id": user_id
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "메시지 전송에 실패했습니다."),
                "details": result
            }
    
    def invite_user_to_channel(self, channel_id: str, user_id: str) -> Dict:
        """
        지정된 채널에 사용자를 초대합니다.
        
        Args:
            channel_id: 초대할 채널의 ID
            user_id: 초대할 사용자의 ID
        
        Returns:
            Dict: API 응답 결과
        """
        data = {
            "channel": channel_id,
            "users": user_id
        }
        
        result = self.make_request("conversations.invite", method="POST", data=data)
        
        if result.get("ok"):
            return {
                "success": True,
                "message": "사용자가 성공적으로 채널에 초대되었습니다.",
                "channel": result.get("channel", {}).get("id"),
                "channel_name": result.get("channel", {}).get("name")
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "채널 초대에 실패했습니다."),
                "details": result
            }
    
    def get_users(self) -> Dict:
        """
        워크스페이스의 모든 사용자 목록을 조회합니다.
        
        Returns:
            Dict: 사용자 목록과 정보 (사용자 ID, 이름, 이메일, 프로필 등)
        """
        result = self.make_request("users.list")
        
        if not result.get("ok"):
            return {
                "success": False,
                "error": result.get("error", "사용자 목록을 가져올 수 없습니다."),
                "details": result
            }
        
        users = []
        for user in result.get("members", []):
            # 삭제된 사용자나 봇은 제외 (선택적)
            if user.get("deleted", False):
                continue
            
            user_data = {
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
    
    def add_reaction(self, channel_id: str, timestamp: str) -> Dict:
        """
        특정 메시지에 jammies-frog 이모지 반응을 추가합니다.
        
        Args:
            channel_id: 메시지가 있는 채널의 ID
            timestamp: 메시지의 타임스탬프 (ts)
        
        Returns:
            Dict: API 응답 결과
        """
        # 고정된 jammies-frog 이모지 사용
        reaction = "jammies-frog"
        
        data = {
            "channel": channel_id,
            "timestamp": timestamp,
            "name": reaction
        }
        
        result = self.make_request("reactions.add", method="POST", data=data)
        
        if result.get("ok"):
            return {
                "success": True,
                "message": f"🐸 '{reaction}' 반응이 성공적으로 추가되었습니다!",
                "reaction": reaction,
                "channel": channel_id,
                "timestamp": timestamp
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "반응 추가에 실패했습니다."),
                "details": result
            }
    
    def search_messages(self, query: str, sort: str = "timestamp", count: int = 20) -> Dict:
        """
        키워드를 통해 워크스페이스의 메시지를 검색합니다.
        ⚠️ 이 기능은 User Token (SLACK_USER_TOKEN)이 필요합니다.
        
        Args:
            query: 검색할 키워드
            sort: 정렬 방식 ("timestamp", "score") 기본값: "timestamp"
            count: 검색할 메시지 수 (기본값: 20, 최대: 100)
        
        Returns:
            Dict: 검색 결과 (메시지 내용, 채널, 작성자 등)
        """
        # count 값 검증
        if count > 100:
            count = 100
        elif count < 1:
            count = 1
            
        data = {
            "query": query,
            "sort": sort,
            "count": count
        }
        
        # User Token을 사용하여 검색 API 호출
        result = self.make_request("search.messages", data=data, use_user_token=True)
        
        if not result.get("ok"):
            return {
                "success": False,
                "error": result.get("error", "메시지 검색에 실패했습니다."),
                "details": result
            }
        
        messages = []
        search_results = result.get("messages", {})
        
        for match in search_results.get("matches", []):
            # 채널 정보 가져오기 (Bot Token 사용)
            channel_info = None
            if match.get("channel", {}).get("id"):
                channel_response = self.make_request("conversations.info", 
                                                   data={"channel": match["channel"]["id"]})
                if channel_response.get("ok"):
                    channel_info = channel_response.get("channel", {})
            
            # 사용자 정보 가져오기 (Bot Token 사용)
            user_info = None
            if match.get("user"):
                user_response = self.make_request("users.info", data={"user": match["user"]})
                if user_response.get("ok"):
                    user_info = user_response.get("user", {})
            
            message_data = {
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
    
    def upload_file(self, channels: str, file_path: str, title: str = "", 
                   initial_comment: str = "", filetype: str = None) -> Dict:
        """
        채널에 파일을 업로드합니다.
        
        Args:
            channels: 파일을 업로드할 채널 ID (쉼표로 구분하여 여러 채널 가능)
            file_path: 업로드할 파일의 경로
            title: 파일 제목 (선택사항)
            initial_comment: 파일과 함께 보낼 코멘트 (선택사항)
            filetype: 파일 타입 (선택사항, 자동 감지됨)
        
        Returns:
            Dict: API 응답 결과
        """
        import os
        
        # 파일 존재 확인
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"파일을 찾을 수 없습니다: {file_path}"
            }
        
        # 파일 크기 확인 (Slack 제한: 1GB)
        file_size = os.path.getsize(file_path)
        if file_size > 1024 * 1024 * 1024:  # 1GB
            return {
                "success": False,
                "error": "파일 크기가 1GB를 초과합니다."
            }
        
        # 파일명 추출
        filename = os.path.basename(file_path)
        if not title:
            title = filename
        
        try:
            import requests
            
            # 파일 업로드 요청
            url = f"{self.base_url}/files.upload"
            
            data = {
                "channels": channels,
                "title": title,
                "initial_comment": initial_comment
            }
            
            if filetype:
                data["filetype"] = filetype
            
            files = {
                "file": (filename, open(file_path, "rb"))
            }
            
            response = requests.post(
                url,
                headers={"Authorization": f"Bearer {self.bot_token}"},
                data=data,
                files=files
            )
            
            # 파일 닫기
            files["file"][1].close()
            
            result = response.json()
            
            if result.get("ok"):
                file_info = result.get("file", {})
                return {
                    "success": True,
                    "message": "파일이 성공적으로 업로드되었습니다.",
                    "file_id": file_info.get("id"),
                    "file_name": file_info.get("name"),
                    "file_size": file_info.get("size"),
                    "file_type": file_info.get("filetype"),
                    "download_url": file_info.get("url_private"),
                    "permalink": file_info.get("permalink")
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
    
    def upload_file_new(self, channels: str, file_path: str, title: str = "", 
                       initial_comment: str = "", filetype: str = None) -> Dict:
        """
        새로운 Slack 파일 업로드 API를 사용하여 채널에 파일을 업로드합니다.
        (files.getUploadURLExternal + files.completeUploadExternal)
        
        Args:
            channels: 파일을 업로드할 채널 ID (쉼표로 구분하여 여러 채널 가능)
            file_path: 업로드할 파일의 경로
            title: 파일 제목 (선택사항)
            initial_comment: 파일과 함께 보낼 코멘트 (선택사항)
            filetype: 파일 타입 (선택사항, 자동 감지됨)
        
        Returns:
            Dict: API 응답 결과
        """
        import os
        import requests
        
        # 파일 존재 확인
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"파일을 찾을 수 없습니다: {file_path}"
            }
        
        # 파일 크기 확인 (Slack 제한: 1GB)
        file_size = os.path.getsize(file_path)
        if file_size > 1024 * 1024 * 1024:  # 1GB
            return {
                "success": False,
                "error": "파일 크기가 1GB를 초과합니다."
            }
        
        # 파일명 추출
        filename = os.path.basename(file_path)
        if not title:
            title = filename
        
        try:
            # 1단계: 업로드 URL 요청
            upload_url_data = {
                "filename": filename,
                "length": file_size
            }
            
            if filetype:
                upload_url_data["filetype"] = filetype
            
            upload_url_result = self.make_request("files.getUploadURLExternal", 
                                                method="GET",  # GET 방식으로 변경
                                                data=upload_url_data)
            
            if not upload_url_result.get("ok"):
                return {
                    "success": False,
                    "error": f"업로드 URL 요청 실패: {upload_url_result.get('error')}",
                    "details": upload_url_result
                }
            
            upload_url = upload_url_result.get("upload_url")
            file_id = upload_url_result.get("file_id")
            
            # 2단계: 파일 업로드
            with open(file_path, "rb") as file_data:
                upload_response = requests.post(upload_url, files={"file": file_data})
            
            if upload_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"파일 업로드 실패: HTTP {upload_response.status_code}"
                }
            
            # 3단계: 업로드 완료 및 채널에 공유
            complete_data = {
                "files": [
                    {
                        "id": file_id,
                        "title": title
                    }
                ],
                "channel_id": channels,
                "initial_comment": initial_comment
            }
            
            complete_result = self.make_request("files.completeUploadExternal", 
                                              method="POST", 
                                              data=complete_data)
            
            if complete_result.get("ok"):
                files_info = complete_result.get("files", [])
                if files_info:
                    file_info = files_info[0]
                    return {
                        "success": True,
                        "message": "파일이 성공적으로 업로드되었습니다.",
                        "file_id": file_info.get("id"),
                        "file_name": file_info.get("name"),
                        "file_size": file_info.get("size"),
                        "file_type": file_info.get("filetype"),
                        "download_url": file_info.get("url_private"),
                        "permalink": file_info.get("permalink")
                    }
                else:
                    return {
                        "success": True,
                        "message": "파일 업로드 완료 (파일 정보 없음)",
                        "file_id": file_id
                    }
            else:
                return {
                    "success": False,
                    "error": f"업로드 완료 실패: {complete_result.get('error')}",
                    "details": complete_result
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"새로운 파일 업로드 중 오류가 발생했습니다: {str(e)}"
            } 