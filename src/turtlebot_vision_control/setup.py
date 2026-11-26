from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'turtlebot_vision_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
        (
            os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.[pxy][yma]*')),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='szynszyl',
    maintainer_email='theszynszyl@gmail.com',
    description=(
        'Interfejs sterowania robotem TurtleBot3 za pomoca klikniec mysza'
    ),
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_teleop = turtlebot_vision_control.node:main',
        ],
    },
)