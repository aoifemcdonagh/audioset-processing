# Set of scripts for downloading raw audio files from AudioSet.

## Prerequisites
- python3
- ffmpeg
- youtube-dl

## Quick start

To download raw audio for class "bird" 
```	
python procas.py download -c "bird"
```
Downloads raw audio to a folder `./output` in current directory.

Uses CSV files found in `./data`. Therefore execute `procas.py` in its' own directory.

## More info
AudioSet can be downloaded from Google [here](https://research.google.com/audioset/download.html) as a set of CSV files. For each element in the dataset the CSV files list an associated YouTube ID, start time, end time and class labels. The CSV files are used to download AudioSet as raw audio files (WAV).

There are several options for downloading files from AudioSet
- `-c` List of classes to download (or find)
- `-fs` Sample rate of audio to download. Default is 16kHz
- `-s` If used, only download/find classes which match exact string arguments passed, i.e. no substring matching. For example, if you wanted to download all instances of class "bird" but not "bird song".
- `-d` Path to directory for storing downloaded files
- `--label_file` Path to CSV file containing AudioSet labels for each class. Defaults to `./data/class_labels_indices.csv` 
- `--csv_dataset` Path to CSV file containing AudioSet in YouTube-id/timestamp/class form. Defaults to `./data/balanced_train_segments.csv`
- `--destination` Path to put downloaded files into. Defaults to `./output`
