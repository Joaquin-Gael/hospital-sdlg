from django.core.files.base import File
from django.core.files.images import ImageFile
from typing import Any
from types import FunctionType

class BaseSerializer:
    def __init__(self, model_class, instance, include_fields=None, exclude_fields=None, deal_for_field_list:dict[str, str]=None):
        self.model_class = model_class
        self.instance = instance
        self.include_fields = include_fields or []
        self.exclude_fields = exclude_fields or []
        self.deal_for_field_list = deal_for_field_list  or {}

    def serialize(self):
        if isinstance(self.instance, list):
            return self._serialize_many(self.instance)
        return self._serialize_single(self.instance)

    def _serialize_single(self, instance):
        json_data = {}
        fields = self.get_fields_to_serialize()

        for field_name in fields:
            if field_name in self.deal_for_field_list.keys():
                value = getattr(instance, self.deal_for_field_list[field_name], None)
            else:
                value = getattr(instance, field_name, None)
            json_data[field_name] = self.serialize_value(value)
        return json_data

    def _serialize_many(self, instances):
        return [self._serialize_single(inst) for inst in instances]

    def get_fields_to_serialize(self):
        all_fields = set(self.get_all_fields())
        if self.include_fields:
            print([field for field in self.include_fields if field in all_fields])
            return [field for field in self.include_fields if field in all_fields]
        elif self.exclude_fields:
            return [field for field in all_fields if field not in self.exclude_fields]
        else:
            return list(all_fields)

    def serialize_value(self, value):
        """Maneja la serialización de valores."""
        if isinstance(value, ImageFile) or isinstance(value, File):
            return value.url if value else None  # Retorna la URL si es un archivo de imagen
        return value  # Retorna el valor como está

    def get_all_fields(self):
        return [field.name for field in self.model_class._meta.fields]
