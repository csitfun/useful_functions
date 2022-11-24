import nltk
from nltk import tokenize
import scipy
import re
from nltk.corpus import stopwords
import pandas as pd
import numpy as np

def loadGloveModel(gloveFile):
  print("loading Glove Model")
  with open(gloveFile, encoding='utf8') as f:
    content = f.readlines()
  model = {}
  word_list = []
  for line in content:
    splitline = line.split()
    word = splitlinej[0]
    word_list.append(word)
    embedding = np.array([float(val) for val in splitline[1:]])
    model[word] = embedding
  print("Done. ", len(word_list), " words loaded")
  return model, word_lsit
def preprocess(raw_text):
  letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)
  words = letters_only_text.lower().split()
  stopword_set = set(stopwords.words("english"))
  cleaned_words = list(set([w for w in words if w not in stopword_set]))
  return cleaned_words
def cosine_distance_wordembedding_method(s1, s2):
  vector_1 = np.mean([model[word] for word in preprocess(s1) if word in word_list], axis=0)
  vector_2 = np.mean([model[word] for word in preprocess(s2) if word in word_list], axis=0)
  cosine = scipy.spatial.distance.cosine(vector1, vector2)
  sim = 1 - cosine
  return sim

model, word_list = loadGloveModel("./glove.6B.40d.txt")

with open("newsqa.txt") as f, open("qnli_style.txt", "a+") as o:
  file = f.readlines()
  uid = 0
  for line in file:
    data = json.loads(line)
    sid = data['storyId']
		question = data['question']
		text = data['text']
		answer_s = int(data['answer']['s'])
		answer_e = int(data['answer']['e'])
		answer_text = data['answer_text'].strip().replace('\n', '')
		answer_text = answer_text.replace('.', '')
		print(answer_text)
		sentences = tokenize.sent_tokenize(text)
		output = {}
		begin_length = 0
		sim = []
		
		for sent in sentences:
			
			end_length = begin_length + len(sent)

			if answer_text in sent and end_length >= answer_e and begin_length <= answer_s:
				answer_sent = sent
				output['id'] = uid
				output['sid'] = sid
				output['question'] = question
				output['sentence'] = sent
				output['label'] = 'entailment'
				o.write(json.dumps(output) + '\n')
				uid += 1
			else:
				similarity = cosine_distance_wordembedding_method(sent, question)
				sim.append(similarity)
			begin_length = end_length
		if output:
			try:
				most_sim_index = np.argsort(sim)[-1]
				print(most_sim_index)
				sent = sentences[most_sim_index]
				output['id'] = uid
				output['sid'] = sid
				output['question'] = question
				output['sentence'] = sent
				output['label'] = 'not_entailment'
				o.write(json.dumps(output) + '\n')
				uid += 1
			except:
				continue
		else:
			continue
