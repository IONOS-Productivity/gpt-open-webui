# Dependency management (Python)

## Adding or upgrading dependencies

```
open-webui $ podman run -it -v.:/app --workdir /app python:3.11-slim-bookworm /bin/bash
container # pip install uv
container # uv add <package>==1.2.3 # add or update
container # uv lock --upgrade-package <package> # upgrade to latest
```



## Creating uv environment from scratch

### Create `uv.lock`

```
open-webui $ podman run -it -v.:/app --workdir /app python:3.11-slim-bookworm /bin/bash
container # pip install uv
container # rm uv.lock                         # we'll regenerate this
container # mv pyproject.toml pyproject_.toml  # only to allow uv init (temporary)
container # uv init --app --name open-webui --no-package --no-readme /app  # to generate empty uv.lock
container # mv pyproject_.toml pyproject.toml  # undo temporary change
container # rm main.py                         # was auto generated, not needed
container # uv lock                            # creates new uv.lock
```

The `mv` of `pyproject.toml` is only done to keep an existing config. The `uv init` is needed to create an empty `uv.lock`.


### Verify `uv.lock`

```
open-webui $ podman run -it -v.:/app --workdir /app python:3.11-slim-bookworm /bin/bash
container # pip install uv
container # UV_PROJECT_ENVIRONMENT=/usr/local uv sync --locked  # install from uv.lock to system
container # python -c 'import torch' # test that torch works    # test that one of the dependencies is available
```


### Index config addition to `pyproject.toml` and adding torch* dependencies

Example of how to add a custom index to `pyproject.toml`:

```
[tool.uv.sources]
# dependency name = { which index to use }
torch = { index = "pytorch" }
torchvision = { index = "pytorch" }
torchaudio = { index = "pytorch" }

# custom index
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
```

Added to the `dependencies` section in `pyproject.toml`:



## Resources

* https://docs.astral.sh/uv/concepts/indexes/#pinning-a-package-to-an-index
* https://docs.astral.sh/uv/pip/packages/
* https://github.com/astral-sh/uv/issues/6692
