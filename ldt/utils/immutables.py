"""Custom immutable objects."""

__all__ = ('FrozenDict', 'ImmutableConfig')


class FrozenDict():
    """Immutable dict following the frozenset semantics."""

    def __init__(self, config):
        self._container = config

    def __setitem__(self, key, value):
        """Set method used for testing."""
        raise Exception('Cannot assign value to a FrozenDict')

    def __getitem__(self, key):
        return self._container[key]

    def __contains__(self, key):
        return key in self._container

    def keys(self):
        return self._container.keys()

    def values(self):
        return self._container.values()

    def items(self):
        return self._container.items()


class ImmutableConfig(FrozenDict):
    """Immutable Configuration.

    Converts an input dict (of dict(s)) to a FrozenDict (of FrozenDict(s))
    """

    def __init__(self, config):
        """Constructor."""
        if not isinstance(config, dict):
            raise Exception(
                'ImmutableConfig requires instance of dict as input parameter')
        super().__init__(self._freeze(config))

    def _get_frozen_value(self, input_value):
        if isinstance(input_value, dict):
            for key, value in input_value.items():
                if isinstance(value, dict):
                    input_value[key] = self._get_frozen_value(value)
            return FrozenDict(input_value)
        return input_value

    def _freeze(self, config):
        """Convert all dicts in config to FrozenDicts."""
        frozen_config = {}
        for key, value in config.items():
            frozen_config[key] = self._get_frozen_value(value)
        return FrozenDict(frozen_config)
