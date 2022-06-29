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
    <td> </td>
    <td colspan="3">Sentences</td>
    <td colspan="3">Information Units</td>
    <td colspan="3">Triples</td>
  </tr>
  <tr>
    <td> </td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
  </tr>
    <td>xgboost-t5small</td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>
    <td colspan="1">F1</td>
    <td colspan="1">P</td>
    <td colspan="1">R</td>

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
