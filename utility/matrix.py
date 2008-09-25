def exp(prev, terms):
    return prev + reduce(lambda c, v: c*v, terms, 1.0)

def dot(a, b):
    return reduce(exp, zip(a, b), 0)

def identity(dim):
    def i(index):
        if index % (dim+1) == 0: return 1.0
        else: return 0.0
    
    matrix = Matrix(dim, dim)
    matrix.matrix = [i(index) for index in range(dim*dim)]

    return matrix

class Matrix:
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.matrix = [0.0 for row in range(self.height) for width in range(self.width)]

    def rows(self):
        rows = []
        for row in range(self.height):
            columns = []
            for column in range(self.width):
                index = column*self.height + row
                columns.append(self.matrix[index])
            rows.append(columns)

        return rows

    def columns(self):
        columns = []
        for column in range(self.width):
            rows = []
            for row in range(self.height):
                index = column*self.height + row
                rows.append(self.matrix[index])
            columns.append(rows)

        return columns

    def __repr__(self):
        rep = ''
        for row in self.rows():
            rep += str(row) + '\n'

        return rep

    def __mul__(self, other):
        result = Matrix(self.height, other.width)
        index = 0
        rows = self.rows()
        for column in other.columns():
            for row in rows:
                result.matrix[index] = dot(column, row)
                index += 1

        return result

    def __rmul__(self, other):
        self.matrix = (self * other).matrix
