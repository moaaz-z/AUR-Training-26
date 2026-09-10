from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    package_share = get_package_share_directory('workshop1')

    config_file = os.path.join(
        package_share,
        'config',
        'controller_params.yaml'
    )

    turtlesim = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim'
    )

    server = Node(
        package='workshop1',
        executable='task2_server',
        name='task2_server',
        parameters=[config_file]
    )

    client = Node(
        package='workshop1',
        executable='task2_client',
        name='task2_client'
    )

    return LaunchDescription([
        turtlesim,
        server,
        client
    ])
