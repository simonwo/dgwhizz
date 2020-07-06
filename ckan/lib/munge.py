# ckan/lib/munge.py:121
def munge_tag(tag):
    tag = substitute_ascii_equivalents(tag)
    tag = tag.lower().strip()
    tag = re.sub(r'[^a-zA-Z0-9\- ]', '', tag).replace(' ', '-')
    tag = _munge_to_length(tag, model.MIN_TAG_LENGTH, model.MAX_TAG_LENGTH)
    return tag
