from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Post by {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def _str_(self):
        return f"Like by {self.user.username} on {self.post.id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Comment by {self.user.username} on {self.post.id}"
