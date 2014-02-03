import ast, _ast, time
from stdlib import Image, Video
from value_repr import value_repr

class Context:

    def __init__(self):
        self.reset()

    def reset(self):
        self.globals = {
            'Image': Image,
            'Video': Video
        }
        self.locals = {}

    def run_code(self, code):
        result = None
        body = ast.parse(code).body
        t0 = time.time()
        try:
            assert len(body) == 1# TODO: multi-line
            node = ast.parse(code).body[0]
            if isinstance(node, _ast.Expr):
                result = eval(code, self.globals, self.locals)
            else:
                exec(code, self.globals, self.locals)
        except Exception, e:
            result = e
        microseconds = int((time.time() - t0) * 1000000)
        return {
            'microseconds': microseconds,
            'result': value_repr(result)
        }
