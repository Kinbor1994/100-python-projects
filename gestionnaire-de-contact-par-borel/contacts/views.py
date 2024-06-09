from django.shortcuts import redirect, render
from api.crm import get_all_users,User

def home(request):
    
    context = {"users":get_all_users()}
    return render(request,'contacts/index.html',context=context)

def add_contact(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone_number = request.POST.get("phone_number")
    address = request.POST.get("address")
    user = User(first_name=first_name,last_name=last_name,phone_number=phone_number,address=address)
    user.save()
    return redirect('home')

def delete_contact(request,id):
    user_dic = User.DB.get(doc_id=id)
    user = User(user_dic['first_name'],user_dic['last_name'])
    user.delete()
    return redirect('home')

# def update_contact(request,id):
#     user_dic = User.DB.get(doc_id=id)
#     first_name = request.POST.get("first_name")
#     last_name = request.POST.get("last_name")
#     phone_number = request.POST.get("phone_number")
#     address = request.POST.get("address")