from pathlib import Path

# GPL-3.0 License header
license_header = """\
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
"""

IGNORE_DIRS: list[str] = [".venv"]


def add_license_header(file_path) -> bool:
    with open(file_path, "r+") as f:
        content = f.read()

        if license_header in content:
            print(f"! License header already exists in {file_path}")
            return False

        f.seek(0, 0)
        f.write(license_header.lstrip("\n") + "\n" + content)
        return True


for file in Path(".").rglob("*.py"):
    try:
        if str(list(file.parents)[-2]) in IGNORE_DIRS:
            continue
    except IndexError:
        pass

    if file.name == "add_license.py":
        print("-> Skipping this file")
        continue

    add_license_header(file)
    print(f"-> Added license header to {file}")
