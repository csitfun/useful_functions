import json
import time
from pyChatGPT import ChatGPT
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
    word = splitline[0]
    word_list.append(word)
    embedding = np.array([float(val) for val in splitline[1:]])
    model[word] = embedding
  print("Done. ", len(word_list), " words loaded")
  return model, word_list
def preprocess(raw_text):
  letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)
  words = letters_only_text.lower().split()
  stopword_set = set(stopwords.words("english"))
  cleaned_words = list(set([w for w in words if w not in stopword_set]))
  return cleaned_words
def cosine_distance_wordembedding_method(s1, s2):
  vector_1 = np.mean([model[word] for word in preprocess(s1) if word in word_list], axis=0)
  vector_2 = np.mean([model[word] for word in preprocess(s2) if word in word_list], axis=0)
  cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
  sim = 1 - cosine
  return sim

model, word_list = loadGloveModel("./glove.6B.50d.txt")

session_token = ""
incontext = "transforming a question and answer into a statement: \n question: Which one of the following, if true, most helps to resolve the apparent discrepancy in the information above? \n answer: Only very careful drivers use headlights when their use is not legally required. \n statement: The statement 'Only very careful drivers use headlights when their use is not legally required' most helps to resolve the apparent discrepancy in the information above. \n transforming a question and answer into a statement: \n question: Which one of the following can be properly inferred from the psychologist’s statements? \n answer: Some children who are taught by the whole-language method are not prevented from learning how sounds are represented by means of letters. \n statement:  Some children who are taught by the whole-language method are not prevented from learning how sounds are represented by means of letters can be properly inferred from the psychologist’s statements. \n transforming a question and answer into a statement: \n question: Which one of the following, if true, most seriously weakens the doctors' recommendation? \n answer: Enlargement of the gland, a common condition infrequently associated with cancer, results in high levels of the protein. \n statement: Enlargement of the gland, a common condition infrequently associated with cancer, results in high levels of the protein most seriously weakens the doctors' recommendation. \n transforming a question and answer into a statement: \n question: Which one of the following is an assumption required by the argument? \n answer: We cannot indefinitely replace exhausted nonrenewable resources with other nonrenewable resources. \n statement: We cannot indefinitely replace exhausted nonrenewable resources with other nonrenewable resources is an assumption required by the argument. \n transforming a question and answer into a statement: \n question: Who is from Shanghai and has a master's degree? \n answer: David. \n statement: David is from Shanghai and has a master's degree. \n transforming a question and answer into a statement: \n question: If U and Z are both on the field, for best performance, which of the following arrangement is appropriate? \n answer:  V is on the field and Y is not on the field. \n statement: If U and Z are both on the field, for best performance, V is on the field and Y is not on the field. \n transforming a question and answer into a statement: \n question: Which one of the followings is the topic of the above? \n answer: Reading habits \n statement: The topic of the above is Reading habits.\n"

#api = ChatGPT(email='754356305b@varnet.asia', password='namvx1031427')
api = ChatGPT(session_token)

with open('train.txt') as f, open('train_nli.txt', 'a+') as o:
	lines = f.readlines()
	output = {}
	for line in lines:
		line_dict = json.loads(line)
		uid = line_dict['id']
		utype = line_dict['type']
		article = line_dict['text']
		answer = line_dict['answer']
		question = line_dict['question']
		label = line_dict['answer']
		options = line_dict['options']
		sim_pre = 0
		option_sim = ""

		for i, option in enumerate(options):
			if label != i:
				try:
					sim = cosine_distance_wordembedding_method(options[label], option)
					if sim > sim_pre:
						sim_pre = sim
						option_sim = option
				except:
					option_sim = option

			
		qa1 = "transforming a question and answer into a statement: \n question: " + question + "\n answer: " + options[label] + "\n statement: "
		retries = 1
		success = False
		while not success:
			try:
				statement = api.send_message(incontext + qa1)
				statement = statement['message']
				print(statement)
				output['id'] = uid
				output['premise'] = article
				output['hypothesis'] = statement
				output['label'] = "entailment"
				output['type'] = utype
				o.write(json.dumps(output) + '\n')
				success = True
			except Exception as exception:
				time.sleep(5*retries)
				retries += 1
				api.refresh_cookies()
				api.refresh_auth()
				api.reset_conversation()
				continue


		qa2 = "transforming a question and answer into a statement: \n question: " + question + "\n answer: " + option_sim + "\n statement: "
		retries = 1
		success = False
		while not success:
			try:
				statement = api.send_message(incontext + qa2)
				statement = statement['message']
				print(statement)
				output['id'] = uid
				output['premise'] = article
				output['hypothesis'] = statement
				output['label'] = "not-entailment"
				output['type'] = utype
				o.write(json.dumps(output) + '\n')
				success = True
			except Exception as exception:
				time.sleep(5*retries)
				retries += 1
				api.refresh_cookies()
				api.refresh_auth()
				api.reset_conversation()
				continue
