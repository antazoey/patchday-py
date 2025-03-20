def __getattr__(name):
    from .main import patchday

    return getattr(patchday, name)
