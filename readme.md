Run on Pyhton3.9 + OpenCV

Click the corresponding image to link to demo video

6/7/2021
- Integrate offline motion planner with the ball tracking UI. 

[![BallTracking + IK](https://github.com/tanat44/PingpongBallTracker/blob/master/doc/fkPlotCv.jpg)](https://youtu.be/clzRVqpBrZ4)

5/7/2021
- Create offline motion planner by pre-computing a look-up table for world-coordinate and join-coordinate. 
- Modify ```Experiment/inverse kinematic.py``` into ```MotionPlanner.py```. 

[![Offline Motion Planner](https://github.com/tanat44/PingpongBallTracker/blob/master/doc/motionPlanner210705.PNG)]()

2/7/2021
- Add Perspective correction.
- Organize controls in tab UI.
- Predict hitting point (light blue line)
- Predict future hitting frames

[![Perspective Correction](https://github.com/tanat44/PingpongBallTracker/blob/master/doc/perspectiveCorrection210702.PNG)]()

1/7/2021
Add PyQt UI for easier parameter tuning

[![Pingpong UI](https://github.com/tanat44/PingpongBallTracker/blob/master/doc/balldetectoroi210701.PNG)](https://youtu.be/TumrMjXR5lo)

17/6/2021
Ball Tracking

[![Tracking Demo](https://github.com/tanat44/PingpongBallTracker/blob/master/doc/tracking210617.PNG)](https://youtu.be/EJ_SHeF628E)

The original tracking idea was developed by Ahx.

    https://stackoverflow.com/questions/63730808/golf-ball-tracking-in-python-opencv-with-different-color-balls 

I modified the tracking to suit orange pingpong ball and to make use of previous frame information.