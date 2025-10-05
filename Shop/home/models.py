from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from smart_selects.db_fields import ChainedForeignKey
class Category(models.Model):
    name=models.CharField(max_length=50,)
    slug=models.SlugField(max_length=200,unique=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('name',)
        verbose_name='Category'
        verbose_name_plural='categories'
    def __str__(self) :
        return self.name
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    

class SubCategory(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name='subcategory')
    name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=200,unique=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        
        ordering=('name',)
        verbose_name='SubCategory'
        verbose_name_plural='Subcategories'
        
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug0})
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
        
        
class Product(models.Model):
    category=models.ForeignKey(Category,  on_delete=models.CASCADE,related_name='product')
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name='product')
    name=models.CharField(max_length=40)
    slug=models.SlugField(max_length=200,unique=True,null=False,blank=True)
    image=models.ImageField(upload_to='product/%Y/%m/%d')
    description=models.TextField()
    price=models.IntegerField()
    availability=models.BooleanField()
    count=models.SmallIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('name',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("home:product_detail", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
