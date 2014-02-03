import unittest
from stdlib import Video, Image, MediaServer

class TestImage(unittest.TestCase):

    def setUp(self):
        MediaServer.stub('mask-o2', {
            'image_id': 'mask-o2',
            'width': 1280,
            'height': 720
        })

    def test_properties(self):
        image = Image('mask-o2')
        assert image.image_id == 'mask-o2'
        assert image.width == 1280
        assert image.height == 720

    def test_toJSON(self):
        assert Image('mask-o2').toJSON() == {
            'type': 'ImageValue',
            'image_id': 'mask-o2',
            'width': 1280,
            'height': 720
        }


class TestVideo(unittest.TestCase):

    def setUp(self):
        MediaServer.stub('o2', {
            'video_id': 'o2',
            'width': 1280,
            'height': 720,
            'num_frames': 124290,
            'fps': 119.88
        })
        MediaServer.stub('t0', {
            'video_id': 't0',
            'width': 1920,
            'height': 1440,
            'num_frames': 33472,
            'fps': 47.95
        })

    def test_properties(self):
        video = Video('o2')
        assert video.video_id == 'o2'
        assert video.width == 1280
        assert video.height == 720
        assert video.first_frame_index == 0
        assert video.num_frames == 124290
        assert video.fps == 119.88

    def test_toJSON(self):
        assert Video('t0').toJSON() == {
            'type': 'VideoValue',
            'video_id': 't0',
            'width': 1920,
            'height': 1440,
            'first_frame_index': 0,
            'num_frames': 33472,
            'fps': 47.95
        }

    def test_frame(self):
        video = Video('o2')
        frame = video[3]
        assert isinstance(frame, Video)
        assert frame.width == 1280
        assert frame.height == 720
        assert frame.first_frame_index == 3
        assert frame.num_frames == 1
        assert frame.fps == 119.88

    def test_last_frame_via_negative(self):
        assert Video('o2')[-1].first_frame_index == 124290 - 1

    def test_first_frame_via_negative(self):
        assert Video('o2')[-124290].first_frame_index == 0

    def test_frame_bounds_fail(self):
        try:
            Video('o2')[124290]
        except IndexError, e:
            if e.message == 'frame index out of range':
                return
        assert False

    def test_frame_bounds_fail_via_negative(self):
        try:
            Video('o2')[-124291]
        except IndexError, e:
            if e.message == 'frame index out of range':
                return
        assert False


if __name__ == '__main__':
  unittest.main()
