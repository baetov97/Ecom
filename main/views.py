from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.base import View
from .forms import *
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt


class HomeView(TemplateView):
    template_name = 'main/store.html'

    def get(self, request, *args, **kwargs):
        data = cartData(request)
        cartItems = data['cartItems']

        products = Product.objects.all()
        print(products)
        context = {'products': products, 'cartItems': cartItems}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class CartView(TemplateView):
    template_name = 'main/cart.html'

    def get(self, request, *args, **kwargs):
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class CheckoutView(TemplateView):
    template_name = 'main/checkout.html'

    def get(self, request, *args, **kwargs):
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class UpdateItemView(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)

        customer = request.user
        product = Product.objects.get(id=productId)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()
        if action == 'delete':
            orderItem.delete()
        return JsonResponse('Item was added', safe=False)


class ProcessOrder(View):

    def post(self, request, *args, **kwargs):
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

        else:
            customer, order = guestOrder(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

        return JsonResponse('Payment complete', safe=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'
    context_object_name = 'product'
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = ReviewForm()
        return context


class SearchResultView(ListView):
    model = Product
    template_name = 'main/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(Q(name__icontains=query))
        return object_list


class AddReview(View):

    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        context = {'form': form}
        return render(request, 'main/product_detail.html', context)

    def post(self, request, pk):
        customer = request.user
        product = Product.objects.get(id=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = customer
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


#####################TESTING
def profile(request):
    data = {
        'name': 'Nurgazy',
        'location': 'Kyrgyzstan',
        'is_active': True,
        'count': 28
    }
    return JsonResponse(data)
