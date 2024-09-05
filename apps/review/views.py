from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from apps.product.models import Product
from apps.order.models import OrderLineItem
from apps.common.decorators import superuser_required

from .models import Review
from .forms import ReviewForm, ReviewStatusForm


@login_required
@superuser_required
def cms_reviews_view(request):
    reviews = Review.objects.all()
    status = None

    if request.GET.get('status'):
        status = request.GET.get('status')
        reviews = reviews.filter(status=status)


    template = "review/cms/reviews.html"
    context = {
        'active': 'reviews',
        'reviews': reviews,
        'status': status
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_review_update_view(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':
        if 'update_status' in request.POST:
            status_form = ReviewStatusForm(request.POST, instance=review)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Review status updated successfully.')
                return redirect('cms_reviews')
    else:
        status_form = ReviewStatusForm(instance=review)

    template = "review/cms/review_update.html"
    context = {
        'active': 'reviews',
        'review': review,
        'status_form': status_form
    }
    return render(request, template, context)


@login_required
def account_reviews_view(request):
    user_reviews = Review.objects.filter(user=request.user)
    purchased = OrderLineItem.objects.filter(order__customer=request.user.customer)
    reviews_filter = request.GET.get('reviews_filter', 'not-reviewed')
    
    if reviews_filter == 'not-reviewed':
        reviews = purchased.exclude(id__in=user_reviews.values('order_line_item_id'))
    elif reviews_filter == 'approved':
        reviews = user_reviews.filter(status='approved')
    elif reviews_filter == 'pending':
        reviews = user_reviews.filter(status='pending')
    elif reviews_filter == 'rejected':
        reviews = user_reviews.filter(status='rejected')

    template = "review/account/reviews.html"
    context = {
        'active': 'reviews',
        'reviews': reviews,
        'reviews_filter': reviews_filter
    }
    return render(request, template, context)


@login_required
def account_review_submit_view(
    request, 
    id
    ):
    
    line_item = get_object_or_404(OrderLineItem, id=id)
    product = line_item.product
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)    
        if form.is_valid():
            review = form.save(commit=False)

            review.user = request.user
            review.product = product
            review.order_line_item = line_item
            
            review.save()
            messages.success(request, 'Review submitted successfully.')
            return redirect('account_reviews')
    else:
        form = ReviewForm()

    template = "review/account/review_submit.html"
    context = {
        'active': 'reviews',
        'line_item': line_item,
        'product': product,
        'form': form
    }
    return render(request, template, context)


@login_required
def account_review_update_view(request, id):
    review = get_object_or_404(Review, id=id, user=request.user)
    product = review.product
    
    actual_text = review.text
    actual_rating = review.rating

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        
        if form.is_valid():
            new_text = form.cleaned_data['text']
            new_rating = form.cleaned_data['rating']
            
            if review.status == 'rejected':
                if new_text == actual_text:
                    messages.error(request, 'You must provide a new text that is different from the previous one to resubmit the review.')
                else:
                    review.text = new_text
                    review.status = 'pending'
                    review.rating = new_rating
                    review.save()
                    messages.success(request, 'Your review has been resubmitted and is now pending approval.')
                    return redirect('account_reviews')

            else:
                if new_text != review.text:
                    review.text = new_text
                    review.status = 'pending'
                    messages.success(request, 'Your review has been updated and is now pending approval for the text change.')
                else:
                    review.rating = new_rating
                    messages.success(request, 'Your review rating has been updated.')
                review.save()
                return redirect('account_reviews')
                
    else:
        form = ReviewForm(instance=review)

    template = "review/account/review_update.html"
    context = {
        'active': 'reviews',
        'review': review,
        'form': form,
        'product': product,
    }
    return render(request, template, context)