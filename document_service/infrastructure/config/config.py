import functools

import pydantic_settings


class GrpcConfig(pydantic_settings.BaseSettings):
    """Config for gRPC server."""

    grpc_host: str = "0.0.0.0"
    grpc_port: int = 50051
    grpc_max_workers: int = 10


class OllamaConfig(pydantic_settings.BaseSettings):
    """Config for Ollama service."""

    ollama_host: str = "0.0.0.0"
    ollama_port: int = 11434
    ollama_model_name: str = "gemma3"


class ServiceConfig(pydantic_settings.BaseSettings):
    """Config for document-service gRPC server."""

    ollama: OllamaConfig = OllamaConfig()
    grpc: GrpcConfig = GrpcConfig()


@functools.cache
def get_settings() -> ServiceConfig:
    return ServiceConfig()
