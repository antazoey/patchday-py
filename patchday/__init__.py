def __getattr__(name: str):
    if name == "patchday":
        from patchday.main import patchday

        return patchday

    # Only the root 'patchday' is available here;
    # If using types, import each type respectively from its module.
    raise AttributeError(name)
