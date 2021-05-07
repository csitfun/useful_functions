'''
AllenNLP
'''
from nltk.stem import PorterStemmer
import spacy
from tqdm import tqdm
import json

ps = PorterStemmer()
nlp = spacy.load("en_ner_bc5cdr_md")

def tag_pubmed_data(input_file_name, output_file_name):
    with open(input_file_name) as input_file, open(output_file_name, 'w') as output_file:
        pbar = tqdm(total=1000000)
        for line in tqdm(input_file):
            chemicals = set()
            diseases = set()
            datum = json.loads(line)
            text = "title: {} abstract: {}".format(datum['article_title'], datum['article_abstract'])
            # text = f"title:{datum['article_title']} abstract:{datum['article_abstract']}"
            doc = nlp(text)
            for sent in doc.sents:
                for ent in sent.ents:
                    if ent.label_ == "CHEMICAL":
                        chemicals.add(ent.text)
                    elif ent.label_ == "DISEASE":
                        diseases.add(ent.text)
            if len(chemicals) > 0 and len(diseases) > 0:
                datum["chemicals"] = list(chemicals)
                datum["diseases"] = list(diseases)
                output_file.write(json.dumps(datum) + "\n")
                pbar.update(1)
            else:
                continue
        pbar.close()

if __name__ == "__main__":
    input_file_name = "/Users/scott/Downloads/pubmed_version1.json"
    output_file_name = "/Users/scott/Downloads/tagged_pubmed.json"
    tag_pubmed_data(input_file_name, output_file_name)
