##############################################################################
# tests/test_example_function.py
# Unit tests for the example Lambda function
# Run with: pytest tests/ -v
##############################################################################

import json
import sys
import os
from unittest.mock import patch, MagicMock

# Make the lambda function importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda', 'functions', 'example_function'))

import handler


class TestLambdaHandler:

    def test_successful_invocation(self):
        """Lambda returns 200 on success"""
        mock_event = {"key": "raw/test/"}

        with patch("handler.s3_client") as mock_s3:
            mock_s3.list_objects_v2.return_value = {"KeyCount": 5}
            response = handler.lambda_handler(mock_event, {})

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["object_count"] == 5

    def test_returns_environment(self):
        """Lambda response includes the environment variable"""
        with patch("handler.s3_client") as mock_s3:
            mock_s3.list_objects_v2.return_value = {"KeyCount": 0}
            response = handler.lambda_handler({}, {})

        body = json.loads(response["body"])
        assert "environment" in body

    def test_handles_s3_error(self):
        """Lambda returns 500 when S3 call fails"""
        with patch("handler.s3_client") as mock_s3:
            mock_s3.list_objects_v2.side_effect = Exception("S3 unavailable")
            response = handler.lambda_handler({}, {})

        assert response["statusCode"] == 500
        body = json.loads(response["body"])
        assert "error" in body
