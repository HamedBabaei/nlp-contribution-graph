"""
    ModelConfig: Model Configuration
"""
import argparse


class ModelConfig:
    """
        Model Configs
    """
    def __init__(self):
        """
            Model configuration
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--tfidf_ml_clf_path", type=str, 
                                default="assets/tfidf_ml_clf.sav", 
                                help='Path to trained tfidf+ml classifier for sentence classifiation')
        self.parser.add_argument("--summarizer_model_path", type=str, 
                                default="assets/t5-small/", 
                                help='Path to fine-tuned T5 summarizer')
        self.parser.add_argument("--output_dir", type=str, 
                                default="dataset/outputs/summarizer (t5-small) - classifier (tfidf+xgboost)", 
                                help='Path to output directory to save outputs')
        self.parser.add_argument("--text_index_th", type=int, default=50, 
                                help='index threshold')
        self.parser.add_argument("--text_lenght_th", type=int, default=3, 
                                help='text lenght threshold')
                                
        self.parser.add_argument("--seed", type=int, default=422, help='random seeds')
        self.parser.add_argument("-f")

    def get_args(self):
        """
            Return parser
        :return: parser
        """
        return self.parser.parse_args()