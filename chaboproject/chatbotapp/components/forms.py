from django import forms

class UserForm(forms.Form):
  texttwo = forms.CharField(
    label="ここからAIと会話",
    widget=forms.TextInput(
      attrs={
        'id':'dropedfile',
        'placeholder': '会話文を入力してください。',
      }
    )
  )