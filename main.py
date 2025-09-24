from modal.image import Image
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import modal
from pydantic import BaseModel


image = modal.Image.from_registry(
    tag="nvidia/cuda:12.4.0-devel-ubuntu22.04",
    add_python="3.12"
).apt_install([
    "ffmpeg",
    "libgl1-mesa-glx",
    "wget",
    "libcudnn8",
    "libcudnn8-dev"
]).pip_install_from_requirements("requirements.txt").run_commands(["mkdir -p /usr/share/fonts/truetype/custom",
 "wget -O /usr/share/fonts/truetype/custom/Anton-Regular.ttf https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf",
 "fc-cache -f -v"
]).add_local_dir("asd","/asd",copy=True)

app = modal.App("ai-podcast-clipper",image=image)

volume = modal.Volume.from_name(
    "ai-podcast-clipper-model-cache", create_if_missing=True
)

mount_path = "/root/.cache/torch"

auth_scheme = HTTPBearer()

