from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=50,)
    slug=models.SlugField(max_length=200,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('name',)
        verbose_name='Category'
        verbose_name_plural='categories'
    def __str__(self) :
        return self.name
    
        
        
class Product(models.Model):
    category=models.ForeignKey(Category,  on_delete=models.CASCADE,related_name='product')
    name=models.CharField(max_length=40)
    slug=models.SlugField(max_length=200,unique=True)
    image=models.ImageField(upload_to='product/%Y/%m/%d')
    descroption=models.TextField()
    price=models.IntegerField()
    availability=models.BooleanField()
    count=models.SmallIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('name',)
    def __str__(self):
        return self.name