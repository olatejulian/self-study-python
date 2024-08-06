from typing import Optional
from pydantic.main import ModelMetaclass

class AllFieldsOptional(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})

        for base in bases:
            optionals = {key: Optional[value] if not key.startswith('__') else value for key, value in base.__annotations__.items()}

            annotations.update(optionals)

        namespaces['__annotations__'] = annotations

        return super().__new__(self, name, bases, namespaces, **kwargs)
