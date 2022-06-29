"""
    EvalConfig: Evaluation Configuration of models
"""
import argparse


TRAIN_TASKS = ['passage_re-ranking', 'temporal_information_extraction', 'part-of-speech_tagging', 
               'prosody_prediction', 'text_generation', 'sentence_compression', 'relation_extraction', 
               'sentence_classification', 'question_similarity', 'question_generation', 
               'sarcasm_detection', 'semantic_parsing', 'negation_scope_resolution', 'question_answering', 
               'semantic_role_labeling', 'paraphrase_generation', 'query_wellformedness', 
               'sentiment_analysis', 'text-to-speech_synthesis', 'phrase_grounding', 
               'natural_language_inference', 'topic_models', 'text_summarization', 'smile_recognition']

TEST_TASKS = ['hypernym_discovery', 'constituency_parsing', 'document_classification', 'face_alignment', 
              'data-to-text_generation', 'dependency_parsing', 'entity_linking', 'coreference_resolution', 
              'face_detection', 'natural_language_inference']

class EvalConfig:
    """
        Data Configs
    """
    def __init__(self):
        """
            Eval configuration
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--train_tasks", type=list, default=TRAIN_TASKS, 
                                help='train tasks for evaluation')
        self.parser.add_argument("--test_tasks", type=list, default=TEST_TASKS, 
                                help='test tasks for evaluation')
        self.parser.add_argument("--problem_name", type=str, default='research-problem', 
                                help='Problem Name for evaluation')
        self.parser.add_argument("-f")

    def get_args(self):
        """
            Return parser
        :return: parser
        """
        return self.parser.parse_args()