from hp8156A import HP8156A
class Agilent8156A(HP8156A):
    def __init__(self,addressString):
        super().__init__(self,addressString)