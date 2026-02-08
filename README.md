# My Learning Journey

## Introduction

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

### Signal vs Noise in Emails

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

## My Pipeline for Pre-processing

This is the pipeline that will be implemented to prepare the data to be fed to the model. For now, we will concentrate on text data from the emails only.

0) Convert HTML email bodies to plain text - html2text
1) Fix broken Unicode, smart quotes, mojibake - ftfy
2) Canonical Unicode normalization - unicodedata
3) Remove quoted replies (previous email threads) - email-reply-parser
4) Strip email signatures and legal disclaimers - Python re (regex)
5) Normalize spaces, URLs, Quoted-Printable encodings and email addresses - Python re
6) Collapse repeated alphabetic characters (not punctuations) only - Python re

This is done so as to reduce noise and the number of tokens being used. After these steps, we have (mostly) clean text to feed to our transformer for analysis.

## Training Data and Validation data

For the training and validation data, the Enron dataset from Kaggle was used along with some AI generated emails. A random sample of 3393 emails was selected and converted to JSON, before being cleaned by the pre-processing pipeline. These emails were first labelled with an "urgency" field each. The urgency values were as follows:

- low: 0
- medium: 1
- high: 2

The urgency allocated to each email depended on a wide range of factors such as context, puntuation use, tone of voice, specific keywords, emotional responses, time limits, consequences, legal implications, financial loss and other urgency cues.

The emails for training the model were of corporate nature, ranging from tech and consulting to legal institutions.

Cases of false positives and edge cases were also included in both the training data and validation data to better train the AI (for example, cases that may seem as urgency 2 if we rely strictly on urgency cues such as punctuation, but which should be classified as urgency 1 if the email is read and understood properly).

## The AI model

Instead of creating an LLM from scratch, the objective was to fine-tune the **google-bert/bert-base-uncased** model using the HuggingFace ecosystem. Hence, we focused on transfer learning to create our model. This required understanding multiple ML concepts such as the training and testing loops, tensors, overfitting, underfitting, loss functions, gradient descent, backpropagation, hyperparameters, weight decay,etc... . Familiarity with the HuggingFace ecosystem and PyTorch was also needed. To further understand the inner mechanisms of transformers, the Deep Learning playlist of 3Blue1Brown is highly recommended as well as the HuggingFace LLM course.

After training the model via the GPU on Google Colab, we reached an accuracy of 98% which was considered acceptable to be used for our email analyser program.

## Connection to the GMAIL account and backend completion

Once the model was trained and saved on Google Colab, we then saved and loaded it into our project.

Code to fetch unread emails from our GMAIL account was written. The emails were prepared to fit a specific JSON schema for normalization. These emails are then fed to the preprocessor to prepare them for the model. Once preprocessed, they are then sent to the model in batches, to predict their urgency score. These scores are then appended to the JSO of each original email, which are then returned by the backend.

> Fetch unread emails from GMAIL account -> Normalize emails to the JSON schema -> Preprocess the emails -> Feed the cleaned emails to model -> Sort emails by urgency -> Send to frontend

FastAPI was used as the backend framework, to allow for API calls from the frontend.

## Frontend connection + HTML emails handling

Finally, the frontend is created and connected to the backend to fetch the emails. However, a clear distinction had to be made between text emails and html emails. HTML emails have to maintain their format and styling when displayed on the frontend. For that purpose, the DOMPurify library had to be used in the frontend, in conjuction with BeatifulSoup in the backend.

The Frontend is created using React and Tailwind.