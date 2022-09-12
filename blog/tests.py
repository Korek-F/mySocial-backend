from django.test import TestCase
from main_auth.models import User
from .models import Post, Comment, Notification


from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import json
from django.urls import reverse


class TestBlogModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="Jack", email="jack@test.com", password="test123123!")
        self.user2 = User.objects.create_user(username="Jerry", email="jerry@test.com", password="test123123!")
        self.post = Post.objects.create(body="aaaaa", author=self.user1, title="bbbbb")
        self.comment = Comment.objects.create(author=self.user2, post=self.post, content="test")

    def test_post_model(self):
        Post.objects.create(body="SSSSSSS", author=self.user1, title="test")
        self.assertEqual(Post.objects.get(id=2).title, "test")
    
    def test_comment_model(self):
        Comment.objects.create(author=self.user2, post=self.post, content="test2")
        self.assertEqual(Comment.objects.get(id=2).content, "test2")
        self.assertEqual(Comment.objects.get(id=2).post.body, "aaaaa")
    
    def test_subcomment_model(self):
        Comment.objects.create(author=self.user1, post=self.post, parent=self.comment, content="test")
        self.assertEqual(Comment.objects.get(id=2).parent, self.comment)
        

class BlogViewTest(TestCase):
    def setUp(self):
        self.user1 =User.objects.create_user(username="Filip",email="filip@onet.pl", password="test123123!")
        self.user1.is_active = True 
        self.user1.save()

        self.user2= User.objects.create_user(username="Jan",email="jan@onet.pl", password="test123123!")
        self.user2.is_active = True 
        self.user2.save()
    
    def api_client(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user1)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client 
    
    def api_client2(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client 

    def test_posts_and_post_view(self):
        client = self.api_client()

        response = client.get(reverse("posts"))
        self.assertEqual(response.status_code, 200)
       
        response = client.post(reverse("posts"),{"title":"test_title", "body":"test_body"})
        self.assertEqual(response.status_code, 201)

        response = client.get(reverse("posts"))
        data = json.loads(response.content)["data"][0]
        self.assertEqual(data["body"], "test_body")
        self.assertEqual(data["title"], "test_title")


        client2 = self.api_client2()
        response = client2.get(reverse('post_details', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data["body"], "test_body")
        self.assertEqual(data["title"], "test_title")

        response = client2.get(reverse('post_details', kwargs={'pk':2}))
        self.assertEqual(response.status_code, 404)


        response = client2.delete(reverse('posts_delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 403)
        response = client.delete(reverse('posts_delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
    
    def test_comments_and_comment_view(self):
        Post.objects.create(body="test_body", author=self.user2, title="test_title")

        client = self.api_client()

        response = client.get(reverse('post_comments', kwargs={'id':1}))
        self.assertEqual(response.status_code, 200)

        #creating comment
        response = client.post(reverse('post_comments', kwargs={'id':1}),{"content":"test_content"})
        self.assertEqual(response.status_code,201)

        #checking comment
        response = client.get(reverse('post_comments', kwargs={'id':1}))
        data = json.loads(response.content)[0]
        self.assertEqual(data["content"],"test_content")
        self.assertEqual(data["post"],1)
        self.assertEqual(data["author"]["username"],"Filip")

        #creating sub-comment
        client2 = self.api_client2()
        response = client2.post(reverse('post_comments', kwargs={'id':1}),{"parent_id":1,"content":"test_content2"})
        self.assertEqual(response.status_code,201)
        
        #checking sub-comment
        response = client.get(reverse('post_comments', kwargs={'id':1}))
        data = json.loads(response.content)[0]["comment_child"][0]
        self.assertEqual(data["content"],"test_content2")
        self.assertEqual(data["parent"],1)
        self.assertEqual(data["author"]["username"],"Jan")


        #checking comment in single comment view
        response = client.get(reverse('comment', kwargs={'pk':1}))
        data=json.loads(response.content)
        self.assertEqual(data["content"],"test_content")
        self.assertEqual(data["comment_child"][0]["content"],"test_content2")

        #deleting sub-comment 
        response = client2.delete(reverse('comment_delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code,403)
        response = client.delete(reverse('comment_delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code,200)
        
    def test_user_posts_view(self):
        Post.objects.create(body="test_body", author=self.user2, title="test_title")
        Post.objects.create(body="test_body2",author=self.user2, title="test_title2")

        client = self.api_client()
        response = client.get(reverse('user_posts', kwargs={'username':"Jan"}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data),2)
    
    def test_like_dislike_post_view(self):
        Post.objects.create(body="test_body", author=self.user2, title="test_title")

        client = self.api_client()

        response = client.get(reverse('post_details', kwargs={'pk':1}))
        data = json.loads(response.content)
        self.assertEqual(data["likes"],0)

        #like post
        client.patch(reverse('post_like_dislike'), {"id":1})
        response = client.get(reverse('post_details', kwargs={'pk':1}))
        data = json.loads(response.content)
        self.assertEqual(data["likes"],1)

        #dislike post
        client.patch(reverse('post_like_dislike'), {"id":1})
        response = client.get(reverse('post_details', kwargs={'pk':1}))
        data = json.loads(response.content)
        self.assertEqual(data["likes"],0)

    def test_like_dislike_comment_view(self):
        post = Post.objects.create(body="test_body", author=self.user2, title="test_title")
        Comment.objects.create(content="test_content", post=post, author=self.user1)

        client = self.api_client2()

        response = client.get(reverse('comment', kwargs={'pk':1}))
        data = json.loads(response.content)
        self.assertEqual(data["likes"],0)

        #like post
        client.patch(reverse('comment_like_dislike'), {"id":1})
        response = client.get(reverse('comment', kwargs={'pk':1}))
        data = json.loads(response.content)
        self.assertEqual(data["likes"],1)
        
        #dislike post
        client.patch(reverse('comment_like_dislike'), {"id":1})
        response = client.get(reverse('comment', kwargs={'pk':1}))
        data = json.loads(response.content)
        self.assertEqual(data["likes"],0)
    
    def test_notifications(self):
        post = Post.objects.create(body="test_body", author=self.user2, title="test_title")
        
        client = self.api_client()
        client2 = self.api_client2()

        #New comment notification
            #Creating new comment 
        response = client.post(reverse('post_comments', kwargs={"id":1}), {"content":"test_content2"})
        self.assertEqual(response.status_code, 201)
            #Checking if notification was created
        response = client2.get(reverse("notifications"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]["notification_type"], "C")

        #New post like notification
            #Creating new like
        client.patch(reverse("post_like_dislike"), {"id":1})
        self.assertEqual(response.status_code, 200)
            #Checking if notification was created
        response = client2.get(reverse("notifications"))
        data = json.loads(response.content)
        self.assertEqual(data[0]["notification_type"], "L")

        #New post like notification
            #Creating new like
        client2.patch(reverse("comment_like_dislike"), {"id":1})
            #Checking if notification was created
        response = client.get(reverse("notifications"))
        data = json.loads(response.content)
        self.assertEqual(data[0]["notification_type"], "LC")

        #New follow notification
            #Creating new follow
        response = client2.post("/auth/follow-action/", {"username":"Filip"})
        self.assertEqual(response.status_code, 200)
            #Checking if notification was created
        response = client.get(reverse("notifications"))
        data = json.loads(response.content)
        self.assertEqual(data[0]["notification_type"], "F")

        #New comment response notification
            #Creating new comment response
        response = client2.post(reverse('post_comments', kwargs={'id':1}),{"parent_id":1,"content":"test_content3"})
        self.assertEqual(response.status_code, 201)
            #Checking if notification was created
        response = client.get(reverse("notifications"))
        data = json.loads(response.content)
        self.assertEqual(data[0]["notification_type"], "CR")

        #Unseen notification count 
        response = client.get(reverse("unseen_notifications_count"))
        data = json.loads(response.content)
        self.assertEqual(response.content, b'3')








       
