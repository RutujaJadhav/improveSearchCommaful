import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import wordnet
antonyms = []
"""Finding synonmyms"""
for syn in wordnet.synsets("increase"):
    for lm in syn.lemmas():
        if lm.antonyms():
            antonyms.append(lm.antonyms()[0].name()) #adding into antonyms
print(set(antonyms))

synonyms = []
for syn in wordnet.synsets("home"):
    for lm in syn.lemmas():
             synonyms.append(lm.name())#adding into synonyms
print (set(synonyms))

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
 


story_content_for_emb = []
st = ""
for s,c in list(story_content.items())[:100]:
    st = (c[0][1][0] + c[0][1][-1]).lower()
    #remove stopwords
    
    s_filtered = [w for w in st.strip().split() if not w in stop_words]
    story_content_for_emb.append(s_filtered)

from gensim.models import Word2Vec
# define training data
sentences = story_content_for_emb
# train model
model = Word2Vec(sentences, min_count=1)
# summarize the loaded model
#print(model)
# summarize vocabulary - all words in the corpus
words = list(model.wv.vocab)
print(len(words))
# access vector for one word
print(len(model['book']))
# save model
model.save('model.bin')
# load model
new_model = Word2Vec.load('model.bin')
#print(new_model)