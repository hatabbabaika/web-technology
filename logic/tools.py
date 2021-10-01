from uuid import UUID


def is_uuid(value):
    if isinstance(value, UUID):
        return True
    if not value:
        return False
    try:
        UUID(value)
    except Exception:
        return False
    return True
