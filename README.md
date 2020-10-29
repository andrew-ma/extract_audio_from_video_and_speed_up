# Extract Audio From Video and Speed Up

* requires ffmpeg in your path
* will extract audio from every video file in source folder and save to output folder
* will speed up all the audio in output folder depending on audio multiplier, and will save it to new output folder like "output-2_00" for 2x speed

## Usage
```buildoutcfg
usage: extract_audio_from_video.py [-h] [--source_folder SOURCE_FOLDER] [--output_folder OUTPUT_FOLDER] [--audio_multiplier AUDIO_MULTIPLIER]
                                   [--output_audio_format OUTPUT_AUDIO_FORMAT]

optional arguments:
  -h, --help            show this help message and exit
  --source_folder SOURCE_FOLDER
                        Source directory (default: input)
  --output_folder OUTPUT_FOLDER
                        Output directory (default: output)
  --audio_multiplier AUDIO_MULTIPLIER
                        Multiple audio speed by numbers >= 0.5 (default: 1)
  --output_audio_format OUTPUT_AUDIO_FORMAT
                        Audio format to extract (default: mp3)
```

### I am only committing this for my own personal use to batch speed up the audio before feeding to automated transcription 