import numpy as np


class BipartiteNetworkGraph:
    def __init__(self, L, R, default_values=0):
        self.s_to_L = default_values * np.ones((L,))  # Edges from s -> L
        self.R_to_T = default_values * np.ones((R,))
        self.L_to_R = default_values * np.ones((L, R))
        self.L = L
        self.R = R
        self.currencies = {}
        self.s, self.t = 0, L + R + 1

    # Sets the weight of an edge
    #   @edge is a tuple (u,v)
    #   @weight is the desired weight to set
    def add_edge(self, edge, weight):
        u, v = edge
        if u == self.s:
            self.s_to_L[v - 1] = weight
        elif v == self.t:
            self.R_to_T[self.t-u] = weight
        else:
            self.L_to_R[u-1, v - self.L - 1] = weight

    def set_currency(self, v, currency):
        self.currencies[v] = currency

    def get_currency(self,v):
        if v in self.currencies:
            return self.currencies[v]
        else:
            return None

    # Returns all edges of the form (v, .)
    def get_out_edges(self, v):
        if v == self.s:
            return self.s_to_L
        elif self.is_in_L(v):
            return self.L_to_R[v,:]
        elif self.is_in_R(v):
            return self.R_to_T
        else:
            return []

    def is_in_R(self, v):
        return len(self.L) < v < len(self.L) + len(self.R) + 1

    def is_in_L(self, v):
        return 1 < v < len(self.L) + 1

    # Returns all edges of the form (.,v)
    def get_in_edges(self, v):
        if v == self.t:
            return self.R_to_T
        elif self.is_in_R(v):
            return self.L_to_R[:,v]
        elif self.is_in_L(v):
            return self.s_to_L
        else:
            return []

    def flatten_matrix(self):
        return self.L_to_R.reshape((self.L_to_R.shape[0] * self.L_to_R.shape[1],))

    def get_L(self):
        return self.L_to_R.shape[0]

    def get_R(self):
        return self.L_to_R.shape[1]
