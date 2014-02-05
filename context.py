import ast, _ast, time
from stdlib import Image, Video
from value_repr import value_repr
from upstream.codegen.codegen import to_source

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
        t0 = time.time()
        try:
            for node in ast.parse(code).body:
                node_code = to_source(node)
                if isinstance(node, _ast.Expr):
                    result = eval(node_code, self.globals, self.locals)
                else:
                    exec(node_code, self.globals, self.locals)
                    result = None
        except Exception, e:
            result = e
        microseconds = int((time.time() - t0) * 1000000)
        return {
            'microseconds': microseconds,
            'result': value_repr(result)
        }
