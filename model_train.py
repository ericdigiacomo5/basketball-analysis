from ultralytics import YOLO
import torch


if __name__ == '__main__':
    if torch.cuda.is_available():
        print("Avail")
    model = YOLO("yolo26n-pose.pt")
    results = model.train(data="data/nets-arena-clean/data.yaml", device='cuda', name="first-run", epochs=100)