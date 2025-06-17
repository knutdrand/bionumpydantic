"""Main module."""
import typing

from pydantic import BaseModel
from dataclasses import dataclass, field, make_dataclass
from bionumpy.bnpdataclass import bnpdataclass, BNPDataClass
from bionumpy.encoded_array import EncodedRaggedArray, RaggedArray
import numpy as np


TYPE_MAPPING = {
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

        dict_annotations = {}
        for name, field in self.model_fields.items():
            try:
                dict_annotations[name] = TYPE_MAPPING[field.annotation]
            except KeyError:
                dict_annotations[name] = typing.Any
        return dict_annotations

    @classmethod
    def to_dataclass(cls) -> type:
        annotations = cls.__annotations__
        fields = [(name, f.annotation) for name, f in cls.model_fields.items()]
        return make_dataclass(
            __class__.__name__,
            fields,
            bases=(object,),
            namespace={'__annotations__': annotations}
        )

    @classmethod
    def to_bnpdataclass(cls) -> type[BNPDataClass]:
        """
        Converts the Pydantic model to a bnpdataclass.
        """
        dc =  bnpdataclass(cls.to_dataclass())
        dc.__annotations__ = cls.convert_annotations()
        return dc

    @classmethod
    def to_pydantic_table_class(cls) -> type[BaseModel]:
        raise NotImplementedError
