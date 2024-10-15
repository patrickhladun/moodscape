from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mood_contact_messages"

    def __str__(self):
        return f"Contact from {self.name}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    section = models.ForeignKey("FAQSection", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mood_faqs"

    def __str__(self):
        return self.question


class FAQSection(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mood_faq_sections"

    def __str__(self):
        return self.name
