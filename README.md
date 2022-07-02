# NLPContributionGraph (NCG) Challenge


## 1. Introduction
[NLPContributionGraph](https://ncg-task.github.io/) challenge aim is to struct scholarly NLP contributions in the open research knowledge graph (ORKG). It posited as a solution to the problem of keeping track of research progress. The dataset for this task is defined in specific structure to be integrable within KG infrastructures such as ORKG.  It consist of the following informations:
1. `Contribution sentences`: A sentence about contributions from papers.
2. `Scientific terms and relations`: A set of scientific term or phrases from contribution sentences.
3. `Triples`: subject-predicate-object statements for KG constructions. The triples are orgnized under thre mandatory (*Research Problem, Approach, Model*) or more information units (IUs) (*Code, Dataset, Experimental Setup, Hyperparameters, Baselines, Results, Tasks, Experiments, and Ablation Analysis*).

In this work the major concern is `Research Problem` extraction. To do this, we need to find contribution sentences that contain `Research Problems` IU. Next, using the contribution sentences we may extract problems. To do this we designed a classifier that identifys contribution sentences with research problems (RPs), next a text summarizer to extracts RP phrases.

## 2. Dataset Preprations
The proposed method to the task is two-fold: (1) a research problem classifier to identify research problem sentences, (2) a text summarizer to extract research problem phrases. Also, we only interested in extracting research problems so the resest of the data such as phrases and triples related to other IU are not relevent to this task. To only consider metada that is needed in this task we considered the following changes:
1. Considered `*-Stanza-out.txt` text files and ignored the other preprocessed text file and original pdf file. (for simplisity)
2. Considered only a `resarch-problem.JSON` file from `info-units` directory.
3. Changed `sentences.txt` content using `info-units/research-problem.json` file to consider indexes of sentences that contain researchp roblems.
4. Considered only a `resarch-problem.txt` file from `triples` directory.

The orignal dataset which presented in [NCG task training-data](https://github.com/ncg-task/training-data) and [NCG task test-data](https://github.com/ncg-task/test-data) converted into the following format. The transformed data exist in `dataset/preprocessed` directory. 
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
Next, to train models, we list all sentences in the train/test for research problem classifier. Next, we used `info-units/research-problem.json` file to build summarization data, where the phrases are the summary and the sentences are input texts to summarization service. These datasets are exist in `dataset/preprocessed/experiment-data` directory. The stats of the research problem classifier and research problem phrase extractions are as follows:
<!-- During data preprations we runned a preprocessings to avoid any complex modelings in future. So the data which construcuted for both tasks are preprocessed (which the preprocessin has been described in section 3 - proposed method).  -->
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
  <td>Research Problem Classifier</td>
    <td colspan="1"> 607 </td>
    <td colspan="1"> 54831 </td>
    <td colspan="1"> 55438 </td>
    <td colspan="1"> 316 </td>
    <td colspan="1"> 33639 </td>
    <td colspan="1"> 33955 </td>
  </tr>
  <tr>
    <td>Research Problem Classifier (preprocessed)</td>
    <td colspan="1"> 607 </td>
    <td colspan="1"> 9816 </td>
    <td colspan="1"> 10423 </td>
    <td colspan="1"> 314 </td>
    <td colspan="1"> 6501 </td>
    <td colspan="1"> 6815 </td>
  </tr>
    <tr>
    <td>Research Problem Summarization</td>
    <td colspan="3"> 602 </td>
    <td colspan="3"> 314 </td>
  </tr>
</table>

<b style='text-align:center;'>Table 1: Statistics of the dataset</b>

**Note**: `build_dataset.py` scripts is doing whole the dataset preprations with proposed method preprocessings.


## 3. Proposed System

The Figure-1 presents the proposed system architectures. After the data preprations, each task (sentence classification and text summarization) builds own data. For sentence classification task we made preprocessing which ended up of decreasing unwanted samples (stats presented in table-1) for fine-tuning transformer model for research problem sentence detection. For text summarization we fine-tuned T5 to summary research problem sentences.

![NLPContributionGraph](images/NLPContributionGraph-Architecture.jpg)

<b style='text-align:center;'>Figure 1: Proposed System Architecture</b>

The preprocessing step and models described in the followings

#### 3.1 Preprocessing

The number of samples were too high for research problem classification part of the proposed system. To reduce the size of dataset we applied two thresholds over data based on hyperparameter tuning over train set.

**1) Maximum Index Threshold**: According to [J. D’Souza and S. Auer](http://ceur-ws.org/Vol-2658/paper2.pdf) effort in designing NCG dataset, most of the research problems come from title, abstract and introduction part of the paper. However here, due to the variant in structure of papers it is hard to seprate these sections.

We made an analysis of the research problem indexes distributions to find appropiate number of samples from each documents to be considered for research problem classification. Here index is the no. of sentence that appeared in the paper to be research problem. 

The Figure-2 shows the distribution of research problem indexes in train and test set. To avoid any bias we select $I_{th} = 50$ where it is the maximum index threshold based on train set. Analysis of test set showed that we only losing 2 samples in train if we set threshold $I_{th} = 5$ however we reduce a significant amount of unwanted samples for training classifiers.

![PreprocessingDist](images/distributions.png)
<b style='text-align:center;'>Figure 2: Distributions of research problem indexes and lenghts </b>

**2) Minimum Text Lenght Threshold**: Most of papers consist of sentences with a single word or multple words that in a few cases research problems are in group that higher than a specific words. To confirm the observations we plot the lenght of research problemts in train set. And according to these observations we used $T_{th} =  3$ as text lenght threshold. 

At the end, we obtained a very good shaped dataset for our classification task. The stats for the dataset is presented in `Table-1`. We reduced **train set by 82%** and **test set by 79%**. During the data reduction we only lost 2 samples in test set, however our models can be trained appropiately. The created datasets stored in `dataset/preprocessed/experiment-data` directory.

#### 3.2 Research Problem Classifier
The research problem sentence identification described as a text classification of the sentences into 0 or 1. Where we interested in category 1. It is highly imbalanced text classification problem. For this manner, we fine-tunned `distilroberta-base` over training data with learning rate of `2e-5`, batch size of `16`, and epoch number of `5`.

#### 3.3 Research Problem Phrase Extraction
After research problem sentence identification, the next step is to extract research problems. To do that we tack summarization approach. To build summarization model specific for this task we fine-tuned `T5-base` model over training data with learning rate of `2e-5`, batch size of `8`, and epoch number of `5`. In tokenization step of T5 text summarization, we used input text `max_length=1024` and summary `max_length=128`. During inference we applied output `max_length=10` for generating summaries.

## 4. Results

#### 4.1 Setups
**Metrics**: For whole system in NCG task a [scoring program](https://github.com/ncg-task/scoring-program) has been designed to calculate F1, precision, and recalls for Sentences, Information Units, and Triples. Here, since we only interested in one IU so results for triples will be the F1, precisin, and recall about research-problem IU. For text summarization, we used Rouge1, Rouge2, RougeL, and RougeLsum for manual evaluations.
<!-- - talk about recall importance in classification here and why and what is the major goal? -->
<!-- **Trainings**:  -->
**Baseline Model**: For comparision of proposed method, we made a simpleset model for the task called `xgboost-t5small`. This model uses TFIDF features and XGBoost Classifier for research problem sentence identification, and T5-Small for text summarizations. According to the analysis we found XGBoost is performing better than other classifiers with TFIDF features.


#### 4.2 Experimental Evaluations
The Table-2 presents the experimental evaluations over test sets. The `research problem classification` results are averaged macro scores. According to the these results, even fine-tuning a transformer model in a simplest way is performing quite well on this task. However, we may believe the data reduction technique effect as well. 
For `research problem phrase extraction`, T5 models are quite appropiate choice here since fine-tuning different version of this models in a simplest way without any hyperparamether tuning is giving very promising results. 
<table style='text-align:center;'>
  <tr>
    <td> <b>Task</b> </td>
    <td colspan="3"><b>Research Problem Classifcation</b></td>
    <td colspan="4"><b>Research Problem Phrase Extraction</b></td>
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
<b style='text-align:center;'>Table 2: ExpPassage_re-ranking/1` paper, first item of `info-units/erimental Evaluations</b>

In conclution, we can see that `distilroberta-t5base` models is good regarding the simplest model. So introducing more complexity on this simple model may allow us to boost the current model performance.



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
Table-2 presents the final results on the test set using NCG task metrics. The main quantitative findings are:
1. The proposed method `distilroberta-t5base` achived averaged f1-score of **0.597** and defeet baseline model by large margin. The averaged F1-Score has been calculated as follows: $(F1_{sentences} + F1_{IU} + F1_{triples})/3$.
2. IUs (research-problem) are being identified in 94% of the cases (the precentage is not representing the correctness of identified sentences as research problem)
3. Research problems are now being identified in 52% of the cases which is two times higher than baseline model.
4. The weekness of the system comes from triples, where we have still low F1 scores in baseline model. This weekness may solve by giving more attention to summarization module. Since, we didn't put much effort on hypterparameter tunnings.

##### Quantitative Analysis:
We have used experimentations on the test set to conclude the `distilroberta-base` model as a final system. The table 2 and table 3 shows experimental and final results. The quantitive analysis are presented as follows:

1. The recall metric become important in sentence classification task since much we could get the possibility of extracting triples that represents the resarch-problems are high. However, the best model is still suffer from this prespective. But considering the baseline model, it is improved by 30% and it shows why summarization service was able to extract triples in double rate of baseline model (f1 score of 32%).

2. The `xgboost-t5small` model shows that TFIDF features are not quite well for this task. The possible reason behind this is the high word correlations between research-problem and other sentences. Which it leads to poor feature quality for research-problem class.

3. Summarization model is working well in development however, its results decreased during final evalution phase where only research problem sentences was considered for phrase extraction.  Here considering sentence detection F1 score of 52% the summarization achived 62.2% of the time (`32.6%/52.4% = 62.2%`) correct summarization. So increasing the accurcy of research problem sentence detection module effects the triple extraction modules. 

4. The 59.7% averaged f1 score of system is mostly effected by IU score, since its been calculated regardless of how much is accurate the content, if a paper has the `research-problem.txt` triples it will be counted toward true positives in IU. Ignoring this metric and considering $(F1_{sents} + F1_{triples})/2$ the obtained averated f1 scores are **0.425** and **0.227** for `distilroberta-t5base` and `xgboost-t5small` models respectively. So, the proposed method boost the baseline models by **53%**.

<!-- In experimental analysis which presented in table-2 summarization has 20% of error (considering rouge1 score) -->


## 5. Oservations && Code Instructions

#### 5.1 Observations
1. Investigations showed that in few cases sentences with research-problem label repeated multiple times in papers, however these sentences didn't appear in the original contribution sentences. As an example, in `training-set/Passage_re-ranking/1` paper, first item of `info-units/resarch-problem.json` appeared once in title and one more time in the body of paper. But its sentence index appeared once in the `sentences.txt`
2. For many of files in `info-units/research-problem.json` there is inconsistency in data structures which we solve this issue in building dataset by hard coding. As an example, in `training-set/natural-language-inference/`, papers `50`, `45`, and `14` have inconsistant data strcuture with other papers. This scenario repeated many times. For inconsistency, research-problems in these papers sould be inside of a list like others.
3. In [scoring program](https://github.com/ncg-task/scoring-program) we saw that the evaluation is being done on two papers for each task only. we fix this by allowing the evaluation go through all the papers. The following line in code has been changed from ```for i in range(2):``` to ```for i in range(len(os.listdir(os.path.join(gold_dir, task)))):```

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
  ├── requirenments.txt                # requirenment of the project
  ├── runner.py                        # the final inferencers that combines models and do the evaluations
  └── train_sentence_classifier_bs.py  # xgboost model
```

1. Building dataset:
```python
python3 build_dataset.py
```
2. Train text-summarization and text-classification models using jupyter-notebooks in `notebooks` dir and save artifacts in `assets` dir with the name of `clf-distilroberta` and `sum-t5base`.
3. Run the following script to produce outputs and evaluations on `outputs/distilroberta-t5base` directory
```python
python3 runner.py
```
<!-- 
## 6. Future works
- Using title, abstract, and introductions only
- Classifier: Transformers 
- Classifier: GCN
- Group Rankings in sentence classificatons
- IE: keyword extraction 
- IE: topic modeling
- IE: NER *
- IE: summarization  -->


## Requirenments
* Python3
* Packages in requirenments.txt


<!-- ### References
https://zenodo.org/record/1157185#.Yr4JZ9JBzeQ
http://ceur-ws.org/Vol-2658/paper2.pdf
1. https://ncg-task.github.io/
2. https://github.com/ncg-task
3. https://github.com/ncg-task/training-data
4. https://github.com/ncg-task/test-data
5. https://github.com/ncg-task/sample-submission -->