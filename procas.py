# Processing utility for AudioSet dataset
# Sort, find and download the entire, or subsets of, AudioSet

# Aoife McDonagh

import argparse
import os

import utils


"""
    Function for finding all examples in a directory containing labels for given classes
"""


def find(args):
    utils.find(args.classes, args.csv_dataset, args.data_dir, args.destination_dir)
    print("Finished finding and sorting files for classes: " + args.classes)


"""
    Function for downloading all examples in AudioSet containing labels for given classes
"""


def download(args):
    print("Downloading classes from AudioSet.")

    for class_name in args.classes:
        utils.download(class_name, args.csv_dataset, args.destination_dir, args.strict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, choices=['find', 'download'])
    parser.add_argument('-s', '--strict', help='If used, only match exact string argument passed')

    parser.add_argument('--label_file', type=str, help='Path to CSV file containing AudioSet labels for each class')
    parser.add_argument('--csv_dataset', type=str, help='Path to CSV file containing AudioSet in YouTube-id/timestamp form')

    parser.add_argument('-c', '--classes', nargs='+', type=str, help='list of classes to find in a given directory of audioset files')
    parser.add_argument('-d', '--audio_data_dir', type=str, help='directory path containing files from AudioSet')
    parser.add_argument('--destination_dir', type=str, help='directory path to put found files into')

    parser.set_defaults(
        label_file='./data/class_labels_indices.csv',
        csv_dataset='./data/balanced_train_segments.csv',
        destination_dir='./output'
    )

    args = parser.parse_args()

    if args.mode == 'find':
        if not os.path.isdir(args.destination_dir):
            os.makedirs(args.destination_dir)
        find(args)

    elif args.mode == 'download':
        download(args)


