import subprocess
import argparse
import os
import math
from typing import Union, List



def valid_video_filename(value: str) -> bool:
    video_formats = ["mp4", "flv"]
    vid_ext = os.path.splitext(value)[1]
    return vid_ext[1:] in video_formats



def speed_up_audio(audio_before_filename: str, audio_after_filename: str, audio_speed: float):
    # if audio_speed < 0.5
    atempo_filter = []

    if audio_speed > 2:
        cur_audio_speed = audio_speed
        twos_inside = 0
        while cur_audio_speed % 2 == 0:
            twos_inside += 1
            cur_audio_speed %= 2

        atempo_filter.extend(["atempo=2" for _ in range(twos_inside)])
        atempo_filter.extend([f"atempo={math.sqrt(cur_audio_speed):.4f}" for _ in range(2)])
    elif audio_speed < 0.5:
        raise Exception(f"Invalid audio speed: {audio_speed}")
    else:
        atempo_filter.extend(["atempo=2"])

    atempo_filter_str = '"' + ','.join(atempo_filter) + '"'

    if not os.path.exists(os.path.dirname(audio_after_filename)):
        os.makedirs(os.path.dirname(audio_after_filename))
    command = ["ffmpeg", "-i", audio_before_filename, "-filter:a", atempo_filter_str, '-q:a',  '100', '-vn', audio_after_filename]
    print(" ".join(command))
    subprocess.call(" ".join(command))


def source_folder_exists(folder: str) -> str:
    if os.path.exists(folder) and os.path.isfile(folder):
        raise argparse.ArgumentTypeError(f"{folder} is not a valid directory")
    if not os.path.exists(folder):
        raise argparse.ArgumentTypeError(f"{folder} does not exist")

    return folder


def is_valid_output_audio_format(value: str) -> str:
    if value not in ('mp3', 'wav'):
        raise argparse.ArgumentTypeError(f"{value} is not mp3 or wav")

    return value


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_folder", type=source_folder_exists, default="input", help="Source directory (default: %(default)s)")
    parser.add_argument("--output_folder", type=str, default="output", help="Output directory (default: %(default)s)")
    parser.add_argument("--audio_multiplier", type=float, default=1, help="Multiple audio speed by numbers >= 0.5 (default: %(default)s)")
    parser.add_argument("--output_audio_format", type=is_valid_output_audio_format, default='mp3', help="Audio format to extract (default: %(default)s)" )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    audio_multiplier = args.audio_multiplier

    input_folder = os.path.join(args.source_folder)
    output_folder = os.path.join(args.output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_audio_format = args.output_audio_format
    ########################################################

    # first extract
    video_filenames = []

    for (dirpath, dirnames, filenames) in os.walk(input_folder):
        full_filenames = [os.path.join(dirpath, fn) for fn in filenames]
        # drops all the files in source folder that are not valid video filenames
        valid_full_filenames = filter(valid_video_filename, full_filenames)
        video_filenames.extend(valid_full_filenames)

    print(video_filenames)
    for video_fn in video_filenames:
        fn, ext = os.path.splitext(video_fn)

        output_fn = os.path.join(output_folder, os.sep.join(fn.split(os.sep)[1:]))
        # look in output directory to see if it already exists
        if output_audio_format == "mp3" and os.path.exists(output_fn + '.mp3'):
            continue
        elif output_audio_format == "wav" and os.path.exists(output_fn + '.wav'):
            continue

        # extract audio
        command = []
        if output_audio_format == "mp3":
            command.extend(["ffmpeg", "-i", video_fn, "-vn"])
            command.extend(["-acodec", "libmp3lame"])
            command.append(output_fn + '.mp3')
        elif output_audio_format == "wav":
            command.extend(["ffmpeg", "-i", video_fn, "-vn"])
            command.append(output_fn + '.wav')

        final_command = " ".join(command)
        print(final_command)
        subprocess.call(final_command)


    # now speed up

    if abs(audio_multiplier - 1) > 0.001:
        # check if audio file is in sped up folder
        speed_suffix = f"{audio_multiplier:.2f}".replace(".", '_')

        speed_output_folder = os.path.join(f'output-{speed_suffix}')

        full_filenames = []
        for (dirpath, dirnames, filenames) in os.walk(output_folder):
            without_output_folder_dirpath = os.sep.join(dirpath.split(os.sep)[1:])
            speed_dirpath = os.path.join(speed_output_folder, without_output_folder_dirpath)

            full_filenames.extend([(os.path.join(dirpath, fn), os.path.join(speed_dirpath, fn)) for fn in filenames])

        # files not in speed folder to speed up
        files_to_speed_up = []
        for fn, speed_up_fn in full_filenames:
            speed_filename, speed_filename_ext = os.path.splitext(speed_up_fn)
            speed_filename = f"{speed_filename}-{speed_suffix}{speed_filename_ext}"
            if not os.path.exists(speed_filename):
                files_to_speed_up.append((fn, speed_filename))


        for fn, speed_up_fn in files_to_speed_up:
            speed_up_audio(fn, speed_up_fn, audio_multiplier)
