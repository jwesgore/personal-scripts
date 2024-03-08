'''
script for batch renaming movie files and moving them to movies folder
'''

import os, sys, re, shutil, subprocess
from pathlib import Path

movies_folder = Path('D:\Movies')
extensions = ['.mkv','.mp4','.avi']
convert_if_extension = ['.avi']

def check_title(title:str) -> str:
    '''special checks for errors in title'''
    # check if title has ( at end
    if title[-1] == "(":
        title = title[:-1]
    return title

def convert(movie_path: Path, extension = ".mp4") -> Path:
    '''convert movie to different file format using ffmpeg'''
    new_file = f"{movie_path.stem}{extension}"
    subprocess.run(f'ffmpeg -i "{movie_path.name}" "{new_file}"', cwd=movie_path.parent)
    return movie_path.parent / new_file

def input_is_directory(input_folder:Path) -> Path:
    '''search directory for movie file if movie is dir'''

    for extension in extensions:
        search = list(input_folder.glob(f"*{extension}"))
        if len(search) > 0:
            return search[0]
        
def get_subtitle_track(input_file:Path):
    '''search for subtitle track'''
    search = list(input_file.parent.glob("*.srt"))
    if len(search) > 0:
        return search[0]
    else:
        return False
    
def move_movie(arg:Path):

    # search for movie file and subtitles
    if arg.is_dir():
        movie_file = input_is_directory(arg)
    else:
        movie_file = arg

    subtitle_track = get_subtitle_track(movie_file)

    os.chdir(movie_file.parent)

    # build new movie name
    movie_year = re.search("\d\d\d\d", movie_file.name)[0]
    movie_title = movie_file.name.split(movie_year)[0].replace(".", " ")
    movie_title = check_title(movie_title)
    movie_rename = movie_title + "(" + movie_year + ")" + movie_file.suffix

    # rename file
    movie_file = movie_file.parent / movie_file.rename(movie_rename)
    
    if subtitle_track:
        subtitle_track = subtitle_track.parent / subtitle_track.rename(movie_file.stem)

    # convert file
    if movie_file.suffix in convert_if_extension:
        movie_file = convert(movie_file)
   
    # move file and subtitle track
    shutil.move(movie_file, movies_folder)

    if subtitle_track:
        shutil.move(subtitle_track, movies_folder)

    # delete parent dir if input is dir
    if arg.is_dir():
        os.chdir(movie_file.parents[1])
        shutil.rmtree(movie_file.parent)

    print("Done: ", movie_file.name)

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        move_movie(Path(arg))