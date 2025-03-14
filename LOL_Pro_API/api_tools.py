def get_attribute_value(data, key, default_value):
    """Helper function to get the value of an attribute, with a fallback to the default value."""
    return data.get(key, default_value)
