# Toolkit for downloading raw audio files from AudioSet.

## Prerequisites
- python3
- ffmpeg
- youtube-dl

## Quick start

To download files from AudioSet for class "bird" 
```	
python3 procas.py download -c "bird"
```
Downloads audio files to a folder `output/bird` in current directory.

Uses CSV files found in `./data` by default. Therefore execute `procas.py` in its' own directory.

## More info
AudioSet can be downloaded from Google [here](https://research.google.com/audioset/download.html) as a set of CSV files. For each element in the dataset the CSV files list an associated YouTube ID, start time, end time and class labels. The CSV files are used to download AudioSet as raw audio files (WAV).

The following options control how the toolkit operates. The first list of options are the most useful. The second list of options aren't necessary to use but offer more fine grained control if desired.

### Most useful
- Mode: `download` or `find`
- `-c` or `--classes` List of classes to download (or find). Use quotation marks for class names with spaces, e.g. `"bird song"`. For multiple classes use format `"bird" "flute" "dog" ...` 
- `-d` or `--destination_dir` Path to directory for storing downloaded (or found) files. Defaults to `./output`
- `--audio_data_dir` Path to directory containing pre-downloaded AudioSet files. Must be used in `find` mode.

### Less used
- `-b` or `--blacklist` List of class labels which will exclude a file from being downloaded/found.
- `-fs` or `--sample_rate` Sample rate of audio to download in Hz (not kHz!!). Default is 16000Hz
- `-s` or `--strict` If used, only download/find classes which match exact string arguments passed, i.e. no substring matching. For example, if you wanted to download all instances of class "bird" but not "bird song".
- `--label_file` Path to CSV file containing AudioSet labels for each class. Defaults to `./data/class_labels_indices.csv` 
- `--csv_dataset` Path to CSV file containing AudioSet in YouTube-ID/timestamp/class form. Defaults to `./data/balanced_train_segments.csv`

