import os

def get_root_dir(file_name=None):
    root = os.path.join(os.path.dirname(__file__), '..')
    if os.path.basename(os.path.abspath(root)) == 'src':
        if file_name==None:
            return root
        else:
            return os.path.join(root, file_name)
    else:
        raise ValueError('Error-001: "%s" is not root directory!' %os.path.basename(os.path.abspath(root)))

def get_asset_dir(file_name=None):
    root = get_root_dir()
    asset_dir = os.path.join(root, 'asset')
    
    if os.path.exists(asset_dir):
        if file_name==None:
            return asset_dir
        else:
            return os.path.join(asset_dir, file_name)
    else:
        raise ValueError('Error-002: missing directory "%s"!' %os.path.basename(os.path.abspath(asset_dir)))