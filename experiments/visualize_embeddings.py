# visualize_embeddings.py
import nltk
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from icecream import ic
ic.configureOutput(prefix=f'Debug | ', includeContext=True)

# --- Part 1: Data Preparation ---

def read_text_from_file(filepath):
    """Reads content from a .txt file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def split_into_sentences(text):
    """
    Splits text into a list of sentences.
    Uses NLTK for better accuracy than simple splitting on periods.
    """
    # NLTK's sentence tokenizer needs to be downloaded once
    try:
        nltk.data.find('tokenizers/punkt')
    except nltk.downloader.DownloadError:
        print("Downloading NLTK's 'punkt' model for sentence tokenization...")
        nltk.download('punkt')
        
    ic(text)
    ic(nltk.sent_tokenize(text))
    return nltk.sent_tokenize(text)

# --- Part 2: Main Execution Logic ---

if __name__ == "__main__":
    # 1. Load data and create sentences
    article_text = read_text_from_file('../sample_article.txt')
    sentences = split_into_sentences(article_text)
    
    print(f"Found {len(sentences)} sentences.")
    for i, s in enumerate(sentences):
        print(f"{i}: {s}")
    print("\n" + "="*50 + "\n")

    # 2. Create sentence embeddings
    print("Loading sentence-transformer model and creating embeddings...")
    # 'all-MiniLM-L6-v2' is a great, fast model for this task.
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(sentences)
    
    # Each sentence is now a 384-dimensional vector
    print("Shape of embeddings matrix:", embeddings.shape)
    print("\n" + "="*50 + "\n")

    # 3. Reduce dimensionality for plotting
    print("Reducing dimensionality using PCA and t-SNE...")
    
    # PCA: A fast method that captures the most variance
    pca = PCA(n_components=2)
    embeddings_pca = pca.fit_transform(embeddings)

    # t-SNE: A slower but often better method for visualizing clusters
    # Perplexity should be less than the number of data points.
    perplexity_value = min(5, len(sentences) - 1)
    tsne = TSNE(n_components=2, perplexity=perplexity_value, random_state=42)
    embeddings_tsne = tsne.fit_transform(embeddings)

    # --- Part 3: Visualization ---
    
    print("Generating plots...")
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Visualizing Sentence Embeddings in 2D', fontsize=16)

    # Plot PCA results
    ax1.scatter(embeddings_pca[:, 0], embeddings_pca[:, 1], alpha=0.7)
    ax1.set_title('PCA Visualization')
    ax1.set_xlabel('Principal Component 1')
    ax1.set_ylabel('Principal Component 2')
    # Add labels to each point
    for i, txt in enumerate(range(len(sentences))):
        ax1.annotate(txt, (embeddings_pca[i, 0], embeddings_pca[i, 1]), xytext=(5, 2), textcoords='offset points')

    # Plot t-SNE results
    ax2.scatter(embeddings_tsne[:, 0], embeddings_tsne[:, 1], alpha=0.7)
    ax2.set_title('t-SNE Visualization')
    ax2.set_xlabel('t-SNE Dimension 1')
    ax2.set_ylabel('t-SNE Dimension 2')
    # Add labels to each point
    for i, txt in enumerate(range(len(sentences))):
        ax2.annotate(txt, (embeddings_tsne[i, 0], embeddings_tsne[i, 1]), xytext=(5, 2), textcoords='offset points')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
