import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import validate  # noqa: E402

TAX = validate.load_taxonomy()
FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def errs(name):
    return validate.validate_file(os.path.join(FIX, name), TAX)


def test_good_problem_has_no_errors():
    assert errs("good_problem.md") == []


def test_good_knowledge_has_no_errors():
    assert errs("good_knowledge.md") == []


def test_bad_problem_flags_missing_status():
    assert any("missing required field 'status'" in e for e in errs("bad_problem.md"))


def test_bad_problem_flags_off_vocab_subject():
    assert any("not_a_real_subject" in e for e in errs("bad_problem.md"))


def test_bad_problem_flags_bad_id():
    assert any("does not match" in e for e in errs("bad_problem.md"))


def test_good_problem_with_outcome_has_no_errors():
    assert errs("good_problem_with_outcome.md") == []


def test_bad_outcome_flags_missing_id_and_date():
    e = errs("bad_outcome.md")
    assert any("missing 'id'" in x for x in e)
    assert any("missing 'date'" in x for x in e)


def test_taxonomy_loads_15_subjects():
    assert len(TAX["subjects"]) == 15
