import unittest

from lib import read_files
import posting

expected_post_data = [
	{
		'type': posting.GALLERY_POST,
		'title': 'Test',
		'gallery': [
            {"image_path":"input/test.gif"},
            {"image_path":"input/seen.png"},
            {"image_path":"input/test.jpg"},
        ]
	},
	{
		'type': posting.VIDEO_POST,
		'title': 'Test',
		'video_path': 'input/test.mp4',
		# 'thumbnail': 'thumbnails/frfrfr.png'
	},
]

test_post_data = [
    {
		'type': posting.TITLE_TEXT_POST,
		'title': 'Test title',
		'text': 'testing',
	},
	{
		'type': posting.TITLE_URL_POST,
		'title': 'Test title',
		'url': 'https://testing.site/',
	},
	{
		'type': posting.IMAGE_POST,
		'title': 'Test image',
		'image_path': 'input/seen.png',
	},
	{
		'type': posting.IMAGE_POST,
		'title': 'Test image',
		'image_path': 'input/test.gif',
	},
] + expected_post_data

class TestPosting(unittest.TestCase):

    def test_posting_data_formatter(self):
        post_data = posting.process_files(read_files('input'), 'Test', False)
        print(post_data)
        self.assertEqual(expected_post_data, post_data)

if __name__ == '__main__':
    unittest.main()