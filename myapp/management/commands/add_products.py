import urllib.request
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from myapp.models import Product

class Command(BaseCommand):
    help = 'เพิ่มข้อมูลสินค้าตัวอย่างและรูปภาพลงในฐานข้อมูล'

    def handle(self, *args, **kwargs):
        products = [
            {
                'title': 'Mechanical Keyboard',
                'detail': 'คีย์บอร์ดกลไกสำหรับโปรแกรมเมอร์ พิมพ์สนุก เสียงเพราะ',
                'others': 'สวิตช์แบบ Blue Switch',
                'image_url': 'https://picsum.photos/seed/keyboard/800/600',
                'filename': 'keyboard.jpg'
            },
            {
                'title': 'Ergonomic Mouse',
                'detail': 'เมาส์เพื่อสุขภาพ จับถนัดมือ ลดอาการปวดข้อมือ',
                'others': 'เชื่อมต่อผ่าน Bluetooth และ Wireless',
                'image_url': 'https://picsum.photos/seed/mouse/800/600',
                'filename': 'mouse.jpg'
            },
            {
                'title': 'Monitor 27 inch 4K',
                'detail': 'หน้าจอความละเอียดสูง 4K สีสันคมชัด เหมาะสำหรับเขียนโค้ดและดูหนัง',
                'others': 'รองรับ USB-C',
                'image_url': 'https://picsum.photos/seed/monitor/800/600',
                'filename': 'monitor.jpg'
            }
        ]

        for p in products:
            product, created = Product.objects.get_or_create(
                title=p['title'],
                defaults={
                    'detail': p['detail'],
                    'others': p['others']
                }
            )
            
            # ดาวน์โหลดและบันทึกรูปภาพ
            if not product.image:
                self.stdout.write(f"กำลังดาวน์โหลดรูปภาพสำหรับ {product.title}...")
                try:
                    req = urllib.request.Request(p['image_url'], headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        if response.status == 200:
                            product.image.save(p['filename'], ContentFile(response.read()), save=True)
                            self.stdout.write(self.style.SUCCESS(f"📸 เพิ่มรูปภาพสำหรับ: {product.title} สำเร็จ!"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ ไม่สามารถดาวน์โหลดรูปภาพ {product.title} ได้: {e}"))

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ เพิ่มสินค้าใหม่: {product.title} เรียบร้อยแล้ว"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ สินค้า: {product.title} มีอยู่ในระบบแล้ว"))

        self.stdout.write(self.style.SUCCESS('🎉 ทำงานเสร็จสิ้น!'))
