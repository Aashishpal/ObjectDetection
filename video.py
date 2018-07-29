import cv2
from darkflow.net.build import TFNet
import numpy as np
import time

option = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolo.weights',
    'threshold': 0.15,
    'gpu': 1.0
}

tfnet = TFNet(option)
capture = cv2.VideoCapture('videos/dubai.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#frame_width = int( videoFile.get(cv2.CAP_PROP_FRAME_WIDTH))
#frame_height =int( videoFile.get( cv2.CAP_PROP_FRAME_HEIGHT)) 
out = cv2.VideoWriter('videos/output1.avi',fourcc,10.0, (1280,720))
colors = [tuple(255 * np.random.rand(3)) for i in range(10)]

while (capture.isOpened()):
    stime = time.time()
    ret, frame = capture.read()
    if ret:
        results = tfnet.return_predict(frame)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            frame = cv2.rectangle(frame, tl, br, color, 7)
            frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow('frame', frame)
        out.write(frame)
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        capture.release()
        out.release()
        cv2.destroyAllWindows()
	break
