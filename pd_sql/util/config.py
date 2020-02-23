import configparser


def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_config(config, section, name):
    return config[section][name]


