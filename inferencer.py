from configuration import ModelConfig, DataConfig
from datahandler import DataReader
from src import RPSentenceDetector, SummarizerInference
import os
import re

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def save_research_problem_triple(output_dir, research_problems):
    with open(os.path.join(output_dir, 'research-problem.txt'), 'w', encoding='utf-8') as file:
        if len(research_problems) == 0:
            file.write('')
        else:
            for research_problem in research_problems:
                file.write(f"(Contribution||has research problem||{research_problem})")
                file.write("\n")

def save_research_problem_sentences(output_dir, indexes):
    with open(os.path.join(output_dir, 'sentences.txt'), 'w', encoding='utf-8') as file:
        if len(indexes) == 0:
            file.write('')
        else:
            for indexe in indexes:
                file.write(str(indexe))
                file.write("\n")

def make_predictions(input_dir_path, output_dir_path):
    # Create output directory
    mkdir(output_dir_path)
    for task in os.listdir(input_dir_path):
        input_task_dir_path = os.path.join(input_dir_path, task)
        output_task_dir_path = os.path.join(output_dir_path, task)
        # Create output/task directory
        mkdir(output_task_dir_path)

        print("working on input task dir path is:", input_task_dir_path)
        for input_task_paper in os.listdir(input_task_dir_path):
            input_task_paper_dir_path = os.path.join(input_task_dir_path, input_task_paper)
            output_task_paper_dir_path = os.path.join(output_task_dir_path, input_task_paper)
            # Create output/task/paper directory
            mkdir(output_task_paper_dir_path)

            input_text_file = [file for file in os.listdir(input_task_paper_dir_path)
                                    if re.search('-Stanza-out.txt', file)][0]
            input_text = DataReader.load_text(os.path.join(input_task_paper_dir_path, input_text_file))
            predict_sents_indexes, predict_sents = CLASSIFIER.predict(input_text)
            research_problems = [SUMMARIZER.summarize(sentence) for sentence in predict_sents]
            
            # output/task/paper/triples/research-problem.txt
            output_task_triple_dir = os.path.join(output_task_paper_dir_path, "triples")
            mkdir(output_task_triple_dir)
            save_research_problem_triple(output_task_triple_dir, research_problems)

            # output/task/paper/sentences.txt
            save_research_problem_sentences(output_task_paper_dir_path, predict_sents_indexes)


if __name__=="__main__":
    DATA_CONFIG = DataConfig().get_args()
    MODEL_CONFIG = ModelConfig().get_args()

    classifier_pkl = DataReader.load_pkl(MODEL_CONFIG.tfidf_ml_clf_path)
    CLASSIFIER = RPSentenceDetector(model=classifier_pkl,
                                    text_index_th = MODEL_CONFIG.text_index_th,
                                    text_lenght_th = MODEL_CONFIG.text_lenght_th)
    SUMMARIZER = SummarizerInference(model_path=MODEL_CONFIG.summarizer_model_path)

    mkdir(MODEL_CONFIG.output_dir)

    # Train Inference
    input_dir_path = DATA_CONFIG.preprocessed_train_dir
    output_dir_path = os.path.join(MODEL_CONFIG.output_dir, "train")
    make_predictions(input_dir_path, output_dir_path)

    # Test Inference
    input_dir_path = DATA_CONFIG.preprocessed_test_dir
    output_dir_path = os.path.join(MODEL_CONFIG.output_dir, "test")
    make_predictions(input_dir_path, output_dir_path)