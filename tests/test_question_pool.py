"""Test exam question pool."""

from typing import List
import re
import pytest
from yaml import SafeLoader, load


def get_exams() -> List[dict]:
    with open("./bot/models/question_pool.yaml") as pool_file:
        return load(pool_file, SafeLoader)


def get_questions() -> List[dict]:
    questions = []
    with open("./bot/models/question_pool.yaml") as pool_file:
        question_pool = load(pool_file, SafeLoader)
    for exam in question_pool:
        questions += exam.get("questions", [])
    return questions


def test_exam_is_list(question_pool: List[dict]) -> None:
    """Ensure that the question pool is a list of dictionaries."""
    assert question_pool is not None
    assert isinstance(question_pool, list)


@pytest.mark.parametrize("exam", get_exams())
def test_exam_is_dictionary(exam: dict) -> None:
    """Ensure that the question pool is a list of dictionaries."""
    assert exam is not None
    assert isinstance(exam, dict)


@pytest.mark.parametrize("exam", get_exams())
def test_exam_meta_names(exam: dict) -> None:
    """Ensure that each exam in the question pool has a stringy meta_name key."""
    assert exam.get("meta_name") is not None
    assert isinstance(exam.get("meta_name"), str)


@pytest.mark.parametrize("exam", get_exams())
def test_exam_meta_descriptions(exam: dict) -> None:
    """Ensure that each exam in the question pool has a stringy meta_description key."""
    assert exam.get("meta_description") is not None
    assert isinstance(exam.get("meta_description"), str)


@pytest.mark.parametrize("exam", get_exams())
def test_exam_command_names(exam: dict) -> None:
    """Ensure that each exam in the question pool has a stringy command_name key."""
    assert exam.get("command_name") is not None
    assert isinstance(exam.get("command_name"), str)


def test_exam_command_names_unique(question_pool: List[dict]) -> None:
    """Ensure that the command_name key of each exam is globally unique."""
    all_command_names = [e.get("command_name") for e in question_pool]
    unique_command_names = list(set(all_command_names))
    assert len(all_command_names) == len(unique_command_names)


@pytest.mark.parametrize("exam", get_exams())
def test_exam_command_names_single_world(exam: dict) -> None:
    """Ensure that the command_name key of each exam is a single word."""
    assert len(exam.get("command_name").split(" ")) == 1


@pytest.mark.parametrize("exam", get_exams())
def test_exam_command_descriptions(exam: dict) -> None:
    """Ensure that each exam in the question pool has a stringy command_description key."""
    assert exam.get("command_description") is not None
    assert isinstance(exam.get("command_description"), str)


@pytest.mark.parametrize("question", get_questions())
def test_exam_questions_type(question: dict) -> None:
    """Ensure that each exam's set of questions is a list of dictionaries."""
    assert isinstance(question, dict)
    # for exam in question_pool:
    #     assert exam.get("questions") is not None
    #     assert isinstance(exam.get("questions"), list)
    #     for q in exam.get("questions"):
    #         assert isinstance(q, dict)


@pytest.mark.parametrize("question", get_questions())
def test_exam_questions_keys(question: dict) -> None:
    """Ensure that each exam's set of questions are properly-formed."""
    assert "prompt" in question.keys()
    assert question.get("prompt") is not None
    assert isinstance(question.get("prompt"), str)
    assert "type" in question.keys()
    assert question.get("type") is not None
    assert isinstance(question.get("type"), str)
    assert question.get("type") == "multiple choice"
    assert "correct_choice" in question.keys()
    assert question.get("correct_choice") is not None
    assert isinstance(question.get("correct_choice"), int)
    assert "choices" in question.keys()
    assert question.get("choices") is not None
    assert isinstance(question.get("choices"), list)


@pytest.mark.parametrize("question", get_questions())
def test_exam_questions_choices(question: dict) -> None:
    """Ensure that each exam's set of questions has properly-formed choices."""
    for choice in question.get("choices", []):
        assert choice.get("id") is not None
        assert isinstance(choice.get("id"), int)
        assert choice.get("text") is not None
        assert isinstance(choice.get("text"), str)


@pytest.mark.parametrize("question", get_questions())
def test_exam_question_prompts_end_with_punctuation(question: dict) -> None:
    """Ensure that each exam's question prompts end with punctuation."""
    punctuation_pattern = re.compile(r"(?:\b|\)|\")[.!?]$")
    assert punctuation_pattern.search(question.get("prompt"))


@pytest.mark.parametrize("question", get_questions())
def test_exam_question_prompts_start_with_capital_letter(question: dict) -> None:
    """Ensure that each exam's question prompts start with a capital letter."""
    assert question.get("prompt")[0].isupper()


@pytest.mark.parametrize("question", get_questions())
def test_exam_question_prompts_fit_in_embed_fields(question: dict) -> None:
    """Ensure that each exam's question prompt is less than or equal to 1024 characters."""
    assert len(question.get("prompt")) <= 1024


@pytest.mark.parametrize("question", get_questions())
def test_exam_question_choices_fit_in_embed_fields(question: dict) -> None:
    """Ensure that each exam's question answer choices is less than or equal to 1024 characters."""
    for choice in question.get("choices"):
        assert len(choice) <= 1024
