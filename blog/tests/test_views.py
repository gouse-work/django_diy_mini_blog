from django.test import TestCase
from django.urls import reverse
from blog.models import Blog,BlogComment,BlogAuthor
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import os

class BlogListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_blogs = 10
        for i in range(number_of_blogs):
            Blog.objects.create(name='blog title {i}',author=None,description='descriptio of {i} ')

    def test_view_url_exists_at_desired_location(self):
        response=self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code,200)

    def test_view_url_accessible_by_name(self):
        response=self.client.get(reverse('blogs-all'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response=self.client.get(reverse('blogs-all'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'blog/blog_list.html')

    def test_pagination_disabled(self):
        response=self.client.get(reverse('blogs-all'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated']==False)

    def test_view_lists_all_blogs(self):
        response=self.client.get(reverse('blogs-all'))
        self.assertEqual(len(response.context['blog_list']),10)


class BolgDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        blog=Blog.objects.create(name='blog title', author=None, description='description of test blog')
        comment=BlogComment.objects.create(blog=blog,description='test comment',author=None)

    def test_view_url_exists_at_desired_location(self):
        response=self.client.get('/blog/blog/1')
        self.assertEqual(response.status_code , 200)

    def test_view_url_accessible_by_name(self):
        response=self.client.get(reverse('blog-detail',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blog-detail', kwargs={'pk': '1'}))
        self.assertTemplateUsed(response,'blog/blog_detail.html')

    def test_view_get_comments(self):
        response = self.client.get(reverse('blog-detail', kwargs={'pk': '1'}))
        self.assertEqual(len(response.context['comments']),1)

class BlogAuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 10
        for i in range(number_of_authors):
            test_user=User.objects.create_user(username=f'testuser{i}',password=f'12345{i}')
            test_user.save()
            BlogAuthor.objects.create(user=test_user,bio='test bio')

    def test_view_url_at_desired_location(self):
        response=self.client.get('/blog/bloggers/')
        self.assertEqual(response.status_code,200)

    def test_view_url_accessible_by_name(self):
        response=self.client.get(reverse('bloggers-all'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response=self.client.get(reverse('bloggers-all'))
        self.assertTemplateUsed(response,'blog/blogauthor_list.html')

    def test_pagination_enabled(self):
        response=self.client.get(reverse('bloggers-all'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated']==True)

class BlogAuthorDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user=User.objects.create_user(username='testuser',password='12345')
        test_user.save()
        blog_author=BlogAuthor.objects.create(user=test_user,bio='test bio')

        for i in range(10):
            Blog.objects.create(name=f'test blog:{i}',author=blog_author,description='test description')

    def test_view_url_desination_exists(self):
        response=self.client.get('/blog/blogger/1')
        self.assertEqual(response.status_code,200)

    def test_view_url_accessible_by_name(self):
        response=self.client.get(reverse('blogs-by-author',args='1'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response=self.client.get(reverse('blogs-by-author',kwargs={'pk':'1'}))
        self.assertTemplateUsed(response,'blog/blogauthor_detail.html')

    def test_view_blogs_exist(self):
        response=self.client.get(reverse('blogs-by-author',args='1'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('blogs' in response.context)

    def test_blogs_are_displayed(self):
        response=self.client.get(reverse('blogs-by-author',args='1'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['blogs']),10)

class CreateCommentBlogTest(TestCase):
    def setUp(self):
        blog=Blog.objects.create(name='test blog',description='test blog description',author=None)
        test_user1=User.objects.create_user(username='testuser1',password='12345')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response=self.client.get(reverse('create-comment-blog',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith('/accounts/login'))

    def test_HTTP404_for_invalid_blog_if_logged_in(self):
        self.client.login(username='testuser1',password='12345')
        response=self.client.get(reverse('create-comment-blog',kwargs={'pk':'2'}))
        self.assertEqual(response.status_code,404)

    def test_uses_correct_template(self):
        self.client.login(username='testuser1',password='12345')
        response=self.client.get(reverse('create-comment-blog',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'blog/create_comment_blog.html')

    def test_description_more_than_allowed(self):
        self.client.login(username='testuser1',password='12345')
        description_length=1001
        description_max_length=BlogComment._meta.get_field('description').max_length
        description=get_random_string(length=description_length)
        response = self.client.post(reverse('create-comment-blog', kwargs={'pk': '1'}),{'description':description})
        self.assertEqual(response.status_code,200)
        self.assertFormError(response,'form','description',f'Ensure this value has at most {description_max_length} characters (it has {description_length}).')

