from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    rating_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Ensure this line exists

    def update_rating(self, new_rating):
        self.rating = (self.rating * self.rating_count + new_rating) / (self.rating_count + 1)
        self.rating_count += 1
        self.save()



class Lecture(models.Model):
    user = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.user
    


class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')  # Adding related_name here
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.username} rated {self.course.title} as {self.rating}'