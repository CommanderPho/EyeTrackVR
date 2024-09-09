#!/usr/bin/env python

import os
import shutil

def remove_dir_if_exists(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

def remove_file_if_exists(path):
    if os.path.isfile(path):
        os.remove(path)

# Removing directories
remove_dir_if_exists('build')
remove_dir_if_exists('dist')
remove_dir_if_exists('EyeTrackApp/__pycache__')
remove_dir_if_exists('EyeTrackApp/app/__pycache__')
remove_dir_if_exists('EyeTrackApp/app/algorithms/__pycache__')

# Removing files
remove_file_if_exists('EyeTrackApp/eyetrack_settings.backup')
remove_file_if_exists('EyeTrackApp/eyetrack_settings.json')

print("Clean up completed.")
