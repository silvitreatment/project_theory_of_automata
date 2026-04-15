"""
Тесты для подпрограммы dfa_recognize и программы find_chains.
Запуск: python3 tests.py
"""

import unittest
from solution import dfa_recognize, find_chains


class TestDfaRecognize(unittest.TestCase):
    """Тесты подпрограммы-распознавателя КА."""

    # --- Допустимые цепочки ---

    def test_empty_inner(self):
        """Пустая внутренняя последовательность: ++"""
        self.assertTrue(dfa_recognize("++"))

    def test_single_a(self):
        """Одна буква a: +a+"""
        self.assertTrue(dfa_recognize("+a+"))

    def test_single_b(self):
        """Одна буква b: +b+"""
        self.assertTrue(dfa_recognize("+b+"))

    def test_different_ab(self):
        """Разные буквы без разделителя: +ab+"""
        self.assertTrue(dfa_recognize("+ab+"))

    def test_different_ba(self):
        """Разные буквы без разделителя: +ba+"""
        self.assertTrue(dfa_recognize("+ba+"))

    def test_same_a_separated(self):
        """Одинаковые a разделены -: +a-a+"""
        self.assertTrue(dfa_recognize("+a-a+"))

    def test_same_b_separated(self):
        """Одинаковые b разделены -: +b-b+"""
        self.assertTrue(dfa_recognize("+b-b+"))

    def test_alternating_no_sep(self):
        """Чередование разных букв: +abab+"""
        self.assertTrue(dfa_recognize("+abab+"))

    def test_long_chain(self):
        """Длинная цепочка из задания: +a-a-ab-b-bab-b+"""
        self.assertTrue(dfa_recognize("+a-a-ab-b-bab-b+"))

    def test_sep_between_different(self):
        """Разделитель между разными символами допустим: +a-b+"""
        self.assertTrue(dfa_recognize("+a-b+"))

    def test_sep_between_different_ba(self):
        """Разделитель между разными символами: +b-a+"""
        self.assertTrue(dfa_recognize("+b-a+"))

    def test_complex_with_sep(self):
        """Сложная цепочка с разделителями: +a-b-a+"""
        self.assertTrue(dfa_recognize("+a-b-a+"))

    # --- Недопустимые цепочки ---

    def test_same_a_no_sep(self):
        """Два одинаковых a без разделителя: +aa+ — недопустимо"""
        self.assertFalse(dfa_recognize("+aa+"))

    def test_same_b_no_sep(self):
        """Два одинаковых b без разделителя: +bb+ — недопустимо"""
        self.assertFalse(dfa_recognize("+bb+"))

    def test_trailing_dash(self):
        """Разделитель перед закрывающим +: +a-+ — недопустимо"""
        self.assertFalse(dfa_recognize("+a-+"))

    def test_leading_dash(self):
        """Разделитель сразу после открывающего +: +-a+ — недопустимо"""
        self.assertFalse(dfa_recognize("+-a+"))

    def test_double_dash(self):
        """Двойной разделитель: +a--a+ — недопустимо"""
        self.assertFalse(dfa_recognize("+a--a+"))

    def test_no_opening_plus(self):
        """Нет открывающего +: a+ — недопустимо"""
        self.assertFalse(dfa_recognize("a+"))

    def test_no_closing_plus(self):
        """Нет закрывающего +: +a — недопустимо"""
        self.assertFalse(dfa_recognize("+a"))

    def test_empty_string(self):
        """Пустая строка — недопустимо"""
        self.assertFalse(dfa_recognize(""))

    def test_single_plus(self):
        """Только один +: + — недопустимо"""
        self.assertFalse(dfa_recognize("+"))

    def test_only_dash(self):
        """Только разделитель: +-+ — недопустимо"""
        self.assertFalse(dfa_recognize("+-+"))

    def test_unknown_symbol(self):
        """Символ вне алфавита: +c+ — недопустимо"""
        self.assertFalse(dfa_recognize("+c+"))


class TestFindChains(unittest.TestCase):
    """Тесты программы поиска цепочек в последовательности."""

    def test_single_empty_chain(self):
        """Одна минимальная цепочка ++"""
        self.assertEqual(find_chains("++"), [(1, "++")])

    def test_single_chain_a(self):
        """Одна цепочка +a+"""
        self.assertEqual(find_chains("+a+"), [(1, "+a+")])

    def test_single_long_chain(self):
        """Одна длинная цепочка из задания"""
        self.assertEqual(find_chains("+a-a-ab-b-bab-b+"), [(1, "+a-a-ab-b-bab-b+")])

    def test_no_chains(self):
        """Нет цепочек языка"""
        self.assertEqual(find_chains("abc"), [])

    def test_no_chains_invalid(self):
        """Недопустимые цепочки не находятся: +aa+"""
        self.assertEqual(find_chains("+aa+"), [])

    def test_no_chains_no_plus(self):
        """Нет открывающего +: aa+bb+"""
        self.assertEqual(find_chains("aa+bb+"), [])

    def test_overlap_closing_is_opening(self):
        """Закрывающий + является открывающим следующей цепочки: ++a+b+"""
        self.assertEqual(find_chains("++a+b+"), [(1, "++"), (2, "+a+"), (4, "+b+")])

    def test_overlap_middle(self):
        """Перекрытие в середине: +a++b+"""
        self.assertEqual(find_chains("+a++b+"), [(1, "+a+"), (3, "++"), (4, "+b+")])

    def test_multiple_chains_with_overlap(self):
        """Несколько цепочек с перекрытием через +: +a-a++b-b+"""
        self.assertEqual(
            find_chains("+a-a++b-b+"), [(1, "+a-a+"), (5, "++"), (6, "+b-b+")]
        )

    def test_foreign_symbols_ignored(self):
        """Символы вне алфавита пропускаются: x+a+y"""
        self.assertEqual(find_chains("x+a+y"), [(2, "+a+")])

    def test_greedy_longest_match(self):
        """Жадный поиск: находит самую длинную цепочку с позиции"""
        # +abab+ длиннее +a+, поэтому должна быть найдена +abab+
        self.assertEqual(find_chains("+abab+"), [(1, "+abab+")])

    def test_no_chains_output(self):
        """Если цепочек нет — список пустой"""
        self.assertEqual(find_chains("+bb+"), [])

    def test_complex_sequence(self):
        """Сложная последовательность с несколькими цепочками"""
        seq = "++a+b+a-a+aa+bb+abab+a-a-ab-b-bab-b+"
        result = find_chains(seq)
        self.assertEqual(
            result,
            [
                (1, "++"),
                (2, "+a+"),
                (4, "+b+"),
                (6, "+a-a+"),
                (16, "+abab+"),
                (21, "+a-a-ab-b-bab-b+"),
            ],
        )

    def test_position_1based(self):
        """Позиция возвращается как 1-based индекс"""
        result = find_chains("x+b+")
        self.assertEqual(result, [(2, "+b+")])

    def test_only_invalid_chains(self):
        """Недопустимые +aa+ и +bb+ не находятся, но ++ на позиции 4 — допустимо"""
        self.assertEqual(find_chains("+aa++bb+"), [(4, "++")])

    def test_truly_no_chains(self):
        """Строка без единой допустимой цепочки: +aa+bb+"""
        self.assertEqual(find_chains("+aa+bb+"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
