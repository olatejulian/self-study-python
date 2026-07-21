class Registry:
    def __init__(self) -> None:
        self._providers: dict[type[object], dict[str, object]] = {}

    def register(self, dependency: type[object], **kwargs: object) -> object:
        self._providers[dependency] = kwargs

        return self

    def resolve[T](self, dependency: type[T]) -> T:
        target = self._providers.get(dependency)

        if target is None:
            raise ValueError(f"Dependency {dependency} is not registered")

        dependencies: dict[str, object] = {}
        for key, value in target.items():
            dependencies[key] = self.resolve(type(value))

        return dependency(**dependencies)
