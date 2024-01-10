# Line Tracking in Mixed Reality
### 1. Clone Repository
```bash
git clone -b develop https://github.com/kstavratis/mixed-reality-line-tracking.git
```
### 2. Install Buildozer
The instruction is [here](https://buildozer.readthedocs.io/en/latest/installation.html).
### 3. Build, Deploy, and Run
In the root of this repository, type the below commands:
```bash
buildozer android debug # Build
buildozer android deploy # Deploy
buildozer android run # Run
# or
buildozer android debug deploy run # All at once
```
### How to Debug
Either before or after running the application, type as below:
```bash
<USER_HOME>/.buildozer/android/platform/android-sdk/platform-tools/adb logcat -s "python"
# e.g. /home/sjkim/.buildozer/android/platform/android-sdk/platform-tools/adb logcat -s "python"
```
### Notes
* [Debugger mode](https://developer.android.com/studio/debug/dev-options) of the mobile phone should be enabled before deploy and run.
* The application does not include explicit asking of the camera permission, though it is needed. Please enable it before running the application.