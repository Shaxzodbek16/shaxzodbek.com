from aiogram.types.input_file import FSInputFile
from django.contrib import admin
from .models import Article, Match, Connection, Author, Category, ProgrammingLanguage, Book, Video
from aiogram import Bot
from django.contrib import messages
from django.conf import settings
import asyncio


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated', 'telegram')
    list_filter = ('created', 'updated')
    search_fields = ('title', 'body')
    date_hierarchy = 'created'
    ordering = ('-created',)
    actions = ['send_to_telegram_channel']

    async def send_to_telegram(self, bot, channel_id, article):
        caption = f"<b>{article.title}</b>\n\n{article.body[:150]}..."
        caption += """<a href="https://shaxzodbek.com">Ko'proq o'qish</a>  """
        if article.picture:
            with open(article.picture.path, 'rb') as photo:
                await bot.send_photo(chat_id=channel_id,
                                     photo=FSInputFile(path=article.picture.url),
                                     caption=caption,
                                     parse_mode='HTML')
        else:
            await bot.send_message(chat_id=channel_id, text=caption, parse_mode='HTML')

    def send_to_telegram_channel(self, request, queryset):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        channel_id = settings.TELEGRAM_CHANNEL_ID

        for article in queryset:
            if not article.telegram:
                try:
                    asyncio.run(self.send_to_telegram(bot, channel_id, article))

                    article.telegram = True
                    article.save()
                    self.message_user(request, f"Successfully sent '{article.title}' to Telegram channel",
                                      messages.SUCCESS)
                except Exception as e:
                    self.message_user(request, f"Failed to send '{article.title}' to Telegram channel: {str(e)}",
                                      messages.ERROR)
            else:
                self.message_user(request, f"'{article.title}' has already been sent to Telegram", messages.WARNING)

        asyncio.run(bot.session.close())

    send_to_telegram_channel.short_description = "Send selected articles to Telegram channel"


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('who_is_it', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('who_is_it',)
    date_hierarchy = 'created'
    ordering = ('-created',)


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job_title', 'birth_date', "home_address")
    list_filter = ('birth_date', 'job_title')
    search_fields = ('first_name', 'last_name', 'job_title', 'met_at')
    date_hierarchy = 'birth_date'
    filter_horizontal = ('who_for_me',)
    ordering = ('-birth_date',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('-first_name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-name',)


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'purpose', 'programming_language')
    list_filter = ('programming_language', 'category')
    search_fields = ('title', 'purpose', 'author__first_name', 'author__last_name')
    filter_horizontal = ('author', 'category')
    ordering = ('-title',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created')
    list_filter = ('title', 'created')
    search_fields = ('title',)
    ordering = ('-created',)
