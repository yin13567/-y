from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from ticket.models import Station, TicketKind, TrainLine, TicketOrder
from userinfo import models
from .forms import UserForm, RegisterForm
import hashlib

from .models import User


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    if request.method == "POST":
        startplace = request.POST.get('startplace')
        endplace = request.POST.get('endplace')
        startime = request.POST.get('starttime')
        startplacenums = Station.objects.filter(name=startplace)
        endplacenums = Station.objects.filter(name=endplace)
        if len(startplacenums) == 0 or len(endplacenums) == 0:
            print("数据不存在")
            return render(request, 'userinfo/index.html')
        startplacenum = startplacenums[0].id
        endplacenum = endplacenums[0].id

        # , trainline__starttime = startime
        tickets = TicketKind.objects.filter(startplace=startplacenum, endplace=endplacenum,
                                            trainline__starttime__gt=startime)
        trainlinesid = []
        for item in tickets:
            trainlinesid.append(item.trainline_id)
        trainlinesid = list(set(trainlinesid))
        trainlines = []
        timelines = []
        for item in trainlinesid:
            trainlines.append(TrainLine.objects.filter(id=item, starttime__gt=startime)[0])
            timelines.append(TrainLine.objects.filter(id=item, starttime__gt=startime)[0].endtime -
                             TrainLine.objects.filter(id=item, starttime__gt=startime)[0].starttime)
        # print(trainlines[0][0].trainnum)
        trainlines = zip(trainlines, timelines)

        alltickets = {}
        for item in trainlinesid:
            alltickets[item] = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for item in tickets:
            if item.name == "商务座特等座":
                alltickets[item.trainline_id][0][0] = item.num
                alltickets[item.trainline_id][0][1] = item.price
            elif item.name == "一等座":
                alltickets[item.trainline_id][1][0] = item.num
                alltickets[item.trainline_id][1][1] = item.price
            elif item.name == "二等座二等包座":
                alltickets[item.trainline_id][2][0] = item.num
                alltickets[item.trainline_id][2][1] = item.price
            elif item.name == "高级软卧":
                alltickets[item.trainline_id][3][0] = item.num
                alltickets[item.trainline_id][3][1] = item.price
            elif item.name == "软卧一等卧":
                alltickets[item.trainline_id][4][0] = item.num
                alltickets[item.trainline_id][4][1] = item.price
            elif item.name == "动卧":
                alltickets[item.trainline_id][5][0] = item.num
                alltickets[item.trainline_id][5][1] = item.price
            elif item.name == "硬卧二等卧":
                alltickets[item.trainline_id][6][0] = item.num
                alltickets[item.trainline_id][6][1] = item.price
            elif item.name == "软座":
                alltickets[item.trainline_id][7][0] = item.num
                alltickets[item.trainline_id][7][1] = item.price
            elif item.name == "硬座":
                alltickets[item.trainline_id][8][0] = item.num
                alltickets[item.trainline_id][8][1] = item.price
            elif item.name == "无座":
                alltickets[item.trainline_id][9][0] = item.num
                alltickets[item.trainline_id][9][1] = item.price

        # print(alltickets)
        return render(request, 'userinfo/index.html', locals())
    print("欢迎访问")
    return render(request, 'userinfo/index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确"
            except:
                message = "用户名不存在!"
        return render(request, 'userinfo/login.html', locals())

    login_form = UserForm()
    return render(request, 'userinfo/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 如果登录之后注册无效，直接跳转
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            idnum = register_form.cleaned_data['idnum']
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            phonenum = register_form.cleaned_data['phonenum']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'userinfo/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'userinfo/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'userinfo/register.html', locals())
                same_id_user = models.User.objects.filter(idnum=idnum)
                if same_id_user:  # 身份证号唯一
                    message = '身份证号已经存在，请重新选择身份证！'
                    return render(request, 'userinfo/register.html', locals())
                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.idnum = idnum
                new_user.email = email
                new_user.phonenum = phonenum
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'userinfo/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def ajax(request):
    if "term" in request.GET:
        print(request.GET['term'])
        stationnames = Station.objects.filter(name__icontains=request.GET['term'])[:10];
        data = []
        for item in stationnames:
            data.append({"label": item.name, "value": item.name})
        return JsonResponse(data, safe=False)
    return HttpResponse()


def ticketorder(request, ticketkindid):
    ticketkindid = ticketkindid
    ticket = TicketKind.objects.filter(trainline_id=ticketkindid)

    return render(request, 'ticket/order.html', locals())


def ticketorderconf(request, ticketkindid):
    ticket = TicketKind.objects.filter(id=ticketkindid)[0]
    curuserid = request.session.get("user_id")
    # print(curuserid)
    user = User.objects.filter(id=curuserid)[0]
    request.session["ticketid"]=ticketkindid
    return render(request, 'ticket/orderinfo.html', locals())


def payandchoice(request,price,choice):
    price=price
    if choice=="0":
        return render(request, "ticket/weixin.html", locals())
    if choice=="1":
        return render(request, "ticket/zhifubao.html", locals())
    if choice=="2":
        return render(request, "ticket/yinhangka.html", locals())
    if choice=="3":
        return render(request, "ticket/xianjin.html", locals())


def payres(request,way,shouldpay,actpay):
    way=int(way)
    shouldpay=shouldpay
    actpay=actpay
    zhaoling=float(actpay)-float(shouldpay)
    userid=request.session.get("user_id")
    ticketid=request.session.get("ticketid")
    print(userid)
    print(ticketid)
    userticket=TicketOrder.objects.filter(userid=userid,ticketid=ticketid)
    if len(userticket)==0:
        newticketorder=TicketOrder.objects.create(userid_id=userid,ticketid_id=ticketid)
        newticketorder.save()
        newticket=TicketKind.objects.filter(id=ticketid)[0]
        newticket.num-=1
        newticket.save()
    else:
        return HttpResponse("您已经购买了该车的票，不可重复购买")

    if way<2:
        return render(request, "ticket/payres.html", locals())
    if way==2:
        cardnum=request.POST.get("cardnum")
        cardpasswd=request.POST.get("cardpasswd")
        paynum=request.POST.get("paypasswd")
        print("银行卡号是："+cardnum)
        print("银行卡密码是：" + cardpasswd)
        print("支付密码是：" + paynum)
        print("恭喜您验证成功！")
        return render(request, "ticket/payres.html", locals())
    if way==3:
        money=request.POST.get("money")
        print("您投入的现金是:"+money)
        zhaoling=float(money)-float(shouldpay)
        actpay=money
        return render(request, "ticket/payres.html", locals())
    return HttpResponse("异常")


def myorder(request):
    userid=request.session.get("user_id")
    tickets=TicketOrder.objects.filter(userid_id=userid)
    ticketids=[]
    ctimes=[]
    for item in tickets:
        ticketids.append(item.ticketid_id)
        ctimes.append(item.ctime)
    alltickets=[]
    for item in ticketids:
        alltickets.append(TicketKind.objects.filter(id=item)[0])
    allinfo=[]
    for item in alltickets:
        allinfo.append([0,0,0,0,0,0,0,0])
    for v,item in enumerate(alltickets):
        print(v)
        fromnum=item.startplace
        endnum=item.endplace
        name=item.name
        price=item.price
        trainlinestarttime=item.trainline.starttime
        trainlineendtime = item.trainline.endtime
        allinfo[v][0]=fromnum.name
        allinfo[v][1] = endnum.name
        allinfo[v][2] = name
        allinfo[v][3] = price
        allinfo[v][4] = trainlinestarttime
        allinfo[v][5] = trainlineendtime
        allinfo[v][6]=ctimes[v]
        allinfo[v][7] = ticketids[v]
    # print(allinfo)
    return render(request,"ticket/myorder.html",locals())


def refund(request,ticketid):
    userid=request.session.get("user_id")
    newticket = TicketKind.objects.filter(id=int(ticketid))[0]
    newticket.num +=1
    newticket.save()
    delticket=TicketOrder.objects.filter(userid_id=userid,ticketid_id=ticketid)
    delticket.delete()
    return render(request,"userinfo/index.html",locals())