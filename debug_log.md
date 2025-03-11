# Debug Log

## 2025-03-11

### 1. 

```
WARN[0000] The "XDG_RUNTIME_DIR" variable is not set. Defaulting to a blank string. 
WARN[0000] /home/zyb/ByteTrack/compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Running 1/1
 ✔ Container bytetrack  Created                                                                                                     0.0s 
Attaching to bytetrack
bytetrack  | 
bytetrack  | =====================
bytetrack  | == NVIDIA TensorRT ==
bytetrack  | =====================
bytetrack  | 
bytetrack  | NVIDIA Release 21.09 (build 26679335)
bytetrack  | 
bytetrack  | NVIDIA TensorRT 8.0.3 (c) 2016-2021, NVIDIA CORPORATION.  All rights reserved.
bytetrack  | Container image (c) 2021, NVIDIA CORPORATION.  All rights reserved.
bytetrack  | 
bytetrack  | https://developer.nvidia.com/tensorrt
bytetrack  | 
bytetrack  | This container image and its contents are governed by the NVIDIA Deep Learning Container License.
bytetrack  | By pulling and using the container, you accept the terms and conditions of this license:
bytetrack  | https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license
bytetrack  | 
bytetrack  | To install Python sample dependencies, run /opt/tensorrt/python/python_setup.sh
bytetrack  | 
bytetrack  | To install the open-source samples corresponding to this TensorRT release version run /opt/tensorrt/install_opensource.sh.
bytetrack  | To build the open source parsers, plugins, and samples for current top-of-tree on master or a different branch, run /opt/tensorrt/install_opensource.sh -b <branch>
bytetrack  | See https://github.com/NVIDIA/TensorRT for more information.
bytetrack  | WARNING: Detected NVIDIA NVIDIA GeForce RTX 4090 GPU, which is not yet supported in this version of the container
bytetrack  | ERROR: No supported GPU(s) detected to run this container
bytetrack  | 
Gracefully stopping... (press Ctrl+C again to force)
[+] Stopping 1/1
 ✔ Container bytetrack  Stopped                                                                                                     0.1s 
zyb@zyb-CORSAIR-VENGEANCE-i8100:~/ByteTrack$ 
```