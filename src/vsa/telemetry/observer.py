from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.trace import Status, StatusCode
import logging
from typing import Optional

class ScientificObserver:
    """
    Layer 5: Telemetry & Observability.
    Provides deep tracing into the agent's decision-making process.
    """
    
    def __init__(self, service_name: str = "vsa-research-agent"):
        provider = TracerProvider()
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        self.tracer = trace.get_tracer(service_name)
        logging.info("Scientific Observer (OTel) initialized.")

    def start_span(self, name: str):
        """Start a new trace span for an operation."""
        return self.tracer.start_as_current_span(name)

    def log_event(self, span, name: str, attributes: dict):
        """Add an event to the current span."""
        span.add_event(name, attributes)

    def set_error(self, span, message: str):
        """Mark the current span as failed."""
        span.set_status(Status(StatusCode.ERROR, message))
        logging.error(f"Trace Error: {message}")
