from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64


class EmailExtractor:

    def __init__(self, token_path, scope):
        self._token_path = token_path
        self._scope = scope

    def get_email_service(self):
        creds = Credentials.from_authorized_user_file(self._token_path, self._scope)
        return build("gmail", "v1", credentials=creds)

    def extract_body(self,payload):
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

    def get_unread_emails(self):
        service = self.get_email_service()

        results = service.users().messages().list(
            userId="me",
            q="is:unread"
        ).execute()

        messages = results.get("messages", [])

        emails_data = []

        for msg in messages:
            msg_data = service.users().messages().get(
                userId="me", id=msg["id"], format="full"
            ).execute()

            headers = msg_data["payload"]["headers"]
            
            id = msg["id"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), None)
            sender = next((h["value"] for h in headers if h["name"] == "From"), None)
            receiver = next((h["value"] for h in headers if h["name"] == "To"), None)
            date = next((h["value"] for h in headers if h["name"] == "Date"), None)
            cc = next((h["value"] for h in headers if h["name"] == "Cc"), None)
            body = self.extract_body(msg_data["payload"])
            
            emails_data.append(
                {
                    "id": id,
                    "subject": subject,
                    "sender": sender,
                    "receiver": receiver,
                    "cc": cc, 
                    "date": date,
                    "body": body
                }
            )

        return {
            "emails": emails_data,
        }