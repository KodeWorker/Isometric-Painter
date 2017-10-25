import os
import sys
from shutil import rmtree, copytree

if __name__ == '__main__':
    
    project_dir = os.path.dirname(__file__)
    build_dir = os.path.join(project_dir, 'build')
    project_name = 'Isometric-Painter'
    
    # delete previous built files
    if os.path.exists(build_dir):
        rmtree(build_dir)

    # build from the source code
    os.system('pyinstaller \
              --windowed \
              --name=%s \
              --specpath=%s \
              --workpath=%s \
              --distpath=%s \
              %s' 
              
              %(project_name,
                build_dir,
                os.path.join(build_dir,'temp'),
                os.path.join(build_dir,'dist'),
                'src/main.py'))

    standalone_dir = os.path.join(build_dir,'dist', project_name)    
    
    # workaround for error: This application failed to start because it could not find or load the Qt platform plugin "windows" in "".
    copytree(os.path.join(standalone_dir, 'PyQt5', 'Qt', 'plugins', 'platforms'), os.path.join(standalone_dir, 'platforms'))
    copytree(os.path.join(project_dir, 'src', 'asset'), os.path.join(standalone_dir, 'asset'))
    
    # open the built executable
    if sys.platform == 'win32':
        os.system('start /d %s %s.exe' %(standalone_dir, project_name))
    elif sys.platform.startswith('linux'):
        os.system('%s' %os.path.join(standalone_dir, project_name))