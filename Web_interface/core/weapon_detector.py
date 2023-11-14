import torch
import cv2
import numpy as np



class WeaponDetector:
    def __init__(self, path_to_weights):
        self.model = torch.hub.load('yolov5', 'custom', path_to_weights, source='local')
        self.model.conf = 0.25
        self.model.iou = 0.45
        self.model.img = 640

    def detect(self, capture, every_kth_frame: int, output_fliepath):
        frame_index = 0
        results = []
        while True:
            ret, frame = capture.read()
            if not ret:
                break
            if frame_index % every_kth_frame:
                continue

            predicted = self.model(frame, size=640)
            conf = predicted.pandas().xyxy[0]['confidence'].max()
            if torch.isnan(torch.tensor([conf]))[0]:
                conf = 0
            results.append((conf, predicted))
        
            frame_index += 1

        results.sort(key = lambda x : x[0], reverse=True)

        results = results[:5]
        
        if 0 < len(results) < 5:
            results += [results[-1]]*(5 - len(results))

        for i in range(len(results)):
            cv2.imwrite(output_fliepath + f"image{i+1}.jpg", np.array(results[i][1].render()[0]))

        return len(results) and results[0][0] > self.model.conf        
    
    def Process(self, filepath, output_filepath):
        weapon_detector = WeaponDetector('weights/best.pt')
        cap = cv2.VideoCapture(filepath)
        return weapon_detector.detect(cap, 20, output_filepath)



