"""
    Dataset Builder for Trainings
"""
from datahandler import DataReader, DataWriter
from configuration import DataConfig
import json
from tqdm import tqdm
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def copy_related_info(task, input_dir, output_dir):
    output_dir_path = os.path.join(output_dir, task)
    input_dir_path  = os.path.join(input_dir, task)
    mkdir(output_dir_path)
    
    for sample_dir in os.listdir(input_dir_path):
        sample_dir_input_path = os.path.join(input_dir_path, sample_dir)
        sample_dir_output_path = os.path.join(output_dir_path, sample_dir)
        mkdir(sample_dir_output_path)
        # copy *Stanza-out.txt
        for item in os.listdir(sample_dir_input_path):
            if item.endswith("Stanza-out.txt"): 
                shutil.copyfile(os.path.join(sample_dir_input_path, item),
                            os.path.join(sample_dir_output_path, item))
                stanza_out_txt = DataReader.load_text(os.path.join(sample_dir_input_path, item))
                stanza_out_txt_list = stanza_out_txt.split("\n")
                break
        # copy RP inof-units
        iu_dir_output_path = os.path.join(sample_dir_output_path, "info-units")
        iu_dir_input_path = os.path.join(sample_dir_input_path, "info-units")
        mkdir(iu_dir_output_path)
        shutil.copyfile(os.path.join(iu_dir_input_path, 'research-problem.json'), 
                    os.path.join(iu_dir_output_path, 'research-problem.json'))        
        ui_rp = DataReader.load_json(os.path.join(iu_dir_input_path, 'research-problem.json'))
        rps = []
        for _, rp_list in ui_rp.items():
            if type(rp_list[0]) == list:
                for items in rp_list:
                    for item in items:
                        if type(item) == dict:
                            rps.append(item['from sentence'])
            else:
                print(">>>>>>>>>>>>>>>>>>>>>>>ISSUE WITH DATA FORMAT IN FILE:",  sample_dir_input_path)
                for item in rp_list:
                    if type(item) == dict:
                        rps.append(item['from sentence'])

        sents_input_index = DataReader.load_text(os.path.join(sample_dir_input_path, "sentences.txt")).split("\n")# [:-1]
        sents_input_index = [eval(index) for index in sents_input_index if len(index) != 0 ]
        sents_output_index = []
        for index, text in enumerate(stanza_out_txt_list):
                if (index+1 in sents_input_index):
                    for rp in rps:
                        if text == rp:
                            sents_output_index.append(index+1)
        if len(sents_output_index) != len(rps):
            print("="*40)
            print("SIZE OF NEWE DATASET SENTENCES IS NOT EQUAL TO RPs: IN FOLLOWING DATA")
            print("sentencs outputs index(new)      :", sents_output_index)
            print("sample input dir(old data path   :", sample_dir_input_path)
            print("sentencs input index (old)       :", sents_input_index)
            print("len of research-problem          :", len(rps))
            print("research problems (new)          :", rps)
            print("UI research problem              :", ui_rp)
            print("="*40)

        sents_output_index = '\n'.join([str(index) for index in sents_output_index])        
        DataWriter.write_text(sents_output_index, os.path.join(sample_dir_output_path, "sentences.txt"))

        # copy RP triples
        triples_dir_output_path = os.path.join(sample_dir_output_path, "triples")
        triples_dir_input_path = os.path.join(sample_dir_input_path, "triples")
        mkdir(triples_dir_output_path)
        shutil.copy(os.path.join(triples_dir_input_path, 'research-problem.txt'), 
                    os.path.join(triples_dir_output_path, 'research-problem.txt'))        

def create_tasks_data(task, input_dir):
    clf_data, ie_data = [], []
    input_dir_path  = os.path.join(input_dir, task)
    for sample_dir in os.listdir(input_dir_path):
        sample_dir_path = os.path.join(input_dir_path, sample_dir)
        sents_index = DataReader.load_text(os.path.join(sample_dir_path, "sentences.txt")).split("\n")
        sents_index = [eval(index) for index in sents_index if len(index)!= 0]

        for item in os.listdir(sample_dir_path):
            if item.endswith("Stanza-out.txt"): 
                texts = DataReader.load_text(os.path.join(sample_dir_path, item)).split("\n")
                break
        
        for index, text in enumerate(texts):
            if index + 1 in sents_index:
                clf_data.append([sample_dir_path, text, index+1, 1])
            else:
                clf_data.append([sample_dir_path, text, index+1, 0])
        
        ui_rp = DataReader.load_json(os.path.join(sample_dir_path, "info-units", 'research-problem.json'))
        
        for _, rp_list in ui_rp.items():
            if type(rp_list[0]) == list:
                for items in rp_list:
                    if len(items[:-1]) > 1:
                        print(f">>>>>>>>>>>>> HIGHER NUMBER OF RPS ENTITY: {len(items[:-1])}   for dir: {sample_dir_path}" )
                    ie_data.append([sample_dir_path, items[:-1],items[-1]['from sentence']])
            else:
                ie_data.append([sample_dir_path, rp_list[:-1],rp_list[-1]['from sentence']])
    return clf_data, ie_data

def plots(data, title, path):
    freq_dict = {}
    for item in data:
        if item not in freq_dict:
            freq_dict[item] = 1
        else:
            freq_dict[item] += 1

    scores = list(freq_dict.keys())
    values = list(freq_dict.values())
    
    fig = plt.figure(figsize = (10, 5))
    
    plt.bar(scores, values, color ='maroon', width = 0.5)
    
    plt.xlabel("index")
    plt.ylabel("No. of indexes")
    plt.title(title)
    plt.show()
    fig.savefig(path)

def plots_lens(data, title, path):
    freq_dict = {}
    for item in data:
        if item not in freq_dict:
            freq_dict[item] = 1
        else:
            freq_dict[item] += 1

    scores = list(freq_dict.keys())
    values = list(freq_dict.values())
    
    fig = plt.figure(figsize = (10, 5))
    
    plt.bar(scores, values, color ='maroon', width = 0.5)
    
    plt.xlabel("Lenghts")
    plt.ylabel("No. of Lenghts")
    plt.title(title)
    plt.show()
    fig.savefig(path)

if __name__ == '__main__':
    stdoutOrigin=sys.stdout 
    DATA_CONFIG = DataConfig().get_args()
    sys.stdout = open(os.path.join(DATA_CONFIG.logs_dir, 'build_dataset.log.txt'), "w")
    SENT_CLF_TRAIN_DATA, IE_TRAIN_DATA = [], []
    SENT_CLF_TEST_DATA, IE_TEST_DATA = [], []
    print("* working on:", DATA_CONFIG.raw_train_dir)
    mkdir(DATA_CONFIG.preprocessed_train_dir)
    for task in os.listdir(DATA_CONFIG.raw_train_dir):
        print(f"{'-'*60} working on train task: {task} -{'-'*60}")
        copy_related_info(task, DATA_CONFIG.raw_train_dir, DATA_CONFIG.preprocessed_train_dir)
        print(f"{'*'*30}  create_tasks_data  {'*'*30}")
        clf_data, ie_data = create_tasks_data(task, DATA_CONFIG.preprocessed_train_dir)
        SENT_CLF_TRAIN_DATA += clf_data
        IE_TRAIN_DATA += ie_data

    print("SIZE OF SENTS:", len(SENT_CLF_TRAIN_DATA))
    print("* working on:", DATA_CONFIG.raw_test_dir)
    mkdir(DATA_CONFIG.preprocessed_test_dir)
    for task in os.listdir(DATA_CONFIG.raw_test_dir):
        print(f"{'-'*60} working on test task: {task} -{'-'*60}")
        copy_related_info(task, DATA_CONFIG.raw_test_dir, DATA_CONFIG.preprocessed_test_dir)
        print(f"{'*'*50}  create_tasks_data  {'*'*50}")
        clf_data, ie_data = create_tasks_data(task, DATA_CONFIG.preprocessed_test_dir)
        SENT_CLF_TEST_DATA += clf_data
        IE_TEST_DATA += ie_data
    

    S_TRAIN_DF = pd.DataFrame(SENT_CLF_TRAIN_DATA, columns =['sample_dir_path', 'text', 'index', 'label'])
    IE_TRAIN_DF = pd.DataFrame(IE_TRAIN_DATA, columns =['sample_dir_path', 'rps', 'sentence'])

    print("Maximum number of index for sent clf task in train for label 1 is:", max(S_TRAIN_DF[S_TRAIN_DF['label'] == 1]['index'].tolist()))
    plots(S_TRAIN_DF[S_TRAIN_DF['label'] == 1]['index'].tolist(), 
         title="index distribution of label 1 in train", 
         path=os.path.join(DATA_CONFIG.logs_dir, "images", "01-research problem-sentence index distributions-train set.jpg"))

    S_TEST_DF = pd.DataFrame(SENT_CLF_TEST_DATA,columns =['sample_dir_path', 'text', 'index', 'label'])
    IE_TEST_DF = pd.DataFrame(IE_TEST_DATA, columns =['sample_dir_path', 'rps', 'sentence'])
    
    print("Maximum number of index for sent clf task in test for label 1 is:", max(S_TEST_DF[S_TEST_DF['label'] == 1]['index'].tolist()))
    plots(S_TEST_DF[S_TEST_DF['label'] == 1]['index'].tolist(), 
         title="index distribution of label 1 in test",
         path=os.path.join(DATA_CONFIG.logs_dir, "images", "02-research problem-sentence index distributions-test set.jpg"))
    
    STATS = {
       "size of IE task in train": IE_TRAIN_DF.shape[0],
       "size of IE task in test": IE_TEST_DF.shape[0],
       "Maximum number of index for sent clf task in train for label 1 (index threshold)": max(S_TRAIN_DF[S_TRAIN_DF['label'] == 1]['index'].tolist()),
       "Maximum number of index for sent clf task in test for label 1": max(S_TEST_DF[S_TEST_DF['label'] == 1]['index'].tolist()),

       "SENT CLF stats before setting index threshold for index":{
        "size of SENT CLF task in train": S_TRAIN_DF.shape[0],
        "size of SENT CLF task in test": S_TEST_DF.shape[0],
        
        "size of class 1 in SENT CLF task in train": sum(S_TRAIN_DF['label'].tolist()),
        "size of class 0 in SENT CLF task in train": S_TRAIN_DF.shape[0] - sum(S_TRAIN_DF['label'].tolist()),

        "size of class 1 in SENT CLF task in test": sum(S_TEST_DF['label'].tolist()),
        "size of class 0 in SENT CLF task in test": S_TEST_DF.shape[0] - sum(S_TEST_DF['label'].tolist())
       }
    }

    INDEX_THRESHODL = max(S_TRAIN_DF[S_TRAIN_DF['label'] == 1]['index'].tolist())
    
    S_TRAIN_DF = S_TRAIN_DF[S_TRAIN_DF['index'] <= INDEX_THRESHODL]
    S_TEST_DF = S_TEST_DF[S_TEST_DF['index'] <= INDEX_THRESHODL]


    STATS["SENT CLF stats after setting index threshold for index"] = {
        "size of SENT CLF task in train": S_TRAIN_DF.shape[0],
        "size of SENT CLF task in test": S_TEST_DF.shape[0],
        
        "size of class 1 in SENT CLF task in train": sum(S_TRAIN_DF['label'].tolist()),
        "size of class 0 in SENT CLF task in train": S_TRAIN_DF.shape[0] - sum(S_TRAIN_DF['label'].tolist()),

        "size of class 1 in SENT CLF task in test": sum(S_TEST_DF['label'].tolist()),
        "size of class 0 in SENT CLF task in test": S_TEST_DF.shape[0] - sum(S_TEST_DF['label'].tolist())
       }
    
    S_TRAIN_DF['text-len'] = [len(text.split()) for text in S_TRAIN_DF['text'].tolist()]
    S_TEST_DF['text-len'] = [len(text.split()) for text in S_TEST_DF['text'].tolist()]

    print("Minimum number of text len for sent clf task in train for label 1 is:", min(S_TRAIN_DF[S_TRAIN_DF['label'] == 1]['text-len'].tolist()))
    plots_lens(S_TRAIN_DF[S_TRAIN_DF['label'] == 1]['text-len'].tolist(), 
         title="text-len distribution of label 1 in train", 
         path=os.path.join(DATA_CONFIG.logs_dir, "images", "03-research problem-sentence text-len distributions-train set.jpg"))

    print("Minimum number of text len for sent clf task in test for label 1 is:", min(S_TEST_DF[S_TEST_DF['label'] == 1]['text-len'].tolist()))
    plots_lens(S_TEST_DF[S_TEST_DF['label'] == 1]['text-len'].tolist(), 
         title="text-len distribution of label 1 in test",
         path=os.path.join(DATA_CONFIG.logs_dir, "images", "04-research problem-sentence text-len distributions-test set.jpg"))

    STATS["Minimum number of text len for sent clf task in train for label 1 (text len threshold)"] = min(S_TRAIN_DF[S_TRAIN_DF['label'] == 1]['text-len'].tolist())
    STATS["Minimum number of text len for sent clf task in test for label 1"] = min(S_TEST_DF[S_TEST_DF['label'] == 1]['text-len'].tolist())

    TEXT_LEN_THRESHODL = min(S_TRAIN_DF[S_TRAIN_DF['label'] == 1]['text-len'].tolist())
    
    S_TRAIN_DF = S_TRAIN_DF[S_TRAIN_DF['text-len'] >= TEXT_LEN_THRESHODL]
    S_TEST_DF = S_TEST_DF[S_TEST_DF['text-len'] >= TEXT_LEN_THRESHODL]

    STATS["SENT CLF stats after setting text-len threshold for index"] = {
        "size of SENT CLF task in train": S_TRAIN_DF.shape[0],
        "size of SENT CLF task in test": S_TEST_DF.shape[0],
        
        "size of class 1 in SENT CLF task in train": sum(S_TRAIN_DF['label'].tolist()),
        "size of class 0 in SENT CLF task in train": S_TRAIN_DF.shape[0] - sum(S_TRAIN_DF['label'].tolist()),

        "size of class 1 in SENT CLF task in test": sum(S_TEST_DF['label'].tolist()),
        "size of class 0 in SENT CLF task in test": S_TEST_DF.shape[0] - sum(S_TEST_DF['label'].tolist())
       }
    
    IE_TRAIN_DF.to_csv(DATA_CONFIG.ie_train_data_path, index=False)
    IE_TEST_DF.to_csv(DATA_CONFIG.ie_test_data_path, index=False)
    S_TEST_DF.to_csv(DATA_CONFIG.sent_clf_test_data_path, index=False)
    S_TRAIN_DF.to_csv(DATA_CONFIG.sent_clf_train_data_path, index=False)
    DataWriter.write_json(STATS, os.path.join(DATA_CONFIG.logs_dir, 'data.stats.json'))
    sys.stdout.close()