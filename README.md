# USD Gallery

A simple python script to allow you to render opensource OpenUSD Scenes with any renderer.

It requires you to download a list of OpenUSD scenes to render the whole gallery:

- USD Assets Working Group
https://github.com/usd-wg/assets

- Netflix Animation Studios ALab - USD Production Scene
https://dpel.aswf.io/alab/

- OpenPBR Shader Playground
https://dpel.aswf.io/openpbr-shader-playground/

## How to use it

### If you renderer supports usdrecord/Hydra

Open a shell with OpenUSD and the renderer you want to use, navigate to the `usdgallery` folder and just call:

```
python render.py "Your Renderer"
```

The script will run `usdrecord` on a predefined list of OpenUSD scenes, adding `Your Renderer.exr` and `Your Renderer_preview.jpg` in the specific output render, and it will update the `gallery.md` with a new column.

You can then commit your new images if you'd like.

Feel free to fix any issue in the python code, and to extend the list of scenes.

For the Karma renders, you can simply open the `Command Line Tools` shell from the Houdini Launcher, and from there, navigate to the `usdgallery` folder and call

```
hython render.py "Karma CPU"
```

### If you renderer doesn't support usdrecord/Hydra

Manually render into EXRs placed in the renders folder, matching the style of the other renderers.

Then just launch the script without any other argument:

```
python render.py
```

The script will search for all the EXRs, convert them to preview JPG and update the gallery.md file.