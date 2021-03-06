# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import os
import random
import glob
import platform
from gomoku.data.index_processor import Index
from six.moves import range

def get_filename(path, data):
    if self.platform == 'Windows':
        return path.replace(data + '\\', '')
    else:
        return path.replace(data + '/', '')

class Sampler:
    def __init__(self, data_dir='data', num_test_games=100, seed=1101):
        self.data_dir = data_dir
        self.num_test_games = num_test_games
        self.test_games = []
        self.train_games = []
        self.test_file = 'sample'
        self.platform = platform.platform().split('-')[0]

        random.seed(seed)
        self.compute_test_samples()

    def draw_data(self, data_type, num_samples):
        if data_type == 'test':
            return self.test_games
        elif data_type == 'train' and num_samples is not None:
            return self.draw_training_samples(num_samples)
        elif data_type == 'train' and num_samples is None:
            return self.draw_all_training()
        else:
            raise ValueError(data_type + " is not a valid data type, choose from 'train' or 'test'")

    # 테스트 샘플 확인
    def draw_samples(self, num_sample_games):
        available_games = []
        base = self.data_dir + '/' + '*.xml'
        for filepath in glob.glob(base):
            filename = get_filename(filepath, self.data_dir)
            available_games.append(filename)
        print('>>> Total number of games used: ' + str(len(available_games)))

        sample_set = set()
        while len(sample_set) < num_sample_games:
            sample = random.choice(available_games)
            if sample not in sample_set:
                sample_set.add(sample)
        print('Drawn ' + str(num_sample_games) + ' samples.')
        return list(sample_set)

    # 테스트 샘플 목록에 없는 데이터 추가
    def draw_training_games(self):
        index = Index(data_directory=self.data_dir)
        for file_info in index.file_info:
            filename = file_info['filename']
            num_games = file_info['num_games']
            for i in range(num_games):
                sample = (filename, i)
                if sample not in self.test_games:
                    self.train_games.append(sample)
        print('total num training games: ' + str(len(self.train_games)))

    # 테스트 샘플이 없을 경우 새로 생성
    def compute_test_samples(self):
        if not os.path.isfile(self.test_file):
            test_games = self.draw_samples(self.num_test_games)
            test_sample_file = open(self.test_file, 'w')
            for sample in test_games:
                if self.platform == 'Windows':
                    test_sample_file.write(str(sample).replace('\\', '/') + '\n')
                else:
                    test_sample_file.write(str(sample) + '\n')
            test_sample_file.close()

        test_sample_file = open(self.test_file, 'r')
        sample_contents = test_sample_file.read()
        test_sample_file.close()
        for line in sample_contents.split('\n'):
            if line != '':
                self.test_games.append(line)

    # 테스트 데이터와 중복되지 않는 샘플 생성
    def draw_training_samples(self, num_sample_games):
        available_games = []
        base = self.data_dir + '/' + '*.xml'
        for filepath in glob.glob(base):
            filename = get_filename(filepath, self.data_dir)
            available_games.append(filename)
        print('total num training games: ' + str(len(available_games)))

        sample_set = set()
        while len(sample_set) < num_sample_games:
            sample = random.choice(available_games)
            if sample not in self.test_games:
                sample_set.add(sample)
        print('Drawn ' + str(num_sample_games) + ' samples.')
        return list(sample_set)

    # 가능한 모든 훈련 데이터 생성
    def draw_all_training(self):
        available_games = []
        base = self.data_dir + '/' + '*.xml'
        for filepath in glob.glob(base):
            filename = get_filename(filepath, self.data_dir)
            available_games.append(filename)
        print('total num training games: ' + str(len(available_games)))

        sample_set = set()
        for sample in available_games:
            if sample not in self.test_games:
                sample_set.add(sample)
        print('Drawn all samples, ie ' + str(len(sample_set)) + ' samples.')
        return list(sample_set)