from django.db import models

class User(models.Model):
    name            = models.CharField(max_length=45)
    email           = models.EmailField(max_length=200 , unique=True)
    password        = models.CharField(max_length=1000)
    phone           = models.CharField(max_length=45)
    likes           = models.ManyToManyField('company.Company', through='Like', related_name='likes')
    tag_filter      = models.ManyToManyField('company.Tag' , through='User_tag_filter' , related_name='user_tags_filters')
    district_filter = models.ManyToManyField('company.District' , through= 'User_district_filter' , related_name= 'user_districts_filters')
    carrer_filter   = models.ManyToManyField('company.Carrer', through='User_carrer_filter' , related_name= 'user_careers_filters')
    apllied_status  = models.ManyToManyField('company.Company', through='AppliedStatus', related_name='applied_status')
    recomender      = models.ManyToManyField('self' , symmetrical=False ,through= 'Recommendation', related_name='recomenders')
    
    class Meta:
        db_table = 'users'  
 
class Like(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company' , on_delete=models.CASCADE)

    class Meta:
        db_table='likes'

class User_tag_filter(models.Model):
    user = models.ForeignKey('User' , on_delete=models.CASCADE)
    tag  = models.ForeignKey('company.Tag' , on_delete= models.CASCADE)

    class Meta:
        db_table='user_tag_filters'

class User_district_filter(models.Model):
     user     = models.ForeignKey('User' , on_delete=models.CASCADE)
     district = models.ForeignKey('company.District' , on_delete=models.CASCADE)

     class Meta:
         db_table='user_district_filters'

class User_carrer_filter(models.Model):
     user     = models.ForeignKey('User' , on_delete=models.CASCADE)
     carrer = models.ForeignKey('company.Carrer' , on_delete=models.CASCADE)

     class Meta:
         db_table='user_carrer_filters'

class AppliedStatus(models.Model):
    user     = models.ForeignKey('User' , on_delete=models.CASCADE)
    company  = models.ForeignKey('company.Company',on_delete=models.CASCADE)

    class Meta:
        db_table='appliedstatus'

class Recommendation(models.Model):
    from_commender  = models.ForeignKey ('User' , on_delete=models.CASCADE ,related_name='recomender_from_comender') 
    to_comender     = models.ForeignKey ('User' , on_delete=models.CASCADE ,related_name='recomender_to_comender')
    contens         = models.CharField  (max_length=1000,null=True)

    class Meta:
        db_table='recommenders'

class Resume(models.Model):
    name   = models.CharField(max_length=45)  
    date   = models.DateField(auto_now=True,null=True)
    user   = models.ForeignKey('User',on_delete=models.CASCADE)

    class Meta:
        db_table='resumes'

class Resume_detail(models.Model):
    intro = models.CharField(max_length=100)
    resume= models.ForeignKey('Resume' , on_delete=models.CASCADE)

    class Meta:
        db_table='resume_details'

class Past_carrer(models.Model):
    year       = models.CharField(max_length=45)
    company    = models.CharField(max_length=45)
    resume  = models.ForeignKey('Resume_detail' , on_delete=models.CASCADE)

    class Meta:
        db_table='past_carrers'

class Achievement(models.Model):
    achievement = models.CharField(max_length=45)
    year        = models.CharField(max_length=45)
    detail      = models.CharField(max_length=200) 
    past_carrer = models.ForeignKey('Past_carrer',on_delete=models.CASCADE)
    
    class Meta:
        db_table='achievements'

class Award(models.Model):
    year   = models.CharField(max_length=45)
    name   = models.CharField(max_length=45)
    detail = models.CharField(max_length=200)
    resume  = models.ForeignKey('Resume_detail' , on_delete=models.CASCADE)

    class Meta:
        db_table='awards'

class Grade(models.Model):
    year        = models.CharField(max_length=45)
    school_name = models.CharField(max_length=45)
    resume  = models.ForeignKey('Resume_detail' , on_delete=models.CASCADE)

    class Meta:
        db_table='grades'