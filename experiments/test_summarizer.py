# test_summarizer.py
# A script to experiment with abstractive text summarization using the Hugging Face transformers library.
from icecream import ic
ic.configureOutput(prefix=f'Debug | ', includeContext=True)

# We are using the 'pipeline' helper function, which is the easiest way to use a pre-trained model for a given task.
from transformers import pipeline

def read_text_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def summarize_text(text_to_summarize):
    """
    Summarizes a given text using a pre-trained BART model from Hugging Face.
    
    Args:
        text_to_summarize (str): The text content to be summarized.
        
    Returns:
        str: The generated summary.
    """
    print("Initializing summarization pipeline...")
    # 1. Initialize the pipeline
    #    - "summarization": The task we want to perform.
    #    - model="facebook/bart-large-cnn": A specific, high-quality model trained for summarizing news articles.
    #      This is an excellent, well-known model to mention in interviews.
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    print("Generating summary... (This may take a moment)")
    # 2. Generate the summary
    #    - We pass the text as a list.
    #    - max_length: The maximum number of words in the summary.
    #    - min_length: The minimum number of words in the summary.
    #    - do_sample=False: Ensures the output is deterministic (not random).
    summary_result = summarizer(text_to_summarize, max_length=150, min_length=40, do_sample=False)
    
    # The result is a list of dictionaries, so we extract the 'summary_text' from the first element.
    return summary_result[0]['summary_text']

# This block ensures the code inside only runs when the script is executed directly
# (not when it's imported as a module into another script).
if __name__ == "__main__":
    # A long sample text to test the summarizer.
    # Sourced from a Wikipedia article about the transformer architecture.
    sample_article = """
    A transformer is a deep learning model that adopts the mechanism of self-attention, differentially weighting the
    significance of each part of the input data. It is used primarily in the fields of natural language processing (NLP)
    and computer vision (CV). Like recurrent neural networks (RNNs), transformers are designed to handle sequential input
    data, such as natural language, for tasks such as translation and text summarization. However, unlike RNNs,
    transformers do not require that the sequential data be processed in order. Rather, the self-attention mechanism
    allows for parallelization. For example, if the input data is a natural language sentence, the transformer does
    not need to process the beginning of the sentence before the end. This feature allows for training on much larger
    datasets than was possible before the transformer was introduced. This has led to the development of pretrained
    systems such as BERT (Bidirectional Encoder Representations from Transformers) and GPT (Generative Pre-trained
    Transformer), which have been trained with huge language datasets, and can be fine-tuned for specific tasks.
    """
    sample_article = read_text_from_file('../sample_article.txt')

    print("--- ORIGINAL TEXT ---")
    print(sample_article)
    print("\n" + "="*50 + "\n")

    # Call our function to get the summary
    generated_summary = summarize_text(sample_article)

    print("--- GENERATED SUMMARY ---")
    print(generated_summary)
