# ONGC-NLP-project
It extracts images from ONGC's Well Completion Reports, names them based on their labels in the PDFs, and then categorises them by applying NLP on the labels. The aim was to help ONGC make an image database and make it easier for employees to look for their desired images instead of having to scroll through numerous lengthy reports.

Since ONGC's data is confidential, ONGC WCRs are not included in the WCR directory, but I've provided publicly available WCRs from other organisations for you to test the code.

Steps to follow:
1) In the terminal: 
    pip install -r requirements.txt
2) For spacy, in the terminal:
    a) pip install -U pip setuptools wheel
    b) pip install -U spacy
    c) python -m spacy download en_core_web_sm
    d) python -m spacy download en_core_web_lg
3) Run main.py
