from yaspin import yaspin


def spin(func):
    """
    Wrap yaspin within a decorator then it's easy to disable it.
    """

    def inner(self, *args, **kwargs):
        with yaspin(text="Loading..."):
            func(self, *args, **kwargs)

    return inner
