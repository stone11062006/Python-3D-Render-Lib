from Renderer.OrigineVector import OrigineVector, math, Axe

class Matrix:

    def __init__(self, matrix=([[1]])):

        if isinstance(matrix, Matrix):
            self.matrix = matrix.matrix
        else:
            self.matrix = matrix

        self.row = len(self.matrix)
        self.column = len(self.matrix[0])
    
    def MultiplyBy(self, matrix):
        MRow = len(matrix.matrix)
        MColumn = len(matrix.matrix[0])
        result = [[o for o in range(matrix.column)] for l in range(self.row)]
        if self.column == matrix.row:
            for i  in range(self.row):
                for j in range(matrix.column):
                    sum = 0
                    for k in range(self.column):
                        sum += self.matrix[i][k] * matrix.matrix[k][j]
                    result[i][j] = sum
        return result





class RotationMatix(Matrix):

    def __init__(self, axe: Axe, angle: float,  origineVector: OrigineVector, useOrigineVector=False):

        self.axe = axe
        self.angle = angle

        if not useOrigineVector:
            self.matrix = self.Matrix()
        else:
            self.origineVector = origineVector
            c = math.cos(self.angle)
            s = math.sin(self.angle)
            vector = self.origineVector.GetOrigineVector(self.axe)
            x = vector.normalizedComp.x
            y = vector.normalizedComp.y
            z = vector.normalizedComp.z
            self.vectorMatix = Matrix([[c + math.pow(x,2) * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
                                         [y * x * (1 - c) + z * s, c + math.pow(y,2) * (1 - c), y * z * (1 - c) - x * s],
                                         [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + math.pow(z,2) * (1 - c)]])
            
            self.matrix = self.vectorMatix
        Matrix.__init__(self, self.matrix)
    
    def Matrix(self):
        if self.axe == Axe.X:
            matrix = Matrix([[1, 0, 0], 
                               [0, math.cos(self.angle), -math.sin(self.angle)], 
                               [0, math.sin(self.angle), math.cos(self.angle)]])
        if self.axe == Axe.Y:
            matrix = Matrix([[math.cos(self.angle), 0, math.sin(self.angle)], 
                               [0, 1, 0], 
                               [-math.sin(self.angle), 0, math.cos(self.angle)]])
        if self.axe == Axe.Z:
            matrix = Matrix([[math.cos(self.angle), -math.sin(self.angle), 0], 
                               [math.sin(self.angle), math.cos(self.angle), 0], 
                               [0, 0, 1]])
        return matrix
    
     