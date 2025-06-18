#!/usr/bin/env python

import numpy as np
from bionumpy import EncodedRaggedArray, as_encoded_array
from bionumpy.util.testing import assert_encoded_array_equal
from npstructures import RaggedArray
from npstructures.testing import assert_raggedarray_equal
from pydantic import BaseModel

from bionumpydantic.pydantic_type_wrappers import NumpyNdArray, BnpRaggedArray, BnpEncodedRaggedArray


class NumpyNdArrayExample(BaseModel):
    array: NumpyNdArray

class BnpRaggedExample(BaseModel):
    array: BnpRaggedArray

class BnpEncodedRaggedExample(BaseModel):
    array: BnpEncodedRaggedArray

def test_numpy_array_in_pydantic():
    """Test that a numpy array can be wrapped in a Pydantic model."""
    arr = np.array([1.0, 2.0, 3.0])
    model = NumpyNdArrayExample(array=arr)

    assert isinstance(model.array, np.ndarray)
    assert np.array_equal(model.array, arr)


def test_bnp_ragged_array_in_pydantic():
    """Test that a RaggedArray can be wrapped in a Pydantic model."""
    ragged_arr = RaggedArray([[1.0, 2.0], [3.0]])

    model = BnpRaggedExample(array=ragged_arr)
    assert isinstance(model.array, RaggedArray)
    assert_raggedarray_equal(model.array, ragged_arr)


def test_bnp_ragged_encode_array_in_pydantic():
    """Test that an EncodedRaggedArray can be wrapped in a Pydantic model."""
    encoded_arr = as_encoded_array(["ctt", "actg", "ag"])
    model = BnpEncodedRaggedExample(array=encoded_arr)
    assert isinstance(model.array, EncodedRaggedArray)
    assert_encoded_array_equal(model.array, encoded_arr)


def test_bnp_ragged_array_json_serialization():
    """Test that a RaggedArray can be serialized to JSON."""
    ragged_arr = RaggedArray([[1.0, 2.0], [3.0]])
    model = BnpRaggedExample(array=ragged_arr)

    json_data = model.model_dump()
    assert json_data == {"array":[[1.0,2.0],[3.0]]}


def test_bnp_encoded_ragged_array_json_serialization():
    """Test that an EncodedRaggedArray can be serialized to JSON."""
    encoded_arr = as_encoded_array(["ctt", "actg", "ag"])
    model = BnpEncodedRaggedExample(array=encoded_arr)

    json_data = model.model_dump()
    assert json_data == {"array":["ctt","actg","ag"]}


def test_numpy_array_json_serialization():
    """Test that a numpy array can be serialized to JSON."""
    arr = np.array([1.0, 2.0, 3.0])
    model = NumpyNdArrayExample(array=arr)

    json_data = model.model_dump()
    assert json_data == {"array":[1.0,2.0,3.0]}