from configuration import ModelConfig, DataConfig
from datahandler import DataReader
from models import RPSentenceDetector
import os
import re

DATA_CONFIG = DataConfig().get_args()
MODEL_CONFIG = ModelConfig().get_args()
classifier_pkl = DataReader.load_pkl(MODEL_CONFIG.tfidf_ml_clf_path)
classifier = RPSentenceDetector(model=classifier_pkl,
                                text_index_th = MODEL_CONFIG.text_index_th,
                                text_lenght_th = MODEL_CONFIG.text_lenght_th)

path = DATA_CONFIG.preprocessed_test_dir

for task in os.listdir(path):
    task_dir_path = os.path.join(path, task)
    print("task dir path is:", task_dir_path)
    for task_paper in os.listdir(task_dir_path):
        task_paper_dir_path = os.path.join(task_dir_path, task_paper)
        input_text_file = [file for file in os.listdir(task_paper_dir_path)
                                if re.search('-Stanza-out.txt', file)][0]
        input_text = DataReader.load_text(os.path.join(task_paper_dir_path, input_text_file))
        print(classifier.predict(input_text))
        break
    break

