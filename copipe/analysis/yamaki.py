# -*- coding: utf-8 -*-
import math
import MeCab
import requests
import json

SEARCH_SECREAT_KEY = 'AIzaSyAxmZ8I_b6lEn2dql8ZKeLfFX_OWhk8ODQ'
SEARCH_ENGINE_ID = '015580778663029974765:ylq9z14qdhu'

class Yamaki(object):

    def __init__(self, base):
        self._base = base
        self._m = MeCab.Tagger('-Ochasen')
        self._base_node = self._m.parseToNode(self._base.encode('utf-8'))
        self._except_features = ["助詞", "助動詞", "記号"] #除外種類
        self._v1 = self._get_text_vec(self._base_node)
        self._google_search = GoogleSearch()

    def cos(self, v1, v2):
        print v1
        print v2
        numerator = sum([v1[c] * v2[c] for c in v1 if c in v2])
        square = lambda x: x * x
        denominator =  math.sqrt(sum(map(square, v1.values())) * sum(map(square, v2.values())))
        return float(numerator) / denominator if denominator != 0 else 0

    def jaccard(self, v1, v2):
        numerator = sum([c in v2 for c in v1])
        denominator = len(v1) + len(v2) - numerator
        return float(numerator) / denominator if denominator != 0 else 0

    def _get_text_vec(self, node):
        word_dic = {}
        if not node:
            return {}
        
        while node:
            type = node.feature.split(",")[0] #nodeのfeatureには「名詞,接尾,人名,*,*,*,さん,サン,サン」の形式で結果が入っているので","で分割する
            if not type in self._except_features and node.surface:
                if not word_dic.get(node.surface):
                    word_dic[node.surface] = 1
                else:
                    word_dic[node.surface] += 1
            node = node.next

        return word_dic
    
    def _get_similarity_text(self, similarity):
        if similarity >= 6.0 and similarity <= 1.0:
            return u'高'
        elif  similarity >= 3.0 and similarity <= 5.0:
            return u'中'
        else: 
            return u'低'

    def copy_check(self, text):
        jsons = self._google_search.custom_search(text) 
        results = []
        for item in jsons['items']:
            node = self._m.parseToNode(item['snippet'].encode('utf-8'))
            similarity = self.cos(self._v1, self._get_text_vec(node))

            tmp = {
                'title': item['title'],
                'link': item['link'],
                'snippet': item['snippet'],
                'similarity': similarity#self._get_similarity_text(similarity) 
            }

            results.append(tmp)

        return results

class GoogleSearch(object):
    """
    Google Custum Search APIを使用して検索を行なう
    """

    def __init__(self):
        self._search_url = 'https://www.googleapis.com/customsearch/v1?key=' + SEARCH_SECREAT_KEY + '&cx=' + SEARCH_ENGINE_ID + '&q=%s'

    def custom_search(self, search_word):
        url = self._search_url % search_word
        try:
            r = requests.get(url)
        except:
            return None
        else:
            status_code = r.status_code
            if status_code != 200:
                return None

            return json.loads(r.content)

if __name__ == '__main__':
    g = GoogleSearch()
    g.custom_search(u'Python')
