from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64


class EmailExtractor:

    def __init__(self, token_path, scope):
        self._token_path = token_path
        self._scope = scope

    def _get_email_service(self):
        creds = Credentials.from_authorized_user_file(self._token_path, self._scope)
        return build("gmail", "v1", credentials=creds)

    def _extract_body(self,payload):
        html_parts = []
        text_parts = []

        def walk(part):
            mime = part.get("mimeType")
            body = part.get("body", {})

            # Ignore attachments explicitly
            if body.get("attachmentId"):
                return

            if mime in ("text/html", "text/plain"):
                data = body.get("data")
                if data:
                    decoded = base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="replace"
                    )

                    if mime == "text/html":
                        html_parts.append(decoded)
                    else:
                        text_parts.append(decoded)

            for subpart in part.get("parts", []):
                walk(subpart)

        walk(payload)

        html = "\n".join(html_parts) if html_parts else None
        text = "\n".join(text_parts) if text_parts else None

        return {
            "html": html,
            "text": text,
            "preferred": "text/html" if html else "text/plain" if text else None
        }

    def _get_gmail_account_email(self):
        service = self._get_email_service()
        profile = service.users().getProfile(userId="me").execute()
        return profile["emailAddress"]  
    
    def get_unread_emails(self):
        service = self._get_email_service()

        results = service.users().messages().list(
            userId="me",
            q="is:unread"
        ).execute()

        message_ids = [m["id"] for m in results.get("messages", [])]
        user_email = self._get_gmail_account_email()
        emails_data = []

        def batch_callback(request_id, response, exception):
            if exception:
                return

            headers = response["payload"]["headers"]

            emails_data.append({
                "id": request_id,
                "user": user_email,
                "subject": next((h["value"] for h in headers if h["name"] == "Subject"), None),
                "sender": next((h["value"] for h in headers if h["name"] == "From"), None),
                "receiver": next((h["value"] for h in headers if h["name"] == "To"), None),
                "cc": next((h["value"] for h in headers if h["name"] == "Cc"), None),
                "date": next((h["value"] for h in headers if h["name"] == "Date"), None),
                "body": self._extract_body(response["payload"])
            })

        BATCH_SIZE = 50

        for i in range(0, len(message_ids), BATCH_SIZE):
            batch = service.new_batch_http_request(callback=batch_callback)

            for msg_id in message_ids[i:i + BATCH_SIZE]:
                batch.add(
                    service.users().messages().get(
                        userId="me",
                        id=msg_id,
                        format="full"
                    ),
                    request_id=msg_id
                )

            batch.execute()

        return {"emails": emails_data}
