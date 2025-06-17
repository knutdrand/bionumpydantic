#!/usr/bin/env python

"""Tests for `bionumpydantic` package."""
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

@pytest.mark.xfail(reason="Not yet implemented")
def test_convert_annotations():
    new_annotations = Example.convert_annotations()
    assert new_annotations['name'] == EncodedRaggedArray
    assert new_annotations['age'] == np.ndarray
    assert new_annotations['scores'] == RaggedArray






def test_pydantic_to_bnpdataclass():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    bnp_class = Example.to_bnpdataclass()
    data = bnp_class(name=['test1', 'test2', 'test13'], age=[25, 30, 35], scores=[[1.0], [3.0, 4.0], [5.0, 6.0]], years=[[2020], [2021, 2022], [2023]],
                    friends=['Alice', 'Bob', 'Charlie'])
    assert_encoded_array_equal(data.name, ['test1', 'test2', 'test13'])
    #assert_bnpdataclass_equal(data, bnp_class(name=['test1', 'test2', 'test13']))

    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
