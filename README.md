# JsonDB

> [!WARNING]
> This is for my personal use only. You really shouldn't
> be using JSON for database.

## Uses
I'm using this for my [Telegram bot](https://github.com/hakimifr/tgbot-python-v2)
and [Elysian's Chemistry Bot](https://github.com/hakimifr/tgbot-python-v2).

## Usage
1. Add it to your project as dependency, for example if you use `uv`:
```bash
uv add jsondb-hakimifr
```

2. profit!!!
```python
from jsondb.database import Database

db = Database("foo.json")
db.read_database()  # actually redundant as __init__ will call this

db.data = {"hello": "world"}
db.write_database()
```

## Extras
- There's a callback registered to `atexit` module, so that a crash
  doesn't throw away unsaved stuff.
- Minimal safeguard to prevent multiple instances from opening the
  same file at the same time (I don't even know if it actually works lol).

## License
```
SPDX-License-Identifier: Apache-2.0

Copyright 2025 Firdaus Hakimi <hakimifirdaus944@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

or

    the LICENSE file in this repository.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
