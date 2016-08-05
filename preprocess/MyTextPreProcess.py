import MySentenceStemmer
from nltk.corpus import stopwords
import MyConvertUnicode
import re

#
#  Remove stop words
#  Stem using (MySentenceStemmer)
#  Convert unicode
#  convert all words into lower case
#  do not take words mix with symbols etc.

class MyTextPreProcess:
	def __init__(self):
		self.convert = MyConvertUnicode.MyConvertUnicode()
		self.st = {};
		self.stfile = open("preprocess/stopwords_mysql.txt", "r")
		for line in self.stfile:
		   l0 = line.rstrip()
		   self.st[l0] = 1
		self.mstem = MySentenceStemmer.MySentenceStemmer(self.st)

	def PreProcess(self, sentence):
		sentence = sentence.lower()
		# line0 = self.convert.convert(sentence)
   		l1 = self.mstem.stem(sentence)

		pattern = r"(^[a-z]+(-?[a-z0-9]+)*$)|(^([a-z]\.)+$)"

		l2 = []
		for w in l1:
			if len(w) <30 and w not in self.st and re.search(pattern, w):
				l2.append(w.lower())

		#l2 = [w.lower() for w in l1 if (w.isalpha() and (w.lower() not in self.st))]
		return l2


