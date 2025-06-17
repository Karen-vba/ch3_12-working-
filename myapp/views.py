from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def search_list(request):
    if "cName" in request.GET:
        cName=request.GET["cName"]
        print(cName)
        result_list=students.objects.filter(cName__contains=cName)
    else:
        result_list=students.objects.all()
    
    error_message=""
    if not result_list:
        error_message="無此資料"
    

    #測試資料是否正確(開發人員使用)
    # for data in result_list:
    #     print(model_to_dict(data))


    # return HttpResponse("Hello")
    return render(request,"search_list.html",locals())

def index(request): 
    if "site_search" in request.GET:
        site_search=request.GET["site_search"]
        site_search=site_search.strip()  #去前後空白
        # print(site_search)
        #一個關鍵字,搜尋一個欄位
        # result_list=students.objects.filter(cName__contains=site_search)
        #一個關鍵字,搜尋多個欄位
        # result_list=students.objects.filter(
        #     Q(cName__contains=site_search)|
        #     Q(cEmail__contains=site_search)|
        #     Q(cBirthday__contains=site_search)|
        #     Q(cAddr__contains=site_search)|
        #     Q(cPhone__contains=site_search)
        # )
        #多個關鍵字,多個欄位
        keywords=site_search.split() #以空格切割
        print(keywords)
        # result_list=[]
        q_object=Q()
        for keyword in keywords:
            q_object.add(Q(cName__contains=keyword),Q.OR)
            q_object.add(Q(cEmail__contains=keyword),Q.OR)
            q_object.add(Q(cBirthday__contains=keyword),Q.OR)
            q_object.add(Q(cAddr__contains=keyword),Q.OR)
            q_object.add(Q(cPhone__contains=keyword),Q.OR)
        result_list=students.objects.filter(q_object)
    else:
        result_list=students.objects.all().order_by("cID")
    dataCount=len(result_list)
    status=True
    errormessage=""
    if not result_list:
        status=False
        errormessage="無此資料"
    
    paginator=Paginator(result_list,1)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number) #依據取得的page_number,得到對應的頁數的資料
    #page_obj包含該頁的資料的物件
    #page_obj.object_list該頁的資料
    #page_obj.has_next,page_obj.has_previous:是否有下一頁或上一頁
    #page_obj.next_page_number,page_obj.previous_page_number:上一頁,下一頁的頁碼
    #page_obj.number目前的頁碼
    #page_obj.paginator.num_pages:總頁數
    
    #分頁設定,每頁顯示3筆

    # print(dataCount)
    # return HttpResponse("Hello")
    return render(request,"index.html",locals())

def edit(request,id=None):    
    print(f"id={id}")
    if request.method == "POST":
        cName=request.POST["cName"]
        cSex=request.POST["cSex"]
        cBirthday=request.POST["cBirthday"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr},")
        #orm
        update=students.objects.get(cID=id)
        update.cName=cName
        update.cSex=cSex
        update.cBirthday=cBirthday
        update.cEmail=cEmail
        update.cPhone=cPhone
        update.cAddr=cAddr
        update.save()
        # return HttpResponse("Hello")
        return redirect("/index/")
    else:
        obj_data=students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        return render(request,"edit.html",locals())


