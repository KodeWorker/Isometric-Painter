import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

def get_root_dir(file_name=None):
    if file_name==None:
        return resource_path('') 
    else:
        return resource_path(file_name)

def get_asset_dir(file_name=None):
    root = get_root_dir()
    asset_dir = os.path.join(root, 'asset')
    
    if os.path.exists(asset_dir):
        if file_name==None:
            return asset_dir
        else:
            return os.path.join(asset_dir, file_name)
    else:
        raise ValueError('Error-001: missing directory "%s"!' %os.path.basename(os.path.abspath(asset_dir)))
