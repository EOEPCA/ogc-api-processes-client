import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from ogc_api_processes_client.api_client_wrapper import ApiClientWrapper
from ogc_api_processes_client.models.status_info import StatusInfo


class DummyResponse:
    def __init__(self, status=200, data=b"") -> None:
        self.status = status
        self.data = data
        self.read = Mock()


class TestApiClientWrapper(unittest.TestCase):
    def _build_wrapper(self, modifier=None):
        fake_api_client = SimpleNamespace(
            configuration=SimpleNamespace(host="https://example.test"),
            rest_client=SimpleNamespace(request=Mock()),
            response_deserialize=Mock(),
            call_api=Mock(),
        )
        with patch(
            "ogc_api_processes_client.api_client_wrapper.ApiClient",
            return_value=fake_api_client,
        ) as api_client_cls:
            wrapper = ApiClientWrapper(
                configuration="cfg",
                header_name="X-Header",
                header_value="token",
                cookie="session=abc",
                modifier=modifier,
            )
        return wrapper, fake_api_client, api_client_cls

    def test_init_uses_api_client_and_initializes_caches(self):
        wrapper, _, api_client_cls = self._build_wrapper()

        api_client_cls.assert_called_once_with(
            configuration="cfg",
            header_name="X-Header",
            header_value="token",
            cookie="session=abc",
        )
        self.assertIsNone(wrapper.capabilities_api)
        self.assertIsNone(wrapper.conformance_declaration_api)
        self.assertIsNone(wrapper.dismiss_api)
        self.assertIsNone(wrapper.execute_api)
        self.assertIsNone(wrapper.job_list_api)
        self.assertIsNone(wrapper.process_description_api)
        self.assertIsNone(wrapper.process_list_api)
        self.assertIsNone(wrapper.result_api)
        self.assertIsNone(wrapper.status_api)

    def test_get_landing_page_lazy_init_and_modifier(self):
        captured_headers = []

        def modifier(headers):
            headers["Authorization"] = "Bearer token"
            captured_headers.append(headers)

        wrapper, _, _ = self._build_wrapper(modifier=modifier)
        capabilities_api = Mock()
        capabilities_api.get_landing_page.return_value = "landing"

        with patch(
            "ogc_api_processes_client.api_client_wrapper.CapabilitiesApi",
            return_value=capabilities_api,
        ) as capabilities_cls:
            result_first = wrapper.get_landing_page()
            result_second = wrapper.get_landing_page(_headers={"X-Custom": "v"})

        self.assertEqual(result_first, "landing")
        self.assertEqual(result_second, "landing")
        capabilities_cls.assert_called_once_with(api_client=wrapper.api_client)
        self.assertEqual(capabilities_api.get_landing_page.call_count, 2)
        self.assertIn("Authorization", captured_headers[0])
        self.assertEqual(captured_headers[1]["X-Custom"], "v")

    def test_get_conformance_classes_and_dismiss_delegate(self):
        wrapper, _, _ = self._build_wrapper()
        wrapper.conformance_declaration_api = Mock()
        wrapper.dismiss_api = Mock()
        wrapper.conformance_declaration_api.get_conformance_classes.return_value = "ok"
        wrapper.dismiss_api.dismiss.return_value = "dismissed"

        headers = {"A": "B"}
        result1 = wrapper.get_conformance_classes(_headers=headers)
        result2 = wrapper.dismiss(job_id="job-1", _headers=headers)

        self.assertEqual(result1, "ok")
        self.assertEqual(result2, "dismissed")
        wrapper.conformance_declaration_api.get_conformance_classes.assert_called_once()
        wrapper.dismiss_api.dismiss.assert_called_once()

    def test_execute_delegates_to_execute_api(self):
        wrapper, _, _ = self._build_wrapper()
        wrapper.execute_api = Mock()
        wrapper.execute_api.execute.return_value = "execute-result"

        result = wrapper.execute(process_id="proc-1", execute={"inputs": {}})

        self.assertEqual(result, "execute-result")
        wrapper.execute_api.execute.assert_called_once()

    def test_execute_simple_returns_status_info_on_accepted_submission(self):
        wrapper, fake_api_client, _ = self._build_wrapper()
        response = DummyResponse(status=201)
        fake_api_client.rest_client.request.return_value = response
        expected = StatusInfo(
            type="process",
            jobID="job-42",
            status="accepted",
        )
        fake_api_client.response_deserialize.return_value = SimpleNamespace(
            data=expected
        )

        result = wrapper.execute_simple(
            process_id="proc-1",
            execute={"inputs": {}},
            _headers={"Accept": "application/json"},
            _request_timeout=7,
        )

        self.assertEqual(result, expected)
        fake_api_client.rest_client.request.assert_called_once_with(
            "POST",
            "https://example.test/processes/proc-1/execution",
            headers={"Accept": "application/json"},
            body={"inputs": {}},
            _request_timeout=7,
        )
        response.read.assert_called_once()

    def test_execute_simple_raises_when_response_is_not_status_info(self):
        wrapper, fake_api_client, _ = self._build_wrapper()
        response = DummyResponse(status=500)
        fake_api_client.rest_client.request.return_value = response
        fake_api_client.response_deserialize.return_value = SimpleNamespace(data={})

        with self.assertRaisesRegex(
            ValueError, "Failed to submit job. Status code: 500"
        ):
            wrapper.execute_simple(process_id="proc-2", execute={})

        response.read.assert_called_once()

    def test_process_and_jobs_delegation_methods(self):
        wrapper, _, _ = self._build_wrapper()
        wrapper.job_list_api = Mock()
        wrapper.process_description_api = Mock()
        wrapper.process_list_api = Mock()
        wrapper.job_list_api.get_jobs.return_value = "jobs"
        wrapper.process_description_api.get_process_description.return_value = "process"
        wrapper.process_list_api.get_processes.return_value = "processes"

        self.assertEqual(wrapper.get_jobs(), "jobs")
        self.assertEqual(wrapper.get_process_description("pid"), "process")
        self.assertEqual(wrapper.get_processes(), "processes")

    def test_get_result_and_get_status_delegate(self):
        wrapper, _, _ = self._build_wrapper()
        wrapper.result_api = Mock()
        wrapper.status_api = Mock()
        wrapper.result_api.get_result.return_value = {"a": 1}
        wrapper.status_api.get_status.return_value = "status"

        self.assertEqual(wrapper.get_result("job-3"), {"a": 1})
        self.assertEqual(wrapper.get_status("job-3"), "status")

    def test_get_result_simple_returns_deserialized_data(self):
        wrapper, fake_api_client, _ = self._build_wrapper()
        response = DummyResponse()
        fake_api_client.call_api.return_value = response
        fake_api_client.response_deserialize.return_value = SimpleNamespace(
            data={"k": "v"}
        )
        wrapper.result_api = Mock()
        wrapper.result_api._get_result_serialize.return_value = (
            "GET",
            "/jobs/job-4/results",
        )

        result = wrapper.get_result_simple("job-4", _request_timeout=9)

        self.assertEqual(result, {"k": "v"})
        fake_api_client.call_api.assert_called_once_with(
            "GET",
            "/jobs/job-4/results",
            _request_timeout=9,
        )
        response.read.assert_called_once()

    def test_get_result_simple_falls_back_to_item_collection(self):
        wrapper, fake_api_client, _ = self._build_wrapper()
        payload = b'{"result":{"type":"FeatureCollection","features":[]}}'
        response = DummyResponse(data=payload)
        fake_api_client.call_api.return_value = response
        fake_api_client.response_deserialize.side_effect = RuntimeError(
            "deserialize fail"
        )
        wrapper.result_api = Mock()
        wrapper.result_api._get_result_serialize.return_value = (
            "GET",
            "/jobs/job-5/results",
        )

        sentinel = object()
        with patch(
            "ogc_api_processes_client.api_client_wrapper.ItemCollection.from_dict",
            return_value=sentinel,
        ) as from_dict:
            result = wrapper.get_result_simple("job-5")

        self.assertIs(result, sentinel)
        from_dict.assert_called_once_with({"type": "FeatureCollection", "features": []})


if __name__ == "__main__":
    unittest.main()
