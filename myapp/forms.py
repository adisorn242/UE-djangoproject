# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ฟอร์มสมัครสมาชิก สืบทอด (inherit) มาจาก UserCreationForm ของ Django
# ทำให้ได้ช่องกรอก username และรหัสผ่าน 2 ช่อง (ยืนยันรหัสผ่าน) พร้อมระบบตรวจสอบมาให้เลยโดยไม่ต้องเขียนเอง
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='อีเมล')  # เพิ่มช่องอีเมลเข้ามาเอง เพราะฟอร์มสมัครสมาชิกมาตรฐานของ Django ไม่มีช่องนี้ให้

    class Meta:
        model = User  # บอกว่าฟอร์มนี้ใช้จัดการข้อมูลของตาราง User (ตารางผู้ใช้มาตรฐานของ Django)
        fields = ['username', 'email']  # ระบุว่าจะแสดงช่องไหนบ้างในฟอร์ม และเรียงลำดับตามนี้ (รหัสผ่านมากับ UserCreationForm อยู่แล้วไม่ต้องระบุซ้ำ)
        labels = {
            # กำหนดข้อความกำกับช่องกรอกให้เป็นภาษาไทย แทนคำว่า "username"/"email" ที่ Django ใช้ default
            'username': 'ชื่อผู้ใช้งาน',
            'email': 'อีเมล',
        }
