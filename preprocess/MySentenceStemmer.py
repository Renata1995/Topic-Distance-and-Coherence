import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

#
# Stemming
#
# Use tagger to tag part of speech
# If word is in stop word list than keep it as it is
# else if word is nonun/verb/adjactive/adverb then use WordNet Lemmatizer to get the sem
# else use the SnowBall Stemmer to stem 

class MySentenceStemmer:
	def __init__(self, st):
		self.sstem = SnowballStemmer("english")
		self.wstem = WordNetLemmatizer()
	 	self.st = st;

	def stem(self, sentence):
		#print sentence
		list1 = nltk.word_tokenize(sentence);
		taglist = nltk.pos_tag(list1);
		#print taglist
		self.res = [];
		for s in taglist:
			tag = s[1];
			pos0 = ' ';
			if (tag[0] == 'N'):
				pos0 = 'n'
			elif (tag[0] == 'V'):
				pos0 = 'v'
			elif (tag[0] == 'J'):
				pos0 = 'a'
			elif (tag[0] == 'R'):
				pos0 = 'r'

			if s[0] not in self.st:
				if (pos0.isalpha()):
					self.res.append(self.wstem.lemmatize(s[0], pos=pos0));
				else:
					self.res.append(self.sstem.stem(s[0]));
		return self.res


