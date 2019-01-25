import jieba
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def segment(request):
    """
    分词
    method:post
    {
        text: not null 需要分词的句子或者段落
    }
    :param request:
    :return:
    """
    # 加载默认字典地址，如果字典不存在，就加载package中的
    if os.path.exists('./dict/dict.txt'):
        jieba.set_dictionary('./dict/dict.txt')

    data = dict()
    if request.method == 'POST':
        try:
            sentence = request.POST.get('text')
            response = list(jieba.cut(sentence))
            data['error_code'] = 0
            data['error_message'] = ''
            data['response'] = response
        except Exception as e:
            data['error_code'] = 1000
            data['error_message'] = e.args

    return JsonResponse(data)


def add_word(request):
    """
    新增词条
    method:get
    {
        word: not null 词条
        freq: null 频数
        tag: null 标签词性
    }
    :param request:
    :return:
    """
    if os.path.exists('./dict/dict.txt'):
        jieba.set_dictionary('./dict/dict.txt')

    data = dict()
    word = request.GET.get('word', None)
    freq = request.GET.get('freq', None)
    tag = request.GET.get('tag', None)
    if not word:
        data['error_code'] = 402
        data['error_message'] = 'word为NULL'
        return JsonResponse(data)
    jieba.add_word(word, freq, tag)
    data['error_code'] = 0
    data['error_message'] = ''
    return JsonResponse(data)


def del_word(request):
    """
    删除词条
    method：get
    {
        word: not null 词条
    }
    :param request:
    :return:
    """
    if os.path.exists('./dict/dict.txt'):
        jieba.set_dictionary('./dict/dict.txt')
    data = dict()
    word = request.GET.get('word', None)
    if not word:
        data['error_code'] = 402
        data['error_message'] = 'word为NULL'
        return JsonResponse(data)
    jieba.del_word(word)
    data['error_code'] = 0
    data['error_message'] = ''

    return JsonResponse(data)

