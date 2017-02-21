# Topic-Distance-and-Coherence

## Table of Contents
 * Introduction
 * Requirements
 * Usage

## Introduction

## Requirements
* [Gensim: A Python library for topic Modeling](https://radimrehurek.com/gensim/)
* [NLTK: Natural Language Toolkit](http://www.nltk.org/)
* [NumPy: A Python package for scientific computing](http://www.numpy.org/)
* [Matplotlib: A Python 2D plotting library](http://matplotlib.org/)

## Usage
#### Run LDA
Prepare for dictionary and corpus files
```
$python lda_process.py lda_dir(default src_LDA) corpus_type num_of_topics alpha eta
```
Run LDA
```
$python lda_process.py lda_dir(default src_LDA) corpus_type num_of_topics alpha eta
```
Analyze data
```
$python lda_analyze.py lda_dir(default src_LDA) corpus_type num_of_topics src alpha eta
```