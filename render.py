#!/bin/env python3

import os
import sys
sys.dont_write_bytecode = True
import subprocess
import shutil
import tempfile
from pathlib import Path

scenes_groups = {
    "usd-wg-assets": {
        "ar_path":"C:/Users/paolo/Desktop/code/assets",
        "scenes": {
            "shaderball_glass":{
                "filepath":"./custom_scenes/shaderball_glass.usda",
                "camera":"camera",
            },
            "shaderball_gold":{
                "filepath":"./custom_scenes/shaderball_gold.usda",
                "camera":"camera",
            },
            "chess_board":{
                "filepath":"./custom_scenes/chess_board.usda",
                "camera":"renderCam",
            }
        }
    },
    "alab": {
        "ar_path":"C:/Users/paolo/Desktop/openusd/ALab-2.3.0",
        "scenes": {
            "stoat_and_remi":{
                "filepath":"./custom_scenes/stoat_and_remi.usda",
                "camera":"renderCam",
            },
        }
    },
    "openpbr-playground": {
        "ar_path":"C:/Users/paolo/Desktop/code/OpenPBRShaderPlayground",
        "scenes": {
            "openpbr-playground":{
                "filepath":"./custom_scenes/openpbr_playground.usda",
                "camera":"renderCam_mainCU",
            },
        }
    }
}

renders_folder = "renders"
purpose = "render"

if len(sys.argv) > 1:
    renderer = sys.argv[1]
    input_scene = ""
    if len(sys.argv) > 2:
        input_scene = sys.argv[2]

    for scene_group, scene_group_data in scenes_groups.items():
        custom_envs = os.environ.copy()
        custom_envs["PXR_AR_DEFAULT_SEARCH_PATH"] = scene_group_data["ar_path"]
        for scene_name, scene_data in scene_group_data["scenes"].items():
            if input_scene != "" and input_scene != scene_name:
                continue
            scene_file = scene_data["filepath"]
            output_folder = "{}/{}/{}".format(renders_folder, scene_group, scene_name, purpose)
            os.makedirs(output_folder, exist_ok=True)
            render_output = "{}/{}.exr".format(output_folder, renderer)
            usdrecord_args = [
                "usdrecord",
                "--colorCorrectionMode",
                "disabled",
                "--renderer",
                renderer,
                "--purposes",
                purpose,
                "--disableCameraLight",
                "--imageWidth",
                "1024",
                "--camera",
                scene_data["camera"],
                scene_file,
                render_output,
            ]
            print(" ".join(usdrecord_args))
            subprocess.run(usdrecord_args, shell=True, env=custom_envs)

# update gallery
renderers = []
gallery = {}
folder = Path('.')
for file_path in folder.glob("**/*.exr"):
    if len(file_path.parts) == 4:
        scene_group = file_path.parts[1]
        scene_name = file_path.parts[2]
        render_output = str(file_path)
        renderer = str(file_path.parts[3]).replace(".exr","")
        gallery_preview = render_output.replace(".exr","_preview.jpg")

        ffmpeg_args = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-apply_trc",
            "iec61966_2_1",
            "-i",
            render_output,
            gallery_preview
        ]
        print(" ".join(ffmpeg_args))
        subprocess.run(ffmpeg_args, shell=True)

        if scene_name not in gallery.keys():
            gallery[scene_name] = {}
        if renderer not in gallery[scene_name].keys():
            gallery[scene_name][renderer] = gallery_preview
        if renderer not in renderers:
            renderers.append(renderer)

gallery_content = "# Render Gallery\n\n"
gallery_content += "## {} purpose\n\n".format(purpose)
# gallery header
gallery_content += "|Scenes|"
for renderer in renderers:
    gallery_content += "{}|".format(renderer)
gallery_content += "\n"
gallery_content += "|-|"
for renderer in renderers:
    gallery_content += "-|"
gallery_content += "\n"

for scene_name in gallery.keys():
    gallery_content += '|{}|'.format(scene_name)
    for renderer in renderers:
        if renderer in gallery[scene_name].keys():
            gallery_content += '<img src="{}" width="256">|'.format(gallery[scene_name][renderer])
        else:
            gallery_content += 'X|'
    gallery_content += "\n"
gallery_content += "\n"

with open("./gallery.md", "w", encoding="utf-8") as file:
    file.write(gallery_content)

