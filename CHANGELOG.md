# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2023-03-11

### Added

- Documentation has been added.

### Changed

- The model and queryset have been refactored and optimized.


## [0.1.0] - 2022-11-18

### Added

- ORM includes the following new features: all, last, count, and as_dict.
- The queryset structure has been added to ORM.
- The slots mechanism has been added to the models.
- Type checker has been added for the field structure of the models.

### Changed

- The field structure of the models has been changed to be defined as type hints.

### Removed

- Shelve module has been removed. Now, Glassjar has its own data management system.

## [0.0.1] - 2022-11-05

### Added

- Data storage, updating, and deletion operations have been added with ORM support by
  specifying the model.

[0.1.0]: https://github.com/furkanonder/glassjar/releases/tag/0.1.0
[0.0.1]: https://github.com/furkanonder/glassjar/releases/tag/0.0.1
