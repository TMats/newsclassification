# coding:utf-8
def classifier():
    import math
    import makekeywords
    import random
    from collections import defaultdict
    from janome.tokenizer import Tokenizer
    import mysql.connector
    import config

    CATEGORY = ("social", "science", "politics", "economics", "international", "sports", "culture")
    cat_num = {}    # カテゴリの記事数
    cat_word_num = {}    # カテゴリ内単語数
    words = set()   # 訓練データで出現した単語を記録
    traindata_num = 0   # 訓練データの数

    # 初期化
    for cat in CATEGORY:
        cat_num[cat] = 0    # 各カテゴリの記事数を0に初期化
        cat_word_num[cat] = defaultdict(int)     # 各カテゴリでの単語出現数を0に初期化

    # 学習器
    traindata_ratio = 0.8    # 訓練データの割合

    def train(train_cat, train_text):
        nonlocal traindata_num
        traindata_num += 1  # 訓練データの数を更新
        cat_num[train_cat] += 1     # カテゴリの記事数を更新
        train_keywords = makekeywords.makekeywords(train_text)   # 訓練データの記事の単語を抽出
        for word in train_keywords:
            words.add(word)     # wordsリストに単語wordを追加(既に存在していたら追加されない)
            cat_word_num[train_cat][word] += 1     # カテゴリで単語が出てきた回数を更新

    # テスト
    def classify(test_text):
        test_keywords = makekeywords.makekeywords(test_text)   # テストデータの記事の単語を抽出
        cat_prob = {}   # カテゴリに属する確率(以降対数をとって計算するため確率の値ではない)
        for cat in CATEGORY:
            cat_prob[cat] = calc_prob(cat, test_keywords)
        return sorted(cat_prob.items(), key=lambda x: x[1], reverse=True)[0][0]

    # 各カテゴリに属する確率を計算(MAP推定を用いた多項モデル)
    def calc_prob(cat, test_keywords):
        prob = math.log(1.0*(cat_num[cat]+1)/(traindata_num+len(CATEGORY)))
        for word in test_keywords:
            prob += math.log(1.0*(cat_word_num[cat][word]+1)/(sum(cat_word_num[cat].values())+len(words)))
        return prob

    # mysql
    con = mysql.connector.connect(
        host=config.host,
        db=config.db,
        user=config.user,
        passwd=config.passwd,
        buffered=True)
    cur = con.cursor()

    # randomカラムを追加して乱数を格納
    cur.execute("""DESCRIBE news random""")
    record = cur.fetchone()
    # もしrandomカラムが存在してなければカラムを追加
    if record == None:
        cur.execute("""ALTER TABLE news ADD random float""")

    cur.execute("""SELECT id FROM news""")
    record = cur.fetchone()
    while record != None:
        sqlid = record[0]
        cur2 = con.cursor()
        cur2.execute("""UPDATE news SET random = %s WHERE id = %s""", (random.random(), sqlid))
        cur2.close()
        record = cur.fetchone()

    # train
    cur.execute("""SELECT category, content FROM news WHERE random < %s""", (traindata_ratio,))
    record = cur.fetchone()
    while record != None:
        train(record[0], record[1])
        record = cur.fetchone()
    print("Finished training")

    # test
    cur.execute("""SELECT category, content FROM news WHERE random >= %s""", (traindata_ratio,))
    record = cur.fetchone()
    test_num = 0
    correct_num = 0
    while record != None:
        classify_result = classify(record[1])
        test_num += 1
        if classify_result == record[0]:
            correct_num += 1
        else:
            print("Correct: "+record[0]+"  Error: "+classify_result+"\n"+str(makekeywords.makekeywords(record[1])))
        record = cur.fetchone()
    print("Training data: "+str(traindata_num))
    print("Test data: "+str(test_num))
    print("Correct Classification Percentage: "+str(1.0*correct_num/test_num*100))

    cur.execute("""ALTER TABLE news DROP COLUMN random""")
    cur.close()
    con.close()
