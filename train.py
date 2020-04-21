import os
import re


def list_directory_files(directory):
    return [os.path.join(r, file) for r, d, f in os.walk(directory) for file in f]


def extract_file_class_from_its_name(file_name):
    if (file_name.find('spam') != -1):
        return 'spam'
    else:
        return 'ham'


def preprocess_file_and_create_vocabulary(filename):
    f = open(filename, "r")
    text = f.read()
    lower_text = text.lower()

    # regex source "https://stackoverflow.com/questions/6202549/word-tokenization-using-python-regular-expressions"
    words = re.findall("[A-Z\-\']{2,}(?![a-z])|[A-Z\-\'][a-z\-\']+(?=[A-Z])|[\'\w\-]+", lower_text)

    return words


if __name__ == '__main__':
    train_files_list = list_directory_files('train')
    print(extract_file_class_from_its_name(' test/test-ham-00039.txt'))
    words = preprocess_file_and_create_vocabulary('train/train-ham-00001.txt')
    print(words)
