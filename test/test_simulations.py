
import numpy as np

from src.data.simulations_X import generate_S

def test_generate_S():
    S_manual = np.array(
                [[1.,    0.5,   0.25,  0.125, 0.0625],
                [0.5,   1.,    0.5,   0.25,  0.125 ],
                [0.25,  0.5,   1.,    0.5,   0.25  ],
                [0.125, 0.25,  0.5,   1.,    0.5   ],
                [0.0625,0.125, 0.25,  0.5,   1.    ]]
                )
    S = generate_S(5, correlated=True)
    assert (S == S_manual).all()

    S_manual = np.array(
                [[1.,  1/3,  1/9, 1/27, 1/81],
                [1/3,   1.,  1/3,  1/9, 1/27],
                [1/9,  1/3,   1.,  1/3,  1/9],
                [1/27, 1/9,  1/3,   1.,  1/3],
                [1/81, 1/27, 1/9,  1/3,   1.]]
                )
    S = generate_S(5, correlated=True, power=3)
    assert (S == S_manual).all()

    S_manual = np.eye(5)
    S = generate_S(5, correlated=False)
    assert (S == S_manual).all()
