# coding:utf-8
def makekeywords(text):
    from janome.tokenizer import Tokenizer
    t = Tokenizer()
    tokens = t.tokenize(text)
    keywords = []
    for token in tokens:
        if token.part_of_speech.find("名詞") >= 0 and token.part_of_speech.find("数") == -1 and token.part_of_speech.find("非自立") == -1 and token.part_of_speech.find("接尾") == -1:
            keywords.append(token.surface)
    return keywords
