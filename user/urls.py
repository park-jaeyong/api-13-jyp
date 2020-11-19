from django.urls import path 
from.views       import DuplicationView,SignUpView,SignInView,LikeView,TagView,ResumeView,GradeView,AwardView,Resume_detailView,RecommendationView,PastCarrerView

urlpatterns = [
    path('/check',DuplicationView.as_view()),
    path('/sign_up',SignUpView.as_view()),
    path('/sign_in',SignInView.as_view()),
    path('/like',LikeView.as_view()),
    path('/tag',TagView.as_view()),
    path('/resume',ResumeView.as_view()),
    path('/resume_detail',Resume_detailView.as_view()),
    path('/resume_detail/<int:resume_id>',Resume_detailView.as_view()),
    path('/grade',GradeView.as_view()),
    path('/award',AwardView.as_view()),
    path('/recommender',RecommendationView.as_view()), 
    path('/past_carrer',PastCarrerView.as_view()),
]