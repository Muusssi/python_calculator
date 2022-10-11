
from decimal import Decimal, InvalidOperation
import math



OPERATORS_TOKENS = ('-', '+', '/', '*', '=', '!', '^')

ORGANISERS = ('(', ')', ',')

SIMPLE_TOKENS = OPERATORS_TOKENS + ORGANISERS + (' ',)

DIGITS = '0123456789.'


class CalculationSyntaxError(Exception):
    pass


VARIABLES = {
    'pi': Decimal('3.141'),
}



class OperandItem():
    def __init__(self, label):
        self.label = label
        self.value = None
        if self.label in VARIABLES:
            self.value = VARIABLES[label]
        else:
            try:
                self.value = Decimal(label)
            except InvalidOperation:
                pass

        self.unit = None

    def set_unit(self, unit_label):
        self.unit = unit_label

    def __repr__(self):
        if self.unit:
            return f'{self.value} [{self.unit}]'
        return str(self.value)

class OperatorItem():
    def __init__(self, name, precedence, associativity='LEFT'):
        self.name = name
        self.precedence = precedence
        self.associativity = associativity

    def __repr__(self):
        return self.name

class FunctionItem():
    def __init__(self, name, n_args=1):
        self.name = name
        self.n_args = n_args

    def __repr__(self):
        return f'{self.name}()'

    def evaluate(self, stack):
        raise NotImplementedError(f"{self.name}() is not implemented")


RESERVED_TOKENS = {
    '^': OperatorItem('^', 4, 'RIGHT'),
    '*': OperatorItem('*', 3),
    '/': OperatorItem('/', 3),
    '-': OperatorItem('-', 2),
    '+': OperatorItem('+', 2),
    '=': OperatorItem('=', 1),
    '(': '(',
    ')': ')',
    ',': ',',
}

FUNCTIONS = {
    'sin': FunctionItem('sin'),
    'cos': FunctionItem('cos'),
    'tan': FunctionItem('tan'),
    'max': FunctionItem('max'),
    'min': FunctionItem('min'),
}


def _has_postfix_precedence(o1, o2):
    """
    there is an operator o2 other than the left parenthesis at the top
    of the operator stack, and (o2 has greater precedence than o1
    or they have the same precedence and o1 is left-associative)
    """
    if o2 != '(' and (o2.precedence > o1.precedence or (o2.precedence == o1.precedence and o1.associativity == 'LEFT')):
        return True
    return False

def postfix(items):
    # https://en.wikipedia.org/wiki/Shunting_yard_algorithm
    stack = []
    operator_stack = []
    for item in items:
        if isinstance(item, OperandItem):
            stack.append(item)
        elif isinstance(item, FunctionItem):
            operator_stack.append(item)
        elif isinstance(item, OperatorItem):
            while operator_stack and _has_postfix_precedence(item, operator_stack[-1]):
                stack.append(operator_stack.pop())
            operator_stack.append(item)
        elif item == '(':
            operator_stack.append(item)
        elif item == ')':
            # There is something fishy here
            while operator_stack and operator_stack[-1] != '(':
                stack.append(operator_stack.pop())
                if not operator_stack:
                    raise CalculationSyntaxError('Mismatched parenthesis')
            if operator_stack[-1] == '(':
                operator_stack.pop()
            else:
                raise CalculationSyntaxError('Mismatched parenthesis')
            if operator_stack and isinstance(operator_stack[-1], FunctionItem):
                stack.append(operator_stack.pop())
    while operator_stack:
        stack.append(operator_stack.pop())
    return stack


def itemize(tokens):
    items = []
    for token in tokens:
        if token == '(' and items and isinstance(items[-1], OperandItem):
            if not items[-1].unit and items[-1].label in FUNCTIONS:
                items.append(FUNCTIONS[items.pop().label])
        if token in RESERVED_TOKENS:
            items.append(RESERVED_TOKENS[token])
        elif items and isinstance(items[-1], OperandItem):
            items[-1].set_unit(token)
        else:
            items.append(OperandItem(token))
    return items

def is_number_token(token):
    if not token:
        return False
    for character in token:
        if character not in DIGITS:
            return False
    return True

def tokenize(string):
    tokens = []
    current_token = ''
    for character in string:
        if character in SIMPLE_TOKENS:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            if not character.isspace():
                tokens.append(character)
        elif is_number_token(current_token) and character not in DIGITS:
            tokens.append(current_token)
            current_token = character
        else:
            current_token += character
    if current_token:
        tokens.append(current_token)
    return tokens


def main():
    OperandItem('pi')
    #Decimal('3.141')


if __name__ == '__main__':
    main()
