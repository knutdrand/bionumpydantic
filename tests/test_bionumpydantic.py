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

from bionumpydantic.bionumpydantic import BNPModel


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






def test_pydantic_to_bnpdataclass():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    bnp_class = Example.to_bnpdataclass()
    data = bnp_class(name=['test1', 'test2', 'test13'], age=[25, 30, 35], scores=[[1.0], [3.0, 4.0], [5.0, 6.0]], years=[[2020], [2021, 2022], [2023]],
                     friends=['Alice', 'Bob', 'Charlie'])
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
