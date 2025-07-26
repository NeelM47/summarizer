---
title: Multi-Document Summarizer
emoji: 📚
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
pinned: true
---

# Hybrid Multi-Document Summarization System

![Project Demo GIF](https://your-link-to-a-gif-of-the-app-working.gif) <!-- You can create this later with a screen recorder -->

A full-stack application that effectively summarizes information from multiple documents, focusing on key topics and reducing redundancy. This project uses a hybrid extractive-abstractive approach to generate coherent and concise summaries.

**https://huggingface.co/spaces/NeelM47/summarizer** <!-- This will be your Hugging Face Spaces link -->

---

## Features

-   **Multi-Document Input**: A dynamic web interface that allows users to input multiple documents for summarization.
-   **Configurable Topic Granularity**: Users can select the number of topics (clusters) to extract, controlling the detail level of the summary.
-   **Redundancy Reduction**: Uses `sentence-transformers` to create semantic embeddings and `scikit-learn` KMeans clustering to identify unique topics across all documents.
-   **Coherent Summaries**: Employs a pre-trained BART model from Hugging Face `transformers` to generate a fluent, abstractive summary from the most representative sentences.
-   **RESTful API**: The core NLP logic is exposed via a robust and fast FastAPI backend.
-   **Containerized Application**: The entire application is containerized with Docker, ensuring easy and reproducible deployment.

## Technology Stack

-   **Backend**: Python 3.9, FastAPI
-   **NLP/ML**: Hugging Face `transformers`, `sentence-transformers`, `scikit-learn`, `nltk`
-   **Frontend**: HTML, CSS, Vanilla JavaScript
-   **Deployment**: Docker, Uvicorn, Hugging Face Spaces

---

## How It Works: The Hybrid Approach

1.  **Ingestion**: The system takes a list of documents and a desired number of topics (`k`) as input.
2.  **Sentence Cleaning & Embedding**: All documents are split into sentences. Each sentence is cleaned (lowercased, punctuation removed) and then converted into a high-dimensional vector embedding using a Sentence-Transformer model.
3.  **Extractive Clustering**: The sentence embeddings are clustered using KMeans with `k` clusters. This groups semantically similar sentences into topics.
4.  **Centroid-Based Selection**: The most representative sentence from each cluster is selected by finding the one closest to the cluster's centroid.
5.  **Abstractive Summarization**: These selected, non-redundant sentences are combined and passed to a BART model, which generates a final, coherent summary.

---

## Running the Project Locally

### 1. Using Conda (for development)

```bash
# Clone the repository
git clone https://github.com/NeelM47/summarizer.git
cd summarizer

# Create and activate the conda environment
conda env create -f environment.yml 
conda activate summarizer

# Run the FastAPI server
uvicorn main:app --reload
```
*Access the app at `http://127.0.0.1:8000`*

### 2. Using Docker (for production/deployment)

Ensure you have Docker installed and running.

```bash
# Clone the repository
git clone https://github.com/NeelM47/summarizer.git
<<<<<<< HEAD
cd summarizer
=======
cd suvidha-summarizer
>>>>>>> 1d551d7cc667304ddd3e9d9a672bebd1f68bc829

# Build the Docker image
docker build -t summarizer .

# Run the Docker container
docker run -p 8000:8000 summarizer
```
*Access the app at `http://127.0.0.1:8000`*

---

## API Documentation

Once the server is running, interactive API documentation (powered by Swagger UI) is available at `http://127.0.0.1:8000/docs`.

