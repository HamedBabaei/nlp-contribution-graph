# NLPContributionGraph (NCG) Challenge
https://github.com/ncg-task

### Idea

### Introduction
The goal is to build a research problem extraction system.

### Data Preprations
train: https://github.com/ncg-task/training-data
test: https://github.com/ncg-task/test-data

1. considering only RP sentences in sentences.txt using info
2. considering triples related to RP in triples directory
3. consider stanza output only (ignore pdf files as well)
4. consider RP in info_units only
5. NEXT: build two type of data:
    - list of all sentences in train/test with labels and preprocessings of removing short texts is not should be done here - text classification data
    - geting research problems with considering only sentences and RPs - extractive text summarization data 

check this befor doing preprations: 
* https://github.com/ncg-task/sample-submission


### Proposed Method
- architecture
- architecture steps
    - preprocessings (remove short texts)
    - classifiers
        - baseline (tfidf + lr)
    - information extraction
        - sentences as RP
https://huggingface.co/docs/transformers/tasks/sequence_classification

### Setups

- Metrics:
    - recall, precition, f1
    - talk about recall importance in classification here and why and what is the major goal?
- dataset


### Evaluation

* https://github.com/ncg-task/scoring-program

- clf eval
- ie eval
- whole system eval



<table style='text-align:center;'>
  <tr>
    <td> <i>Models</i> </td>
    <td colspan="3"><i>Sentences</i></td>
    <td colspan="3"><i>Information Units</i></td>
    <td colspan="3"><i>Triples</i></td>
    <td colspan="1"><i>Average</i></td>
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
  <td><i> distilroberta-t5base </i></td>
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



### Future works
- Using title, abstract, and introductions only
- Classifier: Transformers 
- Classifier: GCN
- Group Rankings in sentence classificatons
- IE: keyword extraction 
- IE: topic modeling
- IE: NER *
- IE: summarization 

### Code Instructions


### Resource

* https://github.com/ncg-task/sample-submission
