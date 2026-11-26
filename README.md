# TurtleBot3 Vision Control (ROS 2 Jazzy)

Projekt realizujący sterowanie robotem mobilnym **TurtleBot3** za pomocą interfejsu graficznego opartego o bibliotekę **OpenCV** oraz zdarzenia myszy, uruchomionego w lekkim środowisku symulacyjnym **RViz2** (`turtlebot3_fake_node`).

## Architektura systemu

* **Węzeł główny (`camera_teleop_node`):** napisany w Pythonie (`rclpy`), wyświetla panel sterowania OpenCV (512×700 px) podzielony poziomą żółtą linią na dwie strefy oraz publikuje komendy ruchu.
* **Publikowane tematy:**
  * `/cmd_vel` (`geometry_msgs/msg/Twist`) — zadana prędkość liniowa $v_x$ publikowana z częstotliwością 10 Hz.
  * `/point` (`geometry_msgs/msg/Point`) — współrzędne $(x, y)$ ostatniego kliknięcia w oknie interfejsu.
* **Parametry ROS 2:**
  * `linear_speed` (domyślnie `0.2` m/s) — prędkość jazdy do przodu i do tyłu.
  * `box_size` (domyślnie `40` px) — rozmiar znacznika rysowanego w miejscu kliknięcia.
* **Automatyzacja (`init.launch.py`):** uruchamia jednocześnie zmienną środowiskową `TURTLEBOT3_MODEL=burger`, węzeł symulacji odometrii `turtlebot3_fake_node` z wizualizacją w **RViz2** oraz węzeł sterujący `camera_teleop_node`.

## Sterowanie w oknie OpenCV

* **Lewy przycisk myszy (LPM) powyżej żółtej linii:** jazda do przodu (`+linear_speed`).
* **Lewy przycisk myszy (LPM) poniżej żółtej linii:** jazda do tyłu (`-linear_speed`).
* **Prawy przycisk myszy (PPM):** natychmiastowe zatrzymanie robota (`0.0` m/s).

## Uruchomienie (Docker — zalecane)

Wymagany zainstalowany Docker z obsługą GUI (X11 / WSLg). W głównym katalogu repozytorium wykonaj:

```bash
bash run.sh