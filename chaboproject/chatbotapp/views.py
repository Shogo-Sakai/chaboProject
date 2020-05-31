from django.shortcuts import render
from .components import forms
from . import talk
from django.template.context_processors import csrf
# from .tf20 import vgg16_imagenet as cl
# Create your views here.

# 応答用の辞書を組み立てて返す
def __makedic(k, txt):
  return {'k': k, 'txt': txt}

def talk_do(request):
  t = talk.Talk()
  if request.method == "POST":
    # テキストボックスに入力されたメッセージ
    q = request.POST['texttwo']
    # Talk-APIからの応答メッセージを取得
    a = t.get(q)
    # 描画用リストに最新のメッセージを格納する
    talktxts = []
    talktxts.append(__makedic('ai', a))
    talktxts.append(__makedic('b', q))
    # 過去の応答履歴をセッションから取り出してリストに追記する
    saveh = []
    if 'hist' in request.session:
      hists = request.session['hist']
      saveh = hists
      for h in reversed(hists):
        x = h.split(':')
        talktxts.append(__makedic(x[0], x[1]))
    # 最新のメッセージを履歴に加えてセッションに保存する
    saveh.append('b:' + q)
    saveh.append('ai:' + a)
    request.session['hist'] = saveh
    # 描画準備
    form = forms.UserForm(label_suffix=":")
    c = {
      'form': form,
      'texttwo': '',
      'talktxts': talktxts
    }
  else:
    # 初期表示のときにセッションもクリアする
    request.session.clear()
    # フォームの初期化
    form = forms.UserForm(label_suffix=':')
    c = {'form': form}
    c.update(csrf(request))
  return render(request, 'talk.html', c)
