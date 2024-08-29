from django.shortcuts import render, get_object_or_404
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
    reviews = Review.objects.filter(user=request.user)

    purchased_items = OrderLineItem.objects.filter(order__customer=request.user.customer)
    unreviewed_items = purchased_items.exclude(id__in=reviews.values('order_line_item_id'))

    template = "review/account/reviews.html"
    context = {
        'active': 'reviews',
        'reviews': reviews,
        'unreviewed_items': unreviewed_items
    }
    return render(request, template, context)


@login_required
def account_review_submit_view(
    request, 
    line_item_id
    ):
    
    line_item = get_object_or_404(OrderLineItem, id=line_item_id)
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



