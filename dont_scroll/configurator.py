import toml


class Configurator:
    # TODO
    def __init__(self):
        self.config = toml.load(f"{self.config_file}")
