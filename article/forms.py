from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Article, ArticleDetail, ArticleType


class EditorCourseForm(forms.ModelForm):
    title = forms.CharField(
        label='课程标题',
        min_length=5,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入课程标题，不少于5个字'})
    )
    icon = forms.ImageField(
        label='课程封面',
        required=False
    )
    content = forms.CharField(
        label='课程介绍',
        # min_length=200,
        widget=CKEditorWidget()
    )
    introduction = forms.CharField(
        label='额外说明',
        max_length=100,
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': '2',
                   'style': 'resize:none;',
                   'placeholder': '添加您的简介- ( ゜- ゜)つロ'
                   }
        )
    )

    class Meta:
        model = Article
        fields = ('article_type', 'grade')

        widgets = {
            'article_type': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'})
        }


class EditorLessonForm(forms.Form):
    num = forms.IntegerField(
        label='课时',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    title = forms.CharField(
        label='课时标题',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    text = forms.CharField(
        label='教学内容',
        # min_length=200,
        widget=CKEditorWidget()
    )
