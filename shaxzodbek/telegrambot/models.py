from django.db import models


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} ({self.user_id})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.user_id})"

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    class Meta:
        db_table = "telegram_user"
        verbose_name_plural = "telegram_users"
        verbose_name = "telegram_user"
        ordering = ['-created_at']