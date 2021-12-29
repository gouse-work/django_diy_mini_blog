import datetime

from django.test import TestCase
from blog.models import Blog,BlogAuthor,BlogComment
from django.contrib.auth.models import User
from datetime import date

class BlogAuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1=User.objects.create_user(username='testuser1',password='12345')
        test_user1.save()
        author=BlogAuthor.objects.create(user=test_user1,bio='this is a short bio')

    def test_user_label(self):
        author=BlogAuthor.objects.get(id=1)
        field_label=author._meta.get_field('user').verbose_name
        self.assertEquals(field_label,'user')

    def test_bio_label(self):
        author = BlogAuthor.objects.get(id=1)
        field_label = author._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'bio')

    def test_bio_max_length(self):
        author = BlogAuthor.objects.get(id=1)
        max_length = author._meta.get_field('bio').max_length
        self.assertEquals(max_length, 1000)

    def test_get_absolute_url(self):
        author=BlogAuthor.objects.get(id=1)
        the_url=author.get_absolute_url()
        self.assertEquals(the_url,'/blog/blogger/1')

    def test_object_str(self):
        author=BlogAuthor.objects.get(id=1)
        str_name=author.user.username
        self.assertEquals(str_name,str(author))

class BlogModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        blog_author = BlogAuthor.objects.create(user=test_user1, bio='the bio of test user')
        blog = Blog.objects.create(name='test blog name', author=blog_author, description='test description')

    def test_name_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        blog=Blog.objects.get(id=1)
        max_length=blog._meta.get_field('name').max_length
        self.assertEquals(max_length,200)

    def test_author_label(self):
        blog=Blog.objects.get(id=1)
        field_label=blog._meta.get_field('author').verbose_name
        self.assertEquals(field_label,'author')

    def test_author(self):
        blog=Blog.objects.get(id=1)
        author=blog.author
        self.assertEquals(author,BlogAuthor.objects.get(id=1))

    def test_description_label(self):
        blog=Blog.objects.get(id=1)
        field_label=blog._meta.get_field('description').verbose_name
        self.assertEquals(field_label,'description')

    def test_description_mac_length(self):
        blog=Blog.objects.get(id=1)
        max_length=blog._meta.get_field('description').max_length
        self.assertEquals(max_length,2000)

    def test_post_date_label(self):
        blog=Blog.objects.get(id=1)
        field_label=blog._meta.get_field('post_date').verbose_name
        self.assertEquals(field_label,'post date')

    def test_post_date(self):
        blog=Blog.objects.get(id=1)
        date=blog.post_date
        self.assertEquals(datetime.date.today(),date)

    def test_object_name(self):
        blog=Blog.objects.get(id=1)
        name=blog.name
        self.assertEquals(name,str(blog))

    def test_get_absolute_url(self):
        blog=Blog.objects.get(id=1)
        url=blog.get_absolute_url()
        self.assertEquals(url,'/blog/blog/1')

class BlogCommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1=User.objects.create_user(username='testuser1',password='12345')
        test_user1.save()
        test_user2=User.objects.create_user(username='testiser2',password='67890')
        test_user2.save()
        test_author=BlogAuthor.objects.create(user=test_user1,bio='Test bio')
        test_blog=Blog.objects.create(name='test blog name',author=test_author,description='Test Description')
        test_comment=BlogComment.objects.create(description='Test comment description',author=test_user2,blog=test_blog)

    def test_description_label(self):
        comment=BlogComment.objects.get(id=1)
        field_label=comment._meta.get_field('description').verbose_name
        self.assertEquals(field_label,'description')

    def test_description_max_length(self):
        comment=BlogComment.objects.get(id=1)
        max_length=comment._meta.get_field('description').max_length
        self.assertEquals(max_length,1000)

    def test_author_label(self):
        comment=BlogComment.objects.get(id=1)
        field_name=comment._meta.get_field('author').verbose_name
        self.assertEquals(field_name,'author')

    def test_post_date(self):
        comment=BlogComment.objects.get(id=1)
        field_name=comment._meta.get_field('post_date').verbose_name
        self.assertEquals(field_name,'post date')


    def test_blog_label(self):
        comment=BlogComment.objects.get(id=1)
        field_label=comment._meta.get_field('blog').verbose_name
        self.assertEquals(field_label,'blog')

    def test_object_str(self):
        comment=BlogComment.objects.get(id=1)
        expected_name=''
        title_len=75

        if len(comment.description)>75:
            expected_name=comment.description[:title_len]+'---'

        else:
            expected_name=comment.description

        self.assertEquals(expected_name,str(comment))

