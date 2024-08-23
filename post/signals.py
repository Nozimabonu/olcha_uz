from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from post.models import Post


@receiver(post_save, sender=Post)
@receiver(pre_save, sender=Post)
def clear_cache_post_data(instance):
    cache.delete('post_list')
    print('Post List cache delete')
    post_id = instance.id
    cache.delete(f'post_detail_{post_id}')
    print('Post Detail cache delete')


@receiver(post_delete, sender=Post)
def clear_cache_on_post_save_or_post_delete(instance):
    post_id = instance.id
    cache.delete(f'post_detail_{post_id}')
    print('Post Detail cache delete')
