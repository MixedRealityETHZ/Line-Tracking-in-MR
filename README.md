# Mixed Reality Tracking

## Installation for C++

### Building

```
mkdir build
cd build
cmake ..
make
```

### Running

**To run on a test video, execute:**

`
./proj
`

## Python support

### Creating a Wheel File

**To create a wheel file inside the dist folder:**

`
python setup.py bdist_wheel
`

**Install it using pip:**
`
pip install dist/*
`

**To test on a video, run:**
`
python test.py
`

### Modes of visualization

To visualize tracked lines (including old ones), set `VIS_TRACK` to True inside the main file.
