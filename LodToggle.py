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
    "description": "Control panel for managing "
    "groups contained in linked libraries",
    "author": "Olivier Amrein, Francesco Siddi",
    "version": (0, 5),
    "blender": (2, 53, 0),
    "location": "Properties Panel",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy
from bpy.props import (FloatProperty, BoolProperty, 
FloatVectorProperty, StringProperty, EnumProperty)


scene = bpy.context.scene


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
    
#  Generic function to toggle across 3 different model resolutions
def SetProxyResolution(elem,target_resolution):

    obj = bpy.data.objects[elem.name]

    try: 
       dupgroup_name = obj.dupli_group.name
    except: 
        return
    
    root = dupgroup_name[:-3]
    ext = dupgroup_name[-3:]
    new_group = root + target_resolution

    if ext in {'_hi', '_lo', '_me'}:
        try: 
            obj.dupli_group = bpy.data.groups[new_group]
            #print("PowerLib: CHANGE " + str(elem) + " to " + new_group)
        except:
            PowerPrint("Group " + pcolor.GREEN + new_group + pcolor.ENDC + " not found")
            
            
class LodTogglePanel(bpy.types.Panel):
    bl_label = "LodToggle"
    bl_idname = "SCENE_PT_lodtoggle"
    bl_context = "scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        ob = bpy.context.active_object
            
        if ob and ob.dupli_type == 'GROUP':
            group = ob.dupli_group
            group_name = group.name  # set variable for group toggle
            group_objs = bpy.data.groups[group.name].objects

            row = layout.row()
            row.label(" GROUP: " + group.name, icon = 'GROUP')
            
            box = layout.box()         
        
  
            resolution = str(ob.dupli_group.name)[-3:]
            if resolution in {'_hi', '_lo', '_me'}:

                res = resolution[-2:].upper()

                subgroup = box.operator("lodtoggle.toggle_subgroup_res",
                text=res, icon='FILE_REFRESH')
                subgroup.item_name = bpy.context.active_object.name
                subgroup.group_name = group.name
                        
        else:
            layout.label(" Select a group")            


class ToggleSubgroupResolution(bpy.types.Operator):
    bl_idname = "lodtoggle.toggle_subgroup_res"
    bl_label = "LodToggle Toggle Soubgroup Res"
    bl_description = "Change the resolution of a subgroup"
    item_name = bpy.props.StringProperty()
    group_name = bpy.props.StringProperty()

    def execute(self, context):

        group_name = self.group_name
        item_name = self.item_name

        obj = bpy.data.objects[item_name]

        dupgroup = obj.dupli_group
        dupgroup_name = obj.dupli_group.name

        root = dupgroup_name[:-2]
        ext = dupgroup_name[-2:]
        
        if (root + 'me') in bpy.data.groups:
            if ext == 'hi':
                new_group = root + "me"
            elif ext == 'me':
                new_group = root + "lo"
            elif ext == 'lo':
                new_group = root + "hi"
            else:
                new_group = dupgroup  #  if error, do not change dupligroup
        else:
            if ext == 'hi':
                new_group = root + "lo"
            elif ext == 'lo':
                new_group = root + "hi"
            else:
                new_group = dupgroup  #  if error, do not change dupligroup

        if bpy.data.groups[dupgroup_name].library:
            # link needed object
            filepath = bpy.data.groups[dupgroup_name].library.filepath

            PowerPrint(filepath)
            with bpy.data.libraries.load(filepath, 
            link=True) as (data_from, data_to):
                data_to.groups.append(new_group)

        try: 
            obj.dupli_group = bpy.data.groups[new_group]
            PowerPrint("CHANGE " + str(item_name) + " to " + new_group)
        except:
            self.report({'WARNING'}, "Group %s not found" % new_group.upper())

        return {'FINISHED'}




    

def register():
    bpy.utils.register_class(ToggleSubgroupResolution)
    bpy.utils.register_class(LodTogglePanel)
    
def unregister():
    bpy.utils.unregister_class(ToggleSubgroupResolution)
    bpy.utils.unregister_class(LodTogglePanel)
    
if __name__ == "__main__":
    register()
