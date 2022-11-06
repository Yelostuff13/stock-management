# from enum import unique
# from pickletools import decimalnl_long

from django.db import models
from django.urls import reverse
from .models import *

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=255,unique=True) #slug=เป็นการตั้งชื่อเล่นให้ข้อมูลในโมเดล,controlข้อมูลที่จะเปลียนไปในproduct


    def __str__(self):
        return self.name

    #เปลี่ยนรูปแบบการแสดงผล เช่น เปลี่ยนในเรื่องภาษา เปลี่ยนลำดับข้อมูล เรียงตามตัวอักษร
    class Meta :
        ordering=('name',)
        verbose_name='หมวดหมู่สินค้า'
        verbose_name_plural="ข้อมูลประเภทสินค้า"

    def get_url(self):
        return reverse('Film_by_product',args=[self.slug])

class Film(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=255,unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    product=models.ForeignKey(Product,on_delete=models.CASCADE) #cascadeลบข้อมูลที่มีอ้างอิงความสัมพันธ์ทั้งหมด
    image=models.ImageField(upload_to="product",blank=True)
    stock=models.IntegerField()
    available=models.BooleanField(default=True) #เก็บสถานะเช่นชำรุด,สินค้ามีปัญหาก็จะไม่แสดงหน้าเว็บ
    created=models.DateTimeField(auto_now_add=True) #วันที่stockสินค้า
    updated=models.DateTimeField(auto_now=True) #เพิ่ม/แก้ไข/ปรับปรุงสินค้า



    def __str__(self):
        return self.name

    #เพิ่มคุณสมบัติให้ model
    class Meta :
        ordering=('name',)
        verbose_name='สินค้า'
        verbose_name_plural="ข้อมูลสินค้า"   

class Cart(models.Model):
    cart_id=models.CharField(max_length=255,blank=True) 
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
    class Meta:
        db_table='cart'
        ordering=('date_added',)
        verbose_name='ตะกร้าสินค้า'
        verbose_name_plural="ข้อมูลตะกร้าสินค้า"

class CartItem(models.Model):
    film=models.ForeignKey(Film,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField() #เก็บจำนวนสินค้าที่เพิ่มลงตะกร้า
    active=models.BooleanField(default=True) 

    class Meta:
        db_table='cartItem'
        verbose_name='รายการสินค้าในตะกร้า'
        verbose_name_plural="ข้อมูลรายการสินค้าในตะกร้า"
    
    def sub_total(self): #หาผลรวมราคาสิ้นค้าแต่ละชิ้น
        return self.film.price * self.quantity
    
    def __str__(self):
        # return self.film.name
        return self.film.name

class Order(models.Model):
    name=models.CharField(max_length=255,blank=True)
    address=models.CharField(max_length=255,blank=True)
    postcode=models.CharField(max_length=255,blank=True)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='Order'
        ordering=('id',)

    def __str__(self):
        return str(self.id)

   

class OrderItem(models.Model):
    Film=models.CharField(max_length=250)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='OrderItem'
        ordering=('order',)

    def sub_total(self):
        return self.quantity*self.price
    
    def __str__(self):
        return self.Film

