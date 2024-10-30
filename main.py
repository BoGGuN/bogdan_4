import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app import models
from django.db.models import Q, Count, Avg, Min, F

# 1
profiles =models.Profile.objects.all()
print(profiles)
for element in profiles:
    print(element.name)

print('1-----------------------------')

comments = models.Comment.objects.all()
print(comments)
for element in comments:
    print(f'{element.author} - {element.text}')

print('1-----------------------------')

items = models.Item.objects.all()
print(items)
for element in items:
    print(f'{element.type} - {element.name} - {element.price} руб.')

print('1-----------------------------')

# 2
items_above_1900_gte = models.Item.objects.all().filter(price__gt=1900)
print(items_above_1900_gte)
for element in items_above_1900_gte:
    print(f'{element.type} - {element.name} - {element.price} руб.')

print('2-----------------------------')

items_above_1700_gt = models.Item.objects.all().filter(price__gte=1900)
print(items_above_1700_gt)
for element in items_above_1700_gt:
    if element.price ==  1900.0:
        print(f'{element.type} - {element.name} - {element.price} руб. ------> gte/gt')
    else:
        print(f'{element.type} - {element.name} - {element.price} руб.')

print('2-----------------------------')

items_food = models.Item.objects.all().filter(type="food")
print(items_food)
for element in items_food:
    print(f'{element.type} - {element.name} - {element.price} руб.')

print('2-----------------------------')

items_above_1900_gte_complex = models.Item.objects.all().filter(price__gt=1900).order_by("-price")
print(items_above_1900_gte_complex)
for element in items_above_1900_gte_complex:
    print(f'{element.type} - {element.name} - {element.price} руб.')

print('2-----------------------------')

items_above_1700_gt_complex = models.Item.objects.all().filter(price__gte=1900).order_by("type", "price")  #Сначала по типу, потом внутри типа по цене
print(items_above_1700_gt_complex)
for element in items_above_1700_gt_complex:
    if element.price ==  1900.0:
        print(f'{element.type} - {element.name} - {element.price} руб. ------> gte/gt')
    else:
        print(f'{element.type} - {element.name} - {element.price} руб.')

print('2-----------------------------')

items_food_complex = models.Item.objects.all().filter(type="food").order_by("-price").exclude(name="Апельсин").exclude(price__lt=100)
print(items_food_complex)
for element in items_food_complex:
    print(f'{element.type} - {element.name} - {element.price} руб.')

print('2-----------------------------')

items_food_complex = models.Item.objects.all().filter(type="food").order_by("-price").exclude(name__startswith="М", price__lt=100)
print(items_food_complex)
for element in items_food_complex:
    print(f'{element.type} - {element.name} - {element.price} руб.')

print('2-----------------------------')

#3
users_with_food = models.User.objects.select_related("profile").prefetch_related("profile__purchased_items").all().filter(profile__purchased_items__type="default").distinct()
print(users_with_food)
for element in users_with_food:
    print(f'{element.profile.name} ')

print('3-----------------------------')

post_with_bogdan_comments = models.Post.objects.prefetch_related("post_comments").all().filter(post_comments__author__login="bogdan").distinct()
print(post_with_bogdan_comments)
for element in post_with_bogdan_comments:
    print(f'Post: {element.title}; comments: {[comment.text for comment in element.post_comments.all()]}')

print('3-----------------------------')

groups_with_posts_names = models.Group.objects.values('name', 'group_posts')
print(groups_with_posts_names)
for element in groups_with_posts_names:
    print(f'Группа: {element["name"]}; Посты: {element["group_posts"]}')

print('3-----------------------------')

groups_with_posts_names = models.Group.objects.values_list('name', 'group_posts')
print(groups_with_posts_names)
for (name, amount) in groups_with_posts_names:
    print(f'Группа: {name}; Посты: {amount}')

print('3-----------------------------')

# 4

items_food_and_M_or_toy_and_D = models.Item.objects.all().filter(Q(Q(type="food") & ~Q(name__startswith="М")) | Q(Q(type="toy") & Q(name__startswith="Д")))
print(items_food_and_M_or_toy_and_D)
for element in items_food_and_M_or_toy_and_D:
    print(f'{element.type} - {element.name} - {element.price} руб.')

print('4-----------------------------')

groups = models.Group.objects.select_related("admin").all().filter(Q(admin__login="bogdan") | ~Q(name__startswith="Г"))
print(groups)
for element in groups:
    print(f'{element.name} - {element.admin.login}')

print('4-----------------------------')

# 5

post_comments_count = models.Post.objects.prefetch_related("post_comments").all().annotate(comments_count = Count("post_comments"))
print(post_comments_count)
for element in post_comments_count:
    print(f'{element.title} - comments: {element.comments_count}')

print('5-----------------------------')

items_average_price = models.Item.objects.all().aggregate(average_price= Avg("price"))
print(items_average_price["average_price"])

print('5-----------------------------')

cheapest_item = models.Item.objects.aggregate(min_price=Min('price'))['min_price']
items_in_cheapest_item = models.Item.objects.all().annotate(x_cheapest = F('price')/cheapest_item)
print(items_in_cheapest_item)
for element in items_in_cheapest_item:
    print(f'{element.name} - comments: {element.x_cheapest: .1f}')

print('5-----------------------------')

group_with_admin_profile = models.Group.objects.annotate(admin_name=F("admin__profile__name"))
print(group_with_admin_profile)
for element in group_with_admin_profile:
    print(f'{element.name} - {element.admin_name} ({element.admin.login})')