FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
ENV TURTLEBOT3_MODEL=burger

RUN apt-get update && apt-get install -y \
    ros-jazzy-turtlebot3* \
    python3-opencv \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws
COPY src/ /ros2_ws/src/

RUN . /opt/ros/jazzy/setup.sh && \
    colcon build --packages-select turtlebot_vision_control

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

CMD ["bash", "-c", "source /ros2_ws/install/setup.bash && ros2 launch turtlebot_vision_control init.launch.py"]