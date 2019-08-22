import platform

from halo import Halo


def get_spinner_object():
    spinner_type = "dots"
    if platform.system() == "Windows":
        # Avoid unicode char issue
        spinner_type = "line"
    return Halo(text="Loading", spinner=spinner_type, color=None)


def spin(func):
    """
   Wrap Halo within a decorator then it's easy to disable it.
   """

    def inner(self, *args, **kwargs):
        with get_spinner_object() as spinner:
            func(self, spinner, *args, **kwargs)

    return inner
