from glassjar.model import Field, Model


class Item(Model):
    name = Field()
    count = Field()

    def __str__(self):
        return f"Item Object"


Item(name="test item", count=20).save()
first_item = Item.records.first()
print(first_item)
