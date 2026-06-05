"""
core/quiz_engine.py
===================
Step 6 — Validate and score quiz attempts.

Public API
----------
validate_questions(raw: list) -> list[dict]
    Filters an arbitrary list to well-formed MCQ dicts (max 5).

score_attempt(questions: list, answers: dict) -> dict
    Scores a student's answers against the question answer keys.
    answers = {question_index (int or str): "A"|"B"|"C"|"D"}
    Returns {"score", "total", "pct", "correct": [bool], "feedback": [str]}
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)

VALID_ANSWER_LETTERS = {"A", "B", "C", "D"}
MAX_QUESTIONS = 5


def validate_questions(raw: list) -> list[dict]:
    """
    Filter *raw* to well-formed MCQ dicts.

    A valid question has:
      - "question": non-empty string
      - "options": list of exactly 4 non-empty strings
      - "answer": one of "A", "B", "C", "D"

    Returns at most MAX_QUESTIONS items.
    """
    if not isinstance(raw, list):
        return []

    validated: list[dict] = []
    for item in raw:
        if not isinstance(item, dict):
            continue

        question = item.get("question", "")
        options  = item.get("options",  [])
        answer   = str(item.get("answer", "")).strip().upper()

        if not (isinstance(question, str) and question.strip()):
            continue
        if not (isinstance(options, list) and len(options) == 4):
            continue
        if not all(isinstance(o, str) and o.strip() for o in options):
            continue
        if answer not in VALID_ANSWER_LETTERS:
            continue

        validated.append({
            "question":    question.strip(),
            "options":     [str(o).strip() for o in options],
            "answer":      answer,
            "explanation": str(item.get("explanation", "")).strip(),
        })

        if len(validated) == MAX_QUESTIONS:
            break

    return validated


def score_attempt(questions: list[dict], answers: dict) -> dict:
    """
    Score a student's quiz attempt.

    Parameters
    ----------
    questions : list of validated MCQ dicts (from validate_questions or generate_quiz)
    answers   : {question_index: letter}  e.g. {0: "B", 1: "A", 2: "C"}
                Keys may be int or str; letters are normalised to uppercase.

    Returns
    -------
    {
        "score":    int,           # number of correct answers
        "total":    int,           # total questions
        "pct":      float,         # 0.0–100.0
        "correct":  [bool, ...],   # one bool per question
        "feedback": [str, ...],    # one feedback string per question
    }
    """
    if not questions:
        return {"score": 0, "total": 0, "pct": 0.0, "correct": [], "feedback": []}

    correct_flags: list[bool] = []
    feedback_msgs: list[str]  = []

    # Normalise answer keys to int
    normalised_answers: dict[int, str] = {}
    for k, v in answers.items():
        try:
            normalised_answers[int(k)] = str(v).strip().upper()
        except (ValueError, TypeError):
            pass

    for i, q in enumerate(questions):
        correct_letter = q.get("answer", "").upper()
        given_letter   = normalised_answers.get(i, "").upper()

        if given_letter not in VALID_ANSWER_LETTERS:
            # Unanswered
            correct_flags.append(False)
            feedback_msgs.append(
                f"Not answered. Correct answer: {correct_letter}."
            )
            continue

        is_correct = given_letter == correct_letter
        correct_flags.append(is_correct)

        if is_correct:
            feedback_msgs.append("Correct!")
        else:
            # Find the text of the correct option for helpful feedback
            options = q.get("options", [])
            correct_option_text = ""
            letter_index = ord(correct_letter) - ord("A")
            if 0 <= letter_index < len(options):
                correct_option_text = options[letter_index]
            if correct_option_text:
                feedback_msgs.append(
                    f"Incorrect. The correct answer is {correct_letter}: {correct_option_text}"
                )
            else:
                feedback_msgs.append(f"Incorrect. The correct answer is {correct_letter}.")

    score = sum(correct_flags)
    total = len(questions)
    pct   = round(score / total * 100, 1) if total > 0 else 0.0

    return {
        "score":    score,
        "total":    total,
        "pct":      pct,
        "correct":  correct_flags,
        "feedback": feedback_msgs,
    }
