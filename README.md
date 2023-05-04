# Reconfigurable-Pneumatic-System

The Timed Rebeca model and written safety properties.
The Python codes augment attacks in the Timed Rebeca model. The attacks include compromised version of the components and false data injections.



The system has two cylinders, CylinderA and CylinderB. Each cylinder is controlled by a dedicated controller to regulate the movement in either left-right or up-down directions. The timing of the movement for cylinders can differ based on the direction of the
movement. The controllers are responsible for coordinating the movements in the correct sequence and timing that involve pick-and-place operations.
The motion plan is moving the cylinders from the initial position (location X) to the target position (location Y), and then moving back to the initial position. In this case, each movement takes 2 units of time. The desired sequence of movements of the cylinders is as follows: (1) CylinderB moves
down, (2) CylinderB moves up, (3) CylinderA moves right, (4) CylinderB moves down and (5) then up, (6) CylinderA moves left.
