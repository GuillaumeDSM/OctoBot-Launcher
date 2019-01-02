#  Drakkar-Software OctoBot-Launcher
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

import argparse
import importlib
import logging
import os
import sys

import requests

from launcher import GITHUB_RAW_CONTENT_URL, LAUNCHER_GITHUB_REPOSITORY, LAUNCHER_PATH

# should have VERSION_DEV_PHASE
LAUNCHER_URL = f"{GITHUB_RAW_CONTENT_URL}/{LAUNCHER_GITHUB_REPOSITORY}/dev/{LAUNCHER_PATH}"

LAUNCHER_FILES = ["__init__.py", "launcher_app.py", "launcher_controller.py", "app_util.py"]

sys.path.append(os.path.dirname(sys.executable))


def update_launcher(force=False):
    for file in LAUNCHER_FILES:
        create_launcher_files(f"{LAUNCHER_URL}/{file}", f"{LAUNCHER_PATH}/{file}", force=force)
    logging.info("Launcher updated")


def create_launcher_files(file_to_dl, result_file_path, force=False):
    file_content = requests.get(file_to_dl).text
    directory = os.path.dirname(result_file_path)

    if not os.path.exists(directory) and directory:
        os.makedirs(directory)

    file_name = result_file_path
    if (not os.path.isfile(file_name) and file_name) or force:
        with open(file_name, "w") as new_file_from_dl:
            new_file_from_dl.write(file_content)


def start_launcher(args):
    if args.version:
        print(LAUNCHER_VERSION)
    else:
        if args.update_launcher:
            update_launcher(force=True)
        elif args.update:
            LauncherApp.update_bot()
        elif args.export_logs:
            LauncherApp.export_logs()
        else:
            LauncherApp()


logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='OctoBot - Launcher')
parser.add_argument('-v', '--version', help='show OctoBot Launcher current version',
                    action='store_true')
parser.add_argument('-u', '--update', help='update OctoBot with the latest version available',
                    action='store_true')
parser.add_argument('-l', '--update_launcher', help='update OctoBot Launcher with the latest version available',
                    action='store_true')
parser.add_argument('-e', '--export_logs', help="export Octobot's last logs",
                    action='store_true')

args = parser.parse_args()

update_launcher()

try:
    from launcher.launcher_app import *
except ImportError:
    importlib.import_module("launcher.launcher_app")

start_launcher(args)
