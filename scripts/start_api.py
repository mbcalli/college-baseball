#!/usr/bin/env python3
"""Start the FastAPI development server."""

import uvicorn

from college_baseball.config import get_settings

def main() -> None:
    """Main function."""
    settings = get_settings()
    
    print(f"Starting API server on {settings.api_host}:{settings.api_port}")
    print(f"API documentation: http://{settings.api_host}:{settings.api_port}/docs")
    
    uvicorn.run(
        "college_baseball.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )


if __name__ == "__main__":
    main()
