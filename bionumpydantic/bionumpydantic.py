"""Main module."""
import typing

from pydantic import BaseModel
from dataclasses import dataclass, field, make_dataclass
from bionumpy import bnpdataclass
from sphinx.builders.html import return_codes_re


def get_type_mapping_bnp() -> dict[type, type]:
    from bionumpy.encoded_array import EncodedRaggedArray, RaggedArray
    import numpy as np

    return {
        int: np.ndarray,
        str: EncodedRaggedArray,
        float: np.ndarray,
        bool: np.ndarray,
        typing.List[int]: RaggedArray,
        typing.List[float]: RaggedArray,
        typing.List[str]: EncodedRaggedArray,
        typing.List[bool]: RaggedArray,
    }


class BNPModel(BaseModel):

    @classmethod
    def convert_annotations(self) -> dict[str, type]:
        """
        Converts the annotations of the Pydantic model to a dictionary.
        """

        TYPE_MAPPING = get_type_mapping_bnp()

        dict_annotations = {}
        for name, field in self.__fields__.items():
            test = field.annotation
            try:
                dict_annotations[name] = TYPE_MAPPING[field.annotation]
            except KeyError:
                dict_annotations[name] = typing.Any
        return dict_annotations

    @classmethod
    def to_dataclass(cls):
        annotations = cls.__annotations__
        fields = [(name, f.annotation) for name, f in cls.__fields__.items()]
        # fields = [(name, field.default if name in cls.__fields__ else field.default_factory) for name in
        #          annotations]

        return make_dataclass(
            __class__.__name__,
            fields,
            bases=(object,),
            namespace={'__annotations__': annotations}
        )

    @classmethod
    def to_bnpdataclass(cls):
        """
        Converts the Pydantic model to a bnpdataclass.
        """
        from bionumpy.bnpdataclass import bnpdataclass
        return bnpdataclass(cls.to_dataclass())
