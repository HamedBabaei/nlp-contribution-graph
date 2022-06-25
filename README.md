# NLPContributionGraph (NCG) Challenge

### Idea

### Introduction
The goal is to build a research problem extraction system.

### Data Preprations
1. considering only RP sentences in sentences.txt using info
2. considering triples related to RP in triples directory
3. consider stanza output only (ignore pdf files as well)
4. consider RP in info_units only
5. NEXT: build two type of data:
    - list of all sentences in train/test with labels and preprocessings of removing short texts is not should be done here - text classification data
    - geting research problems with considering only sentences and RPs - extractive text summarization data 

### Proposed Method
- architecture
- architecture steps
    - preprocessings (remove short texts)
    - classifiers
        - baseline (tfidf + lr)
    - information extraction
        - sentences as RP
        

### Setups

- Metrics:
    - recall, precition, f1
    - talk about recall importance in classification here and why and what is the major goal?
- dataset


### Evaluation

- clf eval
- ie eval
- whole system eval

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