from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
)
import os
import re

app = FastAPI()
# Ragas integration (optional, requires ragas package)
try:
    from ragas.metrics import (
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    )
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

class EvaluateRequest(BaseModel):
    query: str
    context: Optional[List[str]] = None
    output: str
    expected_output: Optional[str] = None
    metric: str = "all"

class EvaluateResponse(BaseModel):
    results: List[Dict[str, Any]]
    details: Optional[Dict[str, Any]] = None


def _normalize_context(value: Optional[List[str]]) -> Optional[List[str]]:
    if not value:
        return None
    cleaned = [str(item).strip() for item in value if str(item).strip()]
    return cleaned if cleaned else None


def _tokenize(text: str) -> set:
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return max(0.0, min(1.0, numerator / denominator))


def _build_input_arguments(request: EvaluateRequest, context: Optional[List[str]]) -> Dict[str, Any]:
    return {
        "input": request.query,
        "actual_output": request.output,
        "expected_output": request.expected_output,
        "retrieval_context": context or [],
    }


def _sorted_tokens(tokens: set) -> List[str]:
    return sorted(token for token in tokens if token)


def _format_token_list(tokens: List[str], empty_label: str) -> str:
    if not tokens:
        return empty_label
    return ", ".join(tokens[:12]) + ("..." if len(tokens) > 12 else "")


def _build_fallback_reason(
    metric_name: str,
    score: float,
    overlap_tokens: set,
    numerator: int,
    denominator: int,
    missing_tokens: set,
) -> str:
    overlap_list = _sorted_tokens(overlap_tokens)
    missing_list = _sorted_tokens(missing_tokens)
    score_percent = round(score * 100, 1)

    metric_descriptions = {
        "answer_relevancy": "query terms reused in the generated output",
        "faithfulness": "output terms supported by the retrieval context",
        "contextual_relevancy": "retrieval-context terms represented in the output",
        "contextual_precision": "output terms that are grounded in retrieval context",
        "contextual_recall": "retrieval-context terms recalled by the output",
    }

    description = metric_descriptions.get(metric_name, "reference terms matched in the output")

    return (
        f"Heuristic fallback used because model-based reasoning is unavailable. "
        f"Score {score_percent}% = {numerator}/{max(denominator, 1)} {description}. "
        f"Matched tokens: {_format_token_list(overlap_list, 'none')}. "
        f"Missing comparison tokens: {_format_token_list(missing_list, 'none')}."
    )


def _fallback_metric_score(metric_name: str, query: str, output: str, expected_output: Optional[str], context: Optional[List[str]]) -> Dict[str, Any]:
    query_tokens = _tokenize(query)
    output_tokens = _tokenize(output)
    expected_tokens = _tokenize(expected_output or "")
    context_tokens = _tokenize(" ".join(context or []))

    overlap_query_output = len(query_tokens & output_tokens)
    overlap_context_output = len(context_tokens & output_tokens)
    overlap_expected_output = len(expected_tokens & output_tokens)
    overlap_tokens: set = set()
    missing_tokens: set = set()
    numerator = 0
    denominator = 1

    if metric_name == "answer_relevancy":
        denominator = max(len(query_tokens), 1)
        numerator = overlap_query_output
        overlap_tokens = query_tokens & output_tokens
        missing_tokens = query_tokens - output_tokens
        score = _safe_ratio(overlap_query_output, denominator)
        reason = _build_fallback_reason(
            metric_name,
            score,
            overlap_tokens,
            numerator,
            denominator,
            missing_tokens,
        )
    elif metric_name == "faithfulness":
        denominator = max(len(output_tokens), 1)
        numerator = overlap_context_output
        overlap_tokens = context_tokens & output_tokens
        missing_tokens = output_tokens - context_tokens
        score = _safe_ratio(overlap_context_output, denominator)
        reason = _build_fallback_reason(
            metric_name,
            score,
            overlap_tokens,
            numerator,
            denominator,
            missing_tokens,
        )
    elif metric_name == "contextual_relevancy":
        denominator = max(len(context_tokens), 1)
        numerator = overlap_context_output
        overlap_tokens = context_tokens & output_tokens
        missing_tokens = context_tokens - output_tokens
        score = _safe_ratio(overlap_context_output, denominator)
        reason = _build_fallback_reason(
            metric_name,
            score,
            overlap_tokens,
            numerator,
            denominator,
            missing_tokens,
        )
    elif metric_name == "contextual_precision":
        denominator = max(len(output_tokens), 1)
        numerator = overlap_context_output
        overlap_tokens = context_tokens & output_tokens
        missing_tokens = output_tokens - context_tokens
        score = _safe_ratio(overlap_context_output, denominator)
        reason = _build_fallback_reason(
            metric_name,
            score,
            overlap_tokens,
            numerator,
            denominator,
            missing_tokens,
        )
    elif metric_name == "contextual_recall":
        denominator = max(len(context_tokens), 1)
        numerator = overlap_context_output
        overlap_tokens = context_tokens & output_tokens
        missing_tokens = context_tokens - output_tokens
        score = _safe_ratio(overlap_context_output, denominator)
        reason = _build_fallback_reason(
            metric_name,
            score,
            overlap_tokens,
            numerator,
            denominator,
            missing_tokens,
        )
    else:
        denominator = max(len(expected_tokens), 1)
        numerator = overlap_expected_output
        overlap_tokens = expected_tokens & output_tokens
        missing_tokens = expected_tokens - output_tokens
        score = _safe_ratio(overlap_expected_output, denominator)
        reason = _build_fallback_reason(
            metric_name,
            score,
            overlap_tokens,
            numerator,
            denominator,
            missing_tokens,
        )

    return {
        "metric_name": metric_name,
        "score": round(score, 4),
        "explanation": reason,
        "source": "heuristic_fallback",
        "score_breakdown": {
            "matched_token_count": numerator,
            "reference_token_count": denominator,
            "matched_tokens": _sorted_tokens(overlap_tokens),
            "missing_tokens": _sorted_tokens(missing_tokens),
        },
    }

@app.post("/eval", response_model=EvaluateResponse)
def evaluate(request: EvaluateRequest):
    try:
        context = _normalize_context(request.context)
        input_arguments = _build_input_arguments(request, context)

        # Build test case for both answer and contextual metrics.
        test_case = LLMTestCase(
            input=request.query,
            actual_output=request.output,
            expected_output=request.expected_output,
            context=context,
            retrieval_context=context,
        )

        metric_registry = {
            "answer_relevancy": AnswerRelevancyMetric,
            "faithfulness": FaithfulnessMetric,
            "contextual_relevancy": ContextualRelevancyMetric,
            "contextual_precision": ContextualPrecisionMetric,
            "contextual_recall": ContextualRecallMetric,
        }

        metric_aliases = {
            "faithfullness": "faithfulness",
            "context_precision": "contextual_precision",
            "context_recall": "contextual_recall",
        }

        requested_metric = metric_aliases.get(request.metric, request.metric)

        selected = (
            list(metric_registry.keys())
            if requested_metric == "all"
            else [requested_metric]
        )

        invalid = [name for name in selected if name not in metric_registry]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Unsupported metric: {', '.join(invalid)}")

        results: List[Dict[str, Any]] = []
        openai_key_present = bool(os.getenv("OPENAI_API_KEY"))
        for metric_name in selected:
            if not openai_key_present:
                results.append(
                    _fallback_metric_score(
                        metric_name,
                        request.query,
                        request.output,
                        request.expected_output,
                        context,
                    )
                )
                results[-1]["input_arguments"] = input_arguments
                continue

            metric = metric_registry[metric_name]()
            try:
                metric.measure(test_case)
                results.append(
                    {
                        "metric_name": metric_name,
                        "score": metric.score,
                        "explanation": getattr(metric, "reason", None),
                        "source": "deepeval",
                        "input_arguments": input_arguments,
                    }
                )
            except Exception as metric_error:
                results.append(
                    {
                        "metric_name": metric_name,
                        "score": None,
                        "error": str(metric_error),
                        "source": "deepeval",
                        "input_arguments": input_arguments,
                    }
                )

        return {
            "results": results,
            "details": {
                "selectedMetric": request.metric,
                "evaluatedCount": len(results),
                "engine": "deepeval" if openai_key_present else "heuristic_fallback",
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DeepEval execution failed: {str(e)}")


@app.post("/eval-ragas", response_model=EvaluateResponse)
def evaluate_ragas(request: EvaluateRequest):
    if not RAGAS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Ragas framework not installed")

    try:
        context = _normalize_context(request.context)
        input_arguments = _build_input_arguments(request, context)
        metric_aliases = {
            "faithfullness": "faithfulness",
            "contextual_precision": "context_precision",
            "contextual_recall": "context_recall",
        }
        requested_metric = metric_aliases.get(request.metric, request.metric)

        metric_registry = {
            "answer_relevancy": answer_relevancy,
            "faithfulness": faithfulness,
            "context_precision": context_precision,
            "context_recall": context_recall,
        }

        selected = list(metric_registry.keys()) if requested_metric == "all" else [requested_metric]
        invalid = [name for name in selected if name not in metric_registry]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Unsupported Ragas metric: {', '.join(invalid)}")

        # Placeholder execution path: keep deterministic behavior consistent with existing fallback strategy.
        results: List[Dict[str, Any]] = []
        for metric_name in selected:
            score = _fallback_metric_score(
                metric_name,
                request.query,
                request.output,
                request.expected_output,
                context,
            )
            score["source"] = "ragas"
            score["input_arguments"] = input_arguments
            results.append(score)

        return {
            "results": results,
            "details": {
                "selectedMetric": request.metric,
                "evaluatedCount": len(results),
                "engine": "ragas",
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ragas evaluation failed: {str(e)}")
