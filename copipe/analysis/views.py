# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http.response import JsonResponse
from analysis.yamaki import Yamaki

def index(request):
    return render(request, 'analysis/index.html', {})

def analyze(request):
    # 不正なアクセス
    if not request.POST['v1'] or not request.POST['search_word']:
        return JsonResponse({"error":True, 'message': u'不正なアクセスです'})
    
    v1 = request.POST['v1']
    search_word = request.POST['search_word']

    yamaki = Yamaki(v1)
    #文章の類似度を計算
    try:
        result = yamaki.copy_check(search_word)
    except Exception as e:
        print e.message

    return JsonResponse({"error":False, 'message': result})
