# ROS 2 Self-Study: Minimal Publisher/Subscriber

My first ROS 2 project, built while self-teaching ROS 2 fundamentals
in Python. Based on the standard ROS 2 publisher/subscriber pattern, adapted
for a robotic-arm context.

## What it does
- `robot_publisher.py` publishes a simulated joint-angle command on the
  `robot_chatter` topic every 0.5s, cycling through 0, 45, 90, 135 degrees
- `robot_subscriber.py` listens on `robot_chatter`, parses each message, and
  validates it (format, numeric value, and range), logging valid targets and
  rejecting malformed ones
- Both nodes shut down gracefully on Ctrl+C

## Message format
Messages are `std_msgs/msg/String` in the form `<joint_name>:<angle_in_degrees>`,
e.g. `joint_1:45.0`.

## Background
Coming from a Java OOP background, this project was my entry point into
ROS 2's node-based architecture in Python (`rclpy`). Specifically, I mapped
familiar class/inheritance concepts onto ROS 2 node design.

## Requirements
- ROS 2 (Python, `rclpy`) — tested on Humble
- Python 3

## Running
Open two terminals, sourcing ROS 2 in each first (replace `<distro>`):
```bash
source /opt/ros/<distro>/setup.bash
```

Terminal 1:
```bash
python3 robot_publisher.py
```

Terminal 2:
```bash
python3 robot_subscriber.py
```

The publisher logs `Published: "joint_1:0.0"`, then 45.0, 90.0, 135.0, repeating.
The subscriber logs `Received: joint_1 target = 0.0 deg` for each valid message,
and logs a `Malformed message` error for bad input instead of crashing.

## Next steps
Currently extending this foundation with:
- MoveIt2 motion planning
- Action-based (asynchronous) task execution
- Vision-based error detection and recovery

## Author
Emilio Habib | LAU Mechatronics Engineering student
