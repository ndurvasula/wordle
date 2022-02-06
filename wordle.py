import numpy as np

sl = np.load("short_list.npy")
ll = np.load("long_list.npy")

def feedback(i, j):
    s = sl[i]
    l = ll[j]
    ret = np.zeros((2,5))

    M = np.outer(np.ones(5), s) - np.outer(l, np.ones(5)) == 0
    ret[0] = np.diagonal(M).copy()

    M *= np.outer(np.logical_not(ret[0]), np.ones(5, dtype=bool))
    M *= np.outer(np.ones(5, dtype=bool), np.logical_not(ret[0]))

    for k in range(5):
        ret[1, k] = np.any(M[k])
        if ret[1,k]:
            M[:, np.argmax(M[k])] = False

    return ret


def dist(i):
    return np.sum([feedback(i,j) for j in range(ll.shape[0])], axis=0)/ll.shape[0]

