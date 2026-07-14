"""Relay: remote endpoint agents that return materialized files."""

from relay.core import (
    DeliveryMethod,
    Endpoint,
    EndpointResult,
    RelayError,
    ProducedFile,
    Relay,
    RelayResult,
    RemoteArtifact,
    RemoteToolOutput,
    Workspace,
    WorkspaceFile,
    WorkspaceSnapshot,
    build_prompt,
)

__all__ = [
    "DeliveryMethod",
    "EndpointResult",
    "RelayError",
    "ProducedFile",
    "RelayResult",
    "RemoteArtifact",
    "RemoteToolOutput",
    "Endpoint",
    "Relay",
    "Workspace",
    "WorkspaceFile",
    "WorkspaceSnapshot",
    "build_prompt",
]
