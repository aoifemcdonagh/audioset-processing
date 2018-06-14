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

    class_ids, classes = get_label_ids(labels)

    youtube_ids = get_yt_ids(class_ids, csv_dataset)

    sort_files(youtube_ids, raw_audio_dir, destination_dir)


"""
    Function for creating csv file containing info for given class
"""


def create_csv(class_name, csv_dataset, dst_dir='./data/', data=None):
    new_csv_path = os.path.join(dst_dir + class_name + '.csv')
    print(new_csv_path)

    if os.path.isfile(
            new_csv_path):  # Should check if CSV already exists and possibly return if so? Overwriting for now
        print("A CSV file for class " + class_name + ' already exists.')
        print("*** Overwriting " + dst_dir + class_name + '.csv ***')

    label_id = get_label_ids([class_name])  # Put in square brackets because get_label_ids needs list as input!

    with open(csv_dataset) as dataset, open(new_csv_path, 'w', newline='') as new_csv:
        reader = csv.reader(dataset, skipinitialspace=True)
        writer = csv.writer(new_csv)

        to_write = [row for row in reader if label_id[class_name] in row[3]]
        writer.writerows(to_write)

    print("Finished writing CSV file for " + class_name)

    return new_csv_path


"""
    Function for getting corresponding label for each class
    Input:
        labels - dictionary of label values to search for
"""


def get_label_ids(labels):
    # populate the label id dictionary with None placeholders
    # so that error checking can be performed later
    label_ids = dict.fromkeys(labels)

    with open('class_labels_indices.csv') as label_file:
        reader = csv.DictReader(label_file)
        index, id, class_name, *_ = reader.fieldnames

        for row in reader:
            for label in labels:
                if label.lower() == row[class_name].lower():  # check if any label has been found
                    label_ids[label] = row[id]  # add label ID to dictionary entry for respective label/class

    for label in labels:
        if label_ids[label] is None:
            print("No id for class " + label + " found. Omitting from search")
            label_ids.pop(label)  # remove class label which doesn't exist
            labels.remove(label)  # remove class label from list of labels we are searching for

    return label_ids


"""
    Function for getting the youtube IDs for all clips where the specified classes are present
    Input:
        - label_ids: dict containing label and label-id pairs
        - csv_dataset: path to csv file containing dataset info (i.e. youtube ids and labels)
"""


def get_yt_ids(label_ids, csv_dataset):
    yt_ids = {label: [] for label in label_ids}

    with open(csv_dataset) as dataset:
        reader = csv.reader(dataset, skipinitialspace=True)

        for row in reader:
            for label, label_id in label_ids.items():  # search for label id in row
                if label_id in row[3]:  # if label is in this clip, add to list of label-yt_id pairs
                    yt_ids[label].append(row[0])

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
    if dst_dir is None:
        dst_dir = file_dir

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

    class_ids = get_label_ids(args.labels)

    print(class_ids)

    youtube_ids = get_yt_ids(class_ids, args.csv_dataset)

    # print(youtube_ids)

    sort_files(youtube_ids, args.raw_audio_dir, args.destination_dir)
