import os, sys, re, shutil, subprocess
from pathlib import Path

def check_title(title:str):
    # check if title has ( at end
    if title[-1] == "(":
        title = title[:-1]
    return title

def convert(file: Path, extension = ".mp4"):
    new_file = f"{file.stem}{extension}"
    subprocess.run(f'ffmpeg -i "{file.name}" "{new_file}"', cwd=file.parent)
    return Path(file.parent / new_file)

def move_movie(dir):

    extensions = ['.mkv','.mp4','.avi']
    movies_folder = Path('D:\Movies')
    input_folder = Path(dir)
    os.chdir(input_folder)

    for extension in extensions:
        search = list(input_folder.glob(f"*{extension}"))
        if len(search) > 0:
            file_path = search[0]
            break

    movie_year = re.search("\d\d\d\d", file_path.name)[0]
    movie_title = file_path.name.split(movie_year)[0].replace(".", " ")
    movie_title = check_title(movie_title)

    movie_rename = movie_title + "(" + movie_year + ")" + extension
    file_path.rename(movie_rename)
    file_path = input_folder / movie_rename

    if extension in ['.avi']:
        file_path = convert(file_path)

    shutil.move(file_path, movies_folder)
    os.chdir(input_folder.parent)
    shutil.rmtree(input_folder)

    print("Done: ", file_path.name)

if __name__ == '__main__':
    for folder in sys.argv[1:]:
        move_movie(folder)