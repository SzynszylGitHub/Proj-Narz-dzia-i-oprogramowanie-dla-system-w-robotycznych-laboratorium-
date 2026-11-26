#!/usr/bin/env python3
import cv2
from cv_bridge import CvBridge
from geometry_msgs.msg import Point, Twist
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class CameraTeleopNode(Node):

  def __init__(self):
    super().__init__('camera_teleop_node')

    # Parametry konfiguracyjne węzła
    self.declare_parameter('linear_speed', 0.15)
    self.declare_parameter('box_size', 40)
    self.declare_parameter('use_camera', False)
    self.declare_parameter('image_topic', '/image_raw')

    self.linear_speed = float(self.get_parameter('linear_speed').value)
    self.box_size = int(self.get_parameter('box_size').value)
    self.use_camera = bool(self.get_parameter('use_camera').value)
    image_topic = str(self.get_parameter('image_topic').value)

    self.window_name = 'TurtleBot Control'
    self.point = None
    self.img_height = 512
    self.img_width = 700
    self.target_linear_x = 0.0

    # Publikatory: współrzędne kliknięcia (/point) i sterowanie (/cmd_vel)
    self.point_publisher = self.create_publisher(Point, '/point', 10)
    self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    # Inicjalizacja okna OpenCV i obsługi myszy
    cv2.namedWindow(self.window_name)
    cv2.setMouseCallback(self.window_name, self.mouse_callback)

    if self.use_camera:
      self.bridge = CvBridge()
      self.subscription = self.create_subscription(
          Image, image_topic, self.camera_callback, 10
      )
      self.get_logger().info(f'Tryb kamery aktywny. Temat: {image_topic}')
    else:
      # Timer odświeżający czarne okno sterowania (30 FPS)
      self.ui_timer = self.create_timer(0.033, self.black_screen_callback)
      self.get_logger().info(
          'Tryb czarnego ekranu aktywny. Kliknij powyżej/poniżej linii.'
      )

    # Timer publikujący komendy prędkości na /cmd_vel (10 Hz)
    self.cmd_timer = self.create_timer(0.1, self.cmd_timer_callback)

  def mouse_callback(self, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      self.point = (x, y)

      point_msg = Point()
      point_msg.x = float(x)
      point_msg.y = float(y)
      point_msg.z = 0.0
      self.point_publisher.publish(point_msg)

      mid_y = self.img_height // 2
      if y < mid_y:
        self.target_linear_x = self.linear_speed
        self.get_logger().info(f'Klik ({x}, {y}) -> PRZOD')
      elif y > mid_y:
        self.target_linear_x = -self.linear_speed
        self.get_logger().info(f'Klik ({x}, {y}) -> TYL')
      else:
        self.target_linear_x = 0.0

    elif event == cv2.EVENT_RBUTTONDOWN:
      self.point = None
      self.target_linear_x = 0.0
      self.get_logger().info('STOP (PPM)')

  def render_interface(self, frame):
    self.img_height, self.img_width, _ = frame.shape
    mid_y = self.img_height // 2

    # Linia środka ekranu i etykiety
    cv2.line(frame, (0, mid_y), (self.img_width, mid_y), (0, 255, 255), 2)
    cv2.putText(
        frame,
        'PRZOD (LPM)',
        (15, mid_y - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2,
    )
    cv2.putText(
        frame,
        'TYL (LPM) | STOP (PPM)',
        (15, mid_y + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2,
    )

    # Rysowanie kwadratu w miejscu kliknięcia
    if self.point is not None:
      half = self.box_size // 2
      cv2.rectangle(
          frame,
          (self.point[0] - half, self.point[1] - half),
          (self.point[0] + half, self.point[1] + half),
          (0, 255, 0),
          3,
      )

    cv2.imshow(self.window_name, frame)
    cv2.waitKey(1)

  def black_screen_callback(self):
    # Czysty czarny obraz (512x700) jak w Zadaniu 3 z zajęć
    black_frame = np.zeros((512, 700, 3), np.uint8)
    self.render_interface(black_frame)

  def camera_callback(self, image_data: Image):
    cv_image = self.bridge.imgmsg_to_cv2(image_data, 'bgr8')
    self.render_interface(cv_image)

  def cmd_timer_callback(self):
    msg = Twist()
    msg.linear.x = self.target_linear_x
    msg.angular.z = 0.0
    self.cmd_publisher.publish(msg)


def main(args=None):
  rclpy.init(args=args)
  node = CameraTeleopNode()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  finally:
    node.cmd_publisher.publish(Twist())
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()