# coding=utf-8

import MySQLdb
import numpy as np
import random
import math
import json
from collections import defaultdict

class Score():

    cast_count_max = 5
    recommend_score_min = 40
    feature_item_number = 8 # 好みの項目数
    feature_evaluation = 5  # 好みの評価段階 5段階

    def __init__(self, customer_id):
        self.customer_id = customer_id

        cnn = MySQLdb.connect(
            host='ccs-dev.cluster-cnkz9ysbhg4k.ap-northeast-1.rds.amazonaws.com',
            db='dev_ccs',
            user='ccs_dev_db',
            passwd='ccs_dev_db_pass',
        )
        self.cur = cnn.cursor(MySQLdb.cursors.DictCursor)


    def _get_customer(self):
        customer = {}
        customer['face'] = random.randint(1, 5)
        customer['style'] = random.randint(1, 5)
        customer['character'] = random.randint(1, 5)
        customer['play'] = random.randint(1, 5)
        customer['feature1'] = random.randint(1, 5)
        customer['feature2'] = random.randint(1, 5)
        customer['feature3'] = random.randint(1, 5)
        customer['feature4'] = random.randint(1, 5)
        customer['feature5'] = random.randint(1, 5)
        customer['feature6'] = random.randint(1, 5)
        customer['feature7'] = random.randint(1, 5)
        customer['feature8'] = random.randint(1, 5)

        return customer


    def _get_casts(self):

        self.cur.execute('select id from casts limit {}'.format(self.cast_count_max))
        cast_data = self.cur.fetchall()

        nested_dict = lambda: defaultdict(nested_dict)
        casts = nested_dict()
        for cast in cast_data:
            casts[cast['id']]['face'] = random.randint(1, 5)
            casts[cast['id']]['style'] = random.randint(1, 5)
            casts[cast['id']]['character'] = random.randint(1, 5)
            casts[cast['id']]['play'] = random.randint(1, 5)
            casts[cast['id']]['feature1'] = random.randint(1, 5)
            casts[cast['id']]['feature2'] = random.randint(1, 5)
            casts[cast['id']]['feature3'] = random.randint(1, 5)
            casts[cast['id']]['feature4'] = random.randint(1, 5)
            casts[cast['id']]['feature5'] = random.randint(1, 5)
            casts[cast['id']]['feature6'] = random.randint(1, 5)
            casts[cast['id']]['feature7'] = random.randint(1, 5)
            casts[cast['id']]['feature8'] = random.randint(1, 5)

        return casts


    """
    ユークリッド距離の最大値を求める
    """
    def _get_euclid_max(self, feature_item_number, feature_evaluation):
        a = 0
        for i in range(feature_item_number):
            a += (feature_evaluation - 1) ** 2
        # get_scoreの計算で0除算しないように小数点を切り上げる
        max = math.ceil(a**0.5)
        return max


    def _get_score(self, customer, cast):

        # 顧客の強みとキャストの売りの計算
        weight_score = (
            customer['face'] * cast['face'] +
            customer['style'] * cast['style'] +
            customer['character'] * cast['character'] +
            customer['play'] * cast['play']
        )

        # 顧客の好みとキャストの特性の計算
        # 顧客の好みを求める
        customer_feature_score = np.array([
            customer['feature1'], customer['feature2'], customer['feature3'], customer['feature4'],
            customer['feature5'], customer['feature6'], customer['feature7'], customer['feature8']
        ])
        # キャストの特徴を求める
        cast_feature_score = np.array([
            cast['feature1'], cast['feature2'], cast['feature3'], cast['feature4'],
            cast['feature5'], cast['feature6'], cast['feature7'], cast['feature8']
        ])
        feature_score = np.linalg.norm(customer_feature_score - cast_feature_score)
        max = self._get_euclid_max(self.feature_item_number, self.feature_evaluation)
        score = math.ceil(weight_score + ((max - feature_score) / max * weight_score / 2)) # 見やすくするため切り上げ

        return score


    def get_scores(self):

        customer = self._get_customer()
        casts = self._get_casts()

        # 計算
        nested_dict = lambda: defaultdict(nested_dict)
        score_dict = nested_dict()
        for id, cast in casts.items():
            score_dict[str(id)] = self._get_score(customer, cast)

        return score_dict
