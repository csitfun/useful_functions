import stanza
from tqdm import tqdm
import json
import argparse

#stanza.download('en', package='craft', processors={'ner':'bc5cdr'})
#stanza.download('en', package='genia', processors={'ner':'bionlp13cg'})

def depparse_pubmed_data(input_file_name, output_file_name):
    with open(input_file_name) as input_file, open(output_file_name, 'w') as output_file:
        pbar = tqdm(total=1530000)
        for line in tqdm(input_file):
            datum = json.loads(line)
            if datum['article_abstract'] == "":
                continue
            else:
                nlp = stanza.Pipeline(lang='en', use_gpu=args.use_gpu, package='craft', processors={'ner': 'bc5cdr'})
                doc = datum['article_title'] + datum['article_abstract']
                parsing = nlp(doc)
                tokenize = " ".join(token.text for sent in parsing.sentences for token in sent.tokens)
                chemicals = []
                diseases = []

                for ent in parsing.entities:
                    if ent.type == "CHEMICAL":
                        chemical = {}
                        chemical['text'] = ent.text
                        chemical['start_char'] = ent.start_char
                        chemical['end_char'] = ent.end_char
                        chemicals.append(chemical)
                    elif ent.type == "DISEASE":
                        disease = {}
                        disease['text'] = ent.text
                        disease['start_char'] = ent.start_char
                        disease['end_char'] = ent.end_char
                        diseases.append(disease)
                    else:
                        continue
                if len(chemicals)>0 and len(diseases)>0:
                    datum['tokenize'] = tokenize
                    datum['chem_parsing'] = parsing.to_dict()

                    nlp_gene = stanza.Pipeline('en', use_gpu=args.use_gpu, package='genia', processors={'ner': 'bionlp13cg'})
                    gene_parsing = nlp_gene(tokenize)
                    genes = []
                    for ent in gene_parsing.entities:
                        if ent.type == "GENE_OR_GENE_PRODUCT":
                            gene = {}
                            gene['text'] = ent.text
                            gene['start_char'] = ent.start_char
                            gene['end_char'] = ent.end_char
                            genes.append(gene)
                        else:
                            continue
                    datum['gene_parsing'] = gene_parsing.to_dict()
                    datum['chemicals'] = chemicals
                    datum['diseases'] = diseases
                    datum['genes'] = genes
                    output_file.write(json.dumps(datum)+'\n')
                    pbar.update(1)
        pbar.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        default="./pubmed_version1_0.json",
        type=str,
        required=True,
        help="The input data dir. Should contain the .tsv files (or other data files) for the task.",
    )
    parser.add_argument(
        "--output_file",
        default='./tagged_pubmed_1.json',
        type=str,
        help="The input training file. If a data dir is specified, will look for the file there"
             +
             "If no data dir or train/predict files are specified, will run with tensorflow_datasets.",
    )
    parser.add_argument(
        "--use_gpu",
        action="store_false",
        default=True,
        help="use gpu",
    )
    file_path = "./data/split/"
    args = parser.parse_args()
    input_file_name = args.input_file
    output_file_name = args.output_file
    depparse_pubmed_data(input_file_name, output_file_name)
