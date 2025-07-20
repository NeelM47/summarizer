# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from summarizer.pipeline import SummarizationPipeline

# Define the request body model for data validation
class SummarizationRequest(BaseModel):
    documents: list[str]
    num_clusters: int = Field(
            default=3,
            gt=1,
            le=10,
            description="Number of topic clusters to find (2-10)."
        )

# Initialize the FastAPI app
app = FastAPI(
    title="Suvidha Multi-Document Summarizer API",
    description="An API that summarizes multiple documents using a hybrid extractive-abstractive approach.",
    version="1.0.0",
)

# --- CRITICAL STEP ---
# Load the pipeline once when the app starts.
# This avoids reloading the heavy models on every request.
summarizer_pipeline = SummarizationPipeline()
# --- END CRITICAL STEP ---


# Define the API endpoint
@app.post("/summarize/", tags=["Summarization"])
async def summarize(request: SummarizationRequest):
    """
    Receives a list of documents and returns a single summary.
    """
    summary = summarizer_pipeline.run(documents=request.documents,
                                      num_clusters=request.num_clusters
                                     )
    return {"summary": summary}

# Mount the 'static' directory to serve our frontend files
# This line makes it so visiting the root URL serves index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")
