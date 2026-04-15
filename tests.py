"""
Тесты для подпрограммы dfa_recognize и программы find_chains.
Запуск: pytest tests.py
        pytest tests.py -v          # подробный вывод
        pytest tests.py -v --tb=short  # с кратким трейсбеком
"""

import pytest
from solution import dfa_recognize, find_chains


# ---------------------------------------------------------------
# Тесты подпрограммы-распознавателя КА
# ---------------------------------------------------------------


class TestDfaRecognize:
    """Тесты подпрограммы dfa_recognize."""

    @pytest.mark.parametrize(
        "chain",
        [
            "++",
            "+a+",
            "+b+",
            "+ab+",
            "+ba+",
            "+a-a+",
            "+b-b+",
            "+abab+",
            "+a-a-ab-b-bab-b+",
            "+a-b+",
            "+b-a+",
            "+a-b-a+",
            "+a-a-b+",
            "+b-b-a+",
        ],
    )
    def test_valid(self, chain: str) -> None:
        """Допустимые цепочки языка должны распознаваться как True."""
        assert (
            dfa_recognize(chain) is True
        ), f"Цепочка {chain!r} должна принадлежать языку"

    @pytest.mark.parametrize(
        "chain",
        [
            "+aa+",
            "+bb+",
            "+a-+",
            "+-a+",
            "+a--a+",
            "+a--b+",
            "a+",
            "+a",
            "",
            "+",
            "+-+",
            "+c+",
            "+aab+",
            "+abb+",
        ],
    )
    def test_invalid(self, chain: str) -> None:
        """Недопустимые цепочки должны распознаваться как False."""
        assert (
            dfa_recognize(chain) is False
        ), f"Цепочка {chain!r} не должна принадлежать языку"


# ---------------------------------------------------------------
# Тесты программы поиска цепочек
# ---------------------------------------------------------------


class TestFindChains:
    """Тесты программы find_chains."""

    @pytest.mark.parametrize(
        "sequence, expected",
        [
            ("++", [(1, "++")]),
            ("+a+", [(1, "+a+")]),
            ("+b+", [(1, "+b+")]),
            ("+abab+", [(1, "+abab+")]),
            ("+a-a-ab-b-bab-b+", [(1, "+a-a-ab-b-bab-b+")]),
            ("+a-b-a+", [(1, "+a-b-a+")]),
            ("x+a+y", [(2, "+a+")]),
            ("x+b+", [(2, "+b+")]),
            ("++a+b+", [(1, "++"), (2, "+a+"), (4, "+b+")]),
            ("+a++b+", [(1, "+a+"), (3, "++"), (4, "+b+")]),
            ("+a-a++b-b+", [(1, "+a-a+"), (5, "++"), (6, "+b-b+")]),
            ("+aa++bb+", [(4, "++")]),
            (
                "++a+b+a-a+aa+bb+abab+a-a-ab-b-bab-b+",
                [
                    (1, "++"),
                    (2, "+a+"),
                    (4, "+b+"),
                    (6, "+a-a+"),
                    (16, "+abab+"),
                    (21, "+a-a-ab-b-bab-b+"),
                ],
            ),
        ],
        ids=[
            "минимальная_++",
            "одна_a",
            "одна_b",
            "чередование_abab",
            "длинная_из_задания",
            "дефис_между_разными",
            "чужой_символ_слева",
            "чужой_символ_справа",
            "перекрытие_++a+b+",
            "перекрытие_+a++b+",
            "перекрытие_+a-a++b-b+",
            "невалидные_с_валидной_внутри",
            "сложная_последовательность",
        ],
    )
    def test_found(self, sequence: str, expected: list) -> None:
        """Цепочки языка находятся корректно."""
        result = find_chains(sequence)
        assert result == expected, (
            f"\nВход:     {sequence!r}\n"
            f"Получено: {result}\n"
            f"Ожидалось:{expected}"
        )

    @pytest.mark.parametrize(
        "sequence",
        [
            "",
            "abc",
            "+aa+",
            "+bb+",
            "aa+bb+",
            "+aa+bb+",
            "+",
        ],
        ids=[
            "пустая_строка",
            "нет_плюсов",
            "только_+aa+",
            "только_+bb+",
            "нет_открывающего_плюса",
            "обе_невалидные",
            "одиночный_плюс",
        ],
    )
    def test_not_found(self, sequence: str) -> None:
        """Если цепочек нет — возвращается пустой список."""
        result = find_chains(sequence)
        assert result == [], (
            f"\nВход:     {sequence!r}\n" f"Получено: {result}\n" f"Ожидалось: []"
        )
