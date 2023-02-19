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

## Installation

_glassjar_ can be installed by running `pip install glassjar`.

## Example

```python
>>> from glassjar.model import Model
>>>
>>> class Item(Model):
...     name: str
...     count: int
...
>>> item = Item(name="test item", count=20).save()
>>> item
Item(name='test item', count=20)
>>> item.as_dict()
{'name': 'test item', 'count': 20}
>>>
```

ORM operations;

```python
>>> item.id
1
>>> Item.records.get(id=1)
Item(name='test item', count=20)
>>> Item.records.first()
Item(name='test item', count=20)
>>> last_item = Item(name='last item', count=1).save()
>>> Item.records.last()
Item(name='last item', count=1)
```
