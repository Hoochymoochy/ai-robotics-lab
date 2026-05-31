import pybullet as p
import pybullet_data
import time

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("racecar/racecar.urdf", [0, 0, 0])
squareId = p.loadURDF("cube.urdf", [-5, 0, .5])

num_joints = p.getNumJoints(robotId)
joint_indices = [2, 3, 4, 5, 6, 7]
print("Number of joints:", num_joints)

slide = []
for i in joint_indices:  # Loop through the list
    joint_info = p.getJointInfo(robotId, i)
    joint_name = joint_info[1].decode("utf-8")
    print(f"Joint {i}: {joint_name}")
    
    slider = p.addUserDebugParameter(joint_name, -3.14, 3.14, 0)
    slide.append((i, slider))  # Store both index and slider

slider = p.addUserDebugParameter("Move all wheels", -50, 50, 0)
slide.append(([2, 3], slider))

while True:
    for joint_ids, slider_id in slide:
        value = p.readUserDebugParameter(slider_id)

        if isinstance(joint_ids, list):
            for joint in joint_ids:
                p.setJointMotorControl2(
                    robotId,
                    joint,
                    p.POSITION_CONTROL,
                    targetPosition=value
                )
        else:
            p.setJointMotorControl2(
                robotId,
                joint_ids,
                p.VELOCITY_CONTROL,
                targetVelocity=value,
                force=20
            )
    
    p.stepSimulation()
    time.sleep(1 / 240)