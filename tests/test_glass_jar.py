import pathlib
import shelve
import unittest

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
        with shelve.open("database.jar", writeback=True) as db:
            db["tables"] = {}

    def tearDown(self):
        pathlib.Path("database.jar").unlink()


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

    def test_type_check(self):
        with self.assertRaises(TypeError):
            Car(brand="Tesla", model="Model S", year=2022.4)


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
        for _ in range(10):
            Item(name="test item", count=20).save()
        self.assertEqual(len(Item.records.all()), 10)

    def test_first(self):
        item_list = []

        for _ in range(10):
            item = Item(name="test item", count=20).save()
            item_list.append(item)

        self.assertEqual(Item.records.first().id, item_list[0].id)

    def test_last(self):
        item_list = []

        for _ in range(10):
            item = Item(name="test item", count=20).save()
            item_list.append(item)

        self.assertEqual(Item.records.last().id, item_list[-1].id)

    def test_count(self):
        for _ in range(5):
            Item(name="test item", count=20).save()
        self.assertEqual(Item.records.count(), 5)
