from glassjar.model import Field, Model


class Item(Model):
    name = Field()
    count = Field()


Item(name="test item", count=20).save()
first_item = Item.records.first()
print(first_item)
print(first_item.as_dict)
