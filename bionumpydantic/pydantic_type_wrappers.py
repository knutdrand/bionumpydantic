import typing

import typing

from bionumpy import as_encoded_array
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from bionumpy.encoded_array import EncodedRaggedArray, RaggedArray
import numpy as np

class NumpyNdArray:
    """
    A Pydantic annotation for NumPy ndarrays.
    """

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: typing.Any,
            _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Add ndarray support to Pydantic.
        """
        def validate_ndarray(value, info):
            return np.asanyarray(value)

        return core_schema.json_or_python_schema(
            json_schema=core_schema.list_schema(),
            python_schema=core_schema.with_info_plain_validator_function(validate_ndarray),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.tolist()
            )
        )


NumpyNdArray = typing.Annotated[np.ndarray, NumpyNdArray]

class BnpRaggedArray:
    """
    A Pydantic annotation for RaggedArray.
    """

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: typing.Any,
            _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Add RaggedArray support to Pydantic.
        """
        return core_schema.json_or_python_schema(
            json_schema=core_schema.list_schema(),
            #python_schema=core_schema.is_instance_schema(RaggedArray),
            python_schema=core_schema.with_info_plain_validator_function(lambda value, info: RaggedArray(value)),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.tolist()
            )
        )

BnpRaggedArray = typing.Annotated[RaggedArray, BnpRaggedArray]

class BnpEncodedRaggedArray:
    """
    A Pydantic annotation for EncodedRaggedArray.
    """

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: typing.Any,
            _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Add EncodedRaggedArray support to Pydantic.
        """
        return core_schema.json_or_python_schema(
            json_schema=core_schema.list_schema(),
            #python_schema=core_schema.is_instance_schema(EncodedRaggedArray),
            python_schema=core_schema.with_info_plain_validator_function(lambda value, info: as_encoded_array(value)),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.tolist()
            )
        )

BnpEncodedRaggedArray = typing.Annotated[EncodedRaggedArray, BnpEncodedRaggedArray]
