from builtins import sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MedicineForm, SaleForm, BillForm, CustomerForm, CustomerCreationForm, CartForm, OrderForm, CheckoutForm
from .models import Pharmacist, Medicine, Total_Customers, Cart, Sale, Bill, Order


# Create your views here.

@login_required
def index(request):
    return render(request, 'pharma/index.html')


@login_required
def pharmacist_index(request):
    return render(request, 'pharma/pharmacist_index.html')

@login_required
def Pharmacist(request,):
    return render(request, 'pharma/pharmacist.html', {'pharmacist': Pharmacist})


@login_required
def Total_Sale(request):
    sales = Total_Sale.objects.all()
    context = {'sales':sales}
    return render(request, 'pharma/sale.html', context)


def make_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.total_amount = sale.medicine.sell_price * sale.quantity
            sale.save()
            return redirect('pharma-make_payment', sale_id=sale.pk)
    else:
        form = SaleForm()
    return render(request, 'make_sale.html', {'form': form})

def make_payment(request, sale_id):
    sale = Sale.objects.get(pk=sale_id)
    return render(request, 'pharma/make_payment.html', {'sale': sale})


@login_required
def Total_Customers_view(request):
    customers = Total_Customers.objects.all()
    context = {'customers': customers}
    return render(request, 'pharma/customer.html', context)


@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pharma-index')
    else:
        form = CustomerCreationForm()

    return render(request, 'pharma/create_customer.html', {'form': form})

@login_required
def update_customer(request, customer_id):
    customer = Total_Customers.objects.get(id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('pharma-customer')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'pharma/update_customer.html', {'form': form, 'customer': customer})

@login_required
def delete_customer(request, customer_id):
    customer = Total_Customers.objects.get(Total_Customers, id=customer_id)

    if request.method == 'POST':
        customer.delete()
        return redirect('pharma-customer')

    return render(request, 'pharma/delete_customer.html', {'customer': customer})

@login_required
def Drugs_Out_of_Stock(request):
    return render(request, 'pharma/drugs_out.html')


@login_required
def Total_Profit(request):
    return render(request, 'pharma/profit.html')


@login_required
def stock_table(request):
    medicine = Medicine.objects.all()
    return render(request, 'pharma/stock_table.html', {'medicine':medicine})


@login_required
def Drugs_Added(request):
    return render(request, 'pharma/drugs_added.html')


@login_required
def Medicine_view(request):
    medicines = Medicine.objects.all()
    context = {'medicines': medicines}
    return render(request, 'pharma/medicine.html', context)

@login_required
def medicine_list(request):
    items = Medicine.objects.all()

    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pharma-medicine_list')
    else:
        form = MedicineForm()
    context = {
        'items': items,
        'form': form

    }
    return render(request, 'pharma/medicine_list.html', context)

@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pharma-medicine')
    else:
        form = MedicineForm()
    return render(request, 'pharma/add_medicine.html', {'form': form})


@login_required
def edit_medicine(request, pk):
    item = Medicine.objects.get(id=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('pharma-medicine_list')
    else:
        form = MedicineForm()
    context = {
        'form': form,
        'item': item,

    }
    return render(request, 'pharma/edit_medicine.html', context)


@login_required
def delete_medicine(request, pk):
    item = Medicine.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('pharma-medicine_list')
    context = {
        'item': item
    }

    return render(request, 'pharma/delete_medicine.html', context)


@login_required
def profile_view(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'pharma-pharmacist_index', context)


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'pharma/cart.html', {'cart_items': cart_items})


@login_required
def add_to_cart(request, medicine_id):
     medicines = Medicine.objects.all()
     cart = Cart.objects.filter(user=request.user)
     cart_total = sum(item.subtotal for item in cart)
     context = {
         'medicines': medicines,
         'cart': cart,
         'cart_total': cart_total,

     }
     if request.method == 'POST':
      form = CartForm(request.POST)
     if form.is_valid():
        cart = form.save(commit=False)
        cart.user = request.user
        cart.save()
        return redirect('pharma-cart')
     else:
       form = CartForm()

     return render(request, 'add_to_cart.html', context)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    if request.method == 'POST':
        cart_item.delete()
        return redirect('pharma-cart')

    return render(request, 'pharma/remove_from_cart.html', {'cart_item': cart_item})



@login_required
def bill(request):
    bills = Bill.objects.all()
    return render(request, 'pharma-bill.html', {'bills': bills})


@login_required
def add_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.total_amount = calculate_total_amount(form.cleaned_data['medicines'])
            bill.save()
            form.save_m2m()  # Save many-to-many relationship
            return redirect('pharma-bill_detail', bill_id=bill.pk)
    else:
        form = BillForm()
    return render(request, 'add_bill.html', {'form': form})


@login_required
def bill_detail(request, bill_id):
    bill = Bill.objects.get(pk=bill_id)
    return render(request, 'pharma/bill_detail.html', {'bill': bill})


@login_required
def calculate_total_amount(medicines):
    total_amount = 0
    for medicine in medicines:
        total_amount += medicine.sell_price
    return total_amount


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'pharma/order.html', {'orders': orders})


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pharma-order_list')
    else:
        form = OrderForm()
    return render(request, 'pharma/create_order.html', {'form': form})


@login_required
def process_checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            # Perform any additional validation or processing as needed
            # Save the sale details to the database
            sale = form.save()
            # Perform any further actions (e.g., sending confirmation email, updating stock, etc.)
            # Redirect to a success page or any other desired page
            return redirect('checkout-success')
    else:
        form = CheckoutForm()

    return render(request, 'pharma/process_checkout.html', {'form': form})


def calculate_order(request):
    if request.method == 'POST':
        form = OrderForm
        pharmacist_id = request.POST.get('pharmacist_id')
        order_ids = request.POST.getlist('order_ids')

        total_selling_price = 0
        for order_id in order_ids:
            try:
                order = Order.objects.get(id=order_id, pharmacist_id=pharmacist_id)
                total_selling_price += order.medicine.selling_price * order.quantity
            except Order.DoesNotExist:
                pass

        context = {
            'total_selling_price': total_selling_price
        }

        return render(request, 'pharma/price.html', context)
    form= OrderForm
    return render(request, 'pharma/price.html', {'form':form})