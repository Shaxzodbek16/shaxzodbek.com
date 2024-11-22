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


class Commands(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, related_name='commands', to_field='user_id',
                             blank=True, null=True)
    command = models.CharField(max_length=255, default='')
    message = models.TextField(blank=True, null=True, default='')
    response = models.TextField(blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name if self.user else 'Unknown User'} - {self.command} at {self.created_at}"

    class Meta:
        db_table = "user_commands"
        verbose_name_plural = "user_commands"
        verbose_name = "user_command"
        ordering = ['-created_at']


class Feedback(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, blank=True, null=True, to_field='user_id')
    message = models.TextField(blank=True, null=True, default='')
    file = models.FileField(blank=True, null=True, upload_to='feedback/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name if self.user else 'Unknown User'} - {self.message} at {self.created_at}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.user.first_name if self.user else 'Unknown User'})"

    def __eq__(self, other):
        return self.user == other.user
    def __hash__(self):
        return hash(self.user)

    class Meta:
        db_table = "feedback"
        verbose_name_plural = "feedback"
        verbose_name = "feedback"
        ordering = ['-created_at']
