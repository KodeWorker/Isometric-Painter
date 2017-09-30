import os
from shutil import rmtree, copytree

if __name__ == '__main__':
    
    project_dir = os.path.dirname(__file__)
    src_dir = os.path.join(project_dir, 'src')
    build_dir = os.path.join(project_dir, 'build')
    project_name = 'Isometric-Painter'
    
    # delete previous built files
    if os.path.exists(build_dir):
        rmtree(build_dir)

    # build from the source code
    os.system('pyinstaller --windowed --name %s --specpath %s --workpath=%s --distpath=%s %s' 
              %(project_name, build_dir, os.path.join(build_dir,'temp'), os.path.join(build_dir,'dist'), 'src/main.py'))
    standalone_dir = os.path.join(build_dir,'dist', project_name)    
    
    # workaround for error: This application failed to start because it could not find or load the Qt platform plugin "windows" in "".
    copytree(os.path.join(standalone_dir, 'PyQt5', 'Qt', 'plugins', 'platforms'), os.path.join(standalone_dir, 'platforms'))
    
    # open the built exicutable
    os.system('start /d %s %s.exe' %(standalone_dir, project_name))