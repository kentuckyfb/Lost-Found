import os
from fastapi import FastAPI, HTTPException
from app.services import index_files, parse_query, search_files
from app.models import File, SearchRequest

# Initialize FastAPI app
app = FastAPI()

@app.post("/search")
async def search(request: SearchRequest):
    """
    Search for files based on a query and directory.
    """
    # Expand ~ to the user's home directory and normalize the path
    directory = os.path.normpath(os.path.expanduser(request.directory))
    
    if not os.path.exists(directory):
        raise HTTPException(status_code=404, detail=f"Directory not found: {directory}")
    
    # Index files
    index = index_files(directory)
    
    # Parse query
    context = parse_query(request.query)
    
    # Search files
    results = search_files(index, context)
    
    # Prepare the response
    response = {
        "query": request.query,
        "results": [
            {
                "path": result["file"].path,
                "name": result["file"].name,
                "created": result["file"].created.isoformat(),
                "modified": result["file"].modified.isoformat(),
                "relevancy_score": result["relevancy_score"]
            }
            for result in results
        ]
    }
    
    return response

@app.get("/")
async def root():
    return {"message": "File Search API is running!"}