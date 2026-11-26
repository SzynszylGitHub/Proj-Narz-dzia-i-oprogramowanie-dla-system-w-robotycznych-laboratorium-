import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
  set_tb3_model = SetEnvironmentVariable(name='TURTLEBOT3_MODEL', value='burger')

  tb3_fake_launch = IncludeLaunchDescription(
      PythonLaunchDescriptionSource(
          os.path.join(
              get_package_share_directory('turtlebot3_fake_node'),
              'launch',
              'turtlebot3_fake_node.launch.py',
          )
      )
  )

  teleop_node = Node(
      package='turtlebot_vision_control',
      executable='camera_teleop',
      name='camera_teleop_node',
      output='screen',
      parameters=[{'linear_speed': 0.2}],
  )

  return LaunchDescription([set_tb3_model, tb3_fake_launch, teleop_node])