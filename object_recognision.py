from ultralytics import YOLO

# Load the exported ONNX model
onnx_model = YOLO("models/15.10.onnx")
path = 'image.png'
# Run inference
results = onnx_model(path)
results[0].show() # Show in file results
