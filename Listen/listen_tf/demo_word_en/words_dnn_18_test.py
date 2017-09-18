# -*- coding: utf-8 -*-

#!/usr/bin/env python
#!/usr/bin/env PYTHONIOENCODING="utf-8" python
import tflearn
import pyaudio
import speech_data
import numpy as np
import os
from collections import Counter
import librosa
import tensorflow as tf
from joblib import Parallel, delayed
from numpy import array

# Simple spoken digit recognition demo, with 98% accuracy in under a minute

# Training Step: 544  | total loss: 0.15866
# | Adam | epoch: 034 | loss: 0.15866 - acc: 0.9818 -- iter: 0000/1000
# 训练样本路径
# wav_path = 'E:\\Dev\\dataSet\\words\\wav\\train'
wav_path = 'E:\\Dev\\dataSet\\words\\wav\\train'
# label_file = 'E:\Dev\dataSet\SpeechRecognition\Chinese\doc\\trans\\train.word.txt'

def get_wav_files(wav_path = wav_path):
    wav_files = []
    for (dirpath, dirnames, filenames) in os.walk(wav_path):
        for filename in filenames:
            if filename.endswith(".wav") or filename.endswith(".WAV"):
                # print([dirpath, filename]) 打印出形如:['E:\\Dev\\dataSet\\google_test\\wav\\train\\one', 'fd395b74_nohash_2.wav']
                filename_path = os.sep.join([dirpath, filename])
                # print(filename_path)  example: E:\Dev\dataSet\google_test\wav\train\no\f8ad3941_nohash_0.wav
                # if os.stat(filename_path).st_size < 240000:     # st_size以字节为单位，240000字节(b)=234.375千字节(kb)
                #     continue                                    # 这里逻辑为忽略太小的音频文件
                wav_files.append(filename_path)

    return wav_files

wav_files = get_wav_files()

def get_wav_label(wav_files = wav_files):
    # labels_dict = {}
    # with open(label_file, "r", encoding='utf-8') as f:
    #     for label in f:
    #         label = label.strip("\n")
    #         label_id, label_text = label.split(' ', 1)
    #         labels_dict[label_id] = label_text

    labels = []
    new_wav_files = []
    for wav_file in wav_files:
        # print(wav_file) # E:\Dev\dataSet\words\wav\train\one\ffd2ba2f_nohash_0.wav
        label = str(wav_file).split("\\")[-2]
        # wav_id = os.path.basename(wav_file).split(".")[0]  # 返回路径后面的文件名，str类型，再用split()处理获取没后缀类型的文件名
        # print(wav_id)
        # if wav_id in labels_dict:
        labels.append(label)
        new_wav_files.append(wav_file)
    return new_wav_files, labels

def get_wav_length(wav):
    #待修改
    import numpy as np
    import librosa

    print(wav)

    wav, sr = librosa.load(wav)   # wav为audio time series，sr为sampling rate of y
    mfcc = np.transpose(librosa.feature.mfcc(wav, sr), [1, 0])
    return len(mfcc)

def load_wav_feature_mfcc(wav_files):
    wav, sr = librosa.load(wav_files)
    mfcc = np.transpose(np.expand_dims(librosa.feature.mfcc(wav, sr), axis=0), [0, 2, 1])
    res = mfcc.tolist()
    return res

pointer = 0
def get_next_batches(batch_size, wav_max_len):
    global pointer
    batches_wavs = []
    batches_labels = []
    # for i in range(batch_size):
    #     wav, sr = librosa.load(wav_files[pointer])  # pointer = 0 从wav_files[0]开始遍历
    #     mfcc = np.transpose(librosa.feature.mfcc(wav, sr), [1,0])
    #     batches_wavs.append(mfcc.tolist())
    #     batches_labels.append(labels_vector[pointer])  # pointer = 0 labels_vector[0]开始遍历
    #     pointer += 1
    for i in range(batch_size):
        # res = speech_data.load_wav_file(wav_files[pointer])  # load_wav_file 返回值为len()值8192的一个列表
        wav, sr = librosa.load(wav_files[pointer])  # pointer = 0 从wav_files[0]开始遍历
        mfcc = np.transpose(librosa.feature.mfcc(wav, sr), [1,0])
        batches_wavs.append(mfcc.tolist())
        # print(len(mfcc.tolist()))  # 44
        # exit()
        # res_list = []
        # for i in range(len(res)):
        #     res_list.append(res[i])
        pointer += 1
    # print(len(wav_files))
    # exit()
    # 取零补齐
    # label append 0 , 0 对应的字符
    # mfcc 默认的计算长度为 20(n_mfcc of mfcc) 作为channel length
    for mfcc in batches_wavs:
        while len(mfcc) < wav_max_len:
            mfcc.append([0]*20)
    for label in batches_labels:
        while len(label) < label_max_len:
            label.append(0)
    # return batches_wavs,batches_labels
    # print(batches_wavs)
    # print(len(batches_wavs[0]))
    # exit()
    return batches_wavs
# softmax 结果概率模型转化为对应单词
def res_to_text(result):   # 2.0 版本 修改了模型输出的概率分布和单词序号对应不上的问题
    mid = result[0].tolist()
    # print(len(mid)) # 18
    print(mid)
    # exit()
    max_probility_index = mid.index(max(mid)) # 返回最大概率的索引
    for key in word_num_map:
        if word_num_map[key] == max_probility_index :
            max_probility = key
            break
    # key_list = word_num_map.keys()
    # print(max_probility_index)
    # res = list(key_list)
    # max_probility = res[max_probility_index]
    # print(res)
    # print(max_probility)
    # exit()
    # max_probility = word_num_map.get(max_probility_index)
    return max_probility

batch = speech_data.wave_batch_generator(10000,target=speech_data.Target.digits)
# X,Y = get_wav_files()
wav_files, labels = get_wav_label()
batch_size = len(wav_files)

all_words = []
for label in labels:
    # 字符分解
    all_words.append(label)
# print(all_words) 这里all_words列表里有重复
counter = Counter(all_words)  # 利用Counter类去重
count_pairs = sorted(counter.items(), key=lambda x: -x[1])

words, _ = zip(*count_pairs)
# print(words)
words_size = len(words)
print(u"词汇表大小：", words_size)

word_num_map = dict(zip(words, range(len(words))))
print(word_num_map)     #  {'one': 3, 'eight': 10, 'left': 9, 'dog': 12, 'bird': 16, 'four': 1, 'down': 6, 'house': 11, 'on': 4, 'nine': 5, 'off': 7, 'happy': 14, 'bed': 17, 'marvin': 13, 'no': 0, 'five': 8, 'go': 2, 'cat': 15}

# 当字符不在已经收集的words中时，赋予其应当的num，这是一个动态的结果
to_num = lambda word: word_num_map.get(word, len(words))   # 返回指定单词对应的索引（1个数字），to_num是个匿名函数
# word = 'dog'
# a = word_num_map.get(word, len(words))
# print(words)
# print(len(words))
# print(a)

# 将单个file的标签映射为num 返回对应list,最终all file组成嵌套list
labels_vector = [list(map(to_num, label)) for label in labels]
label_list = []
# print(labels)
for label in labels:
    label_every = [0]
    label_every = label_every*18    #  有几个分类这里写几
    mid = word_num_map.get(label, len(words))
    label_every[mid] = 1
    # print(label)
    # print(label_every)
    # exit()
    label_list.append(label_every)

# print(label)
# print(labels_vector)
# print(label_list)
# exit()
label_max_len = np.max([len(label) for label in labels_vector])
print(u"最长句子的字数:" + str(label_max_len))

# 下面仅仅计算了语音特征相应的最长的长度。
# 如果仅仅是计算长度是否需要施加变换后计算长度？
parallel_read = False
if parallel_read:
    wav_max_len = np.max(Parallel(n_jobs=7)(delayed(get_wav_length)(wav) for wav in wav_files))
else:
    wav_max_len = 44
print("最长的语音", wav_max_len)


# n_batch = len(wav_files) // batch_size
n_batch = 200

# X = get_next_batches(batch_size,wav_max_len)
# Y = label_list

number_classes = 18 # simple words


# Classification
tflearn.init_graph(num_cores=8, gpu_memory_fraction=0.7)
net = tflearn.input_data(shape=[None, 44, 20])
net = tflearn.fully_connected(net, 64)
net = tflearn.dropout(net, 0.8)
net = tflearn.fully_connected(net, number_classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=0.0001, loss='categorical_crossentropy')

model = tflearn.DNN(net, tensorboard_verbose=3, tensorboard_dir='logs')
# model.fit(X, Y, n_epoch=10, show_metric=True, snapshot_step=100)
# Overfitting okay for now
model.load('Models/word_dnn_18.tflearn')

demo_file = "E:\\Dev\\dataSet\\words\\wav\\validation\\one\\00f0204f_nohash_0.wav"
demo = load_wav_feature_mfcc(demo_file)
result = model.predict(demo)

print("predicted digit for %s : result = %s "%(demo_file,res_to_text(result)))
print("predicted digit for %s : result = %s "%(demo_file,result))
