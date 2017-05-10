from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (DetailView,
									 ListView,
 									CreateView,
  										UpdateView,
  										DeleteView
  										)
from .models import Tweet
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django import forms
from django.forms.utils import ErrorList
from .mixins import FormUserNeededMixin, UserOwnerMixin
from django.http import HttpResponseRedirect
from django.views import View
from .forms import TweetModelForm
# Create your views here.

#Create
class RetweetView(View):
	def get(self, request, pk, *args, **kwargs):
		tweet = get_object_or_404(Tweet, pk=pk)
		if request.user.is_authenticated():
			new_tweet = Tweet.objects.retweet(request.user,tweet)
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(tweet.get_absolute_url())

class TweetCreateView(FormUserNeededMixin,CreateView):
	#queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = 'tweets/create_view.html'
	#success_url = reverse_lazy("tweet:detail")

	#login_url = '/admin/'
	#fields = ['user','content']

class TweetUpdateView(LoginRequiredMixin,UserOwnerMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = 'tweets/update_view.html'
	#success_url = "/tweet/"

	# def form_valid(self, form):
	# 	if self.request.user.is_authenticated():
	# 		form.instance.user = self.request.user
	# 		return super(TweetCreateView, self).form_valid(form)
	# 	else:
	# 		form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue."])
	# 		return self.form_invalid(form)

# def tweet_create_view(request):
# 	form = TweetModelForm(request.POST or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.user = request.user
# 		instance.save()
# 		context = {
# 			"form":form
# 		}
# 		return render(request, 'tweets/create_view.html',context)

#Retrieve

#Update

#Delete
class TweetDeleteView(DeleteView):
	model = Tweet
	success_url = reverse_lazy("tweet:list") #/tweet/
	template_name = 'tweets/delete_confirm.html'

#List/Search

#Retrieve

class TweetDetailView(DetailView):
	#template_name = "tweets/detail_view.html"
	queryset = Tweet.objects.all()

	# def get_object(self):
	# 	print(self.kwargs)
	# 	pk = self.kwargs.get("pk")
	# 	print(pk)
	# 	return Tweet.objects.get(id=pk)

class TweetListView(ListView):
	#template_name = "tweets/tweet_list.html"
	#queryset = Tweet.objects.all()
	def get_queryset(self,*args,**kwargs):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q",None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
		return qs

	def get_context_data(self, *args, **kwargs):
	 	context = super(TweetListView,self).get_context_data(*args, **kwargs)
	 	context['create_form'] = TweetModelForm()
	 	context['create_url'] = reverse_lazy("tweet:create")
	 	return context






# def tweet_detail_view(request, id=1):
# 	obj = Tweet.objects.get(id=id) # GET from database
# 	print(obj)
# 	context = {
# 		"object": obj
# 	}
# 	return render(request, "tweets/detail_view.html", context)

# def tweet_list_view(request):
# 	queryset = Tweet.objects.all()
# 	print(queryset)
# 	for obj in queryset:
# 		print (obj.content)
# 	context = {
# 		"object_list": queryset
# 	}
# 	return render(request, "tweets/detail_view.html", context)