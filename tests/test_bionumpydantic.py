#!/usr/bin/env python

"""Tests for `bionumpydantic` package."""
import datetime
import typing
from typing import List

import numpy as np
import pytest
from bionumpy import EncodedRaggedArray, as_encoded_array
from bionumpy.util.testing import assert_bnpdataclass_equal, assert_encoded_array_equal
from npstructures import RaggedArray
from npstructures.testing import assert_raggedarray_equal
from pydantic import BaseModel, ValidationError, TypeAdapter

from bionumpydantic.bionumpydantic import BNPModel
from bionumpydantic.pydantic_type_wrappers import NumpyNdArray, BnpRaggedArray, BnpEncodedRaggedArray

d: int = 'hei'

class Example(BNPModel):
    name: str
    age: int
    scores: List[float]
    years: List[int]
    friends: List[str]

class TypingExample(Example):
    date: datetime.datetime

class NumpyNdArrayExample(BaseModel):
    array: NumpyNdArray

class BnpRaggedExample(BaseModel):
    array: BnpRaggedArray

class BnpEncodedRaggedExample(BaseModel):
    array: BnpEncodedRaggedArray

# @pytest.mark.xfail(reason="Not yet implemented")
def test_convert_annotations():
    new_annotations = TypingExample.convert_annotations()
    assert new_annotations['name'] == EncodedRaggedArray
    assert new_annotations['age'] == np.ndarray
    assert new_annotations['scores'] == RaggedArray
    assert new_annotations['date'] == typing.Any


@pytest.fixture()
def bnp_class():
    return Example.to_bnpdataclass()

@pytest.fixture()
def init_dict():
    """Create a dictionary with example data."""
    return dict(name=['test1', 'test2', 'test13'], age=[25, 30, 35], scores=[[1.0], [3.0, 4.0], [5.0, 6.0]],
                years=[[2020], [2021, 2022], [2023]], friends=['Alice', 'Bob', 'Charlie'])

@pytest.fixture()
def example_data(bnp_class, init_dict):
    """Create example data for the bnpdataclass."""
    return bnp_class(**init_dict)


def test_pydantic_to_bnpdataclass(bnp_class, example_data):
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    data = example_data
    assert_encoded_array_equal(data.name, ['test1', 'test2', 'test13'])

    true_annotations = {
        'name': EncodedRaggedArray,
        'age': np.ndarray,
        'scores': RaggedArray,
        'years': RaggedArray,
        'friends': EncodedRaggedArray,
        'date': typing.Any
    }
    for name, annotation in bnp_class.__annotations__.items():
        assert true_annotations[name] == annotation, f"Annotation for {name} is {annotation}, expected {true_annotations[name]}"


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

@pytest.mark.xfail(reason="Error converting dict of value to new model")
def test_pydantic_bnp_table(init_dict):
    """Test the conversion of a Pydantic model to a pydantic bnpdataclass.
    name: EncodedRaggedArray
    age: np.ndarray
    scores: RaggedArray
    years: RaggedArray
    friends: EncodedRaggedArray
    """
    cls = Example.to_pydantic_table_class()
    assert issubclass(cls, BaseModel)
    cls(**init_dict)

