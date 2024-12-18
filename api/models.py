from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    image = models.URLField(help_text='Enter the URL of the image',null=True,blank=True)
    advUrl = models.URLField(help_text="Enter adv short link",null=True,blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Cartoon(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="cartoon_category")
    advUrl = models.URLField(help_text="Enter adv short link",null=True,blank=True)
    title = models.CharField(max_length=50,null=False,blank=False)
    image = models.URLField(help_text='Enter the URL of the image',null=True,blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Video(models.Model):
    cartoon = models.ForeignKey(Cartoon,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,null=False,blank=False)
    thumbnail = models.URLField(help_text="Enter the url of thumbnail image",null=True,blank=True)
    videoUrl = models.URLField(help_text="Enter video link",null=False,blank=False)
    advUrl = models.URLField(help_text='Enter adv short link',null=True,blank=True)
    status = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.title

class IGCommerce(models.Model):
    shortcode = models.CharField(max_length=255,null=False,blank=False,unique=True)
    media_id = models.CharField(max_length=255,null=False,blank=False,unique=True)
    thumbnail = models.URLField(null=True,blank=True)
    video = models.URLField(null=True,blank=True)
    likes = models.BigIntegerField(default=0,null=True,blank=True)
    comments = models.BigIntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.shortcode)