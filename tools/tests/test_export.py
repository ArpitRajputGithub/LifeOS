import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import export  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_build_bundle_groups_by_type():
    bundle = export.build_bundle(ROOT)
    assert "problems" in bundle and "knowledge" in bundle
    assert any(p["id"] == "PRB-20260607-01" for p in bundle["problems"])
    assert any(k["id"] == "KND-20260607-01" for k in bundle["knowledge"])


def test_bundle_is_json_serializable():
    bundle = export.build_bundle(ROOT)
    json.dumps(bundle, default=str)  # must not raise
