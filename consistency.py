import json
import random
import time
import openai
import sklearn
import nltk
from nltk import tokenizer
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
openai.api_key = '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' # xiaodi

incontext = ""
def gpt3_api(prompt):
   response = openai.Completion.create(
      model="gpt-3.5-turbo",
      messages = prompt
   )
   return response

# with open('input.json') as f:
#    c = 0
#    lines = f.readlines()

#    line_dict = json.loads(lines[0])
#    prompt_input = line_dict['input']
#    label = line_dict['target']
#    prompt = '\n' + prompt_input
#    output = gpt3_api(prompt)
#    pred = output["choices"]['text'].lower()
#    if label == pred:
#       c += 1

#    print(c)

with open('logiqa.jsonl') as f:
   c = 0
   y_true = []
   y_pred = []
   lines = f.readlines()
   for i, line in enumerate(lines):
      line_dict = json.loads(line)
      prompt_input = line_dict['input']
      context = prompt_input[-1]['content']
      need_shuffle = context.split('\n')[:-1]
      text = need_shuffle[0]
      question = need_shuffle[1]
      options = need_shuffle[-4:]
      for i in range(10):
         new_list = random.shuffle(text, question, random.shuffle(option))
         context = "\n".join(new_list)

      label = line_dict['ideal']
      y_true.append(label)
      prompt = prompt_input
      output = gpt3_api(prompt)
      pred = output.choices[0].text
      y_pred.append(pred)
      print(pred)
      if label == pred:
         c += 1
      print(i, " ", c)
      time.sleep(1)
   print(y_true, y_pred)
   f_score = f1_score(y_true, y_pred, average='binary')
   p_score = precision_score(y_true, y_pred, average='binary')
   r_score = recall_score(y_true, y_pred, average='binary')
   acc = accuracy_score(y_true, y_pred)
   print(f_score)
   print(p_score)
   print(r_score)
   print(acc)
