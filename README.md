# Blender Normalmap Utility
Blender addon to reconstruct normal maps in Blender, adds a small UI panel to Blender's image editor. 

As games compress their normalmaps and so when extracted they lack the Z channel as it is computed on the fly. Normalmap Utils will recreate the normalmap, generating the Z channel from the X&Y data.
The channel this data is in can vary depending on the format they were converted from (BC3,DXT5..) and so there are two common options provided in the drop-down as well as a custom selection mode for extra support.

![295007e9c2912af4d7b1d81f0601d94c](https://github.com/llennoco22/blender_normalmap_utils/assets/38115052/3805c52a-a82e-4a9f-9681-77da7333f075)


**Important:
After converting you must save your result will revert once Blender's cache clears.**


