from io import BytesIO
from PIL import Image 

from django.db import models
from django.core.files import File 
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.db import connection

# Create your models here.

class Base(models.Model):
  class Meta:
    abstract = True

  @classmethod
  def truncate(cls):
    with connection.cursor() as cursor:
      # print('TRUNCATE TABLE {} CASCADE'.format(cls._meta.db_table))
      # cursor.execute('TRUNCATE TABLE {} CASCADE'.format(cls._meta.db_table))
      cursor.execute('DELETE FROM {}'.format(cls._meta.db_table))
      cursor.execute("delete from sqlite_sequence where name='{}';".format(cls._meta.db_table))
      

class Category(Base):
  name = models.CharField(max_length=255)
  slug = models.SlugField(_('slug'), max_length=255, unique=True, null=True, blank=True)

  class Meta:
    ordering = ('name',)

  def __str__(self):
    return self.name
  
  def get_abs_url(self):
    return f'/{self.slug}/'

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super(Category, self).save(*args, **kwargs)


class Product(Base):
  category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  # slug = models.SlugField()
  slug = models.SlugField(_('slug'), max_length=255, unique=True, null=True, blank=True)
  description = models.TextField(blank=True, null=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  image = models.ImageField(upload_to='uploads/', blank=True, null=True)
  thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
  date_added = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-date_added',)

  def __str__(self):
    return self.name
  
  def get_abs_url(self):
    return f'/{self.category.slug}/{self.slug}/'

  def get_image(self):
    if self.image:
      return 'http://127.0.0.1:8000' + self.image.url 
    return ''

  def get_thumbnail(self):
    if self.thumbnail:
      return 'http://127.0.0.1:8000' + self.thumbnail.url
    else:
      if self.image:
        self.thumbnail = self.make_thumbnail(self.image)
        return 'http://127.0.0.1:8000' + self.thumbnail.url
      else:
        return ''
  
  def make_thumbnail(self, image, size=(300, 200)):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)
    thumb_img_io = BytesIO()
    img.save(thumb_img_io, 'JPEG', quality=85)
    thumb_img = File(thumb_img_io, name=image.name)
    return thumb_img

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super(Product, self).save(*args, **kwargs)