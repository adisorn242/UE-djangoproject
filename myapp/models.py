from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# หมวดหมู่สินค้า เช่น "อุปกรณ์คอมพิวเตอร์", "เครื่องเขียน" ฯลฯ
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")

    class Meta:
        verbose_name = "หมวดหมู่"
        verbose_name_plural = "หมวดหมู่"

    def __str__(self):
        # ใช้แสดงชื่อหมวดหมู่ในหน้าแอดมิน แทนที่จะโชว์ "Category object (1)"
        return self.name


# สินค้าที่ขายในร้าน แต่ละชิ้นมีชื่อ รายละเอียด รูปภาพ ราคา และจำนวนคงเหลือ
class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="ชื่อสินค้า")
    detail = models.TextField(null=True, blank=True, verbose_name="รายละเอียด")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="รูปภาพ")
    others = models.TextField(null=True, blank=True, verbose_name="อื่นๆ")

    # เชื่อมสินค้าเข้ากับหมวดหมู่ (1 สินค้า อยู่ได้ 1 หมวดหมู่) ถ้าหมวดหมู่ถูกลบ สินค้าที่อยู่ในหมวดนั้นจะถูกลบตามไปด้วย (CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name="หมวดหมู่"
    )
    # ราคาสินค้า เก็บเป็นทศนิยม 2 ตำแหน่ง (เช่น 199.00)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True, verbose_name="ราคา"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="จำนวนคงเหลือ")  # จำนวนสินค้าคงเหลือในสต็อก (ต้องเป็นเลขบวกเท่านั้น)
    unit = models.CharField(max_length=50, default="ชิ้น", verbose_name="หน่วย")  # หน่วยนับสินค้า เช่น ชิ้น, กล่อง, แพ็ค
    is_available = models.BooleanField(default=True, verbose_name="พร้อมขาย")  # สถานมีโร่อมขายอยู่หรือไม่
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="วันที่สร้าง")  # บันทึกวันเวลาที่สร้างสินค้าโดยอัตโนมัติ (ตั้งครั้งเดียวตอนสร้าง)

    def __str__(self):
        # ใช้แสดงชื่อสินค้าในหน้าแอดมิน แทนที่จะโชว์ "Product object (1)"
        return self.title


# ข้อมูลโปรไฟล์ส่วนตัวของผู้ใช้แต่ละคน เป็นส่วนขยายของ User มาตรฐานของ Django
class Profile(models.Model):
    # ผูกโปรไฟล์นี้กับ User แบบ 1 ต่อ 1 (คนหนึ่งมีโปรไฟล์เดียว) ถ้า User ถูกลบ โปรไฟล์นี้จะถูกลบตามไปด้วย
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255, blank=True)  # ชื่อเต็มของผู้ใช้ (ไม่บังคับกรอก)
    avatar = models.ImageField(upload_to='avatars/', default='default.png')  # รูปโปรไฟล์ ถ้าไม่อัปโหลดจะใช้รูป default.png
    bio = models.TextField(max_length=500, blank=True)  # ประวัติย่อ/แนะนำตัว ยาวได้ไม่เกิน 500 ตัวอักษร
    website = models.URLField(max_length=200, blank=True)  # ลิงก์เว็บไซต์ส่วนตัวของผู้ใช้ (ไม่บังคับกรอก)

    def __str__(self):
        # ใช้แสดงในหน้าแอดมินเป็น "ชื่อผู้ใช้ Profile" จะได้รู้ว่าโปรไฟล์นี้เป็นของใคร
        return f'{self.user.username} - {self.fullname} Profile'

# ตัวดักจับเหตุการณ์ (signal): ทำงานทุกครั้งที่มีการบันทึกข้อมูล User ลงฐานข้อมูล
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # created=True หมายถึงเพิ่งสร้าง User ใหม่ (เช่น เพิ่งสมัครสมาชิก) -> สร้าง Profile เปล่าให้ทันทีแบบอัตโนมัติ
    if created:
        Profile.objects.create(user=instance)

# ตัวดักจับเหตุการณ์อีกตัว: ทำงานทุกครั้งที่ข้อมูล User ถูกบันทึก (ทั้งสร้างใหม่และแก้ไข)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # บันทึก Profile ของ User คนนั้นซ้ำอีกที เพื่อให้ข้อมูลของ User และ Profile sync กันเสมอ
    instance.profile.save()
