# AI Email Urgency Analyzer

An end-to-end Natural Language Processing (NLP) system that analyzes emails from a Gmail inbox and automatically prioritizes them by urgency using a fine-tuned Transformer model.

The system combines:

- A fine-tuned **DeBERTa-v3-base** transformer model
- A custom email preprocessing pipeline
- A FastAPI backend
- Gmail API integration
- A React frontend

The goal is to reduce information overload by automatically identifying which emails require immediate attention.

---

## Features

- 📧 Fetch emails directly from Gmail
- 🧠 AI-powered urgency detection
- 📊 Classify emails into multiple urgency levels
- 🧹 Advanced email preprocessing pipeline
- ⚡ Batch inference for improved performance
- 🔄 Automatic email prioritization
- 🌐 RESTful API architecture
- 🎨 Modern React frontend

---

## Results

| Metric | Score |
|---------|--------|
| Accuracy | 98% |
| F1 Score | 98% |
| Model | DeBERTa-v3-base |
| Framework | PyTorch + HuggingFace |

---

## Key Technical Achievements

### Transformer Fine-Tuning

- Fine-tuned a DeBERTa-v3-base transformer model
- Achieved **98% F1-score**
- Implemented transfer learning using the HuggingFace ecosystem
- Optimized training and validation pipelines

---

### Email Preprocessing Pipeline

Designed a custom preprocessing pipeline to maximize semantic signal while minimizing noise.

Pipeline stages include:

- HTML to text conversion
- Unicode repair
- Text normalization
- Email thread removal
- Signature removal
- Disclaimer removal
- URL normalization
- Character normalization

---

### Backend Engineering

Developed RESTful APIs using FastAPI to:

- Authenticate with Gmail
- Retrieve emails
- Normalize email formats
- Perform batch inference
- Return ranked email priorities

---

## Tech Stack

### Machine Learning

- PyTorch
- HuggingFace Transformers
- DeBERTa-v3-base

### Backend

- FastAPI
- Gmail API
- BeautifulSoup

### Frontend

- React
- Vite
- TailwindCSS
- DOMPurify

### NLP Libraries

- html2text
- ftfy
- email-reply-parser
- regex
- unicodedata

---

## Installation

### Frontend

Navigate to the frontend directory:

```bash
cd client
```

Install dependencies:

```bash
npm install
npm install react-router-dom
```

Run the frontend:

```bash
npm run dev
```

---

### Backend

Navigate to the backend directory:

```bash
cd server
```

Install PyTorch following the official documentation:

https://pytorch.org/get-started/locally/

Install remaining dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
fastapi dev GMAIL_API/api.py
```

---

## Gmail Authentication

Enable the Gmail API in the Google Cloud Console.

Then authenticate your Gmail account:

```bash
python gmail_auth.py
```

This will generate the token required for accessing your inbox.

---

## Model Availability

> [!NOTE]
> The trained model weights are not included in this repository.
>
> Users are free to train their own models and load them into the application.

---

# Engineering Notes

---

## Why Email Urgency Detection is an NLP Problem

This project is fundamentally a supervised Natural Language Processing classification problem.

The objective is not to perform reasoning or general intelligence, but rather statistical pattern recognition over text.

The primary challenge is converting natural language into numerical representations while preserving semantic meaning.

---

## Embeddings

Traditional keyword matching is insufficient because language contains:

- Synonyms
- Paraphrases
- Implicit meanings
- Contextual dependencies

Instead, modern NLP systems use embeddings.

An embedding is a mapping:

```math
Text \rightarrow \mathbb{R}^n
```

where semantically similar texts occupy nearby positions in vector space.

For example:

```
"urgent"
"critical"
"immediate"
```

will have similar vector representations.

---

## Signal vs Noise

Email data contains substantial noise:

- Signatures
- Legal disclaimers
- Previous email chains
- HTML formatting
- URLs
- Encoding issues

Reducing this noise improves:

- Statistical reliability
- Generalization
- Token efficiency
- Model performance

---

## Email Preprocessing Pipeline

The preprocessing pipeline consists of:

| Step | Tool |
|------|------|
| HTML → Text | html2text |
| Unicode Repair | ftfy |
| Unicode Normalization | unicodedata |
| Remove Email Threads | email-reply-parser |
| Remove Signatures | regex |
| Normalize URLs | regex |
| Normalize Emails | regex |
| Collapse Repeated Characters | regex |

---

## Training Dataset

Training data consisted of:

- Enron email dataset
- AI-generated emails
- Corporate emails
- Legal emails
- Consulting emails
- Technology sector emails

A dataset of **3393 labeled emails** was created.

Urgency labels:

| Label | Value |
|--------|--------|
| Low | 0 |
| Medium | 1 |
| High | 2 |

Edge cases and false positives were deliberately included to improve model robustness.

---

## Model Development

Rather than training a language model from scratch, transfer learning was used.

The project involved:

- Transformer fine-tuning
- PyTorch training loops
- Tensor operations
- Gradient descent
- Backpropagation
- Loss functions
- Weight decay
- Regularization
- Hyperparameter tuning
- Validation strategies

Training was performed using Google Colab GPUs.

---

## Backend Pipeline

```text
Fetch Gmail Emails
         │
         ▼
Normalize JSON Schema
         │
         ▼
Preprocess Emails
         │
         ▼
Batch Model Inference
         │
         ▼
Assign Urgency Scores
         │
         ▼
Sort Emails
         │
         ▼
Return Results
```

---

## Frontend

The frontend was developed using:

- React
- Vite
- TailwindCSS

HTML emails are sanitized using DOMPurify while preserving formatting and styling.

---

## Learning Outcomes

This project provided practical experience with:

- Natural Language Processing
- Transformer architectures
- Transfer learning
- HuggingFace ecosystem
- PyTorch
- Text preprocessing
- FastAPI
- Gmail API integration
- React development
- Model deployment pipelines

---

## Future Improvements

- Multi-label classification
- Priority explanations
- Active learning
- User-specific personalization
- RAG-based urgency explanations
- Email summarization
- Calendar integration
- Outlook support

---

# My Learning Journey (For personal notes)

### Introduction

The system is not *general intelligence*, *reasoning* or *autonomous decision-making*.

It is *statistical pattern recognition over text*, guided by *human feedback*.

Formally, this is a *supervised learning ranking problem over natural language inputs*, that is **Natural Language Processing (NLP)**.

Computers understand only numbers (in the form of bits). Hence, the greatest hurdle in the project would be how to assign a numerical value to text that preserve its meaning.

To do so, we convert the texts to vectors: embeddings. Looking for keywords only is insufficient due to synonyms, paraphrasing and implicit meaning. What we need is *semantic similarity*, not string matching.

An **embedding** is a fixed-length vector representation of text, learned from massive *corpora*, where semantic similarity corresponds to geometric proximity. This means that the vectors for words with similar meanings are positioned close to each other, and the distance and direction between the vectors encode the degree of similarity between the words. Mathematically, Text → ℝⁿ (e.g. ℝ⁷⁶⁸).

A **corpus** refers to a large and structured collection of text that is used for training, testing and evaluating NLP models. An example of a corpus would be all of Wikipedia. The process begins with *preprocessing the text* including *tokenization* and removing stopwords and punctuation. A *sliding context window* identifies target and context words, allowing the model to learn word relationships. Then, the model is trained to predict based on their context positioning semantically similar words close together in the vector space. Finally, throughout the training, the model parameters are adjusted to minimize prediction errors.

The **sliding context window** technique in NLP involves analyzing text by considering a subset or "window" of words sequentially. The window shifts through the text, enabling the model to capture context and semantic meaning effectively. For example, for the sentence: "I love chocolate but not cookies.", a sliding window context of size 3 will read: 

- I love chocolate
- but not cookies

#### Signal vs Noise in Emails

When feeding emails in the model, we must make sure to extract maximum meaning in the minimum number of words possible. Long emails hurt. We will try to create a function that outputs one clean string per email.

One way to reduce noise is through *text normalization*. **Text normalization** is everything you do to make a messy text consistent and machine-learning friendly before modelling. Some typical steps are:

- Lowercasing: "FREE Offer" -> "free offer"
- Unicode normalization: smart quotes, weird hyphens, emojis -> consistent forms
- Punctuation handling: remove, keep or seperate (model-dependent)
- Stopword handling: optionally remove ('the', 'and', 'of', etc...)
- Stemming/lemmatization: "running", "ran" -> "run"
- Email-specific cleanup: 
    * Strip signatures, disclaimers
    * Remove quoted replies
    * Normalize URLs and emails
    * Collapse repeated characters ("looove" -> "love")

Text normalization is important as it:

- Reduces vocabulary size
- Improves statistical reliability
- Prevents models from learning noise

### My Pipeline for Pre-processing

This is the pipeline that will be implemented to prepare the data to be fed to the model. We will concentrate on text data from the emails as these usually carry the most weight in determining the urgency of an email.

0) Convert HTML email bodies to plain text - html2text
1) Fix broken Unicode, smart quotes, mojibake - ftfy
2) Canonical Unicode normalization - unicodedata
3) Remove quoted replies (previous email threads) - email-reply-parser
4) Strip email signatures and legal disclaimers - Python re (regex)
5) Normalize spaces, URLs, Quoted-Printable encodings and email addresses - Python re
6) Collapse repeated alphabetic characters (not punctuations) only - Python re

This is done so as to reduce noise and the number of tokens being used. After these steps, we have (mostly) clean text to feed to our transformer for analysis.

### Training Data and Validation data

For the training and validation data, the Enron dataset from Kaggle was used along with some AI generated emails. A random sample of 3393 emails was selected and converted to JSON, before being cleaned by the pre-processing pipeline. These emails were first labelled with an "urgency" field each. The urgency values were as follows:

- low: 0
- medium: 1
- high: 2

The urgency allocated to each email depended on a wide range of factors such as context, puntuation use, tone of voice, specific keywords, emotional responses, time limits, consequences, legal implications, financial loss and other urgency cues.

The emails for training the model were of corporate nature, ranging from tech and consulting to legal institutions.

Cases of false positives and edge cases were also included in both the training data and validation data to better train the AI (for example, cases that may seem as urgency 2 if we rely strictly on urgency cues such as punctuation, but which should be classified as urgency 1 if the email is read and understood properly).

### The AI model

Instead of creating an LLM from scratch, the objective was to fine-tune the **google-bert/bert-base-uncased** model using the HuggingFace ecosystem. Hence, we focused on transfer learning to create our model. This required understanding multiple ML concepts such as the training and testing loops, tensors, overfitting, underfitting, loss functions, gradient descent, backpropagation, hyperparameters, weight decay,etc... . Familiarity with the HuggingFace ecosystem and PyTorch was also needed. To further understand the inner mechanisms of transformers, the Deep Learning playlist of 3Blue1Brown is highly recommended as well as the HuggingFace LLM course.

After training the model via the GPU on Google Colab, we reached an accuracy of 98% which was considered acceptable to be used for our email analyser program.

### Connection to the GMAIL account and backend completion

Once the model was trained and saved on Google Colab, we then saved and loaded it into our project.

Code to fetch unread emails from our GMAIL account was written. The emails were prepared to fit a specific JSON schema for normalization. These emails are then fed to the preprocessor to prepare them for the model. Once preprocessed, they are then sent to the model in batches, to predict their urgency score. These scores are then appended to the JSO of each original email, which are then returned by the backend.

> Fetch unread emails from GMAIL account -> Normalize emails to the JSON schema -> Preprocess the emails -> Feed the cleaned emails to model -> Sort emails by urgency -> Send to frontend

*FastAPI* was used as the backend framework, to allow for API calls from the frontend.

### Frontend connection + HTML emails handling

Finally, the frontend is created and connected to the backend to fetch the emails. However, a clear distinction had to be made between text emails and html emails. HTML emails have to maintain their format and styling when displayed on the frontend. For that purpose, the *DOMPurify* library had to be used in the frontend, in conjuction with *BeatifulSoup* in the backend.

The Frontend is created using React and Tailwind.
