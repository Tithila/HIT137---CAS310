import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from collections import Counter

def split_text(text, max_length=100000):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def extract_entities_spacy(model_name, text, chunk_size=100000):
    nlp = spacy.load(model_name)
    entities = {'disease': [], 'drug': []}
    
    chunks = split_text(text, chunk_size)
    for chunk in chunks:
        doc = nlp(chunk)
        for ent in doc.ents:
            if ent.label_ == 'Disease':
                entities['disease'].append(ent.text)
            elif ent.label_ == 'Drug':
                entities['drug'].append(ent.text)
    
    return entities

def extract_entities_biobert(text, chunk_size=100000):
    tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
    model = AutoModelForTokenClassification.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    
    entities = {'disease': [], 'drug': []}
    chunks = split_text(text, chunk_size)
    
    for chunk in chunks:
        ner_results = nlp(chunk)
        for result in ner_results:
            if result['entity'].startswith('B-Disease') or result['entity'].startswith('I-Disease'):
                entities['disease'].append(result['word'])
            elif result['entity'].startswith('B-Drug') or result['entity'].startswith('I-Drug'):
                entities['drug'].append(result['word'])
    
    return entities

def compare_entities(entities1, entities2):
    count_entities1 = {key: Counter(value) for key, value in entities1.items()}
    count_entities2 = {key: Counter(value) for key, value in entities2.items()}
    
    comparison = {}
    for key in count_entities1.keys():
        comparison[key] = {
            'Total in Model 1': sum(count_entities1[key].values()),
            'Total in Model 2': sum(count_entities2[key].values()),
            'Difference': sum(count_entities1[key].values()) - sum(count_entities2[key].values()),
            'Most Common in Model 1': count_entities1[key].most_common(10),
            'Most Common in Model 2': count_entities2[key].most_common(10)
        }
    
    return comparison

file_path = 'output.txt'

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

text = load_text(file_path)

entities_sci_sm = extract_entities_spacy("en_core_sci_sm", text)
entities_bc5cdr = extract_entities_spacy("en_ner_bc5cdr_md", text)

entities_biobert = extract_entities_biobert(text)

comparison_sci_sm_bc5cdr = compare_entities(entities_sci_sm, entities_bc5cdr)
comparison_biobert_sci_sm = compare_entities(entities_biobert, entities_sci_sm)
comparison_biobert_bc5cdr = compare_entities(entities_biobert, entities_bc5cdr)

print("Comparison between en_core_sci_sm and en_ner_bc5cdr_md:")
print(comparison_sci_sm_bc5cdr)

print("\nComparison between BioBERT and en_core_sci_sm:")
print(comparison_biobert_sci_sm)

print("\nComparison between BioBERT and en_ner_bc5cdr_md:")
print(comparison_biobert_bc5cdr)
