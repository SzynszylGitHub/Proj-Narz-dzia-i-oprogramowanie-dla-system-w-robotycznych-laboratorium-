#!/usr/bin/env bash
xhost +local:docker 2>/dev/null || true

docker build -t turtlebot_vision_control .
docker run --rm -it \
    --net=host \
    -e DISPLAY=$DISPLAY \
    -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
    -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    turtlebot_vision_control