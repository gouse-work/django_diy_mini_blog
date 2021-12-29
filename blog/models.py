from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class BlogAuthor(models.Model):
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    bio=models.TextField(max_length=1000,help_text='Enter a short bio')

    class Meta:
        ordering=["user","bio"]

    def get_absolute_url(self):
        return  reverse('blogs-by-author',args=[str(self.id)])

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    name=models.CharField(max_length=200,help_text='Enter the title of the blog')
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    description=models.TextField(max_length=2000,help_text='Enter the blog description')
    post_date=models.DateField(default=date.today())

    class Meta:
        ordering=["-post_date"]

    def get_absolute_url(self):
        return reverse('blog-detail',args=[str(self.id)])

    def get_short_title(self):
        if len(self.name)<=20:
             short_title=self.name
        else:
            short_title=self.name[:20]+'---'

        return short_title
    get_short_title.short_description='Name'

    def get_short_description(self):
        return self.description[:50]
    get_short_description.short_description='Description'

    def __str__(self):
        return self.name

class BlogComment(models.Model):
    description=models.TextField(max_length=1000,help_text='Enter your comment')
    author=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)

    class meta:
        ordering=["post_date"]

    def __str__(self):
        len_title=75

        if len(self.description)>len_title:
            titlestring=self.description[:len_title]+'---'

        else:
            titlestring=self.description

        return titlestring



