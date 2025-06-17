"""Main module."""
import typing

from pydantic import BaseModel, create_model
from dataclasses import dataclass, field, make_dataclass
from bionumpy.bnpdataclass import bnpdataclass, BNPDataClass
from bionumpy.encoded_array import EncodedRaggedArray, RaggedArray
import numpy as np

from bionumpydantic.pydantic_type_wrappers import NumpyNdArray, BnpEncodedRaggedArray, BnpRaggedArray


TYPE_MAPPING = {
    int: {
        'wrapper_name': NumpyNdArray,
        'name': np.ndarray,
    },
    str: {
        'wrapper_name': BnpEncodedRaggedArray,
        'name': EncodedRaggedArray,
    },
    float: {
        'wrapper_name': NumpyNdArray,
        'name': np.ndarray,
    },
    bool: {
        'wrapper_name': NumpyNdArray,
        'name': np.ndarray,
    },
    typing.List[int]: {
        'wrapper_name': BnpRaggedArray,
        'name': RaggedArray,
    },
    typing.List[float]: {
        'wrapper_name': BnpRaggedArray,
        'name': RaggedArray,
    },
    typing.List[str]: {
        'wrapper_name': BnpEncodedRaggedArray,
        'name': EncodedRaggedArray,
    },
    typing.List[bool]: {
        'wrapper_name': BnpRaggedArray,
        'name': RaggedArray,
    },
}


class BNPModel(BaseModel):

    @classmethod
    def convert_annotations(self, wrapper_name = False) -> dict[str, type]:
        """
        Converts the annotations of the Pydantic model to a dictionary.
        """

        dict_annotations = {}
        for name, field in self.model_fields.items():
            try:
                if wrapper_name:
                    dict_annotations[name] = TYPE_MAPPING[field.annotation]['wrapper_name']
                else:
                    dict_annotations[name] = TYPE_MAPPING[field.annotation]['name']
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
        dc = bnpdataclass(cls.to_dataclass())
        dc.__annotations__ = cls.convert_annotations()
        return dc

    @classmethod
    def to_pydantic_table_class(cls) -> type[BaseModel]:
        dict_wrapper_name = cls.convert_annotations(wrapper_name = True)
        PydanticModel = create_model(cls.__name__, **dict_wrapper_name, __base__ = BaseModel)
        return PydanticModel

