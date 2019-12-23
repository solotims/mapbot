import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

distance  = {
    'side': 0,
    'front': 0,
    }
limit = 2

def update(msg):
    distance['side'] = min(msg.ranges[0:40])
    distance['front'] = min(msg.ranges[320:400])

def handle():
     global error
     error = limit - distance['side']
     if distance['front'] <= limit:
          return 0
     else:
          return 1 

if __name__ == '__main__':
    rospy.init_node('base_node')
    move = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
    subscriber = rospy.Subscriber('/base_scan', LaserScan, update)
    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
       msg = Twist()
       if handle() == 0:
            msg.linear.x = 0
            msg.angular.z = 1
       else:
            msg.linear.x = 1 
            msg.angular.z = 10 * error

       print str(distance['front']) , " < front | side > ",  str(distance['side']) 
       move.publish(msg)
       rate.sleep()


