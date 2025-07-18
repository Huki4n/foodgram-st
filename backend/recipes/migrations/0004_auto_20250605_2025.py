# Generated by Django 3.2.16 on 2025-06-05 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_delete_recipefavorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe_ingredients', through='recipes.RecipeIngredients', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.CreateModel(
            name='RecipeFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_favorite', to=settings.AUTH_USER_MODEL, verbose_name='Владелец избранного')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_favorite', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
                'default_related_name': 'recipe_favorite',
            },
        ),
        migrations.AddConstraint(
            model_name='recipefavorite',
            constraint=models.UniqueConstraint(fields=('author', 'recipe'), name='unique_recipe_favorite'),
        ),
    ]
