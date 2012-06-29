bl_info = {
    "name": "ReplaceObjects",
    "description": "Control panel for replacing "
    "(animated) objects with group instances",
    "author": "Francesco Siddi",
    "version": (0, 1),
    "blender": (2, 56, 0),
    "location": "Properties Panel",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy
from bpy.props import (FloatProperty, BoolProperty, 
FloatVectorProperty, StringProperty, EnumProperty)

bpy.app.debug = 1

DUPLIGROUP_NAME = 'robot_sim'

##  Convenience variables
context = bpy.context
scene = context.scene
selected_objects = bpy.context.selected_objects

##  Debug print function

def dprint(input):
    if bpy.app.debug == 1:
        print(input)
    else:
        pass
                
def ReplaceObject(selection):
    
    if DUPLIGROUP_NAME in bpy.data.groups:
    
        for obj_src in selection:

            dprint(obj_src.name)

            ##  We do not really to copy rotation and location, since we will 
            ##  copy the whole animation data from the source object
            ##
            ##  bpy.ops.object.add(location=(ob.location), 
            ##  rotation=(ob.rotation_euler))

            obj_dst = bpy.data.objects.new(name=obj_src.name, object_data=None)
            scene.objects.link(obj_dst)
            obj_dst.dupli_type = 'GROUP'
            obj_dst.dupli_group = bpy.data.groups[DUPLIGROUP_NAME]


            ##  obj_dst.location = obj_src.location

            ##  Then we copy the animation data from the source object

            if obj_src.animation_data:
                obj_dst.animation_data_create()
                obj_dst.animation_data.action = obj_src.animation_data.action
    else:
        print("No dupligroup called", DUPLIGROUP_NAME)


ReplaceObject(selected_objects)


class ReplaceObjectsPanel(bpy.types.Panel):
    bl_label = "Replace Objects"
    bl_idname = "SCENE_PT_replaceObjects"
    bl_context = "scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(" GROUP: ", icon = 'GROUP')
        
        ob = context.active_object
        row = layout.row()
        row.label(text="", icon='OBJECT_DATA')
        row.prop(ob, "name", text="")
        
        row = layout.row()
        row.label(text=ob.name)
        ## row.prop(ob, "dupli_group", text="Group")
        

def register():
    bpy.types.Scene.DupliGroupName = StringProperty(
            name="name_of_dupligroup",
            default="",
            description="Name of the dupligroup to instance")

    bpy.utils.register_class(ReplaceObjectsPanel)
    
def unregister():
    del bpy.types.Scene.DupliGroupName
    bpy.utils.unregister_class(ReplaceObjectsPanel)


if __name__ == "__main__":
    register()