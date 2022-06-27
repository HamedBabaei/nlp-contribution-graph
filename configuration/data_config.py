"""
    DataConfig: Data Configuration of models
"""
import argparse


class DataConfig:
    """
        Data Configs
    """
    def __init__(self):
        """
            Data configuration
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--raw_train_dir", type=str, 
                                default="dataset/raw/training-data", 
                                help='Path to raw training data')
        self.parser.add_argument("--raw_test_dir", type=str, 
                                default="dataset/raw/test-data", 
                                help='Path to raw test data')

        self.parser.add_argument("--preprocessed_train_dir", type=str, 
                                default="dataset/preprocessed/training-data", 
                                help='Path to preprocessed training data')
        self.parser.add_argument("--preprocessed_test_dir", type=str, 
                                default="dataset/preprocessed/test-data", 
                                help='Path to preprocessed test data')
        
        self.parser.add_argument("--sent_clf_train_data_path", type=str, 
                                default="dataset/preprocessed/sent_clf_train_data.csv", 
                                help='Path to preprocessed sentence classification train data')
        self.parser.add_argument("--sent_clf_test_data_path", type=str, 
                                default="dataset/preprocessed/sent_clf_test_data.csv", 
                                help='Path to preprocessed sentence classification test data')

        self.parser.add_argument("--ie_train_data_path", type=str, 
                                default="dataset/preprocessed/ie_train_data.csv", 
                                help='Path to preprocessed information extraction train data')
        self.parser.add_argument("--ie_test_data_path", type=str, 
                                default="dataset/preprocessed/ie_test_data.csv", 
                                help='Path to preprocessed information extraction test data')

        self.parser.add_argument("--logs", type=str, default="report/data.stats.json", 
                                help='dataset (train and test) stats path')
        self.parser.add_argument("--seed", type=int, default=422, help='random seeds')
        self.parser.add_argument("-f")

    def get_args(self):
        """
            Return parser
        :return: parser
        """
        return self.parser.parse_args()