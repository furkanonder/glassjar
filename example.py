from glassjar.model import Model


class Item(Model):
    name: str
    count: int


Item(name="test item", count=20).save()
first_item = Item.records.first()
print(first_item)
print(first_item.as_dict())
