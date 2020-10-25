import pandas as pd
from utils.tokenizer import segment
import os
import re
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


REMOVE_WORDS = ['|', '[', ']', '语音', '图片', ' ']


def read_stopwords(path):
    lines = set()
    with open(path, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            lines.add(line)
    return lines


def remove_words(words_list):
    words_list = [word for word in words_list if word not in REMOVE_WORDS]
    return words_list

# 去除标点符号
def remove_punc(seg_list):
    seg_list = [word for word in seg_list if re.search('\w+', word)]
    return seg_list

def parse_data(train_path, test_path):
    train_df = pd.read_csv(train_path, encoding='utf-8')
    train_df.dropna(subset=['Report'], how='any', inplace=True)
    train_df.fillna('', inplace=True)
    train_x = train_df.Question.str.cat(train_df.Dialogue)
    print('train_x is ', len(train_x))
    train_x = train_x.apply(preprocess_sentence)
    print('train_x is ', len(train_x))
    train_y = train_df.Report
    print('train_y is ', len(train_y))
    train_y = train_y.apply(preprocess_sentence)
    print('train_y is ', len(train_y))

    test_df = pd.read_csv(test_path, encoding='utf-8')
    test_df.fillna('', inplace=True)
    test_x = test_df.Question.str.cat(test_df.Dialogue)
    test_x = test_x.apply(preprocess_sentence)
    print('test_x is ', len(test_x))

    train_x.to_csv('{}/data/train_set.seg_x.txt'.format(BASE_DIR), index=None, header=False)
    train_y.to_csv('{}/data/train_set.seg_y.txt'.format(BASE_DIR), index=None, header=False)
    test_x.to_csv('{}/data/test_set.seg_x.txt'.format(BASE_DIR), index=None, header=False)


def preprocess_sentence(sentence):
    seg_list = segment(sentence.strip(), cut_type='word')
    seg_list = remove_words(seg_list)
    # seg_list = remove_punc(seg_list)
    seg_line = ' '.join(seg_list)
    return seg_line


if __name__ == '__main__':
    # 需要更换成自己数据的存储地址

    parse_data('{}/data/AutoMaster_TrainSet.csv'.format(BASE_DIR),
               '{}/data/AutoMaster_TestSet.csv'.format(BASE_DIR))


