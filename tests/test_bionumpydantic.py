#!/usr/bin/env python

"""Tests for `bionumpydantic` package."""
import datetime
import typing
from typing import List

import numpy as np
import pytest
from bionumpy import EncodedRaggedArray
from bionumpy.util.testing import assert_bnpdataclass_equal, assert_encoded_array_equal
from npstructures import RaggedArray
from pydantic import BaseModel

from bionumpydantic.bionumpydantic import BNPModel

d: int = 'hei'

class Example(BNPModel):
    name: str
    age: int
    scores: List[float]
    years: List[int]
    friends: List[str]

class TypingExample(Example):
    date: datetime.datetime


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

@pytest.mark.xfail(reason="Not yet implemented")
def test_pydantic_bnp_table(init_dict):
    """Test the conversion of a Pydantic model to a pydantic bnpdataclass."""
    cls = Example.to_pydantic_table_class()
    assert isinstance(cls, BaseModel)
    cls(**init_dict)
