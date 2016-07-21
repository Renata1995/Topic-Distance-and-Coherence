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


def te_preprocess(te, max_words):
    return "/pre_" + te + "_w" + str(max_words) + ".txt"

