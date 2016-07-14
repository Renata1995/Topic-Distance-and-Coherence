#import nltk
#from nltk.stem.snowball import SnowballStemmer
#from nltk.stem import WordNetLemmatizer
import string

class MyConvertUnicode:
	intab = "\x90\x80\xA4\x82\x97\xE1\xA0\x81\x9A\x84\x8A\xA1\x94\x87\xA7\xE8\xFC\xDF\xC7\xE7\x96\x97\xED\xF3\xF4\xF5"
	outtab = "ECneubauUaeioc.eusCc--iooo"
	ignore = "\xA8\xA6\xA7\xAB\x85\xBF\xBB"
	def __init__(self):
		self.trantab = string.maketrans(self.intab, self.outtab)
	def convert(self, sentence):
		#print sentence
		return sentence.translate(self.trantab, self.ignore);


