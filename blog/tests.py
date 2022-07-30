from django.test import TestCase
from main_auth.models import User
from .models import Post, Comment, Notification

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
        
       
  