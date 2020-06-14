import os
import subprocess

import pytube

def make(songName, id):
    yt = pytube.YouTube("https://www.youtube.com/watch?v=" + id)

    vids = yt.streams.all()
    mp4Num = 0

    for i in range(len(vids)):
      if vids[i].abr == '128kbps' and vids[i].mime_type == 'audio/mp4':
        mp4Num = i

    vnum = mp4Num

    parent_dir = "d:/" #다운받을 곳
    vids[vnum].download(parent_dir)

    new_filename = songName + '.mp3'

    default_filename = vids[vnum].default_filename
    subprocess.call(['ffmpeg', '-i', #이것이 mp3로 변환하는 부분이다. ffmpeg 변환파일이 필요하다.
                     os.path.join(parent_dir, default_filename),
                     os.path.join(parent_dir, new_filename)
                     ])

    print("the end: ".join(id))
