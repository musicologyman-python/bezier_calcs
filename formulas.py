from sympy import sympify, diff, Matrix, init_printing, Symbol, solve

init_printing()

bernstein_polynomial = sympify('binomial(n, k) * t**k * (1 - t)**(n - k)')
cubic_bernstein_polynomial = bernstein_polynomial.subs({'n': 3})

def get_cubic_bernstein_polynomial(k):
    return cubic_bernstein_polynomial.subs({'k': k})

def get_cubic_bezier():
    p = [Symbol(f'P_{i}') for i in range(4)]
    return sum([b3.subs({'k': i}) * p[i] for i in range(4)])

def get_cubic_bezier_first_derivative():
    return diff(get_cubic_bezier, 't')

class Point():
    
    def __init__(self, x: float, y:float):
        self.x = x
        self.y = y
        print(f'Point.__init__({self.x}, {self.y})')
    
    def to_matrix(self):
        return Matrix([ self.x, self.y ])
    
    def __add__(self, other):
        match other:
            case Point():
                return Point(self.x + other.x, self.y + other.y)
            case _:
                raise TypeError
                
    def __sub__(self, other):
        match other:
            case Point():
                return Point(self.x - other.x, self.y - other.y)
            case _:
                raise TypeError
                
    def __str__(self):
        # return f'{self.x}, {self.y}'
        return self.__repr__()
    
    
    def __repr__(self):
        return f'{self.__class__.__name__}(x = {self.x}, y={self.y})'
                

