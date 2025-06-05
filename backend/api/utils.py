from rest_framework import serializers


def many_unique_with_minimum_one_validate(
    data_list: list,
    field_name: str,
    singular: str = 'элемент',
    plural: str = 'элементы'
):
    if not data_list:
        raise serializers.ValidationError({
            field_name: f'Необходимо добавить минимум один {singular}.'
        })

    unique_items = set()

    for item in data_list:
        if isinstance(item, dict):
            value = item.get('id')
        else:
            value = getattr(item, 'id', None)

        if value is None:
            raise serializers.ValidationError({
                field_name: f'Некорректные данные у одного из {plural}.'
            })

        if value in unique_items:
            raise serializers.ValidationError({
                field_name: f'{singular.capitalize()} не должны повторяться.'
            })

        unique_items.add(value)