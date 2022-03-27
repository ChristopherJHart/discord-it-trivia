"""Test exam question pool."""

from typing import List


def test_question_pool_types(question_pool: List[dict]) -> None:
    """Ensure that the question pool is a list of dictionaries."""
    assert isinstance(question_pool, list)
    for exam in question_pool:
        assert isinstance(exam, dict)


def test_exam_meta_names(question_pool: List[dict]) -> None:
    """Ensure that each exam in the question pool has a stringy meta_name key."""
    for exam in question_pool:
        assert exam.get("meta_name") is not None
        assert isinstance(exam.get("meta_name"), str)


def test_exam_meta_descriptions(question_pool: List[dict]) -> None:
    """Ensure that each exam in the question pool has a stringy meta_description key."""
    for exam in question_pool:
        assert exam.get("meta_description") is not None
        assert isinstance(exam.get("meta_description"), str)


def test_exam_command_names(question_pool: List[dict]) -> None:
    """Ensure that each exam in the question pool has a stringy command_name key."""
    for exam in question_pool:
        assert exam.get("command_name") is not None
        assert isinstance(exam.get("command_name"), str)


def test_exam_command_descriptions(question_pool: List[dict]) -> None:
    """Ensure that each exam in the question pool has a stringy command_description key."""
    for exam in question_pool:
        assert exam.get("command_description") is not None
        assert isinstance(exam.get("command_description"), str)


def test_exam_questions_type(question_pool: List[dict]) -> None:
    """Ensure that each exam's set of questions is a list of dictionaries."""
    for exam in question_pool:
        assert exam.get("questions") is not None
        assert isinstance(exam.get("questions"), list)
        for q in exam.get("questions"):
            assert isinstance(q, dict)


def test_exam_questions_keys(question_pool: List[dict]) -> None:
    """Ensure that each exam's set of questions are properly-formed."""
    for exam in question_pool:
        for q in exam.get("questions", []):
            assert "prompt" in q.keys()
            assert q.get("prompt") is not None
            assert isinstance(q.get("prompt"), str)
            assert "type" in q.keys()
            assert q.get("type") is not None
            assert isinstance(q.get("type"), str)
            assert q.get("type") == "multiple choice"
            assert "correct_choice" in q.keys()
            assert q.get("correct_choice") is not None
            assert isinstance(q.get("correct_choice"), int)
            assert "choices" in q.keys()
            assert q.get("choices") is not None
            assert isinstance(q.get("choices"), list)


def test_exam_questions_choices(question_pool: List[dict]) -> None:
    """Ensure that each exam's set of questions has properly-formed choices."""
    for exam in question_pool:
        for q in exam.get("questions", []):
            for c in q.get("choices", []):
                assert c.get("id") is not None
                assert isinstance(c.get("id"), int)
                assert c.get("text") is not None
                assert isinstance(c.get("text"), str)
