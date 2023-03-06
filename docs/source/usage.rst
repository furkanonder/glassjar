Usage
=====

Installation
------------

To use GlassJar, first install it using pip:

.. code-block:: console

   $ pip install glassjar

Model
-----

A model is the source of information about your data.

- Each model is a Python class that subclasses **glassjar.model.Model**
- Each model attribute corresponds to a database field.

Following the creation of the models, the data associated with the models are stored in the **database.jar** file.

Field
^^^^^

Each database field must be defined as a class variable in that has a type annotation.

Example::

    from glassjar.model import Model

    class Item(Model):
        name: str
        attrs: dict


Model Functions
^^^^^^^^^^^^^^^

.. function:: Model.save(**fields)

    Saves the model object to the database and returns it.

    Example::

        item = Item(
            name="item",
            attrs={"color": "red", "shape":"rectangle"}
        ).save()


.. function:: Model.delete()

    Deletes the model object.

.. function:: Model.as_dict()

    Converts the model object to a dict.

QuerySet
--------

.. function:: Model.records.create(**fields)

    It creates a model object and returns it.

    Example::

        item = Item.records.create(
            name="item",
            attrs={"color": "red", "shape":"rectangle"}
        )


.. function:: Models.records.delete(id)

    Deletes the model object with the given id.

.. function:: Models.records.get(id)

    Returns the model object with the given id.

.. function:: Models.records.all()

    Returns the all model objects.

.. function:: Models.records.count()

    Returns the count of model objects in the database.

.. function:: Models.records.first()

    Returns the first model object from the database.

.. function:: Models.records.last()

    Returns the last model object from the database.