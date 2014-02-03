from base64 import b64encode
from cStringIO import StringIO

def value_repr(value):

    if hasattr(value, 'toJSON'):
        return value.toJSON()

    if value is None:
        return {'type': 'NullValue'}

    if (value is True) or (value is False):
        return {'type': 'BooleanValue', 'value': value}

    if (
            isinstance(value, int) or
            isinstance(value, long) or
            isinstance(value, float)):
        return {'type': 'NumberValue', 'value': value}

    if isinstance(value, unicode):
        return {'type': 'StringValue', 'value': value}

    if isinstance(value, str):
        try:
            return {'type': 'StringValue', 'value': unicode(value, 'ascii')}
        except UnicodeDecodeError:
            pass

    if isinstance(value, Exception):
        attributes = {
            'type': 'ErrorValue',
            'name': value.__class__.__name__,
        }
        if hasattr(value, 'message'):
            attributes['message'] = value.message
        return attributes

    figure = detect_matplotlib_figure(value)
    if figure:
        return {
            'type': 'InlineImageValue',
            'ext': 'png',
            'data64': b64encode(matplotlib_figure_png(figure))
        }

    if isinstance(value, list) or isinstance(value, tuple):
        return {
            'type': 'ArrayValue',
            'value': [value_repr(element) for element in value]
        }

    if isinstance(value, dict):
        pairs = []
        for k, v in value.items():
            if isinstance(k, str):
                try:
                    k = unicode(k, 'ascii')
                except UnicodeDecodeError:
                    return {'type': 'ReprValue', 'repr': repr(value)}
            if not isinstance(k, unicode):
                return {'type': 'ReprValue', 'repr': repr(value)}
            pairs.append([k, value_repr(v)])
        return {
            'type': 'DictionaryValue',
            'value': dict(pairs)
        }

    return {'type': 'ReprValue', 'repr': repr(value)}


def matplotlib_figure_png(figure, dpi=400):
    f = StringIO()
    figure.savefig(f, dpi=dpi, format='png')
    f.seek(0)
    return f.read()


def detect_matplotlib_figure(value):
    if not hasattr(value, '__class__'):
        return None

    class_str = str(value.__class__)
    if class_str == "<class 'matplotlib.figure.Figure'>":
        return value
    if class_str in [
            "<class 'matplotlib.axes.AxesSubplot'>",
            "<class 'matplotlib.text.Text'>"]:
        return value.figure
    if (
            isinstance(value, list) and
            len(value) == 1 and
            (str(value[0].__class__) == "<class 'matplotlib.lines.Line2D'>")):
        return value[0].figure

    return None
