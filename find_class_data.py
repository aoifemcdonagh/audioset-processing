# This file creates and populates a directory with clips for specified class(es) of Audio Set
# Input arguments:
#       - class labels
#       - CSV file of dataset
#       - directory where raw audio is stored
#
# The term 'label' is used in place of 'class' to avoid conflicts with Python keywords

import csv as csv
from collections import defaultdict
import fnmatch
import os
from shutil import copyfile

"""
    Function for getting corresponding label for each class
    Input:
        labels - dictionary of label values to search for
"""


def get_label_ids(labels):

    with open('class_labels_indices.csv') as label_file:
        reader = csv.reader(label_file)

        label_ids = {}

        # populate the label id dictionary with None placeholders
        # so that error checking can be performed later
        for label in labels:
            label_ids[label] = None

        for row in reader:
            for label in labels:
                if label.lower() in row[2].lower():  # check if any label has been found
                    label_ids[label] = row[1]  # add label ID to dictionary entry for respective label/class

        for label in labels:
            if label_ids[label] is None:
                print("No id for class " + label + " found. Omitting from search")
                label_ids.pop(label)  # remove class label which doesn't exist
                labels.remove(label)  # remove class label from list of labels we are searching for

        return label_ids, labels


"""
    Function for getting the youtube IDs for all clips where the specified classes are present
    Input:
        - label_ids: dict containing label and label-id pairs
        - csv_dataset: path to csv file containing dataset info (i.e. youtube ids and labels)
"""


def get_yt_ids(label_ids, csv_dataset):

    with open(csv_dataset) as dataset:
        reader = csv.reader(dataset)

        yt_ids = defaultdict(list)  # make a dictionary of lists to hold label-yt_id pairs

        for label in label_ids:  # iterate over keys of label_id dict (will be class names)
            yt_ids[label] = []

        for row in reader:
            for label, label_id in label_ids.items():  # search for label id in row
                if label_id in row:  # if label is in this clip, add to list of label-yt_id pairs
                    yt_ids[label].append(row[0])
                    #print(yt_ids)

        for label in label_ids:
            if yt_ids[label] is None:
                print("No clips found for " + label)
                yt_ids.pop(label)  # remove dict entry for label which doesn't have any clips

        return yt_ids  # return dict containing label-yt-id pairs


"""
    Function for getting all wav files associated with given label/class
    Input:
        - yt_ids: dict containing label-yt_id pairs
        - wav_file_dir: directory where all wav files are stored
"""


def sort_wav_files(yt_ids, wav_file_dir):
    for label in yt_ids: # keys in yt_ids are class names
        if not os.path.exists(wav_file_dir + "/" + label):
            os.makedirs(wav_file_dir + "/" + label)
            print("Created directory for class: " + label)
            print(wav_file_dir + "/" + label)

    for file in os.listdir(wav_file_dir):  # Iterate through all files in dir
        for label, yt_id_list in yt_ids.items():  # Iterate through label-yt_id_list pairs
            if any(yt_id in file for yt_id in yt_id_list):  # if the file name in list of yt_ids
                src = wav_file_dir + "/" + file  # source file
                dst = wav_file_dir + "/" + label + "/" + file  # destination directory for current label
                copyfile(src, dst)  # copy file into directory for current label

    print("Finished sorting wav files")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--labels', nargs='+', type=str, help='list of classes')
    parser.add_argument('-c', '--csv_dataset', type=str, help='csv file containing dataset info')
    parser.add_argument('-r', '--raw_audio_dir', type=str, help='directory containing dataset as wav files')

    args = parser.parse_args()

    print(args.labels)

    class_ids, classes = get_label_ids(args.labels)

    print(class_ids)
    print(classes)

    youtube_ids = get_yt_ids(class_ids, args.csv_dataset)

    print(youtube_ids)

    sort_wav_files(youtube_ids, args.raw_audio_dir)




