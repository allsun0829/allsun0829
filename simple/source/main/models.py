from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length= 100)
    body = models.TextField()
    # img = models.ImageField(upload_to = "posts/image", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def summary(self): # self는 자기 자신을 가르킨다.
        return self.body[0:30] + "..." # 포스트 글의 body요소를 돌려주는데 0에서 30까지만 돌려준다.
                                       # 즉 30글자만 보여준다.
                                       # + "..." 문자열을 +연산자로 연결