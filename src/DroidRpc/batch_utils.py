# Contains utility functions for preparing data for batch streaming

__author__ = "LORA Technologies"
__email__ = "asklora@loratechai.com"

from typing import Iterable
from io import BytesIO
import numpy as np

def array_to_bytes(array: Iterable):
    if isinstance(array, np.ndarray):
        output = BytesIO()
        np.save(output, array, allow_pickle=False)
        return output.getvalue()
    if isinstance(array, list):
        raise NotImplementedError("List serialiser not yet implemented!")
    if isinstance(array, tuple):
        raise NotImplementedError("Tuple serialiser not yet implemented!")
