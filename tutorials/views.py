from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse, FileResponse

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from rest_framework.response import Response
 
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view
from .config import *
from .enrollment import get_embedding_view

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import csv

# import cv2
# import base64
# import ctxcore as ctx
# from io import BytesIO




@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    if request.method == 'GET':
        # tutorials = Tutorial.objects.all()
        
        # title = request.query_params.get('title', None)
        # if title is not None:
        #     tutorials = tutorials.filter(title__icontains=title)
        
        # tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return HttpResponse('I am ALIVE!', safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        form = TutorialForm(request.POST, request.FILES)

        # img = request.FILES['Img']
        img = Image.open(request.FILES['Img']).convert('RGB')

        v_array = get_embedding_view(img, eval_model(), device, transform)
        print('%%%%%%%%')
        print(v_array)

        return Response('embedding is: ' + str(v_array))
        
        # img = Image.open(img)
        # def get_base64(image):
        #     buffered = BytesIO()
        #     image.save(buffered, format="JPEG")
        #     img_str = base64.b64encode(buffered.getvalue())
        #     print(img_str.decode())
        #     return img_str.decode()
        
        # base_image = get_base64(img)
        
        # return HttpResponse("<img src='data:image/png;base64,"+base_image+"'/>")

        # with open(img, 'rb') as image_file:
        #     print("=+++++_+_+__+_+")
        #     content = image_file.read()


        # img = Image.open(imgraw)
        # return FileResponse(img, 'rb')

        # img = str(img.read())

        # imgraw2 = Image.open(imgraw)

        # img = np.asarray(Image.open(imgraw2))

        # with open(img, "rb") as imageFile:
        #     imageData = base64.b64encode(imageFile.read()).decode('utf-8')
        #     print(imageData)
        # ctx['image'] = imageData
        # return render(request, '', ctx)   

        # myfile = str(img.read())
        # image = cv2.imdecode(np.frombuffer(img.read(), dtype=np.uint8), cv2.IMREAD_UNCHANGED)

        # if form.is_valid():
        #     form.save()
            
        #     img = request.FILES['Img']
        #     print('request: ', type(img))
        #     # img = Image.open(img)

        #     img_array = np.asarray(Image.open(img))

        #     image = Image.fromarray(img_array)

        #     # print('Img type: ', img_)
            

        #     return HttpResponse(image)
        
        # tutorial_data = JSONParser().parse(request)
        # tutorial_serializer = TutorialSerializer(data=tutorial_data)
        # if tutorial_serializer.is_valid():
        #     tutorial_serializer.save()
        #     return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        # return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
# def success(request):
#     return HttpResponse('successfully uploaded')
 
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    try: 
        tutorial = Tutorial.objects.get(pk=pk) 
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = TutorialSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Tutorial.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
