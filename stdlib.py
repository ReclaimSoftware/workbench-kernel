import urllib2, json
from copy import deepcopy


class MediaServer:
    stubbed = {}

    @classmethod
    def stub(self, id, attributes):
        self.stubbed[id] = attributes

    @classmethod
    def get_attributes(self, plural, singular, id):
        if id in self.stubbed:
            return deepcopy(self.stubbed[id])
        # TODO
        url = "http://localhost:3002/%s/%s.json" % (plural, id)
        attributes = json.loads(urllib2.urlopen(url).read())[singular]
        attributes["%s_id" % singular] = id
        # TODO: KeyError on 404
        return attributes


class ImageOrVideo:

    @property
    def width(self):
        return self.attributes['width']

    @property
    def height(self):
        return self.attributes['height']

    def toJSON(self):
        return self.attributes


class Image(ImageOrVideo):

    def __init__(self, id):
        self.attributes = MediaServer.get_attributes('images', 'image', id)
        self.attributes['type'] = 'ImageValue'

    @property
    def image_id(self):
        return self.attributes['image_id']


class Video(ImageOrVideo):

    def __init__(self, id, first_frame_index=0, num_frames=None, _attributes=None):
        """
        _attributes is private. When you slice a video, there's no need for another media server query.
        """
        if _attributes is None:
            _attributes = MediaServer.get_attributes('videos', 'video', id)
        self.attributes = _attributes
        # TODO: validate first_frame_index, num_frames
        self.attributes['type'] = 'VideoValue'
        self.attributes['first_frame_index'] = first_frame_index
        if num_frames is not None:
            self.attributes['num_frames'] = num_frames

    def __len__(self):
        return self.num_frames

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                key = len(self) + key
                if key < 0:
                    raise IndexError("frame index out of range")
            if (key - self.first_frame_index) >= self.num_frames:
                raise IndexError("frame index out of range")
            return Video(
                        self.video_id,
                        first_frame_index=(self.first_frame_index + key),
                        num_frames=1,
                        _attributes=deepcopy(self.attributes))
        # stop: exclusive
        #       assert selector.step is None
        #       # selector.start, selector.stop, selector.step
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    @property
    def video_id(self):
        return self.attributes['video_id']

    @property
    def first_frame_index(self):
        return self.attributes['first_frame_index']

    @property
    def num_frames(self):
        return self.attributes['num_frames']

    @property
    def fps(self):
        return self.attributes['fps']
