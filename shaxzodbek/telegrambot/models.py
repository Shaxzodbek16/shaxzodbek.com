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
        if isinstance(other, TelegramUser):
            return self.user_id == other.user_id
        return False

    def __hash__(self):
        return hash(self.user_id)

    class Meta:
        db_table = "telegram_user"
        verbose_name_plural = "telegram_users"
        verbose_name = "telegram_user"
        ordering = ["-created_at"]


class UserCommands(models.Model):
    user_id = models.ForeignKey(
        TelegramUser, on_delete=models.SET_NULL, to_field="user_id", null=True
    )
    command = models.CharField(max_length=100)
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.command[:10]}"

    def __repr__(self):
        return f"{self.__class__.__name__} {self.__str__()}"

    class Meta:
        db_table = "user_commands"
        verbose_name_plural = "user_commands"
        verbose_name = "user_command"
        ordering = ["-created_at"]

    def __eq__(self, other):
        return self.command == other.commend and self.user_id == other.user_id

    def __hash__(self):
        return hash(self.command)
