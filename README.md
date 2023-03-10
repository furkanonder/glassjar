<div align="center">
  <img src="/assets/logo/glassjar.png" width=200px/>
  <h3>Pickled database that provide Object-Relational Mapper.</h3>
  <a href="https://github.com/furkanonder/glassjar/actions"><img alt="Actions Status" src="https://github.com/furkanonder/glassjar/workflows/Test/badge.svg"></a>
  <a href="https://github.com/furkanonder/glassjar/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/furkanonder/glassjar"></a>
  <a href="https://github.com/furkanonder/glassjar/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/furkanonder/glassjar"></a>
  <a href="https://github.com/furkanonder/glassjar/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/furkanonder/glassjar"></a>
  <a href="https://pepy.tech/project/glassjar"><img alt="Downloads" src="https://pepy.tech/badge/glassjar"></a>
  <a href="https://img.shields.io/pypi/pyversions/glassjar"><img alt="Supported Versions" src="https://img.shields.io/pypi/pyversions/glassjar"></a>
</div>

## Motivation

Glassjar is a database that provides a storage mechanism based on pickled Python objects
with ORM.

## Installation

_glassjar_ can be installed by running `pip install glassjar`.

## Example

```python
>>> from glassjar.model import Model
>>>
>>> class Item(Model):
...     name: str
...     attrs: dict
...
>>> item = Item.records.create(name="item", attrs={"color": "red", "shape":"rectangle"})
>>> item.as_dict()
{'name': 'item', 'attrs': {'color': 'red', 'shape': 'rectangle'}}
>>> item2 = Item.records.create(name="item 2", attrs={"color": "blue", "shape":"triangle"})
>>> Item.records.first()
Item(name='item', attrs={'color': 'red', 'shape': 'rectangle'})
>>> Item.records.last()
Item(name='item 2', attrs={'color': 'blue', 'shape': 'triangle'})
>>>
```
