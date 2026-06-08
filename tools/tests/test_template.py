import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import validate  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAX = validate.load_taxonomy()


def _validate_dir(rel):
    path = os.path.join(ROOT, rel)
    files = list(validate.iter_files([path]))
    errors = []
    for f in files:
        errors += validate.validate_file(f, TAX)
    return files, errors


def test_examples_exist_and_are_valid():
    files, errors = _validate_dir("examples")
    assert files, "no example entity files found under examples/"
    assert errors == [], f"invalid example files: {errors}"


def test_precedents_exist_and_are_valid():
    files, errors = _validate_dir("precedents")
    assert files, "no precedent files found under precedents/"
    assert errors == [], f"invalid precedent files: {errors}"
