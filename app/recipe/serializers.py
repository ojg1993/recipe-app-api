from rest_framework import serializers
from core import models


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = models.Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link',
                  'tags', 'ingredients'
                  ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        # Handle getting or creating tags as requested
        auth_user = self.context['request'].user
        for tag in tags:
            # Get if already exists, else create -> get_or_create
            tag_obj, created = models.Tag.objects.get_or_create(
                user=auth_user,
                **tag  # name:<TagName>
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        # Handle getting or creating ingredients as requested
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            # Get if already exists, else create -> get_or_create
            ingredient_obj, created = models.Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient  # {"name": "Ingredient Name"}
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        # Create a recipe
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = models.Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        # Update recipe
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}
