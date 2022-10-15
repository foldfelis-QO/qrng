import numpy as np


class Toeplitz:
    def __init__(self, token, in_nbits: int, out_nbits: int) -> None:
        self.token = token
        self.token_bits = np.append(
            np.frombuffer(np.binary_repr(token[1], width=16).encode(), dtype='u1').astype(int)[::-1],
            np.frombuffer(np.binary_repr(token[0], width=16).encode(), dtype='u1').astype(int)
        ) - 48

        self.in_nbits = in_nbits
        self.out_nbits = out_nbits

        self.matrix = np.empty((out_nbits, in_nbits), dtype=np.int64)
        self.build_matrix()

    def build_matrix(self) -> None:
        for i in range(self.out_nbits):
            self.matrix[i, :] = self.token_bits[(self.in_nbits - i):(2*self.in_nbits - i)]

    def hash(self, n) -> int:
        bits = np.frombuffer(np.binary_repr(n, width=self.in_nbits).encode(), dtype='u1').astype(int) - 48
        hash_bits = np.matmul(self.matrix, bits) % 2

        return hash_bits.dot(2**np.arange(hash_bits.size)[::-1])
