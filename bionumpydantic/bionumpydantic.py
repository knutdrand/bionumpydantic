"""Main module."""
from pydantic import BaseModel
from dataclasses import dataclass, field, make_dataclass
from bionumpy import bnpdataclass


class BNPModel(BaseModel):

    @classmethod
    def convert_annotations(self) -> dict[str, type]:
        """
        Converts the annotations of the Pydantic model to a dictionary.
        """
        annotations = self.__annotations__
        fields = {name: field.annotation for name, field in self.__fields__.items()}
        return {**annotations, **fields}

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
