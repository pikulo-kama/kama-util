

class TestNumberUtil:

    def test_is_float(self):

        from kutil.number import is_float

        assert is_float("Invalid.String") is False
        assert is_float("None") is False
        assert is_float("123") is False
        assert is_float("123.0") is True
        assert is_float("123.") is True
