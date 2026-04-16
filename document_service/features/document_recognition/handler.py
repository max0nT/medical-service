import json
import re
from base64 import b64decode

import ollama

from document_service.features.document_recognition.dto import (
    DocumentRecognitionRequestDTO,
    DocumentRecognitionResponseDTO,
)
from document_service.infrastructure.config.config import OllamaConfig


class DocumentRecognitionHandler:
    """Business handler for document recognition."""

    def __init__(self, ollama_config: OllamaConfig) -> None:
        self._model = ollama_config.ollama_model_name
        self._client = ollama.Client(
            host=f"http://{ollama_config.ollama_host}:{ollama_config.ollama_port}",
        )

    def __call__(
        self,
        command: DocumentRecognitionRequestDTO,
    ) -> DocumentRecognitionResponseDTO:
        normalized_image_base64 = self._normalize_image_base64(
            command.image_base64,
        )
        response = self._client.chat(
            model=self._model,
            stream=False,
            format="json",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Extract all document fields from the image and "
                        "return valid JSON only. Do not add markdown."
                    ),
                    "images": [normalized_image_base64],
                },
            ],
        )

        content = response["message"]["content"]
        parsed = json.loads(content)
        return DocumentRecognitionResponseDTO(
            raw=json.dumps(parsed, ensure_ascii=False),
        )

    @staticmethod
    def _normalize_image_base64(value: str) -> str:
        # Accept plain base64 and data URLs, and strip all whitespace.
        if "," in value and value.startswith("data:"):
            _, value = value.split(",", 1)

        normalized = re.sub(r"\s+", "", value)
        if not normalized:
            raise ValueError("image_base64 is empty")

        try:
            b64decode(normalized, validate=True)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("image_base64 is not valid base64") from exc

        return normalized
