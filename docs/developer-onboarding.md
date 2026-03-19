# Developer Onboarding

This guide helps contributors get productive quickly on `ogc-api-processes-client`.

## 1. Prerequisites

Install these tools first:

- Python 3.10+ (3.11+ recommended for local development)
- [Hatch](https://hatch.pypa.io/latest/)
- [Task](https://taskfile.dev/) (`task` CLI)
- Java runtime (required by OpenAPI Generator)
- `yq`
- `wget`
- `redocly` CLI (for bundling OpenAPI sources during generation)

## 2. Clone And Install

```bash
git clone https://github.com/EOEPCA/ogc-api-processes-client.git
cd ogc-api-processes-client
pip install -e .
```

Optional: pre-download Hatch environments by running:

```bash
task test
```

## 3. Repository Layout

- `ogc_api_processes_client/`: generated and patched Python client code
- `test/`: generated baseline tests
- `docs/`: MkDocs content and generated API markdown
- `Taskfile.yaml`: canonical local workflows (`build-safe`, `check`, `lint`, `test`, `docs-serve`, `docs-build`)
- `pyproject.toml`: packaging + Hatch environments

## 4. Daily Developer Workflow

Run these commands from repository root:

```bash
task lint
task check
task test
```

- `lint` formats code (`ruff format`)
- `check` runs lints with fixes (`ruff check --fix`)
- `test` executes `pytest` through Hatch

## 5. Safe Regeneration Workflow

When the upstream API definition changes, regenerate using:

```bash
task build-safe
```

`build-safe` will:

1. regenerate client code
2. apply deterministic compatibility fixes
3. remove legacy generated files that are not used in this project
4. run `check`
5. run `test`

Do not run raw generation commands in isolation unless you know exactly what must be updated.

## 6. Why `build-safe` Exists

This project includes post-generation fixes to keep generated code compatible with the current toolchain (notably `pydantic>=2` and linting constraints). These fixes are automated in Taskfile and should be treated as part of generation.

## 7. Files Protected From Generator Overwrites

`.openapi-generator-ignore` protects project-maintained files (for example CI workflows and `pyproject.toml`).

If you add new hand-maintained files at repo root, update `.openapi-generator-ignore` so regeneration cannot overwrite them.

## 8. Documentation Workflow

Local docs workflows:

```bash
task docs-serve
task docs-build
```

The docs workflow also regenerates API markdown via `pdocs` in CI before `mkdocs` deploy.

## 9. Common Issues

- `task build-safe` fails early:
  - verify Java, `yq`, `wget`, and `redocly` are installed and on `PATH`
- Hatch command missing:
  - install Hatch and retry (`pip install hatch`)
- formatting/lint errors after generation:
  - run `task check` again and confirm no local manual edits conflict with generated code

## 10. Before Opening A PR

Run:

```bash
task build-safe
```

Then review:

- generated client diffs
- docs diffs
- CI/workflow changes (if any)
