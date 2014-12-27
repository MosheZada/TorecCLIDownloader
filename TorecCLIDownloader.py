#!/usr/bin/env python
from TorecSubtitlesDownloader import TorecSubtitlesDownloader
from SubtitleHelper import log
import os, re, string, time, urllib2, sys
import tempfile
import shutil
import argparse

def DownloadTorecSubtitle(search_string, release, dest_dir):
    subtitles_list = []

    downloader = TorecSubtitlesDownloader()
    metadata = downloader.getSubtitleMetaData(search_string)

    for option in metadata.options:
        if release in option.name:
            subtitles_list.append({'page_id'       : metadata.id,
                                   'filename'      : option.name,
                                   'subtitle_id'   : option.id
                                })

    # If there is one match, download it
    if len(subtitles_list) == 1:
        sub = 0
    else:
        print 'Select sub : '

        for i,sub in enumerate(subtitles_list):
          print '%s) %s' % (i, sub['filename'])

        sub = int(raw_input(' > '))

    page_id = subtitles_list[sub]["page_id"]
    subtitle_id = subtitles_list[sub]["subtitle_id"]
    filename = subtitles_list[sub]["filename"]

    downloader = TorecSubtitlesDownloader()
    downloadLink =  downloader.getDownloadLink(page_id, subtitle_id, False)
    (subtitleData, subtitleName) = downloader.download(downloadLink)
    temp_dir = tempfile.mkdtemp()
    file_name = downloader.saveData('%s/%s' % (temp_dir, filename) , subtitleData, True)
    src = os.path.join(temp_dir,file_name)
    dst = os.path.join(dest_dir,file_name)
    log(__name__, "Moving file to %s" % dst)
    shutil.move(src,dst)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and search Torec subtitles')
    parser.add_argument('--dest', '-d', type=str, default="/tmp/",
            help='Destination directory for saving files')
    parser.add_argument('--release', '-r', type=str, default="",
            help='Search this string in the subtitle name')
    parser.add_argument('search', type=str,
            help='search argument')

    args = parser.parse_args()
    try:
        DownloadTorecSubtitle(args.search, args.release, args.dest)
    except KeyboardInterrupt:
        log(__name__, "Got Ctrl+C exiting")

