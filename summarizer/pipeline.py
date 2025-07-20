# summarizer/pipeline.py
import nltk
import re
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from transformers import pipeline as hf_pipeline # Renamed to avoid conflict

class SummarizationPipeline:
    def __init__(self):
        print("Initializing Summarization Pipeline...")
        # Load heavy models only once
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.summarizer = hf_pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Ensure NLTK data is available
        try:
            nltk.data.find('tokenizers/punkt')
        except nltk.downloader.DownloadError:
            nltk.download('punkt')
        print("Pipeline Initialized Successfully.")
    
    def _clean_sentence(self, sentence: str) -> str:
        """Applies basic text cleaning to a single sentence."""
        cleaned = sentence.lower()
        cleaned = re.sub(r'[^a-z\s]', '', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def run(self, documents: list[str], num_clusters: int) -> str:
        """
        Runs the full hybrid summarization pipeline.
        
        Args:
            documents (list[str]): A list of text documents to summarize.
            num_clusters (int): The number of topics to extract.
            
        Returns:
            str: The final abstractive summary.
        """
        # 1. Split into sentences
        sentences = [s for doc in documents for s in nltk.sent_tokenize(doc)]
        if not sentences:
            return "Error: No sentences found in the provided documents."

        cleaned_for_clustering = [self._clean_sentence(s) for s in sentences]

        # 2. Create embeddings
        embeddings = self.embedding_model.encode(cleaned_for_clustering)

        # 3. Perform clustering
        kmeans = KMeans(n_clusters=num_clusters, n_init='auto', random_state=42)
        kmeans.fit(embeddings)

        # 4. Find closest sentences to centroids
        closest_sentence_indices, _ = pairwise_distances_argmin_min(
            kmeans.cluster_centers_, embeddings
        )
        selected_indices = sorted(closest_sentence_indices)
        selected_sentences = [sentences[i] for i in selected_indices]
        print(selected_sentences)
        print(len(selected_sentences))
        
        # 5. Generate abstractive summary from selected sentences
        extractive_summary = " ".join(selected_sentences)
        summary_result = self.summarizer(extractive_summary, max_length=150, min_length=40, do_sample=False)
        
        return summary_result[0]['summary_text']
