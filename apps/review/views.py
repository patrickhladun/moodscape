from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from apps.product.models import Product
from apps.order.models import OrderLineItem
from apps.common.decorators import superuser_required
from apps.common.utils.metadata import make_metadata

from .models import Review
from .forms import ReviewForm, ReviewStatusForm


@login_required
@superuser_required
def cms_reviews_view(request):
    reviews = Review.objects.all()
    status = 'pending'

    metadata = make_metadata(
        request,
        {
            "title": "Reviews Management",
            "meta": {
                "description": "Manage and review customer feedback on products. This page allows administrators to oversee review statuses, edit content, or remove inappropriate reviews."
            }
        },
    )

    if request.GET.get('status'):
        status = request.GET.get('status')
        reviews = reviews.filter(status=status)
    reviews = reviews.filter(status=status)

    template = "review/cms/reviews.html"
    context = {
        'active': 'reviews',
        'metadata': metadata,
        'reviews': reviews,
        'status': status
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_review_update_view(request, id):
    review = get_object_or_404(Review, id=id)

    metadata = make_metadata(
    request,
        {
            "title": "Update Review",
            "meta": {
                "description": "Update the status of a product review. This page provides tools for administrators to approve, reject, or modify customer reviews to maintain quality and relevance on the platform."
            }
        },
    )

    if request.method == 'POST':
        if 'update_status' in request.POST:
            status_form = ReviewStatusForm(request.POST, instance=review)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Review status updated successfully.')
                return redirect('cms_reviews')
    else:
        status_form = ReviewStatusForm(instance=review)

        if review.status == 'pending':
            status_form.fields['status'].choices = [
                ('', 'Select Option'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected'),
                ('deleted', 'Deleted'),
            ]
        elif review.status == 'approved':
            status_form.fields['status'].choices = [
                ('', 'Select Option'),
                ('rejected', 'Rejected'),
                ('deleted', 'Deleted'),
            ]

        elif review.status == 'rejected':
            status_form.fields['status'].choices = [
                ('', 'Select Option'),
                ('approved', 'Approved'),
                ('deleted', 'Deleted'),
            ]

        elif review.status == 'deleted':
            status_form.fields['status'].choices = [
                ('', 'Select Option'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected'),
            ]

    template = "review/cms/review_update.html"
    context = {
        'active': 'reviews',
        'metadata': metadata,
        'review': review,
        'status_form': status_form
    }
    return render(request, template, context)


@login_required
def account_reviews_view(request):
    user = request.user
    customer = user.customer

    # Fetching all reviews made by the user
    user_reviews = Review.objects.filter(user=user)

    # Fetching all OrderLineItems associated with the user
    purchased_items = OrderLineItem.objects.filter(order__customer=customer)

    reviews_filter = request.GET.get('reviews_filter', 'not-reviewed')

    metadata = make_metadata(
        request,
        {
            "title": "Your Reviews",
            "meta": {
                "description": "Review your submitted product reviews."
            }
        },
    )
    
    if reviews_filter == 'not-reviewed':
        # List items that do not have a corresponding review yet
        reviewed_items = user_reviews.values('order_line_item_id')
        reviews = purchased_items.exclude(id__in=reviewed_items)
    elif reviews_filter == 'approved':
        reviews = user_reviews.filter(status='approved')
    elif reviews_filter == 'pending':
        reviews = user_reviews.filter(status='pending')
    elif reviews_filter == 'rejected':
        reviews = user_reviews.filter(status='rejected')

    template = "review/account/reviews.html"
    context = {
        'active': 'reviews',
        'metadata': metadata,
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
    
    metadata = make_metadata(
        request,
        {
            "title": "Review Details",
            "meta": {
                "description": "Edit or view details of your product review."
            }
        },
    )

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
        'metadata': metadata,
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