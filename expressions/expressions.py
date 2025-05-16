class Expression:
    def __init__(self, operands=()):
        self.operands = tuple(operands)

    def __add__(self, other):
        return Add(self, other if isinstance(other, Expression) else Number(other))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return Sub(self, other if isinstance(other, Expression) else Number(other))

    def __rsub__(self, other):
        return Sub(Number(other), self)

    def __mul__(self, other):
        return Mul(self, other if isinstance(other, Expression) else Number(other))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return Div(self, other if isinstance(other, Expression) else Number(other))

    def __rtruediv__(self, other):
        return Div(Number(other), self)

    def __pow__(self, other):
        return Pow(self, other if isinstance(other, Expression) else Number(other))

    def __rpow__(self, other):
        return Pow(Number(other), self)

class Operator(Expression):
    precedence = None
    symbol = None

    def __repr__(self):
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        left, right = self.operands
        left_str = f"({left})" if left.precedence < self.precedence else str(left)
        right_str = f"({right})" if right.precedence < self.precedence else str(right)
        return f"{left_str} {self.symbol} {right_str}"

class Terminal(Expression):
    precedence = float('inf')

    def __init__(self, value):
        super().__init__(operands=())
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

class Number(Terminal):
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Number value must be a numeric type.")
        super().__init__(value)

class Symbol(Terminal):
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Symbol value must be a string.")
        super().__init__(value)

class Add(Operator):
    precedence = 1
    symbol = '+'

class Sub(Operator):
    precedence = 1
    symbol = '-'

class Mul(Operator):
    precedence = 2
    symbol = '*'

class Div(Operator):
    precedence = 2
    symbol = '/'

class Pow(Operator):
    precedence = 3
    symbol = '^'

def postvisitor(expr, fn, **kwargs):
    '''Visit an Expression in postorder applying a function to every node.

    Parameters
    ----------
    expr: Expression
        The expression to be visited.
    fn: function(node, *o, **kwargs)
        A function to be applied at each node. The function should take
        the node to be visited as its first argument, and the results of
        visiting its operands as any further positional arguments. Any
        additional information that the visitor requires can be passed in
        as keyword arguments.
    **kwargs:
        Any additional keyword arguments to be passed to fn.
    '''
    visited = {}
    stack = [expr]
    result_stack = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        if all(c in visited for c in node.operands):
            visited[node] = fn(node, *(visited[c] for c in node.operands), **kwargs)
            result_stack.append(visited[node])
        else:
            stack.append(node)
            for child in reversed(node.operands):
                if child not in visited:
                    stack.append(child)

    return visited[expr]

__all__ = ["Expression", "Number", "Symbol", "Add", "Sub", "Mul", "Div", "Pow"]

