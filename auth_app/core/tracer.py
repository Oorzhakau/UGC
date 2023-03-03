from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


def configure_tracer(app: Flask) -> None:
    resource = Resource(attributes={
        "service.name": app.config['PROJECT_NAME']
    })
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=app.config['JAEGER_HOSTNAME'],
                agent_port=app.config['JAEGER_PORT'],
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
