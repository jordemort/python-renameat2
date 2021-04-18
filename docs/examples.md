# Examples

## Atomically swap two files

```python
from renameat2 import exchange

exchange("/tmp/apples", "/tmp/oranges")
```

## Rename a file

```python
from renameat2 import rename

rename("/tmp/apples", "/tmp/rotten_apples")
```

## Rename a file, failing if it already exists

```python
from renameat2 import rename
from errno import EEXIST

try:
  rename("/tmp/apples", "/tmp/rotten_apples", replace=False)
except OSError as e:
  if e.errno == EEXIST:
    print("/tmp/rotten_apples exists")
  else:
    raise
```

## "Whiteout" a file

```python
from renameat2 import rename

renameat2("/tmp/apples", "/tmp/oranges", whiteout=True)
```
