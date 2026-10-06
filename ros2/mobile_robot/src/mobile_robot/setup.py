import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'mobile_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        #Include launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        #Include URDF / XACRO
        (os.path.join('share', package_name, 'models'), glob(os.path.join('model', '*.urdf')) + glob(os.path.join('model', '*.xacro'))),
        #Include meshes (.STL or .DAE)
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
