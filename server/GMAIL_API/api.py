from services.nlp_preprocessor import EmailPreprocessor
from services.emails_extractor import EmailExtractor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
from services.model import Model
import copy

app = FastAPI()

# Using CORS to prevent illegal api calls
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Get the secrets
load_dotenv()
SCOPES = [os.getenv("GMAIL_SCOPE")]
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "token.json")

# Path to AI Model
MODEL_PATH = "models/trained_model"

@app.get('/')
def main():
    # Get email extractor object
    email_extractor = EmailExtractor(TOKEN_PATH, SCOPES)

    # Create preprocessor object
    email_preprocessor = EmailPreprocessor()

    # Get the unread emails from the user's inbox
    raw_emails = (email_extractor.get_unread_emails())["emails"]

    # Preprocess the emails before feeding the AI
    preprocessed_emails = email_preprocessor.preprocess_emails(copy.deepcopy(raw_emails))

    # Concatenate email subject and body for each email before passing them to the model
    model_input = [email["subject"] + " " + email["body"] for email in preprocessed_emails]

    # Initialise our model class
    model = Model(MODEL_PATH)

    # Make predictions with our model
    predictions = model.predict(model_input)

    for index in range(len(raw_emails)):
        raw_emails[index]["urgency"] = predictions[index]

    # Sort the emails based on urgency
    raw_emails.sort(key=lambda e: e["urgency"], reverse=True)

    # Normalize emails with html bodies
    raw_emails = email_preprocessor.normalize_email_body(raw_emails)

    return raw_emails

    # with open("data/emails_json_val_data.json", "r", encoding="utf-8") as file:
    #     data = json.load(file)

    # preprocessed_emails = email_preprocessor.preprocess_emails(data)

    # with open("data/preprocessed_emails_json_val_data.json", "w", encoding="utf-8") as file:
    #     json.dump(preprocessed_emails, file, indent=4)

    # For training logic

    # training_data = list()

    # for email in preprocessed_emails:

    #     if email['body'] and not('HTML' in email['body']):
    #         training_data.append(email)
