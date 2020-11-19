import json
import bcrypt
import jwt

from django.test import (
    TestCase,
    Client
)

from datetime       import datetime
from my_settings    import SECRET,ALGORITHM
from company.models import Company,Tag,District,Carrer,Maincategory,Subcategory,Salary,District_category,Sub_tag,Money
from .models        import (
    User,
    Like,
    User_tag_filter,
    User_district_filter,
    User_carrer_filter,
    Resume,Grade,Resume_detail,
    Award,Recommendation,Past_carrer,
)

client = Client() 

class DuplicationTest(TestCase):
    def setUp(self):
        User.objects.create(email='test@test.com')

    def tearDown(self):
        User.objects.all().delete()

    def test_duplicationview_post_duplication(self):

        users = {
            
            "email" : 'test@test.com'
        }
        response = client.post('/user/check', json.dumps(users), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SIGN_IN'
            }
        )
    def test_duplicationview_post_sign_up(self):

        users = {
            
            "email" : 'test_1@test.com'
        }
        response = client.post('/user/check', json.dumps(users), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SIGN_UP'
            }
        )

    def test_duplicationview_post_email_not_invalid(self):

        users = {
            
            "email" : 'test_1test.com'
        }
        response = client.post('/user/check', json.dumps(users), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'EMAIL_INVALID'
            }
        )
    def test_duplicationview_post_key_error(self):

        users = {}
        response = client.post('/user/check', json.dumps(users), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error'
            }
        )

class SignUpTest(TestCase): 
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(email='test@test.com', password=hashed_password,name='박재용',phone='01012341234')

    def tearDown(self):
        User.objects.filter(email='test@test.com').delete()

    def test_signup_post_success(self): 

        users = {
            'email': 'test_email@test.com',
            'password': 'test1234!',
            'name': "박재용",
            'phone' : "01012341234"
            }
        response = client.post('/user/sign_up',users, content_type = 'application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "message" : "SUCCESS"
        })

    def test_signup_post_key_error(self): 

        response = client.post('/user/sign_up',{}, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message" : "Key_Error"
        })

class SignInTest(TestCase): 
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(email='test@test.com', password=hashed_password)

    def tearDown(self):
        User.objects.filter(email='test@test.com').delete()

    def test_signin_post_success(self): 
        user          = User.objects.get(email='test@test.com')
        access_token  = jwt.encode({'user_id' : user.id}, SECRET, algorithm = ALGORITHM).decode('utf-8')
        users = {
            'email': 'test@test.com',
            'password': 'test1234!',  
            
            }
        response = client.post('/user/sign_in',users, content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message" : "SUCCESS",
            "authorization":access_token
        })

    def test_signin_post_key_error(self): 

        response = client.post('/user/sign_in',{}, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message" : "Key_Error"
        })

class LikeTest(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(email='test@test.com', password=hashed_password)
        
        Maincategory.objects.create(name="maincategory",image_url="image_url")
        main = Maincategory.objects.get(name="maincategory")

        Subcategory.objects.create(maincategories=main,name="subcategory",image_url="image_url")
        sub  = Subcategory.objects.get(name="subcategory")

        Money.objects.create(recommend=0,applicant=0)
        money   = Money.objects.get(recommend=0,applicant=0)
        
        District_category.objects.create(name="test")
        district_category = District_category.objects.get(name="test")
        
        District.objects.create(name="test",district_categories=district_category)
        district=District.objects.get(name="test")
        
        Carrer.objects.create(carrer="test")
        carrer=Carrer.objects.get(carrer="test")

        Tag.objects.create(name="test")
        tag=Tag.objects.get(name="test")

        Sub_tag.objects.create(name="test",tag=tag)
        sub_tag=Sub_tag.objects.get(name="test")
        
        Company.objects.create(id=1,name="company",subcategories=sub,money=money,district=district,carrer=carrer,sub_tag=sub_tag)

        self.token  = jwt.encode({'user_id' : User.objects.get(email="test@test.com").id}, SECRET, algorithm = ALGORITHM).decode('utf-8')
    
    def tearDown(self):
        Like.objects.all().delete()
        User.objects.all().delete()
        Company.objects.all().delete()
        Tag.objects.all().delete()
        
    def test_like_post_success(self):
        headers        = {"HTTP_AUTHORIZATION": self.token}
        response       = client.post('/user/like', json.dumps({'company_id':1}), **headers, content_type = 'application/json')
      
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )

    def test_like_key_error(self):
        headers        = {"HTTP_AUTHORIZATION": self.token}
        response       = client.post('/user/like', json.dumps({}), **headers, content_type = 'application/json')
   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error'
            }
        )

    def test_like_company_error(self):
        headers        = {"HTTP_AUTHORIZATION": self.token}
        response       = client.post('/user/like', json.dumps({'company_id':2}), **headers, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'company_id INVALID'
            }
        )

    def test_like_get_success(self):
        header         = {"HTTP_Authorization" : self.token}
        response       = client.get('/user/like', **header, content_type = 'application/json')
        user_id        = User.objects.get(email='test@test.com')
        
        company_list=[
            {
                "id"       : company.id ,
                "name"     : company.name,
                "tilte"    : company.title,
                "img_url"  : company.image_url,
                "city"     : company.district.district_categories.name,
                "district" : company.district.name,
                "money"    : company.money.recommend + company.money.applicant
            
            }for company in User.objects.get(id=user_id.id).likes.select_related()]
      
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'job_list':company_list,
                'message':'SUCCESS'
            }
        )

class TagTest(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(email='test@test.com', password=hashed_password)

        Tag.objects.create(id=1,name="test")

        District_category.objects.create(name="test")
        district_category = District_category.objects.get(name="test")
        District.objects.create(name="test",district_categories=district_category)
        
        Carrer.objects.create(carrer="test")

        self.token  = jwt.encode({'user_id' : User.objects.get(email="test@test.com").id}, SECRET, algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        User.objects.all().delete()
        Tag.objects.all().delete()
        District.objects.all().delete()
        Carrer.objects.all().delete()
        
    def test_Tag_post_success(self):
        headers        = {"HTTP_AUTHORIZATION": self.token}
        response       = client.post('/user/tag', json.dumps({'tag_list':[1] , 'district':[1],'carrer':1}), **headers, content_type = 'application/json')
      
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )

    def test_Tag_get_success(self):
        header         = {"HTTP_Authorization" : self.token}
        response       = client.get('/user/tag', **header, content_type = 'application/json')
        user_id        = User.objects.get(email='test@test.com')
        
        tag=[
            {
             "id" : tag.id,
             "name": tag.name
            }for tag in User.objects.get(id=user_id.id).tag_filter.select_related()]
        
        district=[
            {
             "id"       : district.id,
             "city"     : district.district_categories.name,
             "district" : district.name
            }for district in User.objects.get(id=user_id.id).district_filter.select_related()]

        carrer=[
            {
             "id"   : carrer.id,
             "name" : carrer.carrer 
            }for carrer in User.objects.get(id=user_id.id).carrer_filter.select_related()]
      
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message'       : 'SUCCESS',
                "tag_list"      : tag,
                "district_list" : district,
                "carrer"        : carrer
            }
        )

class ResumeTest(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(email='test@test.com' , password=hashed_password)
        user = User.objects.get(email="test@test.com")
        now  = datetime.now()
        Resume.objects.create(id=1,name="test", date=now,user_id=user.id)
        self.token  = jwt.encode({'user_id' : User.objects.get(email="test@test.com").id}, SECRET, algorithm = ALGORITHM).decode('utf-8')
  
    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
   
    def test_ResumeTest_post_update(self):

        header         = {"HTTP_Authorization" : self.token }
        response       = client.post('/user/resume', ({'resume_id':1}),**header, content_type = 'application/json')
        user_id        = User.objects.get(email='test@test.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'UPDATE',
                "resume_id":1
            }
        )

    def test_ResumeTest_post_succecc(self):
        
        header         = {"HTTP_Authorization" : self.token }
        response       = client.post('/user/resume', ({'resume_id':2}),**header, content_type = 'application/json')
        user_id        = User.objects.get(email='test@test.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS',
                "resume_id":2
            }
        )

    def test_ResumeTest_post_key_error(self):
        
        header         = {"HTTP_Authorization" : self.token}
        response       = client.post('/user/resume', ({}),**header, content_type = 'application/json')
        user_id        = User.objects.get(email='test@test.com')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error',
            }
        )
   
    def test_ResumeTest_get_success(self):

        header         = {"HTTP_Authorization" : self.token}
        response       = client.get('/user/resume',**header, content_type = 'application/json')
        user_id        = User.objects.get(email='test@test.com')
        
        resume=[
            {
            "id"      : resume.id  ,
            "name"    : resume.name,
            "date"    : resume.date.strftime('%Y-%m-%d'),
            "user_id" : resume.user_id
            
            }for resume in Resume.objects.filter(user=user_id)]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS',
                "resume" : resume
            }
        )

    def test_ResumeTest_delete_success(self):

        header         = {"HTTP_Authorization" : self.token}
        response       = client.delete('/user/resume',({"resume_id":1}),**header, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'DELETE'
            }
        )

    def test_ResumeTest_delete_resume_id_not(self):
            
        header         = {"HTTP_Authorization" : self.token}
        response       = client.delete('/user/resume',({"resume_id":2}),**header, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'RESUME_ID_NOT_INVALID'
            }
        )

    def test_ResumeTest_delete_key_error(self):
            
        login_response = client.post('/user/sign_in', {'email': 'test@test.com', 'password':'test1234!'}, content_type = 'application/json')
        token          = login_response.json()["authorization"]
        header         = {"HTTP_Authorization" : self.token}
        response       = client.delete('/user/resume',({}),**header, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error'
            }
        )

class Resume_detail_Test(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(email='test@test.com' , password=hashed_password)
        user   = User.objects.get(email="test@test.com")

        Resume.objects.create(id=1 , name="test",user_id=user.id)
        resume=Resume.objects.get(id=1)
        Resume_detail.objects.create(id=1,resume=resume)
        resume_detail = Resume_detail.objects.get(id=1)
        Award.objects.create(year="test",name="test",detail="test",resume=resume_detail)
        Grade.objects.create(year="test",school_name="test", resume=resume_detail)

        self.token  = jwt.encode({'user_id' : User.objects.get(email="test@test.com").id}, SECRET, algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
        Resume_detail.objects.all().delete()
    
    def test_Resume_detail_test_success(self):
        Resume_detail.objects.all().delete()
        header          = {"HTTP_Authorization":self.token}
        response       = client.post('/user/resume_detail',({"resume_id":1}),**header, content_type = 'application/json')
        
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json(),
        {
            'message':'CREATE'
        }
        )

    def test_Resume_detail_post_update(self):
        Resume_detail.objects.create(intro="test", resume_id=1)
        header          = {"HTTP_Authorization":self.token}
        response        = client.post('/user/resume_detail',({"resume_id":1}),**header, content_type = 'application/json')
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
        {
            'message':'UPDATE'
        }
        )

    def test_Resume_detail_post_resume_not_invalid(self):
        header          = {"HTTP_Authorization":self.token}
        response        = client.post('/user/resume_detail',({"resume_id":2}),**header, content_type = 'application/json')
        
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
        {
            'message':'Resume_Not_Invalid',
        }
        )
        
    def test_Resume_detail_post_key_error(self):
        header          = {"HTTP_Authorization":self.token}
        response        = client.post('/user/resume_detail',({}),**header, content_type = 'application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
        {
        'message':'Key_Error',
        }
        )

    def test_Resume_detail_get_success(self):
        header          = {"HTTP_Authorization" : self.token}
        response        = client.get('/user/resume_detail/1', **header)
       
        if Award.objects.filter(resume=1) or Grade.objects.filter(resume=1):
            award=[
                {
                    "year"  : Resume_detail.objects.get(id=1).award_set.all()[award_range].year ,
                    "name"  : Resume_detail.objects.get(id=1).award_set.all()[award_range].name , 
                    "detail": Resume_detail.objects.get(id=1).award_set.all()[award_range].detail        
            }

        if Resume_detail.objects.filter(id=1)  else [] for award_range in  range(len(Award.objects.filter(resume=1))) ]
            grade=[
                {
                    "year"  : Resume_detail.objects.get(id=1).grade_set.all()[grade_range].year ,
                    "school_name"  : Resume_detail.objects.get(id=1).grade_set.all()[grade_range].school_name       
            }
            if Resume_detail.objects.filter(id=1)  else [] for grade_range in  range(len(Grade.objects.filter(resume=1))) ]

            past_carrer=[
                {
                    "year"  : Resume_detail.objects.get(id=1).past_carrer_set.all()[past_range].year ,
                    "company"  : Resume_detail.objects.get(id=1).past_carrer_set.all()[past_range].company       
            }
            if Resume_detail.objects.filter(id=1)  else [] for past_range in  range(len(Past_carrer.objects.filter(resume=1))) ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"award":award,"grade":grade,"past_carrer":past_carrer})

class Grade_Test(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(id=1,email='test@test.com' , password=hashed_password)
        user = User.objects.get(email="test@test.com")
        Resume.objects.create(id=1,name="test",user=user)
        resume = Resume.objects.get(id=1,name="test")
        Resume_detail.objects.create(id=1,resume=resume)

    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
        Resume_detail.objects.all().delete()

    def test_grade_post_success(self):
        response = client.post('/user/grade', json.dumps({"grade_id":1 , "resume_id":1 , "year":"test" , "school_name":"test"}), content_type = 'application/json')
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )

    def test_grade_post_key_error(self):
        response = client.post('/user/grade', json.dumps({}), content_type = 'application/json')
       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error'
            }
        )

class Award_Test(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(id=1,email='test@test.com' , password=hashed_password)
        user = User.objects.get(email="test@test.com")
        Resume.objects.create(id=1,name="test",user=user)
        resume = Resume.objects.get(id=1,name="test")
        Resume_detail.objects.create(id=1,resume=resume)

    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
        Resume_detail.objects.all().delete()

    def test_award_post_success(self):
        response = client.post('/user/award', json.dumps({"award_id":1 , "resume_id":1 , "year":"test" , "name":"test","detail":"test"}), content_type = 'application/json')
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'award_id':1,
                'message':'CREATE'
            }
        )
    def test_award_post_key_error(self):
        response = client.post('/user/award', json.dumps({}), content_type = 'application/json')
       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error'
            }
        )
    def test_award_delete_success(self):
        resume = Resume_detail.objects.get(id=1)
        Award.objects.create(id=1,resume=resume,year="test",name="test",detail="test")
        response = client.delete('/user/award', json.dumps({"award_id":1}), content_type = 'application/json')
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )

class Past_carrer_Test(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(id=1,email='test@test.com' , password=hashed_password)
        user = User.objects.get(email="test@test.com")
        Resume.objects.create(id=1,name="test",user=user)
        resume = Resume.objects.get(id=1,name="test")
        Resume_detail.objects.create(id=1,resume=resume)

    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
        Resume_detail.objects.all().delete()

    def test_past_carrer_post_success(self):
        response = client.post('/user/past_carrer', json.dumps({"past_carrer_id":1 , "resume_id":1 , "year":"test" , "company":"test"}), content_type = 'application/json')
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS',
                'past_carrer_id':1
            }
        )
    def test_past_carrer_post_key_error(self):
        response = client.post('/user/past_carrer', json.dumps({}), content_type = 'application/json')
       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error'
            }
        )
    def test_award_delete_success(self):
        resume = Resume_detail.objects.get(id=1)
        Past_carrer.objects.create(id=1,resume=resume,year="test",company="test")
        response = client.delete('/user/past_carrer', json.dumps({"past_carrer_id":1}), content_type = 'application/json')
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )

class Recommendation_Test(TestCase):

    def setUp(self):
        hashed_password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(id=1,email='test@test.com', password=hashed_password , name="박재용")
        user=User.objects.get(email='test@test.com')
        Recommendation.objects.create(from_commender=user , to_comender=user,contens="")
        self.token  = jwt.encode({'user_id' : User.objects.get(email="test@test.com").id}, SECRET, algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        User.objects.all().delete()
 
    def test_Recommendation_post_success(self):
        Recommendation.objects.all().delete()
        headers        = {"HTTP_AUTHORIZATION": self.token}
        response       = client.post('/user/recommender', json.dumps({"email":"test@test.com"}), **headers, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'CREATE'
            }
        )
    def test_Recommendation_post_key_error(self):
        Recommendation.objects.all().delete()
        headers        = {"HTTP_AUTHORIZATION": self.token}
        response       = client.post('/user/recommender', json.dumps({}), **headers, content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error'
            }
        )
    def test_Recommendation_get_success(self):
        headers        = {"HTTP_AUTHORIZATION": self.token}  
        response       = client.get('/user/recommender?type=written', **headers, content_type = 'application/json')
      
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message': [{'from_user.id':User.objects.get(id=1).name}]
            }
        )
    def test_Recommendation_get_querrystring_error(self):
        headers        = {"HTTP_AUTHORIZATION": self.token}  
        response       = client.get('/user/recommender', **headers, content_type = 'application/json')
      
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message': "QuerryString_Error"
            }
        )
    def test_Recommendation_delete_success(self):
        headers        = {"HTTP_AUTHORIZATION": self.token}
        user           = User.objects.get(email="test@test.com")
        response       = client.delete('/user/recommender', json.dumps({"to_user_id":user.id}), **headers, content_type = 'application/json')
      
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'DELETE'
            }
        )

    def test_Recommendation_delete_key_error(self):
        headers        = {"HTTP_AUTHORIZATION": self.token}
        response       = client.delete('/user/recommender', json.dumps({}), **headers, content_type = 'application/json')
      
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'Key_Error'
            }
        )