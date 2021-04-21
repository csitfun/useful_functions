import xml.etree.ElementTree as ET
import json
import os


path = '/users/scott/Downloads/pubmed/'
save_dir = '/users/scott/Downloads/pubmed.json'

def get_text(element, path, default_val):
    val = str()
    for ele in element.findall(path):
        if ele is None:
            val = default_val
        else:
            val += str(ele.text) + " "
    return val

files = os.listdir(path)
with open(save_dir, "a") as output:
    for file in files:
        try:
            tree = ET.parse(path + "/" + file, parser=ET.XMLParser(encoding='utf-8'))
            root = tree.getroot()
            doc_total = len(root) - 3
            print("doc total : " + str(doc_total), file)

            for ele_article in root[3:]:
                title = get_text(ele_article, "MedlineCitation/Article/ArticleTitle", None)
                id = get_text(ele_article, "MedlineCitation/PMID", None)
                abstract = get_text(ele_article, "MedlineCitation/Article/Abstract/AbstractText", None)

                year = get_text(ele_article, "MedlineCitation/Article/Journal/JournalIssue/PubDate/Year", None)
                month = get_text(ele_article, "MedlineCitation/Article/Journal/JournalIssue/PubDate/Month", None)
                day = get_text(ele_article, "MedlineCitation/Article/Journal/JournalIssue/PubDate/Day", None)

                if abstract is not None and title is not None and id is not None:
                    result = {"pubmed_id": id,
                                   "article_title": title,
                                   "article_abstract": abstract,
                                   # "pub_date": {
                                   #     "year": year,
                                   #     "month": month,
                                   #     "day": day}
                                   }
                    output.write(json.dumps(result) + "\n")
                else:
                    continue
        except:
            continue
