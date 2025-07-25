# download_models.py
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# This line will download and cache the sentence-transformer model
print("--> Downloading Sentence Transformer model: all-MiniLM-L6-v2")
SentenceTransformer('all-MiniLM-L6-v2')
print("--> Sentence Transformer model downloaded.")

# This line will download and cache the BART summarization model and tokenizer
print("--> Downloading BART summarization pipeline: facebook/bart-large-cnn")
pipeline("summarization", model="facebook/bart-large-cnn")
print("--> BART summarization pipeline downloaded.")

print("\nAll models downloaded successfully.")
