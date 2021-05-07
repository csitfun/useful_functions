import os
with open("./pubmed_version1.json") as f:
    lines = f.readlines()
    for i in range(0, len(lines), 100000):
        with open(os.path.join("./split/", f"pubmed_version1_{i}.json"), "w") as f1:
            start = i
            end = i + 100000
            f1.writelines(lines[start: end])
