**A server for executing workbench notebook code fragments**


### Running the server

    python2.7 server.py --port 8000


### Interface

This is a temporary interface with some crazy simplifying assumptions:

* There is no authentication or security (so we only listen on localhost!)
* Only one notebook is active at a time
* Only one HTTP request is active at a time

Requests must include a `Content-Length` header.

#### POST /api/reset

Request body: `{}`

Response body: `{}`

#### POST /api/execute

Request body:
```json
{
  "inputs": [
    "stuff = {}",
    "stuff['k']"
  ]
}
```

Response body:
```json
{
  "execution_results": [
    {
      "microseconds": 39,
      "result": {"type": "NullValue"}
    },
    {
      "microseconds": 47,
      "result": {
        "type": "ErrorValue",
        "name": "KeyError",
        "message": "k"
      }
    }
  ]
}
```


### Implementation

    server.py
      main
    
    context.py
      Context:        .run_code(), .reset(), maintain locals and globals
    
    stdlib.py
      Video, Image:   these get added to Context's globals
    
    value_repr.py
      value_repr:     Python value -> {"type": "FooValue", ...}


### Value Representations

    NullValue
    StringValue       value
    NumberValue       value
    BooleanValue      value
    ArrayValue        value: [...value representations...]
    DictionaryValue   value: {unicode -> value representations}

    ReprValue         repr

    ImageValue        image_id, width, height
    VideoValue        video_id, width, height, first_frame_index, num_frames, fps

    InlineImageValue  width, height, data64, ext: "png"


### matplotlib rendering

matplotlib is not required.

But if the final line of an evaluated code fragment evaluates to any of the following forms, the figure will be rendered and returned as a high-resolution `InlineImageValue`:

    <matplotlib.figure.Figure object ...>     e.g. from "fig"
    <matplotlib.axes.AxesSubplot object ...>  e.g. from "ax"
    <matplotlib.text.Text object ...>         e.g. from "ax.set_title('foo')"
    [<matplotlib.lines.Line2D object...>]     e.g. from "ax.plot(x, y, 'r')"


### Python 3

Pull requests welcome. This ought to support both, but that's far from the top of my TODO list.


### Copyright

Copyright (c) 2014 Andrew Schaaf and https://github.com/ReclaimSoftware/workbench-kernel contributors.

All contributions from Andrew Schaaf are released under the AGPLv3 (see [the license file](LICENSE-AGPLv3.txt)).

All contributions from other project contributors are released under both the AGPLv3 and the Apache 2 license.

This project might become 100% Apache-licensed in the future, but it hasn't yet.
