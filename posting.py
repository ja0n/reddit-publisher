# run: pip3 install praw
# and install ffmpeg from here https://www.ffmpeg.org/

import praw, praw.models, time
from prawcore.exceptions import ResponseException
import lib


# Read subreddits from file
subreddits = lib.read_subreddits()
print('Subreddits:', subreddits)

TITLE_POST = 'title'
TITLE_URL_POST = 'title_url'
TITLE_TEXT_POST = 'title_text'
IMAGE_POST = 'image'
GALLERY_POST = 'gallery'
VIDEO_POST = 'video'
POST_TYPES = [TITLE_POST, TITLE_URL_POST, TITLE_TEXT_POST, IMAGE_POST, GALLERY_POST, VIDEO_POST]


# TODO: mark as nsfw
# TODO: clear thumbnails folder
def process_files(files, title, thumbnail=True):
	post_data = []
	file_types = {'image': [], 'video': []}

	for file in files:
		[_, extension] = file.rsplit('.', 1)
		extension = f'.{extension}'
		if extension in lib.IMAGE_EXTENSIONS:
			file_types['image'].append(file)
		elif extension in lib.VIDEO_EXTENSIONS:
			file_types['video'].append(file)

	if len(file_types['image']) == 1:
		post_data.append({
			'type': IMAGE_POST,
			'title': title,
			'image_path': file_types['image'][0],
		})
	elif len(file_types['image']) > 1:
		post_data.append({
			'type': GALLERY_POST,
			'title': title,
			'gallery': [
				{'image_path': file} for file in file_types['image']
			]
		})

	for file in file_types['video']:
		data = {
			'type': VIDEO_POST,
			'title': title,
			'video_path': file,
		}
		if thumbnail:
			data['thumbnail'] = lib.get_thumbnail(file)
		post_data.append(data)

	return post_data


def submit_post(subreddit, post_data, nsfw=False):
	post_type = post_data['type']
	title = post_data['title']

	if post_type == "title":
		subreddit.submit(title, selftext="")
	elif post_type == "titleurl":
		subreddit.submit(title, url=post_data['url'])
	elif post_type == "titletext":
		subreddit.submit(title, selftext=post_data['text'])
	elif post_type == "image":
		subreddit.submit_image(title, post_data['image_path'], nsfw=nsfw)
	elif post_type == "video":
		if post_data.get('thumbnail'):
			subreddit.submit_video(
				title, post_data['video_path'],
				thumbnail_path=post_data['thumbnail'],
				nsfw=nsfw,
			)
		else:
			subreddit.submit_video(title, post_data['video_path'], nsfw=nsfw)
	elif post_type == "gallery":
		subreddit.submit_gallery(title, post_data['gallery'], nfsw=nsfw)


def authenticate():
	reddit = praw.Reddit()
	reddit.validate_on_submit = True

	try:
		user = reddit.user.me()
		if not user:
			raise EnvironmentError('Unable to authenticate')
		print("Authenticated as {}".format(user))
		return reddit
	except Exception:
		print("Something went wrong during authentication")
		raise


def post(reddit, post_data_list, subreddits=subreddits, nsfw=False):
	print("Posting...")
	for subred in subreddits:
		subreddit = reddit.subreddit(subred)
		for post_data in post_data_list:
			submit_post(subreddit, post_data, nsfw)
			print(f'Posting {post_data} on {subreddit}')
			time.sleep(1)
	print("Posted!")


def input_post_data(thumbnail=True):
	title = input('Insert the title: ')
	print('available post types: {allowed_post_types}')
	post_type = input('Insert the post type: ') or 'title'

	if post_type not in POST_TYPES:
		print('ERROR: invalid post type')
		exit()
	if post_type == TITLE_TEXT_POST:
		text = input('Insert text: \n')
		return {'title': title, 'text': text}
	elif post_type == TITLE_URL_POST:
		url = input('Insert url: ')
		return {'title': title, 'url': url}