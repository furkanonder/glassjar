QuickStart
==========

Model
-----

A model is the source of information about your data.

- Each model is a Python class that subclasses **glassjar.model.Model**
- Each model attribute corresponds to a database field.

Example::

    from glassjar.model import Model

    class Item(Model):
        name: str
        attrs: dict
