import os
import re
import email


def list_directory_files(directory):
    return [os.path.join(r, file) for r, d, f in os.walk(directory) for file in f]


def extract_file_class_from_its_name(file_name):
    if (file_name.find('spam') != -1):
        return 'spam'
    else:
        return 'ham'


def preprocess_file_and_create_vocabulary(filename):
    print(filename)
    f = open(filename, "rb")
    text = f.read()
    f.close()

    # find encoding source https: // stackoverflow.com / questions / 31019854 / typeerror - cant - use - a - string - pattern - on - a - bytes - like - object - in -re - findall
    text = text.decode('ISO-8859-1')

    # regex source "https://stackoverflow.com/questions/6202549/word-tokenization-using-python-regular-expressions"
    # words = re.findall("[A-Z\-\']{2,}(?![a-z])|[A-Z\-\'][a-z\-\']+(?=[A-Z])|[\'\w\-]+", lower_text)
    # words = re.split("[a-zA-Z]+", lower_text)
    words = re.split('\[\^a-zA-Z\]', text)
    words_list = words[0].split()

    return words_list


def create_frequency_table(corpus_folder):
    files_list = list_directory_files(corpus_folder)
    vocab_freq_class_dict = {}
    for file_name in files_list:
        file_category = extract_file_class_from_its_name(file_name)
        list_of_vocabs_in_file = preprocess_file_and_create_vocabulary(file_name)

        # word_count source https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0
        for vocabulcary in list_of_vocabs_in_file:
            if vocabulcary in vocab_freq_class_dict:
                if file_category == 'ham':
                    vocab_freq_class_dict[vocabulcary][0] += 1
                else:
                    vocab_freq_class_dict[vocabulcary][1] += 1

            else:
                if file_category == 'ham':
                    vocab_freq_class_dict[vocabulcary]=[1,0]
                else:
                    vocab_freq_class_dict[vocabulcary]=[0,1]

    return vocab_freq_class_dict

def compute_conditional_probability(vocab_freq_class_dict):
    pass


if __name__ == '__main__':
    frequency_table = create_frequency_table('train')
    print(frequency_table)
