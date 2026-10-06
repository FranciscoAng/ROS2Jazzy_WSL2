FROM osrf/ros:jazzy-desktop

#COPY ./workspace .

RUN sudo apt update && sudo apt install ros-jazzy-turtlesim 
RUN sudo apt install python3-colcon-common-extensions
RUN sudo apt install ros-jazzy-joint-state-publisher-gui -y

WORKDIR /mobile_robot
#RUN apt-get update && apt-get install -y x11-apps