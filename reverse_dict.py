
from __future__ import annotations
import os
import sys

from pathlib import Path
from typing import TYPE_CHECKING

import ujson as json


sys.path.append(str(Path(__file__).absolute().parent))
if TYPE_CHECKING:
    import typing

from collections.abc import Reversible
from typing import Any


class ReverseDict(dict, Reversible):
    """
    A simple class to represent a reversible sequence.
    This is used to ensure that the order of elements can be reversed.
    """

    _inverse: dict[str, Any] | None = None

    def __init__(self, *args: Any, **kwds: Any):
        super().__init__(*args, **kwds)
        self._keys = list(self.keys())
        self._values = list(self.values())
        self._inverse_items = zip(self._values, self._keys)

    @property
    def inverse(self):
        """
        Returns a dictionary with keys and values swapped.
        If the inverse has not been created yet, it will be created.
        """
        if self._inverse is None:
            _inverse = {}
            for item in self._inverse_items:
                _inverse[item[0]] = item[1]
            self._inverse = _inverse
        return self._inverse

    def __contains__(self, key: Any) -> bool:
        """
        Check if the key exists in the dictionary.
        If the key is not found, return False.
        """
        return key in self._keys or key in self.inverse

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set the value for the given key.
        If the key already exists, update its value.
        """
        if key not in self._keys:
            self._keys.append(key)
            self._values.append(value)
        super().__setitem__(key, value)

    def __delitem__(self, key: Any) -> None:
        """
        Delete the key-value pair for the given key.
        If the key does not exist, raise KeyError.
        """
        if key in self._keys:
            super().__delitem__(key)
            index = self._keys.index(key)
            del self._keys[index]
            del self._values[index]
        else:
            raise KeyError(f"Key {key} not found in ReverseDict.")

    def invert(self):
        """
        Invert the dictionary, swapping keys and values.
        This will create a new ReverseDict with the inverted key-value pairs.
        """
        inverted_dict = ReverseDict()
        for key, value in self.items():
            inverted_dict[value] = key
        return inverted_dict

    def __getitem__(self, key: Any) -> Any:
        """
        Get the value for the given key.
        If the key is not found, raise KeyError.
        """
        if key in self._keys:
            return super().__getitem__(key)
        if key in self.inverse:
            return self.inverse[key]
        raise KeyError(f"Key {key} not found in ReverseDict.")
