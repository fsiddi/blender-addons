# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "LodToggle",
    "description": "Control panel for activating "
    "the cameras available in a scene",
    "author": "Francesco Siddi",
    "version": (0, 5),
    "blender": (2, 59, 0),
    "location": "Properties Panel",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy
from bpy.props import (FloatProperty, BoolProperty, 
FloatVectorProperty, StringProperty, EnumProperty)


scene = bpy.context.scene

cameras = []
for ob in bpy.data.objects:
    if ob.type == 'CAMERA':
        print (ob.name)
        cameras.append(ob)


#  Colors class for terminal terminal output
class pcolor:
    BROWN = '\033[90m'
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.BROWN = ''
        self.PINK = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.ENDC = ''


#  Function for printing to terminal with LodToggle message at the beginning
def PowerPrint (message):
    print(pcolor.BROWN + "LodToggle: " + pcolor.ENDC + message)
    return
             
            
class CameraSelectorPanel(bpy.types.Panel):
    bl_label = "Camera Selector"
    bl_idname = "SCENE_PT_cameraselector"
    bl_context = "scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if len(cameras) > 0:
            for camera in cameras:
                row = layout.row()
                row.label(camera.name)
                btn = row.operator("cameraselector.set_scene_camera", 
                text="res", icon='FILE_REFRESH')
                btn.chosen_camera = camera.name
        else:
            layout.label("No cameras in this scene") 
        

class SetSceneCamera(bpy.types.Operator):
    bl_idname = "cameraselector.set_scene_camera"
    bl_label = "Make this object a camera"
    bl_description = "Make this object a camera"
    chosen_camera = bpy.props.StringProperty()

    def execute(self, context):
        
        chosen_camera = self.chosen_camera
    
        try: 
            scene.camera = bpy.data.objects[chosen_camera]
            #print (chosen_camera)
            #PowerPrint("CHANGE " + str(item_name) + " to " + new_group)
        except:
            #self.report({'WARNING'}, "Group %s not found" % new_group.upper())
            self.report({'WARNING'}, "Fail")

        return {'FINISHED'}



def register():
    bpy.utils.register_class(SetSceneCamera)
    bpy.utils.register_class(CameraSelectorPanel)
    
def unregister():
    bpy.utils.unregister_class(SetSceneCamera)
    bpy.utils.unregister_class(CameraSelectorPanel)
    
if __name__ == "__main__":
    register()
