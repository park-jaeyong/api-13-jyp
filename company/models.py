from django.db import models

class Company(models.Model):
    name             = models.CharField(max_length=45)
    subcategories    = models.ForeignKey('Subcategory',on_delete=models.CASCADE)
    money            = models.ForeignKey('Money',on_delete=models.CASCADE)
    district         = models.ForeignKey('District' , on_delete=models.CASCADE)
    title            = models.CharField (max_length=45)
    dead_line        = models.CharField (max_length=45)
    carrer           = models.ForeignKey ('Carrer',on_delete=models.CASCADE)
    image_url        = models.CharField (max_length=1000)
    sub_tag          = models.ForeignKey('Sub_tag',on_delete=models.CASCADE , related_name='sub_tags')
    tag_companies    = models.ManyToManyField('Sub_tag' , through='Tag_company',related_name='tag_companies')
    contens          = models.CharField(max_length=2000,null=True)

    class Meta:
        db_table = 'companies'  

class Subcategory(models.Model):
    maincategories = models.ForeignKey('Maincategory',on_delete=models.CASCADE)
    name           = models.CharField(max_length=45)
    image_url      = models.CharField(max_length=1000,null=True)
    
    class Meta:
        db_table = 'subcategories'

class Maincategory(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.CharField(max_length=1000,null=True)
    class Meta:
        db_table='maincategories'

class Money(models.Model):
    recommend = models.IntegerField()
    applicant = models.IntegerField()

    class Meta:
        db_table='moneys'

class District(models.Model):
    name                = models.CharField(max_length=45)
    district_categories = models.ForeignKey('District_category' , on_delete=models.CASCADE,null=True)

    class Meta:
        db_table='districts' 

class District_category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table='district_categories'

class Carrer(models.Model):
    carrer = models.CharField(max_length=45)

    class Meta:
        db_table='carrers'

class Sub_tag(models.Model):
    name = models.CharField(max_length=45)
    tag  = models.ForeignKey('Tag' , on_delete=models.CASCADE)

    class Meta:
        db_table='sub_tag'

class Tag(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table='tags'

class Salary(models.Model):
    subcategories = models.ForeignKey('Subcategory', on_delete=models.CASCADE)
    carrer        = models.ForeignKey('Carrer' , on_delete=models.CASCADE , null=True)
    maincategories= models.ForeignKey('Maincategory', on_delete=models.CASCADE)
    salary        = models.FloatField()

    class Meta:
        db_table='salaries'

class Tag_company(models.Model):
    sub_tags   = models.ForeignKey('Sub_tag', on_delete=models.CASCADE)
    companies  = models.ForeignKey('Company' , on_delete= models.CASCADE)

    class Meta:
        db_table='tag_companies'