from dataset import load_dataset, load_from_disk
data = load_dataset("json", data_files = "./qnli_data/qnli_ood.json")
data.save_to_disk("./qnli_data/qnli_ood")
data = load_from_disk("./qnli_data/qnli_ood")
print(data.head())
data = data.rename_column("question", "sentence1")
data = data.rename_column("sentence", "sentence2")

def convert(example):
  if example['label'] == "entailment":
    return 1
  elif example['label'] == "not_entailment":
    return 0
  else:
    raise ValueError("label not legal")
data = data.map(lambda examples:{"label": convert(examples)})
  
# data = load_dataset("./datasets/glue", "qnli", cache_dir="./huggingface/datasets")
