import json
from pydantic import Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, Optional, Tuple, Union
from typing_extensions import Annotated

from ogc_api_processes_client.api_client import ApiClient

from ogc_api_processes_client.models.landing_page import LandingPage
from ogc_api_processes_client.models.conf_classes import ConfClasses
from ogc_api_processes_client.models.status_info import StatusInfo
from ogc_api_processes_client.models.execute import Execute
from ogc_api_processes_client.models.execute200_response import Execute200Response
from ogc_api_processes_client.models.job_list import JobList
from ogc_api_processes_client.models.process import Process
from ogc_api_processes_client.models.process_list import ProcessList
from ogc_api_processes_client.models.inline_or_ref_data import InlineOrRefData


from ogc_api_processes_client.api.capabilities_api import CapabilitiesApi
from ogc_api_processes_client.api.conformance_declaration_api import (
    ConformanceDeclarationApi,
)
from ogc_api_processes_client.api.dismiss_api import DismissApi
from ogc_api_processes_client.api.execute_api import ExecuteApi
from ogc_api_processes_client.api.job_list_api import JobListApi
from ogc_api_processes_client.api.process_description_api import ProcessDescriptionApi
from ogc_api_processes_client.api.process_list_api import ProcessListApi
from ogc_api_processes_client.api.result_api import ResultApi
from ogc_api_processes_client.api.status_api import StatusApi

from pystac import ItemCollection


class ApiClientWrapper:
    def __init__(
        self,
        configuration=None,
        header_name=None,
        header_value=None,
        cookie=None,
        modifier=None,
    ):
        self.api_client = ApiClient(
            configuration=configuration,
            header_name=header_name,
            header_value=header_value,
            cookie=cookie,
        )
        self.modifier = modifier
        self.capabilities_api = None
        self.conformance_declaration_api = None
        self.dismiss_api = None
        self.execute_api = None
        self.job_list_api = None
        self.process_description_api = None
        self.process_list_api = None
        self.result_api = None
        self.status_api = None

    # Capabilities API

    def get_landing_page(
        self,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> LandingPage:
        if not self.capabilities_api:
            self.capabilities_api = CapabilitiesApi(api_client=self.api_client)

        if _headers is None:
            _headers = {}
        if self.modifier:
            self.modifier(headers=_headers)

        return self.capabilities_api.get_landing_page(
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

    # Conformance declaration API

    def get_conformance_classes(
        self,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ConfClasses:
        if not self.conformance_declaration_api:
            self.conformance_declaration_api = ConformanceDeclarationApi(
                api_client=self.api_client
            )

        if _headers is None:
            _headers = {}
        if self.modifier:
            self.modifier(headers=_headers)

        return self.conformance_declaration_api.get_conformance_classes(
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

    # Dismiss API

    def dismiss(
        self,
        job_id: Annotated[StrictStr, Field(description="local identifier of a job")],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> StatusInfo:
        if not self.dismiss_api:
            self.dismiss_api = DismissApi(api_client=self.api_client)

        if _headers is None:
            _headers = {}
        if self.modifier:
            self.modifier(headers=_headers)

        return self.dismiss_api.dismiss(
            job_id=job_id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

    # Execute API
    def execute(
        self,
        process_id: StrictStr,
        execute: Annotated[
            Execute, Field(description="Mandatory execute request JSON")
        ],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> Execute200Response:
        if not self.execute_api:
            self.execute_api = ExecuteApi(api_client=self.api_client)

        if _headers is None:
            _headers = {}
        if self.modifier:
            self.modifier(headers=_headers)

        return self.execute_api.execute(
            process_id=process_id,
            execute=execute,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

    def execute_simple(
        self,
        process_id: StrictStr,
        execute: dict,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        response_data = self.api_client.rest_client.request(
            "POST",
            f"{self.api_client.configuration.host}/processes/{process_id}/execution",
            headers=_headers,
            body=execute,
            _request_timeout=_request_timeout,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "Execute200Response",
            "201": "StatusInfo",
            "404": "Exception",
            "500": "Exception",
        }

        response_data.read()
        content = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

        if not isinstance(content, StatusInfo):
            raise ValueError(
                f"Failed to submit job. Status code: {response_data.status}"
            )

        return content

    # Job list API

    def get_jobs(
        self,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> JobList:
        if not self.job_list_api:
            self.job_list_api = JobListApi(api_client=self.api_client)

        if _headers is None:
            _headers = {}
        if self.modifier:
            self.modifier(headers=_headers)

        return self.job_list_api.get_jobs(
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

    # Process description API

    def get_process_description(
        self,
        process_id: StrictStr,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> Process:
        if not self.process_description_api:
            self.process_description_api = ProcessDescriptionApi(
                api_client=self.api_client
            )

        if _headers is None:
            _headers = {}
        if self.modifier:
            self.modifier(headers=_headers)

        return self.process_description_api.get_process_description(
            process_id=process_id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

    # Process list API

    def get_processes(
        self,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ProcessList:

        if not self.process_list_api:
            self.process_list_api = ProcessListApi(api_client=self.api_client)

        if _headers is None:
            _headers = {}
        if self.modifier:
            self.modifier(headers=_headers)

        return self.process_list_api.get_processes(
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

    # Result API

    def get_result(
        self,
        job_id: Annotated[StrictStr, Field(description="local identifier of a job")],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> Dict[str, InlineOrRefData]:
        if not self.result_api:
            self.result_api = ResultApi(api_client=self.api_client)

        return self.result_api.get_result(
            job_id=job_id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

    def get_result_simple(
        self,
        job_id: Annotated[StrictStr, Field(description="local identifier of a job")],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> Dict[str, InlineOrRefData]:
        if not self.result_api:
            self.result_api = ResultApi(api_client=self.api_client)

        _param = self.result_api._get_result_serialize(
            job_id=job_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "Dict[str, InlineOrRefData]",
            "404": "Exception",
            "500": "Exception",
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        response_data.read()

        try:
            return self.api_client.response_deserialize(
                response_data=response_data,
                response_types_map=_response_types_map,
            ).data
        except Exception:
            response_text = response_data.data.decode("utf-8")
            response_dict = json.loads(response_text)
            return ItemCollection.from_dict(next(v for v in response_dict.values()))

    # Status API

    def get_status(
        self,
        job_id: Annotated[StrictStr, Field(description="local identifier of a job")],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> StatusInfo:
        if not self.status_api:
            self.status_api = StatusApi(api_client=self.api_client)

        return self.status_api.get_status(
            job_id=job_id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )
