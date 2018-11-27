# This file creates and populates a directory with clips for specified class(es) of Audio Set
# Works on pre-downloaded files. Doesn't download new files
# Input arguments:
#       - class labels
#       - CSV file of dataset
#       - directory where raw audio is stored
#       - destination directory to store sorted audio files
#
# The term 'label' is used in place of 'class' to avoid conflicts with Python keywords

import csv
from collections import defaultdict
import fnmatch
import os
from shutil import copyfile


def find(labels, csv_dataset, raw_audio_dir, destination_dir):
    print("Finding examples for classes " + str(labels) + " in: " + raw_audio_dir)

    for label in labels:
        class_id = get_label_id(label)
        youtube_id = get_yt_ids(class_id, csv_dataset)
        sort_files(youtube_id, raw_audio_dir, destination_dir)


def download(label, csv_dataset, dst_dir, strict, sample_rate):
    new_csv = create_csv(label, csv_dataset, strict)
    dst_dir = os.path.join(dst_dir, label)

    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)

    with open(new_csv) as dataset:
        reader = csv.reader(dataset)

        for row in reader:
            os.system(("ffmpeg -ss " + str(row[1]) + " -i $(youtube-dl -f 'bestaudio' -g https://www.youtube.com/watch?v=" +
                       str(row[0]) + ") -t 10 -ar " + str(sample_rate) + " -- \"" + dst_dir + "/" + str(row[0]) + "_" + row[1] + ".wav\""))

"""
    Function for creating csv file containing info for given class
"""


def create_csv(class_name, csv_dataset, strict, dst_dir='./data/'):
    new_csv_path = os.path.join(dst_dir + class_name + '.csv')
    print(new_csv_path)

    # Should check if CSV already exists and possibly return if so? Overwriting for now
    if os.path.isfile(new_csv_path):
        print("A CSV file for class " + class_name + ' already exists.')
        print("*** Overwriting " + dst_dir + class_name + '.csv ***')

    label_id = get_label_id(class_name,strict)

    with open(csv_dataset) as dataset, open(new_csv_path, 'w', newline='') as new_csv:
        reader = csv.reader(dataset, skipinitialspace=True)
        writer = csv.writer(new_csv)

        to_write = [row for row in reader for label in label_id if label in row[3]]
        writer.writerows(to_write)

    print("Finished writing CSV file for " + class_name)

    return new_csv_path


"""
    Function for getting corresponding label for a class
    Input:
        labels - label value to search for

    Returns:
        label_id - ID for given label. Given as a list as there can be multiple matching IDs found (e.g. "dog")

    The function looks for class name in the CSV file of label indices. It performs sub-string searching rather than
    matching so that class labels are more reliably found. Problematic naming convention of classes in AudioSet
    forces this to be the case. For example, inputting "female speech" as 'label' will not find class
    "Female speech, woman speaking" if exact string matching is performed. Also problems with exact string matching if
    there are spaces in class names.
    Sub-string matching will result in multiple class labels being found for certain input stings. e.g. "dog"

    28/06/18: implemented 'strict' option
"""


def get_label_id(label, strict):

    with open('./data/class_labels_indices.csv') as label_file:
        reader = csv.DictReader(label_file)
        index, id, class_name, = reader.fieldnames

        if strict:
            label_id = [row[id] for row in reader if (label.lower() == row[class_name].lower())]

        else:
            label_id = [row[id] for row in reader if (label.lower() in row[class_name].lower())]

        if label_id is None:
            print("No id for class " + label)

        if len(label_id) > 1: # If there is more than one class containing the specified string
            print("Multiple labels found for " + label)
            print(label_id)

    return label_id


"""
    Function for getting the youtube IDs for all clips where the specified classes are present
    Input:
        - label_ids: list of label IDs (will most often only contain 1 label)
        - csv_dataset: path to csv file containing dataset info (i.e. youtube ids and labels)
"""


def get_yt_ids(label_ids, csv_dataset):
    yt_ids = {label: [] for label in label_ids}

    with open(csv_dataset) as dataset:
        reader = csv.reader(dataset, skipinitialspace=True)

        # Add youtube id to list for label if corresponding audio contains that label/class
        [(yt_ids[label].append(row[0])) for row in reader for label in label_ids if label in row[3]]

    for label in yt_ids:
        if not yt_ids[label]:
            print("No clips found for " + label)
            yt_ids.pop(label)  # remove dict entry for label which doesn't have any clips

        print("Youtube ids for label " + label)
        print(yt_ids[label])
        print("Total number of labels for label " + label + ": " + str(len(yt_ids[label])))

    return yt_ids  # return dict containing label-yt-id pairs


"""
    Function for getting all wav files associated with given label/class
    Input:
        - yt_ids: dict containing label-yt_id pairs
        - wav_file_dir: directory where all wav files are stored

    Name of function was originally 'sort_wav_files' but 'wav' was removed to avoid confusion. Script can be used to
    sort archive files, or any other type of file, no distinction is made.
"""


def sort_files(yt_ids, file_dir, dst_dir=None):
    dst_dir = file_dir if dst_dir is None else dst_dir

    for label in yt_ids:  # keys in yt_ids are class names
        if not os.path.exists(dst_dir + "/" + label):
            os.makedirs(dst_dir + "/" + label)
            print("Created directory for class: " + label)
            print(dst_dir + "/" + label)

    for file in os.listdir(file_dir):  # Iterate through all files in dir
        for label, yt_id_list in yt_ids.items():  # Iterate through label-yt_id_list pairs
            if any(yt_id in file for yt_id in yt_id_list):  # if the file name in list of yt_ids
                src = file_dir + "/" + file  # source file
                dst = (dst_dir + "/" + label + "/" + file)  # destination of file
                copyfile(src, dst)  # copy file into directory for current label

    print("Finished sorting files")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--labels', nargs='+', type=str, help='list of classes')
    parser.add_argument('-c', '--csv_dataset', type=str, help='csv file containing dataset info')
    parser.add_argument('-r', '--raw_audio_dir', type=str, help='directory containing dataset as wav files')
    parser.add_argument('-d', '--destination_dir', type=str, help='directory to put sorted files into')

    args = parser.parse_args()

    print(args.labels)

    class_ids = [get_label_id(label) for label in args.labels]

    #class_ids = get_label_ids(args.labels)

    class_ids = dict(zip(args.labels, class_ids))

    print(class_ids)

    # yt_ids = [get_yt_ids(label_id, args.csv_dataset) for label_id in class_ids]

    youtube_ids = get_yt_ids(class_ids, args.csv_dataset)

    # print(youtube_ids)

    sort_files(youtube_ids, args.raw_audio_dir, args.destination_dir)
