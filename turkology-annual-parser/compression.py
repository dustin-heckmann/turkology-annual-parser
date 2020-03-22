import zipfile
from os import walk, makedirs
from os.path import join, relpath, basename
from zipfile import ZipFile

ZIP_DIR = '/ta-data'
ZIP_FILE = 'turkology_annual_export.zip'
ZIP_PATH = join(ZIP_DIR, ZIP_FILE)
RESOURCES_DIR = '/ta-data/export'


def create_zip_file(dump_file_names):
    ensure_dir_exists(ZIP_DIR)
    with ZipFile(ZIP_PATH, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file_handle:
        for root, dirs, files in walk(RESOURCES_DIR):
            for file in files:
                file_name = join(root, file)
                zip_file_handle.write(file_name, relpath(file_name, RESOURCES_DIR))
        for dump_file_name in dump_file_names:
            zip_file_handle.write(dump_file_name, basename(dump_file_name))


def ensure_dir_exists(dir):
    makedirs(dir, exist_ok=True)
