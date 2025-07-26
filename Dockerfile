# 1. Base Image - THIS IS THE MISSING "BUILD STAGE"
FROM python:3.9-slim

# 2. Set Working Directory and Python Path
WORKDIR /app
ENV PYTHONPATH="."

# 3. Set Environment Variables for Caching
ENV HF_HOME="/app/cache/huggingface"
ENV HF_DATASETS_CACHE="/app/cache/datasets"
ENV TRANSFORMERS_CACHE="/app/cache/transformers"

# 4. Copy and Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# 6. Copy and run the model download script
COPY download_models.py .
RUN python download_models.py

# 7. Copy the rest of the application code
COPY . .

# 8. Expose Port
EXPOSE 8000

# 9. Run Command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
