
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