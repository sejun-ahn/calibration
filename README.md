# Camera Calibration Using Checkerboard

### Install OpenCV
```bash
pip install opencv-python
```

### 0. Prepare the video file
- Place the video file at main directory
- The `<video>` file must follow this naming format\
`<device>_<case>.<extension>`\
(Use an underscore `_` to separate `<device>` and `<case>`.)

### 1. Export frames from the video
```bash
python export.py <video>
```
- You should manually select the frames to be used for calibration and delete the rest
- You can set the step to jump by adding an argument like `--step 10` 
### 2. Perform camera calibration and save the result
```bash
python calibrate.py <video>
```
### 3. Clean up unnecessary files
```bash
python cleanup.py <video>
```