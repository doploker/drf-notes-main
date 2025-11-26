from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.template.defaulttags import csrf_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from notes.models import Note
from notes.serializer import NoteSerializer
@csrf_exempt
# Create your views here.
def note_list(request):

    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def note_detail(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note does not exist'}, status=404)

    if request.method == 'DELETE':
        note.delete()
        return JsonResponse({
            'status': 'success',
            "id": pk,
        }, status=200)
    elif request.method == 'GET':
        serializer = NoteSerializer(note)
        return JsonResponse(serializer.data,    status=200)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NoteSerializer(note, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,     status=200)
        return JsonResponse(serializer.errors, status=400)
