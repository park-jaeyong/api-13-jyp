import jwt
from django.http import JsonResponse
from .models import User
from my_settings  import SECRET,ALGORITHM

def token_check(func): 
    def wrapper(self, request, *args, **kwargs):
        encode_token = request.headers.get('AUTHORIZATION', None)
        if encode_token == None: 
            return func(self, request, *args, **kwargs)
        try:
            payload  = jwt.decode(encode_token, SECRET, algorithm = ALGORITHM)
            user     = User.objects.get(id=payload["user_id"])
            if user == None :
                return JsonResponse({"message":"INVALID_USER"}, status=400)
            request.user = user
            return func(self, request,*args ,**kwargs) 
            
        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"UNKNOWN_USER"}, status=400)
    return wrapper