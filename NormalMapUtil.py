bl_info = {
    "name": "Normal Map Utility",
    "author": "Ed O'Connell (llennoco)",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Image Editor",
    "description": "Simple tool for reconstructing normal maps in the image editor.",
    "warning": "Written by an ape.",
    "category": "Image"
}


import bpy
import numpy as np

def NmapCalc(input_image):
    input_image.colorspace_settings.name = 'Non-Color'
    output_image_name = input_image.name

    w, h = input_image.size
    pixel_data = np.zeros((w, h, 4), 'f')
    input_image.pixels.foreach_get(pixel_data.ravel())
    Nmap_props = bpy.context.scene.nmap_props
    
    if Nmap_props.normaltype == 'XYA':       
        X = pixel_data[:, :, 3]
        Y = pixel_data[:, :, 1]
    elif Nmap_props.normaltype == 'XY':
        X = pixel_data[:, :, 0]
        Y = pixel_data[:, :, 1]
    elif Nmap_props.normaltype == 'CUSTOM':
        X = pixel_data[:, :, int(Nmap_props.customx)]
        Y = pixel_data[:, :, int(Nmap_props.customy)]
    
    nx = (X*2-1)
    ny = (Y*2-1)
    
    pixel_data[:, :, 0] = X
    pixel_data[:, :, 1] = Y
    pixel_data[:, :, 2] = (np.sqrt(np.clip((1.0 - np.hypot(nx,ny)),0.0,1.0)*0.5+0.5))
    pixel_data[:, :, 3] = 1.0

    output_image = bpy.data.images[output_image_name]
    output_image.pixels.foreach_set(pixel_data.ravel())
    output_image.update()
    

class NormalPanelProp(bpy.types.PropertyGroup):
    normaltype : bpy.props.EnumProperty(name="Type",description="Conversion Type.",items=[ ("XYA", "XY Alpha (Pink)", ""),("XY", "XY (Yellow)", ""),("CUSTOM", "Custom", ""),])
    customx : bpy.props.EnumProperty(name="X",description="X Channel",items=[ ("0", "Red", ""),("1", "Green", ""),("2", "Blue", ""),("3", "Alpha", ""),])
    customy : bpy.props.EnumProperty(name="Y",description="Y Channel",items=[ ("0", "Red", ""),("1", "Green", ""),("2", "Blue", ""),("3", "Alpha", ""),])

class NormalMapTools(bpy.types.Operator):
    bl_idname = "image.nmaputil"
    bl_label = "Convert Normalmap"
    bl_description = "Convert image using current config."
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.space_data.image

    def execute(self, context):
        NmapCalc(bpy.context.space_data.image)
        return {'FINISHED'}

class NormalMapToolPanel(bpy.types.Panel):
    bl_idname = "IMAGE_PT_my_panel"
    bl_label = "Normalmap Utility"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Normal map Utility"

    def draw(self, context):
        layout = self.layout
        props = context.scene.nmap_props
        box = layout.box()
        box.prop(props, 'normaltype')
        if bpy.context.scene.nmap_props.normaltype == 'CUSTOM':
                    box = layout.box()
                    box.label(text="Custom Config", icon='PREFERENCES')
                    box.prop(props, 'customx')
                    box.prop(props, 'customy')                  
        box = layout.box()
        box.operator("image.nmaputil", text="Convert")
        box.operator("image.reload", text="Revert")
        row = box.row()
        row.operator("image.save_as", text="Save as")
        row.operator("image.save", text="Overwrite")
        
classes = (NormalMapTools,NormalPanelProp,NormalMapToolPanel)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.nmap_props = bpy.props.PointerProperty(type= NormalPanelProp)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.nmap_props


if __name__ == "__main__":
    register()
