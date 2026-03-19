import unittest
import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch

import urllib3

from ogc_api_processes_client.configuration import Configuration
from ogc_api_processes_client.exceptions import ApiException, ApiValueError
from ogc_api_processes_client.rest import (
    RESTClientObject,
    RESTResponse,
    is_socks_proxy_url,
)


class TestRestHelpers(unittest.TestCase):
    def test_is_socks_proxy_url(self):
        self.assertTrue(is_socks_proxy_url("socks5://localhost:8080"))
        self.assertTrue(is_socks_proxy_url("SOCKS4A://proxy"))
        self.assertFalse(is_socks_proxy_url("http://localhost:8080"))
        self.assertFalse(is_socks_proxy_url("localhost:8080"))
        self.assertFalse(is_socks_proxy_url(None))

    def test_rest_response_helpers(self):
        raw = SimpleNamespace(
            status=201, reason="CREATED", data=b"x", headers={"a": "b"}
        )
        resp = RESTResponse(raw)
        self.assertEqual(resp.status, 201)
        self.assertEqual(resp.read(), b"x")
        self.assertEqual(resp.read(), b"x")
        self.assertEqual(resp.getheaders(), {"a": "b"})
        self.assertEqual(resp.getheader("a"), "b")


class TestRESTClientObject(unittest.TestCase):
    def _cfg(self):
        return Configuration(host="https://example.test")

    def _http_response(self):
        return SimpleNamespace(
            status=200,
            reason="OK",
            data=b"{}",
            headers={"content-type": "application/json"},
        )

    def test_init_uses_pool_manager_without_proxy(self):
        cfg = self._cfg()
        with patch(
            "ogc_api_processes_client.rest.urllib3.PoolManager", return_value=Mock()
        ) as pm:
            client = RESTClientObject(cfg)
        self.assertIsNotNone(client.pool_manager)
        pm.assert_called_once()

    def test_init_uses_proxy_and_socks_managers(self):
        cfg = self._cfg()
        cfg.proxy = "http://proxy:8080"
        with patch(
            "ogc_api_processes_client.rest.urllib3.ProxyManager", return_value=Mock()
        ) as proxy_pm:
            RESTClientObject(cfg)
        proxy_pm.assert_called_once()

        cfg2 = self._cfg()
        cfg2.proxy = "socks5://proxy:1080"
        socks_manager = Mock(return_value=Mock())
        fake_socks_mod = SimpleNamespace(SOCKSProxyManager=socks_manager)
        with patch.dict(sys.modules, {"urllib3.contrib.socks": fake_socks_mod}):
            client = RESTClientObject(cfg2)
        self.assertIsNotNone(client.pool_manager)
        socks_manager.assert_called_once()

    def test_request_get_and_timeout_modes(self):
        cfg = self._cfg()
        client = RESTClientObject(cfg)
        client.pool_manager = Mock()
        client.pool_manager.request.return_value = self._http_response()

        out = client.request("GET", "https://example.test/x", _request_timeout=3.5)
        self.assertEqual(out.status, 200)
        args, kwargs = client.pool_manager.request.call_args
        self.assertEqual(args[0], "GET")
        self.assertIsInstance(kwargs["timeout"], urllib3.Timeout)

        client.request("GET", "https://example.test/x", _request_timeout=(1, 2))
        _, kwargs2 = client.pool_manager.request.call_args
        self.assertIsInstance(kwargs2["timeout"], urllib3.Timeout)

    def test_request_rejects_body_with_post_params(self):
        cfg = self._cfg()
        client = RESTClientObject(cfg)
        with self.assertRaises(ApiValueError):
            client.request(
                "POST", "https://example.test/x", body={"a": 1}, post_params={"b": 2}
            )

    def test_request_json_urlencoded_and_multipart_paths(self):
        cfg = self._cfg()
        client = RESTClientObject(cfg)
        client.pool_manager = Mock()
        client.pool_manager.request.return_value = self._http_response()

        client.request(
            "POST",
            "https://example.test/a",
            headers={"Content-Type": "application/json"},
            body={"a": 1},
        )
        _, kwargs_json = client.pool_manager.request.call_args
        self.assertEqual(kwargs_json["body"], '{"a": 1}')

        client.request(
            "PUT",
            "https://example.test/b",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            post_params={"a": "1"},
        )
        _, kwargs_form = client.pool_manager.request.call_args
        self.assertFalse(kwargs_form["encode_multipart"])
        self.assertEqual(kwargs_form["fields"], {"a": "1"})

        headers = {"Content-Type": "multipart/form-data"}
        post_params = [("a", {"x": 1}), ("b", "2")]
        client.request(
            "PATCH", "https://example.test/c", headers=headers, post_params=post_params
        )
        _, kwargs_multi = client.pool_manager.request.call_args
        self.assertTrue(kwargs_multi["encode_multipart"])
        self.assertEqual(kwargs_multi["fields"][0][1], '{"x": 1}')

    def test_request_string_and_text_boolean_paths(self):
        cfg = self._cfg()
        client = RESTClientObject(cfg)
        client.pool_manager = Mock()
        client.pool_manager.request.return_value = self._http_response()

        client.request(
            "DELETE",
            "https://example.test/d",
            headers={"Content-Type": "application/xml"},
            body="<x/>",
        )
        _, kwargs_str = client.pool_manager.request.call_args
        self.assertEqual(kwargs_str["body"], "<x/>")

        client.request(
            "OPTIONS",
            "https://example.test/e",
            headers={"Content-Type": "text/plain"},
            body=True,
        )
        _, kwargs_bool = client.pool_manager.request.call_args
        self.assertEqual(kwargs_bool["body"], "true")

    def test_request_raises_for_unsupported_content_type(self):
        cfg = self._cfg()
        client = RESTClientObject(cfg)
        client.pool_manager = Mock()
        with self.assertRaises(ApiException):
            client.request(
                "POST",
                "https://example.test/x",
                headers={"Content-Type": "application/xml"},
                body={"a": 1},
            )

    def test_request_maps_ssl_errors(self):
        cfg = self._cfg()
        client = RESTClientObject(cfg)
        client.pool_manager = Mock()
        client.pool_manager.request.side_effect = urllib3.exceptions.SSLError(
            "ssl failed"
        )
        with self.assertRaises(ApiException):
            client.request("GET", "https://example.test/x")


if __name__ == "__main__":
    unittest.main()
