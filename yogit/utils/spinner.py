import platform

from yaspin import yaspin, Spinner


def spin(func):
    """
   Wrap yaspin within a decorator then it's easy to disable it.
   """

    def inner(self, *args, **kwargs):
        if platform.system() == "Windows":
            # Avoid unicode char issue
            sp = Spinner(["|", "/", "-", "\\"], 80)
        else:
            sp = Spinner(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"], 80)
        with yaspin(sp, text="Loading...") as spinner:
            func(self, spinner, *args, **kwargs)

    return inner
