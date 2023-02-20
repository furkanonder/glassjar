import pathlib
import unittest

from glassjar.constants import DB_NAME
from glassjar.db import create_table
from glassjar.exceptions import DoesNotExist
from glassjar.model import Model


class Item(Model):
    name: str
    count: int


class Car(Model):
    brand: str
    model: str
    year: int


class TestBase(unittest.TestCase):
    def setUp(self):
        create_table("Item_table")
        create_table("Car_table")

    def tearDown(self):
        pathlib.Path(DB_NAME).unlink()


class TestModel(TestBase):
    def test_save(self):
        item_obj = Item(name="test item", count=20).save()
        self.assertEqual(item_obj.name, "test item")
        self.assertEqual(item_obj.count, 20)

        car_obj = Car(brand="Tesla", model="Model S", year=2022).save()
        self.assertEqual(car_obj.brand, "Tesla")
        self.assertEqual(car_obj.model, "Model S")
        self.assertEqual(car_obj.year, 2022)

    def test_update(self):
        car_db_obj = Car(brand="Tesla", model="Model S", year=2022).save()
        self.assertEqual(car_db_obj.year, 2022)

        car_db_obj.year = 2010
        car_db_obj.save()
        self.assertEqual(car_db_obj.year, 2010)

        fresh_car_db_obj = Car.records.get(id=1)
        self.assertEqual(fresh_car_db_obj.year, 2010)

    def test_delete(self):
        car_obj = Car(brand="Tesla", model="Model S", year=2022).save()
        car_obj.delete(id=1)

        self.assertRaises(DoesNotExist, Car.records.get, id=1)
        self.assertRaises(DoesNotExist, car_obj.delete, id=1)

    def test_slot_feature(self):
        car_obj = Car(brand="Tesla", model="Model S", year=2022)

        with self.assertRaises(AttributeError):
            car_obj.dummy_attr = "dummy"

    def test_change_table_name(self):
        car_obj = Car(brand="Tesla", model="Model S", year=2022)

        with self.assertRaises(AttributeError) as exc:
            car_obj.table_name = "changed_table"

        self.assertEqual(type(exc.exception), AttributeError)

    def test_type_check(self):
        with self.assertRaises(TypeError):
            Car(brand="Tesla", model="Model S", year=2022.4)

    def test_as_dict(self):
        car_obj = Car(brand="Tesla", model="Model S", year=2022)
        car_dict = car_obj.as_dict()

        self.assertEqual(car_obj.brand, car_dict["brand"])
        self.assertEqual(car_obj.model, car_dict["model"])
        self.assertEqual(car_obj.year, car_dict["year"])


class TestQuery(TestBase):
    def test_get(self):
        item_obj = Item(name="test item", count=20).save()
        item_db_obj = Item.records.get(id=1)
        self.assertEqual(item_db_obj.id, item_obj.id)
        self.assertEqual(item_db_obj.name, item_obj.name)
        self.assertEqual(item_db_obj.count, item_obj.count)

        car_obj = Car(brand="Tesla", model="Model S", year=2022).save()
        car_db_obj = Car.records.get(id=1)
        self.assertEqual(car_db_obj.id, car_obj.id)
        self.assertEqual(car_db_obj.brand, car_obj.brand)
        self.assertEqual(car_db_obj.model, car_obj.model)
        self.assertEqual(car_db_obj.year, car_obj.year)

    def test_all(self):
        items = [Item(name="test item", count=20).save() for _ in range(10)]

        for item, other_item in zip(items, Item.records.all()):
            self.assertEqual(item, other_item)

        self.assertEqual(len(Item.records.all()), len(items))

    def test_first(self):
        for _ in range(10):
            Item(name="test item", count=20).save()

        items = Item.records.all()
        self.assertEqual(Item.records.first(), items.first())

    def test_last(self):
        for _ in range(10):
            Item(name="test item", count=20).save()

        items = Item.records.all()
        self.assertEqual(Item.records.last(), items.last())

    def test_count(self):
        for _ in range(5):
            Item(name="test item", count=20).save()

        items = Item.records.all()
        self.assertEqual(Item.records.count(), items.count())

    def test_create(self):
        item = Item.records.create(name="fresh item")
        self.assertEqual(item.name, "fresh item")
