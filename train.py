import os
import re
import math


# returns list of existing files in the input directory
def list_directory_files(directory):
    return [os.path.join(r, file) for r, d, f in os.walk(directory) for file in f]


# returns file category(spam or ham) based on the input name
def extract_file_class_from_its_name(file_name):
    if (file_name.find('spam') != -1):
        return 'spam'
    else:
        return 'ham'


# reads the input file in binary mode, decode it decode it(bcs some files are not readable in utf-8 format), convert
# all alphabets to lowercase and split it based on the provided regex
def preprocess_file_and_create_vocabulary(filename):
    f = open(filename, "rb")
    text = f.read()
    f.close()

    # find encoding source https: // stackoverflow.com / questions / 31019854 / typeerror - cant - use - a - string - pattern - on - a - bytes - like - object - in -re - findall
    text = text.decode('ISO-8859-1')

    words = re.split('[^a-zA-Z]', text.lower())

    return words


# calculates required probabilities and provides the frequency table for the input corpus, the data structure for
# frequency tabla is dictionary where the vocabulary is its key and there is a two element list for value of each key.
# the first element of list is ham frequency and the 2nd is spam frequency
def create_frequency_table(corpus_folder):
    files_list = list_directory_files(corpus_folder)
    vocab_freq_dict = {}

    total_document_count = 0
    ham_document_count = 0
    spam_document_count = 0

    for file_name in files_list:
        file_category = extract_file_class_from_its_name(file_name)
        list_of_vocabs_in_file = preprocess_file_and_create_vocabulary(file_name)

        total_document_count += 1
        if file_category == 'ham':
            ham_document_count += 1
        else:
            spam_document_count += 1

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

        p_ham = ham_document_count / total_document_count
        p_spam = spam_document_count / total_document_count

    return vocab_freq_dict, p_ham, p_spam


# return the conditional probability by applying delta to smooth values, the data structure for returning value is
# dictionary, where its key are vocabs and the values are 4 element lists for each key. first ham freq, 2nd ham
# probability, 3rd spam freq, 4th spam probability
def compute_conditional_probability_with_smoothing(vocab_freq_dict, delta):
    total_ham_count = 0
    total_spam_count = 0

    for vocab, freq in vocab_freq_dict.items():
        total_ham_count += freq[0] + delta
        total_spam_count += freq[1] + delta

    for vocab, freq in vocab_freq_dict.items():
        ham_probability = (freq[0] + delta) / total_ham_count
        spam_probability = (freq[1] + delta) / total_spam_count
        freq.insert(1, ham_probability)
        freq.append(spam_probability)
    return vocab_freq_dict


#  based on the dictionary structure explained in previous function, here the values are printed in model file
def generate_model_file(vocab_dict, model_file):
    file1 = open(model_file, "w")
    sorted_key_list = sorted(vocab_dict)
    line_counter = 0
    for vocab in sorted_key_list:
        line_counter += 1
        line_string = '%i  %s  %i  %s  %i  %s\n' % (line_counter, vocab, vocab_dict[vocab][0],
                                                    str(vocab_dict[vocab][1]), vocab_dict[vocab][2],
                                                    str(vocab_dict[vocab][3]))
        file1.write(line_string)
    file1.close()
    return


def classify_emails(corpus_folder, vocab_freq_probability_dict, p_ham, p_spam):
    files_list = list_directory_files(corpus_folder)
    result = []
    ham_right = 0
    ham_wrong = 0
    spam_right = 0
    spam_wrong = 0
    for file_name in files_list:
        score_ham = math.log10(p_ham)
        score_spam = math.log10(p_spam)
        file_category = extract_file_class_from_its_name(file_name)
        list_of_vocabs_in_file = preprocess_file_and_create_vocabulary(file_name)

        for vocabulary in list_of_vocabs_in_file:
            if vocabulary in vocab_freq_probability_dict:
                score_ham += math.log10(vocab_freq_probability_dict[vocabulary][1])
                score_spam += math.log10(vocab_freq_probability_dict[vocabulary][3])

        if score_ham >= score_spam:
            predicted_category = "ham"
        else:
            predicted_category = "spam"

        if predicted_category == file_category:
            prediction_result = "right"
            if file_category == "ham":
                ham_right += 1
            else:
                spam_right += 1
        else:
            prediction_result = "wrong"
            if file_category == "ham":
                ham_wrong += 1
            else:
                spam_wrong += 1

        f_name = file_name[file_name.find('\\') + 1:]
        result.append([f_name, predicted_category, score_ham, score_spam, file_category, prediction_result])
        # print(file_name, predicted_category, score_ham, score_spam, file_category, prediction_result)
    return result, ham_right, ham_wrong, spam_right, spam_wrong


def generate_result_file(result, result_file):
    file1 = open(result_file, "w")
    line_counter = 0
    for file_name, predicted_category, score_ham, score_spam, file_category, prediction_result in result:
        line_counter += 1
        line_string = '%i  %s  %s  %s  %s  %s  %s\n' % (line_counter, file_name, predicted_category,
                                                        str(score_ham), str(score_spam),
                                                        file_category, prediction_result)
        file1.write(line_string)
    file1.close()
    return


if __name__ == '__main__':
    delta = 0.5
    vocab_freq_dict, p_ham, p_spam = create_frequency_table('train')
    vocab_freq_probability_dict = compute_conditional_probability_with_smoothing(vocab_freq_dict, delta)
    generate_model_file(vocab_freq_probability_dict, 'model.txt')

    # print('ham probability = ', p_ham)
    # print('spam probability = ', p_spam)

    ############### CLASSIFY TEST SET ################

    result, ham_right, ham_wrong, spam_right, spam_wrong = classify_emails('test', vocab_freq_probability_dict, p_ham,
                                                                           p_spam)
    generate_result_file(result, 'result.txt')

    #################### ANALYZE #####################
    print("******************Class Ham**********************")
    print("TP: ", ham_right, " | FP: ", spam_wrong, "\nFN: ", ham_wrong, "   | TN: ", spam_right)
    print("Accuracy: ", (ham_right + spam_right) / (ham_right + ham_wrong + spam_wrong + spam_right))
    precision = ham_right / (ham_right + spam_wrong)
    recall = ham_right / (ham_right + ham_wrong)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F-measure ", (2 * precision * recall) / (precision + recall))

    print("******************Class Spam**********************")
    print("Class Spam:")
    print("TP: ", spam_right, " | FP: ", ham_wrong, "\nFN:", spam_wrong, "   | TN: ", ham_right)
    print("Accuracy: ", (ham_right + spam_right) / (ham_right + ham_wrong + spam_wrong + spam_right))
    precision = spam_right / (spam_right + ham_wrong)
    recall = spam_right / (spam_right + spam_wrong)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F-measure ", (2 * precision * recall) / (precision + recall))
