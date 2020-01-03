# TODO
# get and parse clips from filesystem
# uploader to blob storage
# mounting filesystem
# select and discard x amount of clips per event
# run upload jobs in background
# notification

from teslacam import ( config, filesystem )

config = config.load()
filesystem.read_clips(filesystem.ClipType.SAVED)