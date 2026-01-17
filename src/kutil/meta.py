
class SingletonMeta(type):
    """
    Metaclass that implements the Singleton pattern.

    Ensures that only one instance of the class exists and provides
    a post-initialization hook.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Intercepts class instantiation to return the existing instance 
        or create a new one.

        Args:
            *args: Positional arguments for the class constructor.
            **kwargs: Keyword arguments for the class constructor.

        Returns:
            object: The single instance of the class.
        """

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
            instance.post_init()

        return cls._instances[cls]

    def post_init(self):  # pragma: no cover
        """
        A lifecycle hook to be overridden in classes using this metaclass.
        It is called only once, after the first instantiation.
        """
        pass
