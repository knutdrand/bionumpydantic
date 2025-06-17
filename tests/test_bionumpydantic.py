#!/usr/bin/env python

"""Tests for `bionumpydantic` package."""
import numpy as np
import pytest
from bionumpy import EncodedRaggedArray
from bionumpy.util.testing import assert_bnpdataclass_equal, assert_encoded_array_equal

from bionumpydantic.bionumpydantic import BNPModel


class Example(BNPModel):
    name: str
    age: int


@pytest.mark.skip(reason="Not yet implemented")
def test_convert_annotations():
    new_annotations = Example.convert_annotations()
    assert new_annotations['name'] == EncodedRaggedArray
    assert new_annotations['age'] == np.ndarray





def test_pydantic_to_bnpdataclass():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    bnp_class = Example.to_bnpdataclass()
    data = bnp_class(name=['test1', 'test2', 'test13'], age=[25, 30, 35])
    assert_encoded_array_equal(data.name, ['test1', 'test2', 'test13'])
    #assert_bnpdataclass_equal(data, bnp_class(name=['test1', 'test2', 'test13']))

    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
