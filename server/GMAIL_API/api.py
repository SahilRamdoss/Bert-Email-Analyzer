from services.nlp_preprocessor import EmailPreprocessor
from services.emails_extractor import EmailExtractor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
from services.model import Model
import copy
import time

# Get the secrets
load_dotenv()
SCOPES = [os.getenv("GMAIL_SCOPE")]
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "token.json")

# Path to AI Model
MODEL_PATH = "models/trained_model"

# Initialise our model class
model = Model(MODEL_PATH)

# Get email extractor object
email_extractor = EmailExtractor(TOKEN_PATH, SCOPES)

# Create preprocessor object
email_preprocessor = EmailPreprocessor()

app = FastAPI()

# Using CORS to prevent illegal api calls
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def main():

    start = time.perf_counter()

    # Get the unread emails from the user's inbox
    raw_emails = (email_extractor.get_unread_emails())["emails"]

    if (len(raw_emails) == 0):
        return list()

    end = time.perf_counter()

    print(f"\nTook {end - start:.3f} seconds to load emails")

    start = time.perf_counter()

    # Preprocess the emails before feeding the AI
    preprocessed_emails = email_preprocessor.preprocess_emails(copy.deepcopy(raw_emails))

    end = time.perf_counter()

    print(f"\nTook {end - start:.3f} seconds to preprocess emails")

    # Concatenate email subject and body for each email before passing them to the model
    model_input = [email["subject"] + " " + email["body"] for email in preprocessed_emails]

    start = time.perf_counter()

    # Make predictions with our model
    predictions = model.predict(model_input)

    end = time.perf_counter()

    print(f"\nTook {end - start:.3f} seconds to predict email urgency")

    for index in range(len(raw_emails)):
        raw_emails[index]["urgency"] = predictions[index]

    start = time.perf_counter()

    # Sort the emails based on urgency
    raw_emails.sort(key=lambda e: e["urgency"], reverse=True)

    # Normalize emails with html bodies
    raw_emails = email_preprocessor.normalize_email_body(raw_emails)

    end = time.perf_counter()

    print(f"\nTook {end - start:.3f} seconds to sort and normalize emails email urgency")

    return raw_emails
