# This file creates and populates a directory with clips for specified class(es) of Audio Set
# Input arguments:
#       - class labels
#       - CSV file of dataset
#       - directory where raw audio is stored
#
# The term 'label' is used in place of 'class' to avoid conflicts with Python keywords

import csv as csv


"""
    Function for getting corresponding label for each class
    Input:
        labels - dictionary of label values to search for
"""


def get_label_ids(labels):

    with open('class_labels_indices.csv') as label_file:
        reader = csv.reader(label_file)
        # c1, c2, c3, *_ = reader.fieldnames

        label_ids = {}

        # populate the label id dictionary with None placeholders
        # so that error checking can be performed later
        for label in labels:
            label_ids[label] = None

        for row in reader:
            for label in labels:
                if row[2] in labels[label]: # check if any label has been found
                    label_ids[label] = row[1] # add label to dictionary entry for respective class

        for label in label_ids:
            if label_ids[label] == None:
                print("No id for class " + label + " found. Omitting from search")
                del dict[label] # remove class label which doesn't exist

        return label_ids


"""
    Function for getting the youtube IDs for all clips where the specified classes are present
    Input:
        - label_ids: dict containing label and label-id pairs
        - csv_dataset: path to csv file containing dataset info (i.e. youtube ids and labels)
"""


def get_yt_ids(label_ids, csv_dataset):
    with open(csv_dataset) as dataset:
        for


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--labels', nargs='+', type=str, help='list of classes')
    parser.add_argument('-c', '--csv_dataset', type=str, help='csv file containing dataset info')
    parser.add_argument('-r', '--raw_audio_dir', type=str, help='directory containing dataset as wav files')

    args = parser.parse_args()

    class_ids = get_label_ids(args.labels)


