# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2025 Firdaus Hakimi <hakimifirdaus944@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import atexit
import json
import logging
import time

from pathlib import Path

from jsondb._lockfile_util import is_lock_file_exist, remove_lock_file, write_lock_file

log: logging.Logger = logging.getLogger(__name__)


class JsonDB:
    active_config: list[str] = []

    def __init__(self, file: str):
        if file in JsonDB.active_config:
            raise ValueError("The config file is already opened by another instance!")

        self.write_pending: bool = False
        self._data: dict = {}
        self.closed: bool = False

        if not file.endswith(".json"):
            file = f"{file}.json"

        self.file: str = file
        self.log = lambda text: log.info(f"[Config: {self.file}] {text}")

        JsonDB.active_config.append(file)

        # Automatically load config from file if exist
        if Path(self.file).exists() and Path(self.file).is_file():
            self.log(f"Auto-loading config from {self.file} since it exists")
            if is_lock_file_exist(Path(self.file)):
                self.log("Config file is locked, waiting for it to be unlocked")
                while is_lock_file_exist(Path(self.file)):
                    time.sleep(0.1)
                self.log("Config file is unlocked, loading config")
            self.read_database()
        else:
            # Create the file to avoid traceback during read_config() call
            with open(self.file, "w") as config:
                config.write("{}")
            self.read_database()

        # Make sure changes are written upon exit
        atexit.register(self._on_exit)

    @staticmethod
    def _ensure_open(method):
        def wrapper(self, *args, **kwargs):
            if self.closed:
                raise RuntimeError("This config instance is already closed")
            return method(self, *args, **kwargs)

        return wrapper

    def _on_exit(self) -> None:
        if self.closed:
            self.log("Instance already closed, will not write config")
            return

        if not self.write_pending:
            self.log("No need to save changes")

        self.log("Writing unsaved changes")
        self.write_database()

    @_ensure_open
    def write_database(self) -> None:
        self.log(f"Writing config to {self.file}")
        with open(self.file, "w") as config_file:
            json.dump(self.data, config_file, indent=2)
        self.write_pending = False
        remove_lock_file(Path(self.file))

    @_ensure_open
    def read_database(self) -> None:
        self.log(f"Reading config from {self.file}")
        with open(self.file, "r") as config_file:
            self.data = json.load(config_file)

    @property
    def data(self) -> dict:
        return self._data

    @_ensure_open
    @data.setter
    def data(self, value) -> None:
        self._data = value
        self.write_pending = True
        write_lock_file(Path(self.file))

    def close(self) -> None:
        self.write_database()
        self.write_pending = False
        remove_lock_file(Path(self.file))
        JsonDB.active_config.remove(self.file)
        self.closed = True
