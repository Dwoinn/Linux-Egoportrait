# Linux Egoportrait
Linux Egoportrait adds a virtual webcam to your system that masks your background with a blur or image.
The new webcam will appear in the list of devices of your chat apps like Microsoft Teams, Zoom

This project is based on :
- [Google MediaPipe](https://github.com/google/mediapipe) for the body recognitions
- [pyfakewebcam](https://github.com/jremmons/pyfakewebcam) / video4linux2 for the virtual webcam
- [OpenCV](https://opencv.org/) for image processing

## Install
### dependencies
- Ubuntu/debian
  ``` bash
  sudo apt update
  sudo apt install python3 python3-pip v4l2loopback-dkms v4l-utils
  ```

- TODO Others

### Pip modules
``` bash
pip install -r requirements.txt
```

## Usage
Before start for the first time you need to create the virtual device :
``` bash
sudo modprobe v4l2loopback exclusive_caps=1 video_nr=7 card_label="Egoportrait"
```
(if the device /dev/video7 already exist, you can change the *video_nr* value, but don't forget to add the `--output` argument of Linux Egoportrait command)

### Basic start with blur background
``` bash
python3 main.py
```

### Arguments
`--help`: show help message and exit
`--width WIDTH` : Width of the input and output video (default : 1280)
`--height HEIGHT` : Height of the input and output video (default : 720)
`--input INPUT` : Input webcam id (default : 0)
`--output OUTPUT` : Output virtual webcam id (default : 7)
`--background-image BACKGROUND_IMAGE` : Path of the background image
`--background-name {datacenter,officespace1,officespace2,server-room-nightmare}` : Name of the buitin background image
`--level LEVEL` : Segmentation level (default : 0.75)

### Start with a different resolution
``` bash
python3 main.py --width 640 --height 480
```

### Chose a different input webcam
``` bash
python3 main.py --input 1
```

### Chose a different output virtual webcam id
The id need to be the same than the value chosen when creating the virtual device
``` bash
python3 main.py --output 3
```

### Start with a builtin background
``` bash
python3 main.py --background-name officespace2
```

### Start with a personal background
``` bash
python3 main.py --background-image /path/to/my/image.jpg
```
The following file formats are usaly supported (sometime may need to install the development library of the format on your system):
- Windows bitmaps - *.bmp, *.dib 
- JPEG files - *.jpeg, *.jpg, *.jpe 
- JPEG 2000 files - *.jp2 
- Portable Network Graphics - *.png 
- WebP - *.webp 
- Portable image format - *.pbm, *.pgm, *.ppm *.pxm, *.pnm 
- Sun rasters - *.sr, *.ras 
- TIFF files - *.tiff, *.tif 
- OpenEXR Image files - *.exr 
- Radiance HDR - *.hdr, *.pic 
- Raster and Vector geospatial data supported by GDAL 

### Change the detection sensibility
If you find that the contours of your body are not well detected, you can adjust the segmentation level (between 0 and 1. Close to 0 : ajusted, close to 1 : wider).
The default value is 0.75
``` bash
python3 main.py --level 0.1
```

## Troubleshoot
1. Sometimes an error `OSError: [Errno 22] Invalid argument` happen on start.
To resolve it, the solution is to remove the virtual device and recreate it.
    ``` bash
    sudo modprobe -r v4l2loopback
    sudo modprobe v4l2loopback exclusive_caps=1 video_nr=7 card_label="Egoportrait"
    ```
<br/>

2. If you start Linux Egoportrait while your chat application (e.g. Microsoft Teams) is running, `Egoportrait` webcam may not appear in the devices list. In this case, you need to restart your chat application.