# audioset-processing [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aoifemcdonagh/audioset-processing/blob/master/demo.ipynb)
Toolkit for downloading raw audio files from AudioSet.

## Dependencies
- python3
- ffmpeg
- youtube-dl 2019.7.2

## Quick start

To download files from AudioSet for class "bird" 
```	
python3 process.py download -c "bird"
```
Downloads audio files to a folder `output/bird` in current directory.

Uses CSV files found in `data/` by default. Execute `process.py` in its' own directory.

## process.py Arguments
The following options control how the toolkit operates. The first list of options are the most useful. The second list of options aren't necessary to use but offer more fine grained control if desired.

#### Most useful
- Mode: `download` or `find`
- `-c` or `--classes` List of classes to download (or find). Use quotation marks for class names with spaces, e.g. `"bird song"`. For multiple classes use format `"bird" "flute" "dog" ...` 
- `-d` or `--destination_dir` Path to directory for storing downloaded (or found) files. Defaults to `./output`
- `--audio_data_dir` Path to directory containing pre-downloaded AudioSet files. Must be used in `find` mode.

#### Less used
- `-b` or `--blacklist` List of class labels which will exclude a file from being downloaded/found.
- `-fs` or `--sample_rate` Sample rate of audio to download in Hz (not kHz!!). Default is 16000Hz
- `-s` or `--strict` If used, only download/find classes which match exact string arguments passed, i.e. no substring matching. For example, if you wanted to download all instances of class "bird" but not "bird song".
- `--label_file` Path to CSV file containing AudioSet labels for each class. Defaults to `./data/class_labels_indices.csv` 
- `--csv_dataset` Path to CSV file containing AudioSet in YouTube-ID/timestamp/class form. Defaults to `./data/balanced_train_segments.csv`

## Project Overview
This toolkit was developed as part of a project for my Master's thesis. This project involved training a WaveGAN model on subsets of the AudioSet dataset.  

AudioSet is publicly available in two formats; as a list of YouTube-IDs structured as CSV files, or as 128-dimensional feature vectors stored as TFRecord files.
Neither of these formats could be used as training data for the model I was trying to train.
* The problem with using the dataset's audio feature vectors is that in general, audio feature representations are not invertible.
* The problem with using YouTube-IDs is that they are only references to where the audio can be found online, not the samples themselves.

However, using these identifiers is the only way to obtain raw audio to train a WaveGAN model for this project. 
Gathering all samples for an entire class would take an extremely long time and be prone to human error. It would involve a number of lengthy steps which would have to be repeated every time a new data needed to be downloaded;  
1. Parsing the CSV dataset for samples labelled with corresponding class identifier 

2. Storing YouTube-IDs labelled with class identifier. 

3. Putting all IDs into a separate URL addresses. 

4. Downloading YouTube video from which a sample originated 

5. Extract audio, discard video stream. 

6. Using timestamp information in CSV file to retrieve sample. 

7. Storing sample on local machine.  

Since these steps are repeatable for downloading any target class in AudioSet, it made sense to automate this process. A toolkit for downloading the raw audio samples in AudioSet was developed to solve this problem. The toolkit comprises of a set of Python scripts for taking user input, parsing through the dataset, and downloading the relevant audio clips.  

#### Downloading
To download a sub-set of AudioSet, the user can specify target classes they wish to download. Then the csv files distributed for the dataset are parsed for all YouTube-IDs which have a label associated with the given class. Using a number of Python packages, URLs are formed with the YouTube-IDs. Ten second audio clips are downloaded using the generated URLs and corresponding timestamps for each video. Clips are stored locally on the user's machine for future use.  

![alt text](https://github.com/aoifemcdonagh/audioset-processing/blob/master/src/pictures/audioset-processing-download.png "Download flowchart")

## AudioSet
AudioSet can be downloaded from Google [here](https://research.google.com/audioset/download.html) as a set of CSV files. For each element in the dataset the CSV files list an associated YouTube ID, start time, end time and class labels. The CSV files are used to download AudioSet as raw audio files (WAV).

## Structure
```
audioset-processing
├── procas
|   ├── utils.py
|   └── download.sh
├── data
|   ├── balanced_train_segments.csv
|   ├── class_labels_indices.csv
|   ├── unbalanced_train_segments.csv
|   └── eval_segments.csv
├── src
|   └── pictures
├── demo.ipynb
├── LICENCE
├── process.py
├── requirements.txt
└── README.md
```