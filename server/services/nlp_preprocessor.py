import html2text
import ftfy
import unicodedata
from email_reply_parser import EmailReplyParser
import re
import quopri
from bs4 import BeautifulSoup

URGENCY_CHARACTERS = [
    "!",
    "?",
    "*",
    "-"
]

DISCLAIMER_PATTERNS = [
r'\bthis email and any attachments are confidential\b',
r'\bthis message is intended only for\b',
r'\bthe information contained in this email\b',
r'\bconfidentiality notice\b',
r'\bimportant notice\b',
r'\bdisclaimer\b.*$'
]

SIGNATURE_PATTERNS = [
    r'\\-- +',
    r'\\__+',
    r'\\-- ?',
    r'\bKind regards,',
    r'\bBest regards,'
]

FORWARDED_AND_REPLIES_PATTERNS = [
    r'-+ ?Forward.*',
    r'-+ ?Original Message.*'
]

DISCLAIMER_REGEX = [
    re.compile(pattern, re.IGNORECASE | re.DOTALL)
    for pattern in DISCLAIMER_PATTERNS
]

SIGNATURE_REGEX = [
    re.compile(pattern, re.IGNORECASE) 
    for pattern in SIGNATURE_PATTERNS
]

FORWARDED_AND_REPLIES_REGEX = [
    re.compile(pattern,flags=re.IGNORECASE) 
    for pattern in FORWARDED_AND_REPLIES_PATTERNS
]

EMAIL_PATTERN = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
URL_PATTERN = r'https?://\S+|www\.\S+'


class EmailPreprocessor:

    def __init__(self):
        self._html_cleaner = html2text.HTML2Text()
        self._html_cleaner.ignore_links = True
        self._html_cleaner.ignore_tables = True
        self._html_cleaner.ignore_images = True
        self._html_cleaner.body_width = 0

    def normalize_email_body(self, emails):
        for email in emails:
            if email["body"]["preferred"] == "text/html":
                soup = BeautifulSoup(email["body"]["html"], "html.parser")

                if soup.body:
                    email["body"]["html"] = soup.body.decode_contents()

            if email["body"]["text"] is None:
                soup = BeautifulSoup(email["body"]["html"], "html.parser")

                email["body"]["text"] = soup.get_text()

        return emails

    def _html_cleanup(self, emails):     
        for email in emails:
            preferred_content_type = email["body"]["preferred"]

            cleaned_email_content = ""

            if preferred_content_type == "text/html":
                email_content = email["body"]["html"]
                cleaned_email_content = self._html_cleaner.handle(email_content)

            elif preferred_content_type == "text/plain":
                cleaned_email_content = email["body"]["text"]
            else:
                cleaned_email_content = ""

            # email["urgency"] = email["body"]["urgency"]
            email["body"] = cleaned_email_content

        return emails

    def _clean_whitespace_printable_and_unicode(self, text: str) -> str:
        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cf')
        text = re.sub(r'[\u00A0\u2000-\u200B\u202F\u205F\u3000\u003C\u003E]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        # 1. Convert the string to bytes (usually 'ascii' or 'utf-8' for QP)
        text_bytes = text.encode("utf-8")
        
        # 2. Decode the Quoted-Printable encoding
        decoded_bytes = quopri.decodestring(text_bytes)
        
        # 3. Convert back to a clean utf-8 string
        text = decoded_bytes.decode("utf-8", errors="replace")

        # Fix broken other Quoted-Printable encoding
        text = re.sub(r'= ', '', text)
        text = re.sub(r'\t', ' ', text)

        return text.strip()

    def _unicode_and_mojibake_fix(self, emails):

        for email in emails:
            # fixed_subject = ftfy.fix_text(email["subject"].encode('utf-8').decode('unicode_escape'))
            fixed_subject = ftfy.fix_text(email["subject"])
            fixed_body = ftfy.fix_text(email["body"])

            unicode_normalised_subject = unicodedata.normalize("NFC", fixed_subject)
            unicode_normalised_body = unicodedata.normalize("NFC", fixed_body)

            email['subject'] = self._clean_whitespace_printable_and_unicode(unicode_normalised_subject)
            email['body'] = self._clean_whitespace_printable_and_unicode(unicode_normalised_body)

        return emails
    
    def _remove_forwarded_messages_and_replies(self, content):

        for regex in FORWARDED_AND_REPLIES_REGEX:
            forward_or_reply = regex.search(content)

            if forward_or_reply:
                return content[:forward_or_reply.start()].strip()
            
        return content.strip()

    def _remove_quoted_replies(self,emails):
        for email in emails:
            body = EmailReplyParser.parse_reply(email["body"])

            # Remove trailing separator line if it exists
            lines = body.strip().splitlines()
            if lines and lines[-1].startswith("On ") and " wrote:" in lines[-1]:
                lines = lines[:-1]

            email["body"] = "\n".join(lines)

            # For forwarded messages and replies, keep only new text
            email["body"] = self._remove_forwarded_messages_and_replies(email["body"])

        return emails

    def _strip_signature(self, content: str) -> str:
        content_lower = content.lower()

        cutoff_point = int(len(content_lower) * 0.6)

        content_tail = content_lower[cutoff_point:]

        for regex in SIGNATURE_REGEX:
            signature = regex.search(content_tail)

            if signature:
                return content[:(cutoff_point + signature.start())].strip() 

        return content.strip()

    def _strip_disclaimer(self, content: str) -> str:
        content_lower = content.lower()

        cutoff_point = int(len(content_lower) * 0.6)

        content_tail = content_lower[cutoff_point:]

        for regex in DISCLAIMER_REGEX:
            disclaimer = regex.search(content_tail)

            if disclaimer:
                return content[:(cutoff_point + disclaimer.start())].strip()
            
        return content.strip()

    def _strip_signatures_and_disclaimers(self, emails):   

        for email in emails:
            email["body"] = self._strip_signature(email["body"])
            email['body'] = self._strip_disclaimer(email['body'])

        return emails

    def _normalize_emails_and_urls(self,emails):

        for email in emails:
            # Normalizing emails
            email['body'] = re.sub(EMAIL_PATTERN, 'EMAIL', email['body'])

            # Normalizing urls
            email['body'] = re.sub(URL_PATTERN, 'URL', email['body'])

        return emails

    def _collapse_repeated_characters(self,emails):
        collapse_characters_regex = r'([a-zA-Z=_~•?!*-])\1{2,}'

        def replace_character(match):
            character = match.group(1)

            if character.isalpha() or (character in URGENCY_CHARACTERS):
                return character * 2
            else:
                return ""

        for email in emails:
            email['body'] = re.sub(collapse_characters_regex, replace_character , email['body'])

        return emails

    def preprocess_emails(self,raw_emails):
        # Convert all HTML content to plaintext
        html_cleaned_emails = self._html_cleanup(raw_emails)

        # Remove quoted replies
        unquoted_emails = self._remove_quoted_replies(html_cleaned_emails)

        # Fixing and normalizing Unicode, smart quotes, unnecessary spaces and mojibake
        unicode_mojibake_fixed_emails = self._unicode_and_mojibake_fix(unquoted_emails)

        # Remove email signatures and disclaimers
        stripped_emails = self._strip_signatures_and_disclaimers(unicode_mojibake_fixed_emails)

        # Normalize emails and urls
        email_and_url_normalized_emails = self._normalize_emails_and_urls(stripped_emails)

        # Collapse repeated alphabetic characters
        collapsed_emails = self._collapse_repeated_characters(email_and_url_normalized_emails)

        return collapsed_emails