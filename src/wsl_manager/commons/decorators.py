from models import System


def raise_if_system_is_running(f):
    def wrapper(*args, **kw):
        for arg in args:
            if isinstance(arg, System) and arg.running:
                raise RuntimeError(f"System {arg.name} is running")
        return f(*args, **kw)

    return wrapper
