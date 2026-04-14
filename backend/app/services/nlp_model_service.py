from __future__ import annotations

import logging
from threading import Lock
from typing import Any

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

logger = logging.getLogger(__name__)

_pipeline: Any = None
_load_attempted = False
_load_lock = Lock()


def _load_pipeline() -> Any | None:
    global _pipeline, _load_attempted

    if _pipeline is not None:
        return _pipeline

    if _load_attempted:
        return None

    with _load_lock:
        if _pipeline is not None:
            return _pipeline

        if _load_attempted:
            return None

        _load_attempted = True

        try:
            from transformers import pipeline

            _pipeline = pipeline(
                "sentiment-analysis",
                model=MODEL_NAME,
            )
        except Exception as error:
            logger.warning("Falling back to rule-based sentiment; model load failed: %s", error)
            _pipeline = None

    return _pipeline


def classify_sentiment_with_model(text: str) -> dict[str, str] | None:
    sentiment_pipeline = _load_pipeline()
    if sentiment_pipeline is None:
        return None

    try:
        result = sentiment_pipeline(text[:512])[0]
    except Exception as error:
        logger.warning("Model sentiment inference failed: %s", error)
        return None

    label = str(result.get("label", "")).upper()
    if label == "POSITIVE":
        return {"sentiment": "positive"}
    if label == "NEGATIVE":
        return {"sentiment": "negative"}

    return None
