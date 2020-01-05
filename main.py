# TODO
# get and parse clips from filesystem
# uploader to blob storage
# mounting filesystem
# select and discard x amount of clips per event
# run upload jobs in background
# notification

from teslacam import ( config )
from teslacam.enums import ClipType
from teslacam.filesystem import Filesystem

config = config.load()
fs = Filesystem(config)

for type in [ClipType.SAVED, ClipType.SENTRY]:
    clips = fs.read_clips(type)
    print(clips)