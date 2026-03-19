import datetime
import decimal
import os
import tempfile
import unittest
from enum import Enum
from unittest.mock import Mock, patch

from pydantic import SecretStr

from ogc_api_processes_client.api_client import ApiClient
from ogc_api_processes_client.configuration import Configuration
from ogc_api_processes_client.exceptions import ApiException, ApiValueError
from ogc_api_processes_client.models.status_code import StatusCode


class Color(Enum):
    RED = "red"


class DummyModel:
    def to_dict(self):
        return {"x": 1}


class DummyResponse:
    def __init__(self, status=200, data=b'{"a":1}', headers=None, reason="OK"):
        self.status = status
        self.data = data
        self.reason = reason
        self._headers = headers or {"content-type": "application/json; charset=utf-8"}

    def getheader(self, name, default=None):
        return self._headers.get(name, default)

    def getheaders(self):
        return self._headers


class TestApiClient(unittest.TestCase):
    def _client(self):
        cfg = Configuration(host="https://example.test")
        return ApiClient(
            configuration=cfg, header_name="X-A", header_value="B", cookie="c=v"
        )

    def test_sanitize_for_serialization_supports_common_types(self):
        client = self._client()
        payload = {
            "enum": Color.RED,
            "secret": SecretStr("s3cr3t"),
            "date": datetime.date(2024, 1, 2),
            "dt": datetime.datetime(2024, 1, 2, 3, 4, 5),
            "dec": decimal.Decimal("1.23"),
            "list": [1, 2],
            "tuple": (3, 4),
            "model": DummyModel(),
        }

        data = client.sanitize_for_serialization(payload)

        self.assertEqual(data["enum"], "red")
        self.assertEqual(data["secret"], "s3cr3t")
        self.assertEqual(data["date"], "2024-01-02")
        self.assertEqual(data["dec"], "1.23")
        self.assertEqual(data["list"], [1, 2])
        self.assertEqual(data["tuple"], (3, 4))
        self.assertEqual(data["model"], {"x": 1})

    def test_parameters_to_tuples_and_url_query(self):
        client = self._client()
        tuples = client.parameters_to_tuples(
            {"m": [1, 2], "s": ["a", "b"], "p": ["x", "y"], "c": ["u", "v"]},
            {"m": "multi", "s": "ssv", "p": "pipes", "c": "csv"},
        )
        self.assertIn(("m", 1), tuples)
        self.assertIn(("s", "a b"), tuples)
        self.assertIn(("p", "x|y"), tuples)
        self.assertIn(("c", "u,v"), tuples)

        query = client.parameters_to_url_query(
            {"flag": True, "n": 2, "obj": {"k": "v"}, "m": ["a b", "c"]},
            {"m": "multi"},
        )
        self.assertIn("flag=true", query)
        self.assertIn("n=2", query)
        self.assertIn("obj=%7B%22k%22%3A%20%22v%22%7D", query)
        self.assertIn("m=a%20b", query)

    def test_files_parameters_with_supported_values(self):
        client = self._client()
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            f.write(b"abc")
            path = f.name
        self.addCleanup(lambda: os.path.exists(path) and os.unlink(path))

        params = client.files_parameters(
            {
                "f1": path,
                "f2": b"raw",
                "f3": ("name.txt", b"tuple"),
                "f4": [b"a", b"b"],
            }
        )
        self.assertGreaterEqual(len(params), 5)

        with self.assertRaises(ValueError):
            client.files_parameters({"bad": 123})

    def test_select_headers(self):
        client = self._client()
        self.assertEqual(
            client.select_header_accept(["text/plain", "application/json"]),
            "application/json",
        )
        self.assertEqual(client.select_header_accept(["text/plain"]), "text/plain")
        self.assertIsNone(client.select_header_accept([]))
        self.assertEqual(
            client.select_header_content_type(["text/plain", "application/json"]),
            "application/json",
        )
        self.assertIsNone(client.select_header_content_type([]))

    def test_update_params_for_auth_and_apply_auth_params(self):
        client = self._client()
        headers = {}
        queries = []
        client.update_params_for_auth(
            headers,
            queries,
            auth_settings=None,
            resource_path="/x",
            method="GET",
            body=None,
        )
        self.assertEqual(headers, {})
        self.assertEqual(queries, [])

        request_auth = {"in": "query", "type": "api_key", "key": "k", "value": "v"}
        client.update_params_for_auth(
            headers,
            queries,
            auth_settings=["unused"],
            resource_path="/x",
            method="GET",
            body=None,
            request_auth=request_auth,
        )
        self.assertIn(("k", "v"), queries)

        client._apply_auth_params(
            headers,
            queries,
            "/x",
            "GET",
            None,
            {"in": "header", "type": "api_key", "key": "X-K", "value": "V"},
        )
        self.assertEqual(headers["X-K"], "V")
        client._apply_auth_params(
            headers,
            queries,
            "/x",
            "GET",
            None,
            {"in": "cookie", "type": "api_key", "key": "Cookie", "value": "a=b"},
        )
        self.assertEqual(headers["Cookie"], "a=b")
        client._apply_auth_params(
            headers,
            queries,
            "/x",
            "GET",
            None,
            {"in": "header", "type": "http-signature", "key": "Sig", "value": "skip"},
        )
        self.assertNotIn("Sig", headers)
        with self.assertRaises(ApiValueError):
            client._apply_auth_params(
                headers,
                queries,
                "/x",
                "GET",
                None,
                {"in": "body", "type": "api_key", "key": "k", "value": "v"},
            )

    def test_param_serialize_builds_url_and_headers(self):
        client = self._client()
        method, url, headers, body, post_params = client.param_serialize(
            method="POST",
            resource_path="/r/{id}",
            path_params={"id": "a/b"},
            query_params={"q": "hello world"},
            header_params={"X-Test": "1"},
            body={"k": "v"},
            auth_settings=["dummy"],
            collection_formats={},
            _host="https://override.test",
            _request_auth={
                "in": "header",
                "type": "api_key",
                "key": "X-Auth",
                "value": "token",
            },
        )
        self.assertEqual(method, "POST")
        self.assertTrue(url.startswith("https://override.test/r/a%2Fb?q=hello%20world"))
        self.assertEqual(headers["X-Test"], "1")
        self.assertEqual(headers["X-A"], "B")
        self.assertEqual(headers["Cookie"], "c=v")
        self.assertEqual(headers["X-Auth"], "token")
        self.assertEqual(body, {"k": "v"})
        self.assertIsNone(post_params)

    def test_call_api_success_and_rethrow(self):
        client = self._client()
        client.rest_client = Mock()
        client.rest_client.request.return_value = "ok"
        self.assertEqual(client.call_api("GET", "https://example.test"), "ok")
        client.rest_client.request.side_effect = ApiException(status=500, reason="boom")
        with self.assertRaises(ApiException):
            client.call_api("GET", "https://example.test")

    def test_deserialize_and_private_deserializers(self):
        client = self._client()
        self.assertEqual(client.deserialize('{"a":1}', "object", None), {"a": 1})
        self.assertEqual(client.deserialize("plain", "str", "text/plain"), "plain")
        with self.assertRaises(ApiException):
            client.deserialize("x", "str", "application/xml")

        self.assertEqual(client._ApiClient__deserialize([1, 2], "List[int]"), [1, 2])
        self.assertEqual(
            client._ApiClient__deserialize({"a": 1}, "Dict[str, int]"), {"a": 1}
        )
        self.assertEqual(
            client._ApiClient__deserialize("successful", StatusCode),
            StatusCode.SUCCESSFUL,
        )
        with self.assertRaises(ApiException):
            client._ApiClient__deserialize_enum("nope", StatusCode)

        self.assertEqual(
            client._ApiClient__deserialize_date("2024-01-01"), datetime.date(2024, 1, 1)
        )
        self.assertEqual(
            client._ApiClient__deserialize_datetime("2024-01-01T00:00:00Z").year, 2024
        )
        with self.assertRaises(ApiException):
            client._ApiClient__deserialize_date("not-a-date")
        with self.assertRaises(ApiException):
            client._ApiClient__deserialize_datetime("not-a-datetime")

    def test_response_deserialize_handles_success_and_errors(self):
        client = self._client()

        # bytearray response type
        response = DummyResponse(status=200, data=b"abc")
        out = client.response_deserialize(response, {"200": "bytearray"})
        self.assertEqual(out.data, b"abc")

        # file response type
        response_file = DummyResponse(
            status=200,
            data=b"filedata",
            headers={"Content-Disposition": 'attachment; filename="x.bin"'},
        )
        with patch.object(
            client, "_ApiClient__deserialize_file", return_value="/tmp/x.bin"
        ):
            out_file = client.response_deserialize(response_file, {"200": "file"})
        self.assertEqual(out_file.data, "/tmp/x.bin")

        # typed model via charset decode path
        response_json = DummyResponse(
            status=200,
            data=b'"successful"',
            headers={"content-type": "application/json; charset=utf-8"},
        )
        out_json = client.response_deserialize(response_json, {"200": "StatusCode"})
        self.assertEqual(out_json.data, StatusCode.SUCCESSFUL)

        # non-2xx raises mapped exception
        response_err = DummyResponse(status=500, data=b'{"error":"x"}')
        with self.assertRaises(ApiException):
            client.response_deserialize(response_err, {"500": "object"})

        # asserting read precondition
        response_no_data = DummyResponse(status=200, data=None)
        with self.assertRaises(AssertionError):
            client.response_deserialize(response_no_data, {"200": "object"})

    def test_deserialize_file_writes_response_data(self):
        client = self._client()
        with tempfile.TemporaryDirectory() as tmpdir:
            client.configuration.temp_folder_path = tmpdir
            response = DummyResponse(
                status=200,
                data=b"payload",
                headers={"Content-Disposition": 'attachment; filename="out.txt"'},
            )
            path = client._ApiClient__deserialize_file(response)
            self.assertTrue(path.endswith("out.txt"))
            with open(path, "rb") as f:
                self.assertEqual(f.read(), b"payload")


if __name__ == "__main__":
    unittest.main()
