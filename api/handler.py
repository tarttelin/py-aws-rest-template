from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, APIGatewayRestResolver

tracer = Tracer()
logger = Logger()
app = APIGatewayHttpResolver()
rest = APIGatewayRestResolver()


@app.get("/")
@tracer.capture_method
def hello(*args):
    return {
        "message": "Hello",
        "input": "stuff"}


@app.post("/")
@tracer.capture_method
def greet():
    payload = app.current_event.json_body
    return {"message": f"Hello {payload.get('message')}"}


@rest.post("/secure")
@tracer.capture_method
def secret():
    payload = app.current_event.json_body
    return {"message": f"Hello {payload.get('message')}"}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def handle_http(event, context):
    return app.resolve(event, context)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def handle_rest(event, context):
    return rest.resolve(event, context)
