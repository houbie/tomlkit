import json
import uuid

from doctest import DocTestParser
from doctest import Example
from pathlib import Path


def generate_notebook(src):
    nb = notebook()
    cur_cell = None
    cur_cell_is_code = False

    with open(src, "r") as md:
        docs = DocTestParser().parse(md.read())
        for part in docs:
            if isinstance(part, Example):
                source = part.source
                if source.strip() and (not cur_cell or not cur_cell_is_code):
                    cur_cell = code_cell()
                    cur_cell_is_code = True
                    nb["cells"].append(cur_cell)
            else:
                source = part
                if source.strip() and (not cur_cell or cur_cell_is_code):
                    cur_cell = markdown_cell()
                    cur_cell_is_code = False
                    nb["cells"].append(cur_cell)
            if source:
                cur_cell["source"].append(source)
    return json.dumps(nb)


def notebook():
    return {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.9.6",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def markdown_cell():
    return {"cell_type": "markdown", "id": cell_id(), "metadata": {}, "source": []}


def code_cell():
    return {
        "cell_type": "code",
        "id": cell_id(),
        "execution_count": 0,
        "metadata": {},
        "outputs": [],
        "source": [],
    }


def cell_id():
    return uuid.uuid4().hex[:8]


if __name__ == "__main__":
    src = Path(__file__).with_name("quickstart.md")
    dest = Path(__file__).with_name("quickstart.ipynb")
    if not dest.exists():
        ipynb = generate_notebook(src)
        with open(dest, "w") as file:
            file.write(ipynb)
