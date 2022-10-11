
import unittest

from godculator import calculator


ONE = calculator.OperandItem('1')
TWO = calculator.OperandItem('2')
THREE = calculator.OperandItem('3')
FOUR = calculator.OperandItem('4')
FIVE = calculator.OperandItem('5')
PLUS = calculator.RESERVED_TOKENS['+']
MINUS = calculator.RESERVED_TOKENS['-']
DIV = calculator.RESERVED_TOKENS['/']
TIMES = calculator.RESERVED_TOKENS['*']
POWER = calculator.RESERVED_TOKENS['^']
SIN = calculator.FUNCTIONS['sin']
MAX = calculator.FUNCTIONS['max']
PI = calculator.OperandItem('pi')


class TestParser(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(
            calculator.tokenize("var1"),
            ['var1'])
        self.assertEqual(
            calculator.tokenize("(10a+sin(-15^0.3))/2"),
            ['(', '10', 'a', '+', 'sin', '(', '-', '15', '^', '0.3', ')', ')', '/', '2'])
        self.assertEqual(
            calculator.tokenize("speed = 10km/2.2h"),
            ['speed', '=', '10', 'km', '/', '2.2', 'h'])
        self.assertEqual(
            calculator.tokenize("c3 = 130.8 Hz"),
            ['c3', '=', '130.8', 'Hz'])
        self.assertEqual(
            calculator.tokenize("sin ( max ( 2, 3 ) / 3 * pi )"),
            ['sin', '(', 'max', '(', '2', ',', '3', ')', '/', '3', '*', 'pi', ')'])



    def test_itemize(self):
        items = calculator.itemize(['c3', '=', '130.8', 'Hz'])
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].label, 'c3')
        self.assertEqual(items[1].name, '=')
        self.assertEqual(str(items[2].value), '130.8')
        self.assertEqual(items[2].unit, 'Hz')

        items = calculator.itemize(['sin', '(', 'max', '(', '2', ',', '3', ')',
                                    '/', '3', '*', 'pi', ')'])
        self.assertEqual(len(items), 13)
        self.assertEqual(items[0], calculator.FUNCTIONS['sin'])
        self.assertEqual(items[2], calculator.FUNCTIONS['max'])
        self.assertEqual(items[11].label, 'pi')
        self.assertEqual(str(items[11].value), '3.141')

    def test_postfix_simple(self):
        self.assertEqual(calculator.postfix([TWO, PLUS, THREE]), [TWO, THREE, PLUS])

    def test_postfix_complex(self):
        # 3 + 4 × 2 ÷ ( 1 − 5 ) ^ 2 ^ 3
        calculation = [THREE, PLUS, FOUR, TIMES, TWO, DIV,
                       '(', ONE, MINUS, FIVE, ')',
                       POWER, TWO, POWER, THREE]
        # 3 4 2 × 1 5 − 2 3 ^ ^ ÷ +
        expected = [THREE, FOUR, TWO, TIMES, ONE, FIVE, MINUS, TWO, THREE,
                    POWER, POWER, DIV, PLUS]
        self.assertEqual(calculator.postfix(calculation), expected)

    def test_postfix_with_functions(self):
        # sin ( max ( 2, 3 ) / 3 * pi )
        calculation = [SIN, '(', MAX, '(', TWO, ',', THREE, ')', DIV, THREE, TIMES, PI, ')']
        # 2 3 max 3 / pi * sin
        expected = [TWO, THREE, MAX, THREE, DIV, PI, TIMES, SIN]
        self.assertEqual(calculator.postfix(calculation), expected)




