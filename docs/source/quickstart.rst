QuickStart
==========

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

