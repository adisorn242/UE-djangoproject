from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, Category
from .forms import UserRegisterForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

def Home(request):
    # หน้าแรกของเว็บไซต์ แค่ render template home.html เฉยๆ ไม่มีข้อมูลจากฐานข้อมูล
    return render(request, 'home.html')

def About(request):
    # หน้าเกี่ยวกับเรา แค่ render template about.html เฉยๆ เหมือนกัน
    return render(request, 'about.html')

def AllProducts(request):
    # ดึงสินค้าทั้งหมด พร้อม category ในคิวรีเดียว (select_related กัน query ซ้ำซ้อน)
    products = Product.objects.select_related('category').all()
    # ดึงหมวดหมู่ทั้งหมดมาไว้สร้างปุ่ม filter แบบไดนามิก (ไม่ hardcode เหมือนไฟล์ static เดิม)
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    # ส่งข้อมูลสินค้าและหมวดหมู่ไปแสดงผลที่หน้า allproducts.html
    return render(request, 'allproducts.html', context)

def ProductDetail(request, id):
    # ดึงสินค้าตา id ที่ส่งมาจาก URL ถ้าไม่เจอจะขึ้นหน้า 404 ให้อัตโนมัติ (get_object_or_404)
    product = get_object_or_404(Product, id=id)
    context = {'product': product}
    # ส่งข้อมูลสินค้าชิ้นนั้นไปแสดงผลที่หน้า product_detail.html
    return render(request, 'product_detail.html', context)

def register(request):
    # ถ้าเป็นการส่งฟอร์ม (POST) ให้เอาข้อมูลที่กรอกมาสร้างฟอร์ม
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # ตรวจสอบว่าข้อมูลที่กรอกถูกต้องไหม (username ซ้ำ, รหัสผ่านตรงกันไหม ฯลฯ)
        if form.is_valid():
            form.save()  # บันทึก User ใหม่ลงฐานข้อมูล (Profile จะถูกสร้างอัตโนมัติผ่าน signal ใน models.py)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')  # แจ้งเตือนสมัครสำเร็จ
            return redirect('login')  # เสร็จแล้วพาไปหน้า login
    else:
        # ถ้าเป็นการเปิดหน้าครั้งแรก (GET) ให้แสดงฟอร์มเปล่าๆ
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



def login(request):
    # ถ้าเป็นการส่งฟอร์ม (POST) ให้ตรวจสอบ username/password ที่กรอกมา
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # ดึงข้อมูลผู้ใช้ที่ผ่านการตรวจสอบแล้ว
            auth_login(request, user)  # สั่ง login จริง (สร้าง session ให้ผู้ใช้)
            return redirect('home')  # login สำเร็จ พาไปหน้าแรก
    else:
        # เปิดหน้าครั้งแรก (GET) ให้แสดงฟอร์มเปล่าๆ
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    # สั่งออกจากระบบ (ลบ session ผู้ใช้) แล้วพากลับไปหน้าแรก
    auth_logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required

@login_required  # ถ้ายังไม่ได้ login จะถูกเด้งไปหน้า login อัตโนมัติ เข้าหน้านี้ไม่ได้
def profile(request):
    # หน้าข้อมูลส่วนตัว เข้าถึงได้เฉพาะคนที่ login แล้วเท่านั้น
    return render(request, 'profile.html')
