import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


class ImagePostprocessorNode(Node):
    """Subscribes to a raw/color Image topic, applies OpenCV postprocessing,
    and publishes the resulting Image."""

    def __init__(self) -> None:
        super().__init__('image_postprocessor')

        # Declare parameters so topics and thresholds can be configured at runtime
        self.declare_parameter('input_topic', '/camera/image')
        self.declare_parameter('output_topic', '/camera/image_processed')
        self.declare_parameter('canny_low', 50)
        self.declare_parameter('canny_high', 150)

        input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        output_topic = self.get_parameter('output_topic').get_parameter_value().string_value

        self.bridge = CvBridge()

        # QoS depth of 10 is standard for camera streams; adjust if dropping frames
        self.subscription = self.create_subscription(
            Image,
            input_topic,
            self.image_callback,
            10,
        )
        self.publisher = self.create_publisher(Image, output_topic, 10)

        self.get_logger().info(
            f"Subscribed to '{input_topic}', publishing processed images to '{output_topic}'"
        )

    def postprocess_frame(self, cv_image):
        """Apply postprocessing steps to an OpenCV BGR image."""
        canny_low = self.get_parameter('canny_low').get_parameter_value().integer_value
        canny_high = self.get_parameter('canny_high').get_parameter_value().integer_value

        # Example pipeline: grayscale -> smooth noise -> detect edges
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
        edges = cv2.Canny(blurred, canny_low, canny_high)
        return edges

    def image_callback(self, msg: Image) -> None:
        try:
            # Convert ROS Image message to OpenCV BGR format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except CvBridgeError as exc:
            self.get_logger().error(f"cv_bridge conversion failed: {exc}")
            return

        processed = self.postprocess_frame(cv_image)

        try:
            # Single-channel edge image uses 'mono8' encoding
            out_msg = self.bridge.cv2_to_imgmsg(processed, encoding='mono8')
        except CvBridgeError as exc:
            self.get_logger().error(f"Failed to convert processed image back: {exc}")
            return

        # Preserve original timestamp and frame_id for TF/sync alignment
        out_msg.header = msg.header
        self.publisher.publish(out_msg)
        cv2.imshow("Color Segmentation", processed)
        cv2.waitKey(1)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ImagePostprocessorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()