*************
#Spam Detector
*************


##Submitted Files:

1. Python code: 
train.py implements python-based spam detector. It builds a probabilistic model from training set and evaluates a test set based on that model by classifying the input file as Spam or Ham and labeling it right/wrong for further analysis.
2. Generated output: 
<ul>
<li>
model.txt is generated from the provided training set. It basically consist of the vocabulary in each file, frequency and smoothed conditional probability of words for class Ham and class Spam.
</li>
<li>
result.txt is generated afer evaluation of model using the given test set. It classifies each file as spam or ham and label it right or wrong based on actual classification.
</li>
</ul>
3. Project Report:
It describes the evaluation metrics like accuracy, precision etc. for the implemented classifier and also lists team information and references followed for the work.

----------------------------------------------------------------------
##How to run code: 
To run the implementation, simply run the train.py file using python interpreter. Since, training and testing data is already imported in project. The output is generated in form of two text files model.txt which is generated after training and result.txt which is final output of testing.

To test with another dataset user simply needs to replace the files in test folder and run train.py

###Generating the evaluating results: Accuracy, precision, recall and F1-measure are calculated based on the classifications labeled as right or wrong in result.txt. They are further explained in project report.

----------------------------------------------------------------------
##Working of Code:

The program execution starts with main function which implements following methods:

(a) Training Model:

create_frequency_table() takes 'train' input as directory name and maintains a list of files in that folder. It further categorize the files as 'Spam' and 'Ham' based on file name using extract_file_class_from_its_name() and creates vocabulary from each file using preprocess_file_and_create_vocabulary(). This function reads the content of a file and split words based on a regular expression. Further, frequency of each word is calculated to get the vocabulary. 

compute_conditional_probability_with_smoothing() takes delta = 0.5 and the vocabulary dictionary created in previous function as input and compute the smoothed probability for each word with respect to class ham and class spam. It further inserts the computed values for each word in the existing dictionary vocab_freq_dict.

generate_model_file() takes the updated vocabulary dictionary obtained from previous function and an empty model.txt file as input and returns training model implemented to that file in the specified format.

(b) Evaluating Model:

classify_emails('test', vocab_freq_probability_dict, p_ham, p_spam) takes the dataset as input, calculate score_ham and score_spam for each file. It creates vocabulary list for test set in the same way and based on score classify the files as spam or ham. It further compares the result with actual labels and mark them right/wrong which forms the basis of analysis. The function finally writes output in specified format to result.txt file.


