import unittest
from value_repr import value_repr

class TestValueRepr(unittest.TestCase):

    def test_toJSON(self):
        class Foo:
            def toJSON(self):
                return {'x': 123}
        foo = Foo()
        assert value_repr(foo) == {'x': 123}

    def test_None(self):
        assert value_repr(None) == {
            'type': 'NullValue'
        }

    def test_True(self):
        assert value_repr(True) == {
            'type': 'BooleanValue',
            'value': True
        }

    def test_False(self):
        assert value_repr(False) == {
            'type': 'BooleanValue',
            'value': False
        }

    def test_int(self):
        assert value_repr(123) == {
            'type': 'NumberValue',
            'value': 123
        }

    def test_long(self):
        assert value_repr(2**65) == {
            'type': 'NumberValue',
            'value': 36893488147419103232L
        }

    def test_float(self):
        assert value_repr(1.23) == {
            'type': 'NumberValue',
            'value': 1.23
        }

    def test_unicode(self):
        assert value_repr(u'foo') == {
            'type': 'StringValue',
            'value': u'foo'
        }

    def test_ascii(self):
        assert value_repr('foo') == {
            'type': 'StringValue',
            'value': u'foo'
        }

    def test_exception(self):
        assert value_repr(IOError('oh noes!')) == {
            'type': 'ErrorValue',
            'name': 'IOError',
            'message': 'oh noes!'
        }

    def test_list(self):
        assert value_repr([123]) == {
            'type': 'ArrayValue',
            'value': [
                {
                    'type': 'NumberValue',
                    'value': 123
                }
            ]
        }

    def test_tuple(self):
        assert value_repr((123,)) == {
            'type': 'ArrayValue',
            'value': [
                {
                    'type': 'NumberValue',
                    'value': 123
                }
            ]
        }

    def test_dict(self):
        assert value_repr({u'foo': u'bar'}) == {
            'type': 'DictionaryValue',
            'value': {
                u'foo': {
                    'type': 'StringValue',
                    'value': u'bar'
                }
            }
        }

    def test_dict_with_ascii_keys(self):
        assert value_repr({'foo': u'bar'}) == {
            'type': 'DictionaryValue',
            'value': {
                u'foo': {
                    'type': 'StringValue',
                    'value': u'bar'
                }
            }
        }

    def test_dict_with_non_ascii_str_keys(self):
        assert value_repr({u'\u2014'.encode('utf8'): u'bar'}) == {
            'type': 'ReprValue',
            'repr': "{'\\xe2\\x80\\x94': u'bar'}"
        }

    def test_dict_with_int_keys(self):
        assert value_repr({123: u'bar'}) == {
            'type': 'ReprValue',
            'repr': "{123: u'bar'}"
        }

    def test_other(self):
        assert value_repr(list) == {
            'type': 'ReprValue',
            'repr': "<type 'list'>"
        }


if __name__ == '__main__':
  unittest.main()
