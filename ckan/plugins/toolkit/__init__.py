import future.utils as six

# ckan/common.py:128
def asbool(obj):
    if isinstance(obj, six.string_types):
        obj = obj.strip().lower()
        if obj in truthy:
            return True
        elif obj in falsy:
            return False
        else:
            raise ValueError(u"String is not true/false: {}".format(obj))
    return bool(obj)

# False is easier to hack around than True!
def check_ckan_version(**args):
    return False

# Hack around gettext translation API
def _(arg):
    return arg
