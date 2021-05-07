diaimport stanza
# from common.stanza_download import download

stanza.download('en')       # zh This downloads the English models for the neural pipeline
# nlp = stanza.Pipeline('en', dir='/home/zjc/stanza_resources') # This sets up a default neural pipeline in English

class StanzaUtil:
    nlp = None
    '''
    用于英文
    '''

    def __init__(self):
        if StanzaUtil.nlp is None:
            StanzaUtil.nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma, depparse', tokenize_pretokenized=True)


    def nlp_results(self, multi_words):
        doc = StanzaUtil.nlp(multi_words)
        multi_results = []
        for i, sent in enumerate(doc.sentences):
            toks, pos, dep_heads, dep_types = [], [], [], []
            for token in sent.words:
                toks.append(token.text)
                pos.append(token.xpos)
                dep_heads.append(token.head - 1)
                dep_types.append(token.deprel)
            multi_results.append((toks, pos, dep_heads, dep_types))

        return multi_results



class StanzaZHUtil:
    nlp = None
    '''
        用于中文
     '''

    def __init__(self):
        if StanzaUtil.nlp is None:
            StanzaUtil.nlp = stanza.Pipeline(lang='zh', processors='tokenize,pos,lemma, depparse', tokenize_pretokenized=True)


    def nlp_results(self, multi_words):
        doc = StanzaUtil.nlp(multi_words)
        multi_results = []
        for i, sent in enumerate(doc.sentences):
            toks, pos, dep_heads, dep_types = [], [], [], []
            for token in sent.words:
                toks.append(token.text)
                pos.append(token.xpos)
                dep_heads.append(token.head - 1)
                dep_types.append(token.deprel)
            multi_results.append((toks, pos, dep_heads, dep_types))

        return multi_results

    def nlp_first_result(self, words):

        return self.nlp_results([words])[0]

if __name__ == '__main__':
    words = ['It`s','a','nice','day']
    print(StanzaUtil().nlp_results(words))