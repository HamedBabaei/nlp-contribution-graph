# NLPContributionGraph (NCG) Challenge


## 1. Introduction
[NLPContributionGraph](https://ncg-task.github.io/) challenge aim is to struct scholarly NLP contributions in the open research knowledge graph (ORKG). It is posited as a solution to the problem of keeping track of research progress. The dataset for this task is defined in a specific structure to be integrable within KG infrastructures such as ORKG.  It consists of the following information:
1. `Contribution sentences`: A sentence about contributions from papers.
2. `Scientific terms and relations`: A set of scientific terms or phrases from contribution sentences.
3. `Triples`: subject-predicate-object statements for KG constructions. The triples are organized under three mandatory (*Research Problem, Approach, Model*) or more information units (IUs) (*Code, Dataset, Experimental Setup, Hyperparameters, Baselines, Results, Tasks, Experiments, and Ablation Analysis*).

In this work, the major concern is `Research Problem` (RP) extraction. To do this, we need to find contribution sentences that contain RPs. Next, using the contribution sentences we are able to extract RPs. To do this we designed a classifier that identifies contribution sentences that contain RPs. Next, we feed them into a text summarizer to extract RP phrases.


## 2. Dataset Preparations
The proposed method for the task is two-fold: (1) an RP classifier to identify RP sentences, and (2) a text summarizer to extract RP phrases. Also, we are only interested in extracting RPs so the rest of the data such as phrases and triples related to other IUs, are not relevant to this task. To only consider the metadata that is needed in this task, the original dataset was presented in [NCG task training-data](https://github.com/ncg-task/training-data) and [NCG task test-data](https://github.com/ncg-task/test-data) converted into the following format. The transformed data exist in the `dataset/preprocessed` directory. 
```
[task-name-folder]/                               
    ├── [article-counter-folder]/                 
    │   ├── [articlename]-Stanza-out.txt          
    │   ├── sentences.txt                         
    │   └── info-units/                           
    │   │   └── research-problem.json             
    │   └── triples/                              
    │   │   └── research-problem.txt              
    │   └── ...                                   
    └── ...
```
Next, to train models, we list all sentences in the train/test for the RP classifier. Next, we used the `info-units/research-problem.json` file to build summarization data, where the phrases are the summary and the sentences are input texts for the summarization task. These datasets are exist in `dataset/preprocessed/experiment-data` directory. The stats of the RP classification and RP summarization tasks are as follows:

<table style='text-align:center;'>
  <tr>
    <td> <b>Tasks\Datasets</b> </td>
    <td colspan="3"><b>Training-data</b></td>
    <td colspan="3"><b>Test-data</b></td>
  </tr>
  <tr>
    <td>  </td>
    <td colspan="1"> Class-0 </td>
    <td colspan="1"> Class-1 </td>
    <td colspan="1"> All-data </td>
    <td colspan="1"> Class-0 </td>
    <td colspan="1"> Class-1 </td>
    <td colspan="1"> All-data </td>    
  </tr>
  <tr>
  <td>RP Classifcation - Raw Data</td>
    <td colspan="1"> 607 </td>
    <td colspan="1"> 54831 </td>
    <td colspan="1"> 55438 </td>
    <td colspan="1"> 316 </td>
    <td colspan="1"> 33639 </td>
    <td colspan="1"> 33955 </td>
  </tr>
  <tr>
    <td>RP Classifcation - Preprocessed Data</td>
    <td colspan="1"> 607 </td>
    <td colspan="1"> 9816 </td>
    <td colspan="1"> 10423 </td>
    <td colspan="1"> 314 </td>
    <td colspan="1"> 6501 </td>
    <td colspan="1"> 6815 </td>
  </tr>
    <tr>
    <td>RP Summarization</td>
    <td colspan="3"> 602 </td>
    <td colspan="3"> 314 </td>
  </tr>
</table>

<b style='text-align:center;'>Table 1: Statistics of the dataset</b>

**Note**: `build_dataset.py` scripts are doing whole the dataset preparations with the proposed preprocessing method.


## 3. Proposed System

Figure 1 presents the proposed system architectures. After the data preparations, each task (RP classification and RP summarization) builds its own data. For the RP classification task, we made preprocessing which ended up decreasing unwanted samples (stats presented in Table 1) for fine-tuning the transformer model for RP sentences identification. For RP summarization, we fine-tuned T5 to summary RP sentences.

![NLPContributionGraph](images/NLPContributionGraph-Architecture.jpg)

<b style='text-align:center;'>Figure 1: Proposed System Architecture</b>

The preprocessing step and models are described in the following.

#### 3.1 Preprocessing

The number of samples was too high for the RP classification task of the proposed system. To reduce the size of the dataset we applied two thresholds over data based on hyperparameter tuning over the train set.

**1) Maximum Index Threshold**: According to [J. D’Souza and S. Auer](http://ceur-ws.org/Vol-2658/paper2.pdf) action in designing NCG dataset, most of the research problems come from the title, abstract, and introduction part of the paper. However here, due to the variant in the structure of papers, it is hard to separate these sections in order to reduce the amount of training unwanted sentences.

We made an analysis of the RP indexes distributions to find an appropriate number of samples from each document to be considered for the RP classification task. Here indexes are the no. of sentences that appeared in the paper to be RP. 

Figure 2 shows the distribution of RP indexes in the train and test sets. To avoid any bias we select $I_{th} = 50$ where it is the maximum index threshold based on the train set. Analysis of the test set showed that we only lost 2 samples in such a case, but the threshold reduced a significant amount of unwanted samples for training the RP classifier.

![PreprocessingDist](images/distributions.png)
<b style='text-align:center;'>Figure 2: Distributions of RP indexes and lenghts </b>

**2) Minimum Text Length Threshold**: Most papers consist of sentences with a single word or 2, 3 words. This might not happen in RP sentences. To confirm the observations we plot the length of RP sentences in the train set. And according to these observations we used $T_{th} =  3$ as the text length threshold to reduce the number of unwanted sentences.

In the end, we obtained a very good-shaped dataset for our classification task. The stats for the dataset is presented in Table 1. We reduced the **train set by 82%** and **test set by 79%**. During the data reduction, we only lost 2 samples in the test set. The created datasets are stored in the `dataset/preprocessed/experiment-data` directory.

#### 3.2 RP Classification for RP Sentence Detection
The RP sentence identification is described as a text classification of the sentences into 0 or 1. Where we are interested in the category of 1. It is a highly imbalanced text classification problem. For this manner, we fine-tunned `distilroberta-base` with a learning rate of `2e-5`, batch size of `16`, and epoch number of `5`.

#### 3.3 RP Summarization for RP Phrase Extraction
After RP sentence identification, the next step is to extract RP phrases. To do that we tack a summarization approach. To build a summarization model specific for this task we fine-tuned the `T5-base` model with a learning rate of `2e-5`, batch size of `8`, and epoch number of `5`. In tokenization step of T5 text summarization, we used input text `max_length=1024` and summary `max_length=128`. During inference, we applied output `max_length=10` for generating summaries.

## 4. Results

#### 4.1 Setups
**Metrics**: For the whole system in the NCG task, the [scoring program](https://github.com/ncg-task/scoring-program) has been designed to calculate F1, precision, and recalls for Sentences, Information Units, and Triples. Here, since we are only interested in one IU so results for triples will be the F1, precision, and recall of research-problem IU. For text summarization, we used Rouge1, Rouge2, RougeL, and RougeLsum for manual evaluations.

**Baseline Model**: For comparison of the proposed method, we made the simplest model for the task called `xgboost-t5small`. This model uses TFIDF features and XGBoost Classifier for RP sentence identification, and T5-Small for text summarization. According to the analysis, we found that XGBoost is performing better than other classifiers with TFIDF features.


#### 4.2 Experimental Evaluations
Table 2 presents the experimental evaluations over test sets. The `RP Classification` results are averaged macro scores. According to these results, even fine-tuning a transformer model in the simplest way is performing quite well on this task. However, we may believe the data reduction technique effect as well. 

For `RP Summarization`, T5 models are quite appropiate choice here since fine-tuning different version of this models in a simplest way without any hyperparamether tuning is giving very promising results. 
<table style='text-align:center;'>
  <tr>
    <td> <b>Task</b> </td>
    <td colspan="3"><b>RP Classifcation</b></td>
    <td colspan="4"><b>RP Summarization</b></td>
  </tr>
  <tr>
    <td><i> Metrics </i></td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
    <td colspan="1">Rouge1</td>
    <td colspan="1">Rouge2</td>
    <td colspan="1">RougeL</td>
    <td colspan="1">RougheLsum</td>
  </tr>
  <tr>
    <td>xgboost-t5small</td>
    <td colspan="1">0.63</td>
    <td colspan="1">0.78</td>
    <td colspan="1">0.59</td>
    <td colspan="1">75.12</td>
    <td colspan="1">55.04</td>
    <td colspan="1">64.86</td>
    <td colspan="1">64.86</td>
  </tr>
  <tr>
  <td>distilroberta-t5base</td>
     <td colspan="1">0.75</td>
    <td colspan="1">0.77</td>
    <td colspan="1">0.74 </td>
    <td colspan="1">79.56</td>
    <td colspan="1">62.95</td>
    <td colspan="1">71.42</td>
    <td colspan="1">71.42</td>
  </tr>
</table>
<b style='text-align:center;'>Table 2: Experimental Evaluations</b>

In conclusion, we can see that the `distilroberta-t5base` model is performing well. So introducing more complexity to this model may allow us to boost the current model performance.

#### 4.3 Final Evaluations


<table style='text-align:center;'>
  <tr>
    <td> <b>Models</b> </td>
    <td colspan="3"><b>Sentences</b></td>
    <td colspan="3"><b>Information Units</b></td>
    <td colspan="3"><b>Triples</b></td>
    <td colspan="1"><b>Average</b></td>
  </tr>
  <tr>
    <td><i> Metrics </i></td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
    <td colspan="1">F1</td>
  </tr>
  <tr>
    <td>xgboost-t5small</td>
    <td colspan="1">0.281</td>
    <td colspan="1">0.604</td>
    <td colspan="1">0.183</td>
    <td colspan="1">0.609</td>
    <td colspan="1">1.0</td>
    <td colspan="1">0.438</td>
    <td colspan="1">0.173</td>
    <td colspan="1">0.385</td>
    <td colspan="1">0.112</td>
    <td colspan="1">0.355</td>
  </tr>
  <tr>
  <td>distilroberta-t5base</td>
    <td colspan="1">0.524</td>
    <td colspan="1">0.568</td>
    <td colspan="1">0.487</td>
    <td colspan="1">0.941</td>
    <td colspan="1">1.0</td>
    <td colspan="1">0.890</td>
    <td colspan="1">0.326</td>
    <td colspan="1">0.362</td>
    <td colspan="1">0.297</td>
    <td colspan="1">0.597</td>
  </tr>
</table>
<b style='text-align:center;'>Table 3: Final Evaluations - NCG Task Metrics</b>


##### Main Quantitative Findings: 
Table 3 presents the final results of the test set using NCG task metrics. The main quantitative findings are:
1. The proposed method `distilroberta-t5base` achieved averaged f1-score of **0.597** and beat the baseline model by a large margin. The averaged F1-Score has been calculated as follows: $(F1_{sentences} + F1_{IU} + F1_{triples})/3$.
2. IUs (RPs) are being identified in 94% of the cases (the percentage is not representing the correctness of identified sentences as an RPs)
3. RPs are now being identified in 52% of the cases which is two times higher than the baseline model.
4. The weakness of the system comes from triples, where we have still low F1 scores in the `distilroberta-t5base` model. This weakness may solve by giving more attention to the summarization module. Since we didn't put much effort into hyperparameter tuning of this module.

##### Quantitative Analysis:
We have used experimentations on the test set to conclude the `distilroberta-base` model as a final system. Table 2 and Table 3 show experimental and final results. The quantitive analysis is presented as follows:

1. The recall metric become important in the RP classification task since we could get a high possibility of extracting RP phrases with RP summarization. However, the best model still suffers from this perspective. But considering the baseline model, it is improved by 30% and it shows why the summarization service was able to extract triples in the double rate of the baseline model (f1 score of 32%).

2. The `xgboost-t5small` model shows that TFIDF features are not quite well for this task. The possible reason behind this is the high word correlations between RP and other IU sentences. This leads to poor feature quality for RP class.

3. Summarization model is working well in development however, its results decreased during the final evaluation phase where only RP sentences were considered for phrase extraction.  Here considering RP sentence detection F1 score of 52% the summarization achieved 62.2% of the time (`32.6%/52.4% = 62.2%`) correct summarization. So increasing the accuracy of the RP sentence detection module affects the triple (RP phrase) extraction module as well. 

4. The 59.7% averaged f1 score of the system is mostly affected by IU score since it is been calculated regardless of how much is accurate the content if a paper has the `research-problem.txt` triples it will be counted toward true positives in IU. Ignoring this metric and considering $(F1_{sents} + F1_{triples})/2$ the obtained averaged f1 scores are **0.425** and **0.227** for `distilroberta-t5base` and `xgboost-t5small` models respectively. So, the proposed method boosts the baseline models by **53%**.

## 5. Oservations && Code Instructions

#### 5.1 Observations
1. Investigations showed that in a few cases sentences with RP labels were repeated multiple times in papers, however, these sentences didn't appear in the original contribution sentences. As an example, in the `training-set/Passage_re-ranking/1` paper, the first item of `info-units/resarch-problem.json` appeared once in the title and one more time in the body of the paper. But the body sentence index didn't appear in the `sentences.txt`
2. For many of the files in `info-units/research-problem.json` there is inconsistency in data structures and the issue has been solved in building the dataset by hard coding. As an example, in `training-set/natural-language-inference/`, papers `50`, `45`, and `14` have an inconsistent data structure with other papers. This scenario is repeated many times. For inconsistency, RPs in these papers should be inside of a list like others.

3. In [scoring program](https://github.com/ncg-task/scoring-program) we saw that the evaluation is being done on two papers for each task only. we fix this by allowing the evaluation to go through all the papers. The following line in code has been changed from ```for i in range(2):``` to ```for i in range(len(os.listdir(os.path.join(gold_dir, task)))):```

#### 5.2 Code Instructions

```
[assets]/                    # Model artifacts directory
[configuration]/             # Configs of model, data and evaluations
[datahandler]/               # data loader/saver modules to load/save files
[dataset]/                   # dataset directory consist of created data and experimental data
[images]/                    # repository image directory
[notebooks]/                 # experimental jupyter notebook of the project such as training text-summarization (section 3.2) and classifications (section 3.3)
[outputs]/                   # output of the models and evaluation results
[report]/                    # build dataset and dataset stats report dir
[src]/                       # classifcation, evaluation, and summarizer script dir
  ├── .gitignore
  ├── README.md
  ├── __init__.py
  ├── build_dataset.py                 # building datasets that mentioned in section 2
  ├── requirements.txt                 # requirenment of the project
  ├── runner.py                        # the final inferencers that combines models and do the evaluations
  └── train_sentence_classifier_bs.py  # xgboost model
```

1. Building dataset:
```python
python3 build_dataset.py
```
2. Train text-summarization and text-classification models using Jupyter-notebooks in `notebooks` dir and save artifacts in `assets` dir with the name of `clf-distilroberta` and `sum-t5base`.
3. Run the following script to produce outputs and evaluations on `outputs/distilroberta-t5base` directory
```python
python3 runner.py
```

## Requirements
* Python3
* Packages in requirements.txt
