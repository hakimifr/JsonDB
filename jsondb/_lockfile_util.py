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

import logging
import os

from pathlib import Path

log: logging.Logger = logging.getLogger(__name__)


def write_lock_file(file: Path) -> None:
    log.info(f"Creating lock file: '{file.as_posix()}.lock'")
    with open(f"{file.as_posix()}.lock", "w") as f:
        f.write(str(os.getpid()))


def remove_lock_file(file: Path) -> None:
    log.info(f"Removing lock file: '{file.as_posix()}.lock'")
    try:
        Path(f"{file.as_posix()}.lock").unlink()
    except FileNotFoundError:
        log.warning(f"Failed to remove lock file: '{file.as_posix()}.lock'")


def is_lock_file_exist(file: Path) -> bool:
    return Path(f"{file.as_posix()}.lock").exists()
