# FirstWeb Django Project - Products & Media Guide

โปรเจคนี้เป็นการเรียนรู้การสร้างเว็บไซต์ด้วย Django โดยมีตัวอย่างการสร้างระบบแสดงข้อมูลสินค้า (Products) และการตั้งค่าระบบอัปโหลดและแสดงผลรูปภาพ (Media Files) แบบสมบูรณ์

---

## 📦 1. Product Model (โครงสร้างข้อมูลสินค้า)

`Product` เป็น Model ที่ใช้สำหรับจัดเก็บข้อมูลสินค้า ประกอบไปด้วย 4 ฟิลด์หลัก ถูกสร้างไว้ในไฟล์ `myapp/models.py`

### โครงสร้าง Model
```python
class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="ชื่อสินค้า")
    detail = models.TextField(null=True, blank=True, verbose_name="รายละเอียด")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="รูปภาพ")
    others = models.TextField(null=True, blank=True, verbose_name="อื่นๆ")

    def __str__(self):
        return self.title
```

**คำอธิบายฟิลด์:**
1. **`title`**: (CharField) ใช้สำหรับเก็บชื่อสินค้า ความยาวสูงสุด 255 ตัวอักษร
2. **`detail`**: (TextField) รายละเอียดของสินค้า ใช้เก็บข้อความยาวๆ สามารถเว้นว่างได้ (`null=True, blank=True`)
3. **`image`**: (ImageField) ใช้สำหรับอัปโหลดรูปภาพสินค้า โดยรูปภาพจะถูกนำไปเก็บไว้ในโฟลเดอร์ที่กำหนดใน `upload_to='products/'` (ซึ่งจะไปต่อท้าย `MEDIA_ROOT` อีกที)
4. **`others`**: (TextField) ข้อมูลอื่นๆ เพิ่มเติมเกี่ยวกับสินค้า

### การแสดงผลบนหน้าเว็บ
ระบบสินค้าแบ่งการแสดงผลออกเป็น 2 หน้าหลัก ดังนี้:

#### 1. หน้าสินค้าทั้งหมด (All Products)
- **View:** `AllProducts(request)` ใน `myapp/views.py` ทำการดึงข้อมูลด้วย `Product.objects.all()`
- **URL:** เข้าถึงผ่าน `/products` ตามที่กำหนดใน `myapp/urls.py`
- **Template:** `myapp/templates/allproducts.html` มีการเขียน loop แสดงสินค้าและมีลิงก์สำหรับกดไปยังหน้า Detail

#### 2. หน้ารายละเอียดสินค้า (Product Detail)
- **View:** `ProductDetail(request, id)` ใน `myapp/views.py` ทำการดึงข้อมูลรายตัวผ่าน ID ด้วยฟังก์ชัน `get_object_or_404`
- **URL:** เข้าถึงผ่าน `/products/<int:id>/` เช่น `/products/1/`
- **Template:** `myapp/templates/product_detail.html` แสดงรูปภาพขนาดใหญ่และรายละเอียดของสินค้านั้นๆ อย่างครบถ้วน

---

## 🖼️ 2. การตั้งค่า Media Files (รูปภาพและไฟล์อัปโหลด)

เพื่อให้ Django สามารถจัดการไฟล์ที่ผู้ใช้อัปโหลด (เช่น รูปภาพสินค้า) เราจำเป็นต้องมีการตั้งค่า **Media** ในส่วนต่างๆ อย่างละเอียด ดังนี้ครับ:

### ขั้นตอนที่ 1: ตั้งค่าใน `firstweb/settings.py`
จำเป็นต้องกำหนดตำแหน่งที่จะใช้เก็บไฟล์ (บนเซิร์ฟเวอร์) และ URL ที่จะใช้อ้างอิงถึงไฟล์เหล่านั้น

```python
import os

# MEDIA_ROOT คือ Path ในเครื่องคอมพิวเตอร์ หรือ Server ที่จะเก็บไฟล์จริงๆ
# ในที่นี้คือจะสร้างโฟลเดอร์ชื่อ 'media' ไว้ที่ root ของโปรเจค (ระดับเดียวกับ manage.py)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# MEDIA_URL คือ URL พื้นฐานที่เราจะใช้เข้าถึงไฟล์ผ่าน Browser 
# เช่น หากมีไฟล์ชื่อ test.png มันจะเข้าถึงได้ผ่าน http://localhost:8000/media/test.png
MEDIA_URL = '/media/'
```

### ขั้นตอนที่ 2: ตั้งค่า Routing ใน `firstweb/urls.py` (ไฟล์ urls หลักของโปรเจค)
เพื่อให้ Development Server ของ Django ทราบว่าเมื่อมีผู้ใช้ Request เข้ามาที่ URL ซึ่งขึ้นต้นด้วย `/media/` จะต้องไปดึงไฟล์จากที่ไหนมาแสดงผล ต้องเพิ่มโค้ดด้านล่างนี้:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

# เป็นการบวก path สำหรับ Media Files เข้าไป 
# (หมายเหตุ: การทำแบบนี้แนะนำให้ใช้เฉพาะตอน Development (DEBUG=True) เท่านั้น)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### ขั้นตอนที่ 3: ติดตั้งไลบรารีที่จำเป็น
สำหรับการใช้ `ImageField` ใน Django คุณจำเป็นต้องติดตั้งไลบรารีชื่อ **Pillow** เพื่อจัดการรูปภาพ หากยังไม่ได้ติดตั้ง สามารถติดตั้งได้ผ่าน Terminal:
```bash
pip install Pillow
```

---

## 🚀 3. คำสั่งพิเศษ (Custom Management Command)

เราได้เตรียมคำสั่งพิเศษสำหรับอำนวยความสะดวกในการเพิ่มข้อมูลสินค้าตัวอย่างเข้าฐานข้อมูลโดยไม่ต้องเข้าหน้า Admin หรือ Python Shell

**วิธีใช้งาน:**
เปิด Terminal ขึ้นมาและพิมพ์คำสั่ง:
```bash
python manage.py add_products
```
โค้ดนี้จะไปรันไฟล์คำสั่งที่เราเขียนไว้ใน `myapp/management/commands/add_products.py` ซึ่งมีความสามารถดังนี้:
1. ทำการใส่ข้อมูลสินค้า 3 รายการเข้าไปในฐานข้อมูลอัตโนมัติ (Data Seeding)
2. **ทำการดาวน์โหลดรูปภาพ** จากอินเทอร์เน็ต (เช่น Picsum Photos) แล้วนำมาบันทึกเป็นไฟล์ลงในโฟลเดอร์ `media/products/`
3. ผูกรูปภาพที่ดาวน์โหลดมาเข้ากับโมเดลสินค้าให้พร้อมใช้งานทันที
