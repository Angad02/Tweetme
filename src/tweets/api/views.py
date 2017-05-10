from rest_framework import generics
from django.db.models import Q
from tweets.models import Tweet
from rest_framework import permissions
from .pagination import StandardResultsPagination
from .serializers import TweetModelSerializer

class TweetCreateAPIView(generics.CreateAPIView):
	serializer_class = TweetModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
		


class TweetListAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsPagination


	def get_queryset(self,*args,**kwargs):
		requested_user = self.kwargs.get("username")
		if requested_user:
			#they_follow = self.request.user.profile.get_following()
			#qs1 = Tweet.objects.filter(user__in=im_following)
			qs = Tweet.objects.filter(user__username=requested_user).order_by("-timestamp")
			 #print(self.request.GET)
			#qs = Tweet.objects.all().order_by("-timestamp")
			query = self.request.GET.get("q",None)
			if query is not None:
				qs = qs.filter(
					Q(content__icontains=query) |
					Q(user__username__icontains=query)
					)
			return qs
		else:
			im_following = self.request.user.profile.get_following()
			qs1 = Tweet.objects.filter(user__in=im_following)
			qs2 = Tweet.objects.filter(user=self.request.user)
			qs = (qs1 | qs2).distinct().order_by("-timestamp") # combining two queries
			 #print(self.request.GET)
			#qs = Tweet.objects.all().order_by("-timestamp")
		query = self.request.GET.get("q",None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
		return qs


class SearchAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsPagination

	def get_queryset(self, *args,**kwargs):
		qs = Tweet.objects.all().order_by("-timestamp")
		return qs

