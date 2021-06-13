import unittest

from utils.audio_trim import get_segments_as_duration, get_true_audio_segments


class AudioTrimGetTrueAudioSegmentsTest(unittest.TestCase):
    def test_in_middle(self):
        value = [
            (5, 10), (15, 20)
        ]
        duration = 30
        expected = [
            (0, 5), (10, 15), (20, 30)
        ]
        result = get_true_audio_segments(value, duration)

        self.assertListEqual(expected, result)

    def test_at_beginning(self):
        value = [
            (0, 10), (15, 20)
        ]
        duration = 30
        expected = [
            (10, 15), (20, 30)
        ]
        result = get_true_audio_segments(value, duration)

        self.assertListEqual(expected, result)

    def test_at_end(self):
        value = [
            (5, 10), (15, 30)
        ]
        duration = 30
        expected = [
            (0, 5), (10, 15),
        ]
        result = get_true_audio_segments(value, duration)

        self.assertListEqual(expected, result)

    def test_two_start_and_end_at_same_time(self):
        value = [
            (5, 10), (10, 20)
        ]
        duration = 30
        expected = [
            (0, 5), (20, 30),
        ]
        result = get_true_audio_segments(value, duration)

        self.assertListEqual(expected, result)

    def test_same_time_on_one_segment(self):
        value = [
            (5, 10), (12, 12), (15, 20)
        ]
        duration = 30
        expected = [
            (0, 5), (10, 12), (12, 15), (20, 30),
        ]
        result = get_true_audio_segments(value, duration)

        self.assertListEqual(expected, result)


class AudioTrimGetSegmentsAsDuration(unittest.TestCase):
    def test_get_correct_value(self):
        value = [
            (5, 10), (15, 20), (20, 30)
        ]
        expected = [
            (5, 5), (15, 5), (20, 10)
        ]
        result = get_segments_as_duration(value)

        self.assertListEqual(expected, result)
