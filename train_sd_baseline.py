"""
    Train Sentence Detector Baseline Model: Word/Character TFIDF + ML
"""
from datahandler import DataReader, DataWriter
from configuration import ModelConfig, DataConfig
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import sys 
import os


if __name__=='__main__':
    DATA_CONFIG = DataConfig().get_args()
    MODEL_CONFIG = ModelConfig().get_args()
    
    stdoutOrigin=sys.stdout
    sys.stdout = open(os.path.join(DATA_CONFIG.logs_dir, 'sentence_detector_baseline.log.txt'), "w")
    
    TFIDF_MODEL = Pipeline([
                    ("feature",  TfidfVectorizer(ngram_range=(1, 2))),
                    ('clf', XGBClassifier())
                ])

    
    TRAIN = DataReader.load_csv(DATA_CONFIG.sent_clf_train_data_path)
    TEST = DataReader.load_csv(DATA_CONFIG.sent_clf_test_data_path)
    
    print(f"Train shape is:{TRAIN.shape}, Test shape is: {TEST.shape}")
    print("train/evaluate TFIDF+XGBClassifier model...")
    TFIDF_MODEL.fit(TRAIN['text'].tolist(), TRAIN['label'].tolist())
    
    TFIDF_MODEL_TEST_PRED = TFIDF_MODEL.predict(TEST['text'].tolist())
    
    print("save model report on the report file")
    print("-"*100)
    print("Word TFIDF +  XGBClassifier")
    print("-"*100)
    print(classification_report(TEST['label'].tolist(), TFIDF_MODEL_TEST_PRED))
    print("-"*100)
    print("Confusion matrix")
    print("-"*100)
    print(confusion_matrix(TEST['label'].tolist(), TFIDF_MODEL_TEST_PRED))
    print("-"*100)
    print("save model...")
    DataWriter.write_pkl(TFIDF_MODEL, MODEL_CONFIG.tfidf_ml_clf_path)
    sys.stdout.close()