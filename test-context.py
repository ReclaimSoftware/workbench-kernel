import unittest
from context import Context

class TestContext(unittest.TestCase):

    def test_Image_in_globals(self):
        s = Context().run_code("repr(Image)")['result']['value']
        assert s.startswith("<class stdlib.Image at ")

    def test_Video_in_globals(self):
        s = Context().run_code("repr(Video)")['result']['value']
        assert s.startswith("<class stdlib.Video at ")

    def test_reset_clears_variables(self):
        c = Context()
        c.run_code("x = 123")
        assert c.run_code("locals().get('x')")['result']['value'] == 123
        c.reset()
        assert c.run_code("locals().get('x')")['result']['type'] == 'NullValue'

    def test_reset_keeps_Video(self):
        c = Context()
        c.reset()
        s = Context().run_code("repr(Video)")['result']['value']
        assert s.startswith("<class stdlib.Video at ")

    def test_run_code(self):
        c = Context()
        assert set(c.run_code("1").keys()) == set(['microseconds', 'result'])

    def test_multiline_ending_with_expression(self):
        c = Context()
        import ast
        assert c.run_code("x = 2\n3")['result']['value'] == 3

    def test_multiline_ending_with_statement(self):
        c = Context()
        assert c.run_code("3\nx = 2")['result']['type'] == 'NullValue'

    def test_Assign_exception(self):
        c = Context()
        assert c.run_code("x = {}['k']")['result']['type'] == 'ErrorValue'

    def test_Expr_exception(self):
        c = Context()
        assert c.run_code("{}['k']")['result']['type'] == 'ErrorValue'

if __name__ == '__main__':
  unittest.main()
