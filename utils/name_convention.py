def get_output_dir(corpus_type, topics_count, src, model="LDA"):
    """
    Return the default output directory name
    :param corpus_type: values "tfidf", "bow", or "binary"
    :param topics_count: number of topics
    :param src: input directory that contains files of tokens
    :param model: model used to generate topics
    :return:
    """
    return model+"_"+src+"_"+corpus_type+"_t"+str(topics_count)


def get_model_dir(src, model="LDA"):
    return src+model


def topics_dir():
    return "/topics"


def te_preprocess(te, max_words, startw=0):
    if startw <= 0:
        fname = "/pre_" + te + "_w" + str(max_words) + ".txt"
    else:
        fname = "/pre_" + te + "_w" + str(max_words) + "_start" + str(startw) + ".txt"
    return fname


def tc_tf_file(dname, corpus_type, topics_count, startw=0, tfidf=False):
    if tfidf:
        return dname + "/wdoc_freq_tfidf_" + corpus_type + "_t" + str(topics_count) + "_start" + str(startw) + ".txt"
    else:
        return dname + "/wdoc_freq_" + corpus_type + "_t" + str(topics_count) + "_start" + str(startw) + ".txt"


def tc_co_occur_file(dname, corpus_type, topics_count, startw=0, tfidf=False):
    if tfidf:
        return dname + "/cofreq_tfidf_" + corpus_type + "_t" + str(topics_count) + "_start" + str(startw) + ".txt"
    else:
        return dname + "/cofreq_" + corpus_type + "_t" + str(topics_count) + "_start" + str(startw) + ".txt"


def tc_contribution(dname, words_count, startw=0, tfidf=False):
    if tfidf:
        if startw == 0:
            return dname + "/tc_tfidf_freq_" + str(words_count) + ".txt"
        else:
            return dname + "/tc_tfidf_freq_" + str(words_count) + "_start" + str(startw) + ".txt"
    else:
        if startw == 0:
            return dname + "/tc_freq_" + str(words_count) + ".txt"
        else:
            return dname + "/tc_freq_" + str(words_count) + "_start" + str(startw) + ".txt"


def tc_output_file(dname, words_count, startw=0, tfidf=False):
    if tfidf:
        if startw == 0:
            return dname + "/top_topics_tfidf_" + str(words_count) + ".txt"
        else:
            return dname + "/top_topics_tfidf_" + str(words_count) + "_start" + str(startw) + ".txt"
    else:
        if startw == 0:
            return dname + "/top_topics_" + str(words_count) + ".txt"
        else:
            return dname + "top_topics_" + str(words_count) + "_start" + str(startw) + ".txt"
