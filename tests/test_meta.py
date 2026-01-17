import pytest
from unittest.mock import MagicMock

from pytest_mock import MockerFixture


# Assuming SingletonMeta is in kutil.singleton
# from kutil.singleton import SingletonMeta

class TestSingletonMeta:

    @pytest.fixture(autouse=True)
    def _setup(self):
        """
        Ensures the singleton registry is empty before and after each test.
        """

        from kutil.meta import SingletonMeta

        SingletonMeta._instances.clear()
        yield
        SingletonMeta._instances.clear()

    def test_singleton_identity(self):
        """
        Tests that two calls to the constructor return the exact same object ID.
        """

        from kutil.meta import SingletonMeta

        class DatabaseConnection(metaclass=SingletonMeta):
            def post_init(self):
                pass

        instance1 = DatabaseConnection()
        instance2 = DatabaseConnection()

        assert instance1 is instance2
        assert id(instance1) == id(instance2)

    def test_post_init_called_only_once(self, mocker: MockerFixture):
        """
        Tests that post_init is triggered on first init but not on subsequent calls.
        """

        from kutil.meta import SingletonMeta

        class Service(metaclass=SingletonMeta):
            def post_init(self): pass

        post_init_mock = mocker.patch.object(Service, "post_init")

        Service()
        assert post_init_mock.call_count == 1

        Service()
        # Still 1, because it's a singleton
        assert post_init_mock.call_count == 1

    def test_different_classes_have_different_instances(self):
        """
        Tests that the metaclass tracks instances per class type.
        """

        from kutil.meta import SingletonMeta

        class Logger(metaclass=SingletonMeta):
            def post_init(self): pass

        class Config(metaclass=SingletonMeta):
            def post_init(self): pass

        logger = Logger()
        config = Config()

        assert logger is not config
        assert isinstance(logger, Logger)
        assert isinstance(config, Config)

    def test_init_args_ignored_on_subsequent_calls(self):
        """
        Tests that only the first set of args is used for the instance.
        """

        from kutil.meta import SingletonMeta

        class User(metaclass=SingletonMeta):
            def __init__(self, name):
                self.name = name

            def post_init(self): pass

        user1 = User("Alice")
        user2 = User("Bob")

        assert user1.name == "Alice"
        assert user2.name == "Alice"
        assert user1 is user2
