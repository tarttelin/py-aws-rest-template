from api.handler import handle_http, handle_rest
import json
import pytest
from dataclasses import dataclass


@pytest.fixture
def context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:eu-west-1:809313241:function:test"
        aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"
    return LambdaContext()


def test_hello(context):
    result = json.loads(handle_http(create_event(), context)['body'])
    assert result == {"message": "Hello", "input": "stuff"}


def create_event(path="/", method="GET", body=""):
    return {
        "rawPath": path,
        "requestContext": {
            "resourcePath": "/",
            "http": {
                "method": method,
                "path": "/",
                "protocol": "HTTP/1.1",
                "sourceIp": "IP",
                "userAgent": "agent"
            },
            "path": "/Prod/",
            "stage": "$default"
        },
        "body": body,
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "Host": "70ixmpl4fl.execute-api.us-east-2.amazonaws.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "X-Amzn-Trace-Id": "Root=1-5e66d96f-7491f09xmpl79d18acf3d050"
        },
        "multiValueHeaders": {
            "accept": [
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            ],
            "accept-encoding": [
                "gzip, deflate, br"
            ]
        }
    }
