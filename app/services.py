import os
from datetime import datetime
from typing import List
from .models import File, Context
from .utils import preprocess_text, compute_tfidf
import numpy as np

def index_files(directory: str) -> List[File]:
    """
    Index files in the specified directory.
    """
    index = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_stats = os.stat(file_path)
            index.append(File(
                path=file_path,
                name=file,
                created=datetime.fromtimestamp(file_stats.st_ctime),
                modified=datetime.fromtimestamp(file_stats.st_mtime),
            ))
    return index

def parse_query(query: str) -> Context:
    """
    Parse a natural language query to extract context.
    """
    processed_query = preprocess_text(query)
    return Context(query=processed_query)

def search_files(index: List[File], context: Context) -> List[dict]:
    """
    Search files based on the query context and return the top 5 results with relevancy scores.
    """
    # Extract file names and preprocess them
    file_names = [file.name for file in index]
    processed_file_names = [preprocess_text(name) for name in file_names]
    
    # Debug: Print processed file names
    print(f"Processed file names: {processed_file_names}")
    
    # Compute TF-IDF scores
    scores = compute_tfidf(processed_file_names, context.query)
    
    # Debug: Print TF-IDF scores
    print(f"TF-IDF scores: {scores}")
    
    # Pair scores with files and sort by score
    scored_files = list(zip(scores, index))
    scored_files.sort(key=lambda x: x[0], reverse=True)  # Sort by score in descending order
    
    # Normalize scores to a range of 0 to 1
    max_score = np.max(scores) if scores.size > 0 else 1  # Avoid division by zero
    normalized_scores = scores / max_score
    
    # Debug: Print normalized scores
    print(f"Normalized scores: {normalized_scores}")
    
    # Prepare the top 5 results with relevancy scores
    top_results = []
    for (score, file), normalized_score in zip(scored_files[:5], normalized_scores[:5]):
        top_results.append({
            "file": file,
            "relevancy_score": float(normalized_score)  # Convert to Python float for JSON serialization
        })
    
    return top_results