from django.shortcuts import render
from django.views import View
# Create your views here.

from .models import HashTag


class HashTagView(View):
	def get(self, request, Hashtag, *args, **kwargs):
		obj, Created = HashTag.objects.get_or_create(tag=hashtag)
		return render(request, 'hashtags/tag_view.html', {"obj": obj})

