import os
import shutil


def find_files_with_extension(folder, extension):
    matching_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                file_stat = os.stat(file_path)

                file_size_bytes = os.path.getsize(file_path)
                file_size_mb = file_size_bytes / (1024 * 1024)  # Convert bytes to MB

                print(file_stat)

                matching_files.append((file_path, file_size_mb))
    return matching_files


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    else:
        return False


def move_or_copy_file(file_path, destination_folder, action='copy'):
    if not os.path.isfile(file_path):
        return False

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, os.path.basename(file_path))

    if action == 'cut':
        shutil.move(file_path, destination_path)
    else:
        shutil.copy(file_path, destination_path)

    return True


print(find_files_with_extension("testing-folder", "zip"))

