import bcrypt
import jwt
import re
import json

from django.views import View
from django.http  import JsonResponse

from datetime       import datetime
from my_settings    import SECRET,ALGORITHM
from company.models import Company,Tag,District,Carrer
from .utils         import token_check
from .models        import (
    User,
    Like,
    User_tag_filter,
    User_district_filter,
    User_carrer_filter,
    Resume,Grade,Resume_detail,
    Award,Recommendation,Past_carrer,
)

class DuplicationView(View):
    def post(self , request):
        try:
            data    = json.loads(request.body)
            email   = data ["email"]
            pattern = r'[A-Z0-9._%+-]+@[A-Z0-9,-]+\.[A-Z]{2,4}'    
            regex   = re.compile(pattern,flags=re.IGNORECASE)
            users   = User.objects.filter(email=email).exists()
 
            if len(regex.findall(email)) == 0:
                return JsonResponse({"message":"EMAIL_INVALID"},status=400)
            
            if users:
                return JsonResponse({"message":"SIGN_IN"},status=200)
            
            return JsonResponse({"message":"SIGN_UP"},status=200)

        except KeyError:
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

class SignUpView(View):
    def post(self , request):
        try :
            data          = json.loads(request.body)
            email         = data ["email"]
            password      = data ["password"]
            name          = data ["name"]
            phone         = data ["phone"] 
            hash_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                email    = email,
                password = hash_password,
                name     = name ,
                phone    = phone 
            )
            return JsonResponse({"message":"SUCCESS"},status=201)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

class SignInView(View):
    def post(self , request):
        try : 
            data              = json.loads(request.body)
            email             = data["email"]
            password          = data["password"]
            password_encode   = User.objects.get(email=email).password.encode('utf-8')
            users             = User.objects.get(email=email)
            
            if bcrypt.checkpw(password.encode('utf-8'), password_encode) :
                access_token  = jwt.encode({'user_id' : users.id}, SECRET, algorithm = ALGORITHM).decode('utf-8')

                return JsonResponse ({"message":"SUCCESS",'authorization':access_token },status=200)

            return JsonResponse({"message":"INVALID EMAIL OR PASSWORD"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)

        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

        except User.DoesNotExist :
            return JsonResponse({"message":"Id not invalid"},status=400)

class LikeView(View):
    @token_check
    def post(self,request):
        try:
            data       = json.loads(request.body)
            company    = data['company_id']
            user_id    = request.user
            company_id = Company.objects.get(id=company)
            likes      = Like.objects.filter (user_id = user_id , company_id=company_id)

            if user_id and company_id and not likes:
                Like.objects.create(company=company_id  , user= user_id)
                return JsonResponse({"message":"SUCCESS"}, status=201)
            return JsonResponse({"message":"id or like_duplication INVALID"},status=400)
        
        except Company.DoesNotExist:
            return JsonResponse({"message":"company_id INVALID"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)

        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

    @token_check
    def delete(self,request):
        try:
            data       = json.loads(request.body)
            company    = data['company_id']
            user_id    = request.user
            company_id = Company.objects.get(id=company)

            if user_id and company_id :
                Like.objects.get(user = user_id , company=company_id).delete()
                return JsonResponse({"message":"SUCCESS"}, status=200)

            return JsonResponse({"message":"user_id or company_id INVALID"},status=400)

        except Like.DoesNotExist:
            return JsonResponse({"message":"LIKE_VALUE_INVALID"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)

        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

    @token_check
    def get(self,request):
        user_id=request.user.id

        company_list=[
            {
                "id"       : company.id ,
                "name"     : company.name,
                "tilte"    : company.title,
                "img_url"  : company.image_url,
                "city"     : company.district.district_categories.name,
                "district" : company.district.name ,
                "money"    : company.money.recommend + company.money.applicant

            }for company in User.objects.get(id=user_id).likes.select_related()]
        
        return JsonResponse({"message":"SUCCESS","job_list":company_list}, status=200)

class TagView(View):
    @token_check
    def post(self,request):
        data = json.loads(request.body)
        user_id =request.user
        
        if "tag_list" in data : 
            tag_list = data["tag_list"]
            if data.get("tag_list"):
                User_tag_filter.objects.filter(user=user_id).delete()
                for tag in tag_list:
                    
                    tag_1=Tag.objects.get(id=tag)
                    User_tag_filter.objects.create(user=user_id , tag=tag_1)

        if "district_list" in data : 
            district_list = data["district_list"]
            
            if data.get("district_list"):
          
                User_district_filter.objects.filter(user=user_id).delete()
                
                for district in district_list:
                    
                    district_1=District.objects.get(id=district)
                    User_district_filter.objects.create(user=user_id , district=district_1)

        if "career_list" in data : 
            career_list = data["career_list"]
            
            if data.get("career_list"):
          
                User_carrer_filter.objects.filter(user=user_id).delete()
                
                for carrer in career_list:
                    
                    carrer_1=Carrer.objects.get(id=carrer)
                    User_carrer_filter.objects.create(user=user_id , carrer=carrer_1)
        
        return JsonResponse({"message":"SUCCESS"},status=200)

    @token_check
    def get(self,request):
        user_id=request.user.id
        tag=[
            {
             "id" : tag.id ,
             "name": tag.name
            }for tag in User.objects.get(id=user_id).tag_filter.select_related()]
        
        district=[
            {
             "id"       : district.id ,
             "city"     : district.district_categories.name ,
             "district" : district.name
            }for district in User.objects.get(id=user_id).district_filter.select_related()]

        carrer=[
            {
             "id"   : carrer.id     ,
             "name" : carrer.carrer 
            }for carrer in User.objects.get(id=user_id).carrer_filter.select_related()]
        
        return JsonResponse({"message":"SUCCESS","tag_list":tag,"district_list":district,"carrer":carrer},status=200)

class ResumeView(View):
    @token_check
    def post(self,request):
        try:
            data        = json.loads(request.body)
            resume_id   = data['resume_id']
            user_id     = request.user
            resume_id_f = Resume.objects.filter(id=resume_id)
            now         = datetime.now()
            if resume_id_f :
                resume_id_f.update(name=user_id.name,user=user_id,date=now)
                return JsonResponse({"message":"UPDATE","resume_id":resume_id},status=200)

            Resume.objects.create(id=resume_id,name=user_id.name,user=user_id ,date=now)
            return JsonResponse({"message":"SUCCESS","resume_id":resume_id},status=200)
        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)
            
    @token_check
    def get(self,request):
        user_id=request.user
        resume=[
            {
             "id"      : resume.id  ,
             "name"    : resume.name,
             "date"    : resume.date ,
             "user_id" : resume.user_id
            
            }for resume in Resume.objects.filter(user=user_id)]

        return JsonResponse({"message":"SUCCESS","resume":resume},status=200)

    @token_check
    def delete(self,request):
        try:
            data            = json.loads(request.body)
            resume_id       = data['resume_id']
            resume          = Resume.objects.get(id=resume_id)

            if resume:
                for resume in Resume.objects.get(id=resume_id).resume_detail_set.all() :
                    resume.grade_set.all().delete()
                    resume.award_set.all().delete()
                    resume.past_carrer_set.all().delete()
                resume.delete()
                return JsonResponse({"message":"DELETE"},status=200)
            else :
                return JsonResponse({"message":"RESUME_NOT_INVALID"},status=400)
                
        except Resume.DoesNotExist : 
            return JsonResponse({"message":"RESUME_ID_NOT_INVALID"},status=400)
        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

class Resume_detailView(View):
    @token_check
    def post(self,request):
        try:
            data            = json.loads(request.body)
            resume_id       = data['resume_id']
            resume          = Resume.objects.get(id=resume_id)
            Resume_detail_f = Resume_detail.objects.filter(resume=resume_id)

            if  "intro" in data : 
                intro = data['intro']
            else :
                intro=""

            if Resume_detail_f :
                Resume_detail_f.update(intro=intro,resume_id=resume.id)
                return JsonResponse({"message":"UPDATE"},status=200)
            
            Resume_detail.objects.create(intro=intro,resume_id=resume.id)
            return JsonResponse({"message":"CREATE"},status=201)
        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except Resume.DoesNotExist:
            return JsonResponse({"message":"Resume_Not_Invalid"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

    @token_check
    def get(self,request,resume_id):
        try:
            resume_id = resume_id
            resume    = Resume.objects.get(id=resume_id)
            
            if Award.objects.filter(resume=resume.id) or Grade.objects.filter(resume=resume.id):
                award=[
                    {
                        "year"  : Resume_detail.objects.get(id=resume_id).award_set.all()[award_range].year ,
                        "name"  : Resume_detail.objects.get(id=resume_id).award_set.all()[award_range].name , 
                        "detail": Resume_detail.objects.get(id=resume_id).award_set.all()[award_range].detail        
                }
                if Resume_detail.objects.filter(id=resume_id)  else [] for award_range in  range(len(Award.objects.filter(resume=resume.id))) ]
                grade=[
                    {
                        "year"  : Resume_detail.objects.get(id=resume_id).grade_set.all()[grade_range].year ,
                        "school_name"  : Resume_detail.objects.get(id=resume_id).grade_set.all()[grade_range].school_name       
                }
                if Resume_detail.objects.filter(id=resume_id)  else [] for grade_range in  range(len(Grade.objects.filter(resume=resume.id))) ]

                past_carrer=[
                    {
                        "year"  : Resume_detail.objects.get(id=resume_id).past_carrer_set.all()[past_range].year ,
                        "company"  : Resume_detail.objects.get(id=resume_id).past_carrer_set.all()[past_range].company       
                }
                if Resume_detail.objects.filter(id=resume_id)  else [] for past_range in  range(len(Past_carrer.objects.filter(resume=resume.id))) ]

                return JsonResponse({"award":award,"grade":grade,"past_carrer":past_carrer},status=200)
            return JsonResponse({"message":"SUCCESS"},status=200)
        except Resume.DoesNotExist:
            return JsonResponse({"message":"Resume_Not_Invalid"},status=400)

class GradeView(View):
    
    def post(self,request):
        try:
            data        = json.loads(request.body)
            grade_id    = data["grade_id"]
            resume_id   = data['resume_id']
            year        = data["year"]
            school_name = data["school_name"]
            grade_id_f  = Grade.objects.filter(id=grade_id)
            resume      = Resume_detail.objects.get(id=resume_id)
      
            if grade_id_f  :
                grade_id_f.update(id=Grade.objects.get(id=grade_id).id,year=year,school_name=school_name,resume=resume)
                return JsonResponse({"message":"UPDATE"},status=200)

            Grade.objects.create(id=grade_id,year=year,school_name=school_name,resume=resume)
            return JsonResponse({"message":"SUCCESS"},status=200)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

    def delete(self,request):
        try:
            data       = json.loads(request.body)
            grade_id   = data['grade_id']
            Grade.objects.get(id=grade_id).delete()
            return JsonResponse({"message":"SUCCESS"},status=200)

        except Grade.DoesNotExist :
            return JsonResponse({"message":"Award_Not_Invalid"},status=200)

class AwardView(View):
    def post(self,request):
        try:
            data        = json.loads(request.body)
            award_id    = data ["award_id"]
            resume_id   = data['resume_id']
            year        = data["year"]
            name        = data["name"]
            detail      = data ["detail"]
            resume      = Resume_detail.objects.get(id=resume_id)
            award_id_f  = Award.objects.filter(id=award_id)

            if award_id_f :
                award_id_f.update(id=award_id,year=year,name=name,resume=resume,detail=detail)   
                return JsonResponse({"message":"UPDATE","award_id":award_id},status=200)
    
            Award.objects.create(id=award_id,year=year,name=name,resume=resume,detail=detail) 
            return JsonResponse({"message":"CREATE","award_id":award_id},status=200)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

    def delete(self,request):
        try:
            data       = json.loads(request.body)
            award_id   = data['award_id']

            Award.objects.get(id=award_id).delete()
            return JsonResponse({"message":"SUCCESS"},status=200)

        except Award.DoesNotExist :
            return JsonResponse({"message":"Award_Not_Invalid"},status=200)

class PastCarrerView(View):

    def post(self,request):
        try:
            data              = json.loads(request.body)
            past_carrer_id    = data ["past_carrer_id"]
            resume_id         = data['resume_id']
            year              = data["year"]
            company           = data["company"]
            resume            = Resume_detail.objects.get(id=resume_id)
            past_carrer_id_f  = Past_carrer.objects.filter(id=past_carrer_id)

            if past_carrer_id_f :
                past_carrer_id_f.update(id=past_carrer_id,year=year,company=company, resume=resume)   
                return JsonResponse({"message":"UPDATE","past_carrer_id":past_carrer_id},status=200)

            Past_carrer.objects.create(id=past_carrer_id , year=year , company=company , resume=resume)
            return JsonResponse({"message":"SUCCESS","past_carrer_id":past_carrer_id},status=200)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

    def delete(self,request):
        try:
            data            = json.loads(request.body)
            past_carrer_id  = data ["past_carrer_id"]

            Past_carrer.objects.get(id=past_carrer_id).delete()
            return JsonResponse({"message":"SUCCESS"},status=200)

        except Past_carrer.DoesNotExist :
            return JsonResponse({"message":"Past_Carrer_Not_Invalid"},status=200)

class RecommendationView(View):
    @token_check
    def post(self,request):
        try:
            data             = json.loads(request.body)
            email            = data ["email"]
            from_user        = request.user
            to_user          = User.objects.get(email=email)
            Recommendation_f = Recommendation.objects.filter(from_commender_id=from_user.id,to_comender_id=to_user.id)

            if "contens" in data :
                contens = data["contens"] 
            else :
                contens = 'NULL'
           
            if  Recommendation_f  :
                Recommendation_f.update(from_commender_id=from_user.id,to_comender_id=to_user.id,contens=contens)
                return JsonResponse({"message":"UPDATE"},status=200)

            Recommendation.objects.create(from_commender_id=from_user.id,to_comender_id=to_user.id,contens=contens)
            return JsonResponse({"message":"CREATE"},status=200)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

    @token_check
    def get(self,request): 
        try:
            recommendatin_type = request.GET.get('type') 
            from_user          = request.user

            if recommendatin_type == "written": 
                recommendatin_type=User.objects.get(id=from_user.id).recomender_from_comender.all()
            elif recommendatin_type == "given":
                recommendatin_type=User.objects.get(id=from_user.id).recomender_to_comender.all()
            else :
                return JsonResponse({"message":"QuerryString_Error"},status=400)
                
            recommendation = [
                {
                    "from_user.id":User.objects.get(id=from_user.to_comender_id).name
                }
            for from_user in recommendatin_type]

            return JsonResponse({"message":recommendation},status=200)
        except AttributeError :
            return JsonResponse({"message":"QuerryString_Error"},status=400)

    @token_check
    def delete(self,request):
        try:
            data       = json.loads(request.body)
            from_user  = request.user
            to_user_id = data["to_user_id"]
            to_user    = User.objects.get(id=to_user_id)

            Recommendation.objects.get(from_commender_id=from_user.id,to_comender_id=to_user.id).delete()
            return JsonResponse({"message":"DELETE"},status=200)
       
        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)
        except Recommendation.DoesNotExist:
            return JsonResponse({"message":"USER_ID_NOT_INVALIED"},status=400)