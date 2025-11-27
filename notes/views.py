from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.template.defaulttags import csrf_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from notes.models import Note
from notes.serializer import NoteSerializer
class NoteList(generics.ListCreateAPIView):

    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #получить заметки по user id
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    #создать заметку и присвоить владельцу
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)



# class NoteList(APIView):
#     def get(self, request):
#         notes = Note.objects.all()
#         serializer = NoteSerializer(notes, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = NoteSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
# class NoteDetail(APIView):
#
#     def get(self, request, pk):
#         try:
#             note = Note.objects.get(pk=pk)
#         except Note.DoesNotExist:
#             return JsonResponse({'error': 'Note does not exist'}, status=404)
#         serializer = NoteSerializer(note)
#         return JsonResponse(serializer.data, status=200)
#     def put(self, request, pk):
#         try:
#             note = Note.objects.get(pk=pk)
#         except Note.DoesNotExist:
#             return JsonResponse({'error': 'Note does not exist'}, status=404)
#         data = JSONParser().parse(request)
#         serializer = NoteSerializer(note, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=200)
#         return JsonResponse(serializer.errors, status=400)
#     def delete(self, request, pk):
#         try:
#             note = Note.objects.get(pk=pk)
#         except Note.DoesNotExist:
#             return JsonResponse({'error': 'Note does not exist'}, status=404)
#         note.delete()
#         return JsonResponse({
#             'status': 'success',
#             "id": pk,
#         }, status=200)
