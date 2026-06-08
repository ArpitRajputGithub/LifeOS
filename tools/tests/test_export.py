import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import export  # noqa: E402

SAMPLE_ROOT = os.path.join(os.path.dirname(__file__), "fixtures", "sample_root")


def test_build_bundle_groups_by_type():
    bundle = export.build_bundle(SAMPLE_ROOT)
    assert "problems" in bundle and "knowledge" in bundle and "precedents" in bundle
    assert any(p["id"] == "PRB-20000101-01" for p in bundle["problems"])
    assert any(k["id"] == "KND-20000101-01" for k in bundle["knowledge"])
    assert any(r["id"] == "PRE-20000101-01" for r in bundle["precedents"])


def test_bundle_is_json_serializable():
    bundle = export.build_bundle(SAMPLE_ROOT)
    json.dumps(bundle, default=str)  # must not raise
