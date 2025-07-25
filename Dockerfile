FROM python:3.9-slim
WORKDIR /app
ENV PYTHONPATH="."
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
COPY download_models.py .
RUN python download_models.py
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
