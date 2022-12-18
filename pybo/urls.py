from django.urls import path

from .views import base_views, question_views, answer_views, info_views, pr_views, sale_views

app_name = 'pybo'

urlpatterns = [
    # base
    path('', base_views.index, name='index'),
    path('<int:question_id>/', base_views.detail, name='detail'),

    # question
    path('question/create/', question_views.question_create, name='question_create'),

    # 고유 질문 생성 (Type 부여)
    path('info/question/create/', question_views.question_create_2, name='question_create_2'),
    path('pr/question/create/', question_views.question_create_3, name='question_create_3'),
    path('sale/question/create/', question_views.question_create_4, name='question_create_4'),

    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),

    # info page
    path('info/', info_views.index, name='index'),
    path('pr/', pr_views.index, name='index'),
    path('sale/', sale_views.index, name='index'),
]
