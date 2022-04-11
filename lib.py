import string, random
import mimetypes
mimetypes.init()


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


VIDEO_EXTENSIONS = tuple(get_extensions_for_type('video'))
AUDIO_EXTENSIONS = tuple(get_extensions_for_type('audio'))
IMAGE_EXTENSIONS = tuple(get_extensions_for_type('image'))


def read_subreddits(file_name='subreddits.txt'):
	file = open(file_name, 'r')
	return file.read().splitlines()


def read_files(dir='input'):
	from os import listdir
	from os.path import isfile, join
	files = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]
	return files


def random_text_generator(size=10, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def get_thumbnail(file_path):
    import subprocess
    ##get thumbnail for the video
    ##once in a while delete the contents of the thumbnail folders, BUT REMEMBER NEVER DELETE THE FOLDER "thumbnails"
    thumbnailPath = "thumbnails/thumbnail_" + random_text_generator() + ".jpg"
    subprocess.call(['ffmpeg', '-i', file_path, '-ss', '00:00:02.000', '-vframes', '1', thumbnailPath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ##if you want to see the output of the ffmpeg in the terminal(delete the one above and uncomment this):
    ##subprocess.call(['ffmpeg', '-i', video, '-ss', '00:00:02.000', '-vframes', '1', thumbnailPath])
    return thumbnailPath