import os
import shutil


def find_files_with_extension(folder, extension):
    """
    Recursively finds all files with a specified extension in a given folder.

    Args:
        folder (str): The folder path to search.
        extension (str): The file extension to look for (e.g., '.txt').

    Returns:
        list: A list of dictionaries, each containing file information.
              Dictionary keys: 'Name', 'Extension', 'Path', 'Size',
                               'Modification Time', 'Creation Time'.
    """
    matching_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                file_stat = os.stat(file_path)

                file_size_bytes = file_stat.st_size
                modification_time = file_stat.st_mtime
                creation_time = file_stat.st_ctime

                file_name, file_extension = os.path.splitext(file)

                file_info = {"Name": file_name, "Extension": file_extension,
                             "Path": file_path, "Size": file_size_bytes,
                             "Modification Time": modification_time,
                             "Creation Time": creation_time}

                matching_files.append(file_info)
    return matching_files


def delete_file(file_path):
    """
    Deletes a file if it exists.

    Args:
        file_path (str): The path of the file to delete.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    else:
        return False


def move_or_copy_file(file_path, destination_folder, action='copy'):
    """
    Moves or copies a file to a specified destination folder.

    Args:
        file_path (str): The path of the file to move/copy.
        destination_folder (str): The destination folder path.
        action (str, optional): 'copy' to copy the file, 'cut' or 'move' to move the file.
                                Defaults to 'copy'.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    if not os.path.isfile(file_path):
        return False

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, os.path.basename(file_path))

    if action == 'cut' or action == 'move':
        shutil.move(file_path, destination_path)
    else:
        shutil.copy(file_path, destination_path)

    return True


def open_file_or_folder(file_path, file=True):
    """
    Opens a file or folder using the default application.

    Args:
        file_path (str): The path of the file or folder to open.
        file (bool, optional): True if opening a file, False if opening a folder.
                               Defaults to True.

    Returns:
        bool: True if the file/folder was opened successfully, False otherwise.
    """
    try:
        if file:
            os.startfile(file_path)
        else:
            file_path = os.path.dirname(file_path)
            os.startfile(file_path)
        return True
    except OSError:
        return False


def rename_file(file_path, new_name):
    """
    Renames a file.

    Args:
        file_path (str): The path of the file to rename.
        new_name (str): The new name (without extension) for the file.

    Returns:
        bool: True if the file was renamed successfully, False otherwise.
    """
    if not os.path.isfile(file_path):
        return False

    directory = os.path.dirname(file_path)
    file_name, file_extension = os.path.splitext(file_path)
    new_file_path = os.path.join(directory, new_name + file_extension)

    try:
        os.rename(file_path, new_file_path)
        return True
    except OSError:
        return False

