import pandas as pd
import re
import json

enron_emails = pd.read_csv("data/emails.csv")

message_list_one = (enron_emails.sample(2000)).iloc[:,1]
message_list_two = enron_emails.iloc[0:2,1]

SUBJECT_REGEX = re.compile(r'\bSubject:.*')
START_OF_BODY_REGEX = re.compile(r'\bX-FileName:.*')

emails_json = list()

for message in message_list_one:
    subject_line = (re.findall(SUBJECT_REGEX, message))[0]
    subject = (subject_line[8:]).strip()

    start_of_body_index = (re.search(START_OF_BODY_REGEX, message)).end()
    body = (message[start_of_body_index:]).strip()

    emails_json.append(
        {
            "subject": subject,
            "body": {
                "html": None,
                "text": body,
                "preferred": "text/plain",
                "urgency": None
            }
        }
    )

try:
    with open("data/emails_json_data.json", "w", encoding="utf-8") as file:
        json.dump(emails_json, file, indent=2)
except:
    raise Exception("Exception: {e}")
