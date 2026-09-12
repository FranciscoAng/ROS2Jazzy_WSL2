FROM osrf/ros:jazzy-desktop

#COPY ./workspace .

RUN sudo apt update && sudo apt install ros-jazzy-turtlesim 
RUN sudo apt install python3-colcon-common-extensions

WORKDIR /mobile_robot
#RUN apt-get update && apt-get install -y x11-apps