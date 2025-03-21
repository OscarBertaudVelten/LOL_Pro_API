from mwrogue.esports_client import EsportsClient

site = EsportsClient("lol")


def get_attribute_value(data, key, default_value):
    """Helper function to get the value of an attribute, with a fallback to the default value."""
    if isinstance(default_value, bool):
        return data.get(key, default_value) == '1'
    elif isinstance(default_value, int):
        return int(data.get(key, default_value))
    else:
        return data.get(key, default_value)
