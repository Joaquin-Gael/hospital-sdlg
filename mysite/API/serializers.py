from django.core.files.base import File
from django.core.files.images import ImageFile
from typing import Optional, List, Dict
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import asyncio

class BaseSerializer:
    def __init__(self, model_class, instance, include_fields=None, exclude_fields=None, deal_for_field_list:dict[str, str]=None):
        self._model_class = model_class
        self._instance = instance
        self._include_fields = include_fields or []
        self._exclude_fields = exclude_fields or []
        self._deal_for_field_list = deal_for_field_list  or {}

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def set_instance(self, new_instance):
        self._instance = new_instance

    @property
    def deal_for_field_list(self):
        return self._deal_for_field_list

    @deal_for_field_list.setter
    def set_deal_for_field_list(self, new_deal_for_field_list: dict[str, str]):
        self._deal_for_field_list = new_deal_for_field_list

    def serialize(self):
        if isinstance(self.instance, list):
            return self._serialize_many(self.instance)
        return self._serialize_single(self.instance)

    def _serialize_single(self, instance):
        json_data = {}
        fields = self.get_fields_to_serialize()

        for field_name in fields:
            if field_name in self._deal_for_field_list.keys():
                value = getattr(instance, self._deal_for_field_list[field_name], None)
            else:
                value = getattr(instance, field_name, None)
            json_data[field_name] = self.serialize_value(value)
        return json_data

    def _serialize_many(self, instances):
        return [self._serialize_single(inst) for inst in instances]

    def get_fields_to_serialize(self):
        all_fields = set(self.get_all_fields())
        if self._include_fields:
            print([field for field in self._include_fields if field in all_fields])
            return [field for field in self._include_fields if field in all_fields]
        elif self._exclude_fields:
            return [field for field in all_fields if field not in self._exclude_fields]
        else:
            return list(all_fields)

    def serialize_value(self, value):
        """Maneja la serialización de valores."""
        if isinstance(value, ImageFile) or isinstance(value, File):
            return value.url if value else None  # Retorna la URL si es un archivo de imagen
        return value  # Retorna el valor como está

    def get_all_fields(self):
        return [field.name for field in self._model_class._meta.fields]

class AsyncBaseSerializer:
    def __init__(self, model_class, instance, include_fields: Optional[List[str]] = None,
                 exclude_fields: Optional[List[str]] = None, deal_for_field_list: Optional[Dict[str, str]] = None):
        self._model_class = model_class
        self._instance = instance
        self._include_fields = include_fields or []
        self._exclude_fields = exclude_fields or []
        self._deal_for_field_list = deal_for_field_list or {}

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, new_instance):
        self._instance = new_instance

    @property
    def deal_for_field_list(self):
        return self._deal_for_field_list

    @deal_for_field_list.setter
    def deal_for_field_list(self, new_deal_for_field_list: Dict[str, str]):
        self._deal_for_field_list = new_deal_for_field_list

    async def serialize(self):
        """Serializa la instancia o una lista de instancias."""
        if isinstance(self.instance, list):
            return await self._serialize_many(self.instance)
        return await self._serialize_single(self.instance)

    async def _serialize_single(self, instance):
        json_data = {}
        fields = await self.get_fields_to_serialize()

        for field_name in fields:
            if field_name in self._deal_for_field_list.keys():
                value = await database_sync_to_async(getattr)(instance, self._deal_for_field_list[field_name], None)
            else:
                value = await database_sync_to_async(getattr)(instance, field_name, None)
            json_data[field_name] = self.serialize_value(value)
        return json_data

    async def _serialize_many(self, instances):
        return await asyncio.gather(*(self._serialize_single(inst) for inst in instances))

    async def get_fields_to_serialize(self):
        all_fields = set(await self.get_all_fields())
        if self._include_fields:
            return [field for field in self._include_fields if field in all_fields]
        elif self._exclude_fields:
            return [field for field in all_fields if field not in self._exclude_fields]
        else:
            return list(all_fields)

    def serialize_value(self, value):
        """Maneja la serialización de valores."""
        if isinstance(value, ImageFile) or isinstance(value, File):
            return value.url if value else None  # Retorna la URL si es un archivo de imagen
        return value  # Retorna el valor como está

    async def get_all_fields(self):
        return await database_sync_to_async(lambda: [field.name for field in self._model_class._meta.fields])()