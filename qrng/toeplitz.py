import numpy as np


class Toeplitz:
    def __init__(self, token, in_nbits: int, out_nbits: int) -> None:
        self.token = token
        self.token_bits = np.zeros(2*in_nbits, dtype=np.int64)

        self.in_nbits = in_nbits
        self.out_nbits = out_nbits

        self.matrix = np.empty((out_nbits, in_nbits), dtype=np.int64)

        self.handle_token()
        self.build_matrix()


    def handle_token(self):
        i = -1
        for b in bin(self.token[0])[:1:-1]:
            (b == '1') and self.token_bits.__setitem__(i, 1)
            i -= 1

        i = -self.in_nbits - 1
        for b in bin(self.token[1])[2:]:
            (b == '1') and self.token_bits.__setitem__(i, 1)
            i -= 1

    def build_matrix(self):
        for i in range(self.out_nbits):
            self.matrix[i, :] = self.token_bits[(self.in_nbits - i):(2*self.in_nbits - i)]
