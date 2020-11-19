import json

from django.db.models import Q
from django.views import View
from django.http  import JsonResponse

from company.models import Company,Subcategory

class CompaniesView(View): 
    def get(self,request):
        try:
            data                = json.loads(request.body)
            q_tags              = Q()
            q_district          = Q()
            q_carrer            = Q()
            company_type        = request.GET.get('sub_category_id',None)
            tag_ids             = request.GET.getlist('tag_ids',None)
            district_ids        = request.GET.getlist('district_ids',None)
            carrer_id           = request.GET.get('carrer_id',None)
            
            if tag_ids:
                for tag_ids in tag_ids:
                    q_tags |= Q(sub_tag_id=tag_ids) 
                if q_district :
                    q_tags &= q_district
                if company_type :  
                    q_tags &= Q(subcategories_id=company_type)
                companies=Company.objects.filter(q_tags).select_related('district','money','district__district_categories')
            
            if district_ids:
                for district_ids in district_ids:
                    q_district |= Q(district_id=district_ids)
                if q_tags :
                    q_district &= q_tags
                if company_type :  
                    q_district &= Q(subcategories_id=company_type)
                companies=Company.objects.filter(q_district).select_related('district','money','district__district_categories')

            if carrer_id:  
                q_carrer = Q(carrer_id=carrer_id)
                if q_tags :
                    q_carrer &= q_tags
                if q_district :
                    q_carrer &= q_district
                if company_type :  
                    q_carrer &= Q(subcategories_id=company_type)
                companies=Company.objects.filter(q_carrer).select_related('district','money','district__district_categories')

            company_list = [
                {
                    "name"      : company.name ,
                    "money"     : company.money.recommend + company.money.applicant,
                    "city"      : company.district.district_categories.name,
                    "district"  : company.district.name
                } for company in companies ]
        
            return JsonResponse({"message":company_list},status=200)

        except NameError:
            return JsonResponse({"message":"NameError"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)