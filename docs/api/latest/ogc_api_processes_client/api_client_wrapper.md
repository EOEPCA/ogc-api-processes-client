# Module ogc_api_processes_client.api_client_wrapper

## Classes

### ApiClientWrapper

```python3
class ApiClientWrapper(
    configuration=None,
    header_name=None,
    header_value=None,
    cookie=None,
    modifier=None
)
```

#### Methods

    
#### dismiss

```python3
def dismiss(
    self,
    job_id: Annotated[str, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, description='local identifier of a job')],
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> ogc_api_processes_client.models.status_info.StatusInfo
```

    
#### execute

```python3
def execute(
    self,
    process_id: Annotated[str, Strict(strict=True)],
    execute: Annotated[ogc_api_processes_client.models.execute.Execute, FieldInfo(annotation=NoneType, required=True, description='Mandatory execute request JSON')],
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> ogc_api_processes_client.models.execute200_response.Execute200Response
```

    
#### execute_simple

```python3
def execute_simple(
    self,
    process_id: Annotated[str, Strict(strict=True)],
    execute: dict,
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
)
```

    
#### get_conformance_classes

```python3
def get_conformance_classes(
    self,
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> ogc_api_processes_client.models.conf_classes.ConfClasses
```

    
#### get_jobs

```python3
def get_jobs(
    self,
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> ogc_api_processes_client.models.job_list.JobList
```

    
#### get_landing_page

```python3
def get_landing_page(
    self,
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> ogc_api_processes_client.models.landing_page.LandingPage
```

    
#### get_process_description

```python3
def get_process_description(
    self,
    process_id: Annotated[str, Strict(strict=True)],
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> ogc_api_processes_client.models.process.Process
```

    
#### get_processes

```python3
def get_processes(
    self,
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> ogc_api_processes_client.models.process_list.ProcessList
```

    
#### get_result

```python3
def get_result(
    self,
    job_id: Annotated[str, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, description='local identifier of a job')],
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> Dict[str, ogc_api_processes_client.models.inline_or_ref_data.InlineOrRefData]
```

    
#### get_result_simple

```python3
def get_result_simple(
    self,
    job_id: Annotated[str, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, description='local identifier of a job')],
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> Dict[str, ogc_api_processes_client.models.inline_or_ref_data.InlineOrRefData]
```

    
#### get_status

```python3
def get_status(
    self,
    job_id: Annotated[str, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, description='local identifier of a job')],
    _request_timeout: None | Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])] | Tuple[Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])], Annotated[float, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Gt(gt=0)])]] = None,
    _request_auth: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _content_type: Annotated[str, Strict(strict=True)] | None = None,
    _headers: Dict[Annotated[str, Strict(strict=True)], Any] | None = None,
    _host_index: Annotated[int, Strict(strict=True), FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=0)])] = 0
) -> ogc_api_processes_client.models.status_info.StatusInfo
```