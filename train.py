import os
import re
import email
import numpy as np

p_ham = 2/5
p_spam = 3/5

def list_directory_files(directory):
    return [os.path.join(r, file) for r, d, f in os.walk(directory) for file in f]


def extract_file_class_from_its_name(file_name):
    if (file_name.find('spam') != -1):
        return 'spam'
    else:
        return 'ham'


def preprocess_file_and_create_vocabulary(filename):
    #print(filename)
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
    vocab_freq_dict = {}
    for file_name in files_list:
        file_category = extract_file_class_from_its_name(file_name)
        list_of_vocabs_in_file = preprocess_file_and_create_vocabulary(file_name)

        # word_count source https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0
        for vocabulary in list_of_vocabs_in_file:
            if vocabulary in vocab_freq_dict:
                if file_category == 'ham':
                    vocab_freq_dict[vocabulary][0] += 1
                else:
                    vocab_freq_dict[vocabulary][1] += 1

            else:
                if file_category == 'ham':
                    vocab_freq_dict[vocabulary] = [1, 0]
                else:
                    vocab_freq_dict[vocabulary] = [0, 1]

    return vocab_freq_dict


def compute_conditional_probability_with_smoothing(vocab_freq_dict, delta):

    total_ham_count = 0
    total_spam_count = 0

    for vocab,freq in vocab_freq_dict.items():
        total_ham_count += freq[0] + delta
        total_spam_count += freq[1] + delta

    for vocab,freq in vocab_freq_dict.items():
        ham_probability = (freq[0]+delta)/total_ham_count
        spam_probability = (freq[1]+delta)/total_spam_count
        freq.insert(1,ham_probability)
        freq.append(spam_probability)
    return vocab_freq_dict


def classify_emails(corpus_folder, vocab_freq_probability_dict):
    files_list = list_directory_files(corpus_folder)
    for file_name in files_list:
        score_ham = np.log10(p_ham)
        score_spam = np.log10(p_spam)
        file_category = extract_file_class_from_its_name(file_name)
        list_of_vocabs_in_file = preprocess_file_and_create_vocabulary(file_name)

        for vocabulary in list_of_vocabs_in_file:
            if vocabulary in vocab_freq_probability_dict:
                score_ham += np.log10(vocab_freq_probability_dict[vocabulary][1])
                score_spam += np.log10(vocab_freq_probability_dict[vocabulary][3])

        if score_ham >= score_spam:
            predicted_category = "ham"
        else:
            predicted_category = "spam"

        if predicted_category == file_category:
            prediction_result = "right"
        else:
            prediction_result = "wrong"

        print(file_name, predicted_category, score_ham, score_spam, file_category, prediction_result)



if __name__ == '__main__':
    delta = 0.5
    vocab_freq_dict = create_frequency_table('train')
    vocab_freq_probability_dict = compute_conditional_probability_with_smoothing(vocab_freq_dict,delta)

    #print(vocab_freq_probability_dict)

    ############### CLASSIFY TEST SET ################

    classify_emails('test', vocab_freq_probability_dict)
