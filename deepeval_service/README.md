# DeepEval Service (Python)

This is a minimal FastAPI wrapper for DeepEval metrics, exposing an `/eval` endpoint for use by your Node.js backend.

## Quick Start

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Start the service:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## API
- **POST /eval**
  - Request body:
    ```json
    {
      "query": "...",
      "context": ["..."],
      "output": "...",
      "expected_output": "...",
      "metric": "all" // or "answer_relevancy", "faithfulness"
    }
    ```
  - Response:
    ```json
    {
      "results": {
        "AnswerRelevancyMetric": 0.92,
        "FaithfulnessMetric": 0.88
      },
      "details": {
        "AnswerRelevancyMetric": "reasoning...",
        "FaithfulnessMetric": "reasoning..."
      }
    }
    ```
