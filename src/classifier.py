import numpy as np


class RPSentenceDetector:

    def __init__(self, model, text_index_th, text_lenght_th):
        self.model = model
        self.text_lenght_th = text_lenght_th
        self.text_index_th = text_index_th

    def predict(self, text):
        sentences = [[sentence, len(sentence.split()), index+1] 
                    for index, sentence in enumerate(text.split("\n"))]
        clean_setns, clean_setns_indexs = [], []
        for sentence in sentences:
            if sentence[2] <= self.text_index_th and sentence[1] >= self.text_lenght_th:
                clean_setns.append(sentence[0])
                clean_setns_indexs.append(sentence[2])
        
        predictions = np.array(self.model.predict(clean_setns)).astype(bool)
        predict_sent_indexes = list(np.array(clean_setns_indexs)[predictions])
        predict_sents = list(set(list(np.array(clean_setns)[predictions])))
        return predict_sent_indexes, predict_sents

class TFIDFXGBoost:
    def __init__(self, model):
        self.model = model

    def predict(self, X):
        return self.model.predict(X)