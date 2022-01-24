# Executable documentation PoC

Automagically start markdown documentation as [Jupyter](https://jupyter.org/) notebook:

* mac/linux

```shell
git clone https://github.com/houbie/tomlkit.git
cd tomlkit
# windows users: remove the leading ./
./pw rD # shorthand for ./pw run-docs
```

This will launch a Jupyter server after which you can open the _quickstart_ notebook and start experimenting.

You only need git and python 3.7+ to be available on your path, everything else gets installed in _.pyprojectx_
inside the project dir (comparable with _node_modules_).

## How does it work?

* Jupyter and the project dir (current dir) are added to the _tool.pyprojectx_ section in _pyproject.toml_, making them
  both available in an isolated virtual environment (no impact on project dependencies).

```toml
[tool.pyprojectx]
jupyter = """\
jupyter
.
"""
```

* The _run-docs_ alias is configured to generate a Jupyter notebook from the markdown documentation and start the
  Jupyter server:

```toml
[tool.pyprojectx.aliases]
run-docs = "pw@poetry run python docs/rst2notebook.py && pw@jupyter notebook --notebook-dir=docs"
```

## Notebook generation

The _rst2notebook.py_ script generates a _ipynb_ json with markdown cells and code cells. The code cells are extracted
from the interactive Python sessions inside the markdown docs.

```markdown
Modifying
---------
TOML Kit provides an intuitive API to modify TOML documents::
    >>> from tomlkit import dumps
    >>> from tomlkit import parse
    >>> from tomlkit import table
```

is converted to:

```json
[
  {
    "cell_type": "markdown",
    "source": [
      "Modifying\n",
      "---------\n",
      "TOML Kit provides an intuitive API to modify TOML documents::\n"
    ]
  },
  {
    "cell_type": "code",
    "source": [
      "from tomlkit import dumps\n",
      "from tomlkit import parse\n",
      "from tomlkit import table\n"
    ]
  }
]
```
