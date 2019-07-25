import platform

from halo import Halo


def spin(func):
    """
   Wrap Halo within a decorator then it's easy to disable it.
   """

    def inner(self, *args, **kwargs):
        spinner_type = "dots"
        if platform.system() == "Windows":
            # Avoid unicode char issue
            spinner_type = "line"
        with Halo(text="Loading", spinner=spinner_type, color=None) as spinner:
            func(self, spinner, *args, **kwargs)

    return inner
