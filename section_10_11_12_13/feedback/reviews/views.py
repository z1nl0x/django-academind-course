from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ReviewForm
from .models import Review

from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView

from django.views import View

# Create your views here.

# class ReviewView(View):
#     def get(self, requests):
#         form = ReviewForm()

#         return render(requests, "reviews/review.html", {
#             "form": form
#         })

#     def post(self, requests):
#         form = ReviewForm(requests.POST)
        
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/thank-you")
        
#         return render(requests, "reviews/review.html", {
#             "form": form
#         })
    
class ReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"


    # def form_valid(self, form):

    #     form.save()

    #     return super().form_valid(form)

    # def get(self, requests):
    #     form = ReviewForm()

    #     return render(requests, "reviews/review.html", {
    #         "form": form
    #     })

    # def post(self, requests):
    #     form = ReviewForm(requests.POST)
        
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect("/thank-you")
        
    #     return render(requests, "reviews/review.html", {
    #         "form": form
    #     })


class ThankYouView(TemplateView):

    template_name = "reviews/thank_you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "This Works!"

        return context

    # def get(self, requests):
    #     return render(requests, "reviews/thank_you.html")


# class ReviewsListView(TemplateView):
#     template_name = "reviews/review_list.html"

#     def get_context_data(self, **kwargs: Any):
#         context = super().get_context_data(**kwargs)
#         reviews = Review.objects.all()
#         context["reviews"] = reviews
#         return context
    
class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    model = Review
    context_object_name = "reviews"

    # def get_queryset(self):
    #     base_query = super().get_queryset()
    #     data = base_query.filter(rating__gt=4)
    #     return data

# class SingleReviewView(TemplateView):
#     template_name = "reviews/single_review.html"

#     def get_context_data(self, **kwargs: Any):
#         context = super().get_context_data(**kwargs)
#         review_id = kwargs["id"]
#         selected_review = Review.objects.get(pk=review_id)
#         context["review"] = selected_review
#         return context

class SingleReviewView(DetailView):
    template_name = "reviews/single_review.html"
    model = Review

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favorite_id = request.session.get("favorite_review")
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context
    

# def review(requests):

#     if requests.method == "POST":
#         # entered_username = requests.POST["username"]

#         # if entered_username == "" and len(entered_username) >= 100:
#         #     return render(requests, "reviews/review.html", {
#         #         "has_error": True 
#         #     })

#         # print(entered_username)
#         # existing_data = Review.objects.get(pk=1)
#         # form = ReviewForm(requests.POST, instance=existing_data)

#         form = ReviewForm(requests.POST)
        
#         if form.is_valid():
#             # review = Review(user_name=form.cleaned_data['user_name'], review_text=form.cleaned_data['review_text'], rating=form.cleaned_data['rating'])
#             # review.save()
#             form.save()
#             return HttpResponseRedirect("/thank-you")
#     else:
#         form = ReviewForm()

#     return render(requests, "reviews/review.html", {
#         "form": form
#     })


# def thank_you(requests):
#     return render(requests, "reviews/thank_you.html")


class AddFavoriteView(View):

    def post(self, request):
        review_id = request.POST["review_id"]
        # fav_review = Review.objects.get(pk=review_id)
        request.session["favorite_review"] = review_id

        return HttpResponseRedirect("/reviews/" + review_id)
