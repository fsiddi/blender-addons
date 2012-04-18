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
    "name": "Powerlib",
    "description": "Control panel for managing"
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


class PowerlibPanel(bpy.types.Panel):
    bl_label = "Powerlib"
    bl_idname = "SCENE_PT_powerlib"
    bl_context = "scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        object = bpy.context.active_object

        ob = bpy.context.active_object

        if ob.dupli_type == 'GROUP':
            group = ob.dupli_group
            group_name = group.name  # set variable for group toggle
            group_objs = bpy.data.groups[group.name].objects

            layout.label(" GROUP: " + group.name, icon = 'GROUP')

            row = layout.row()

            for elem in group_objs:

                row = layout.row()
                row.label(elem.name)
                if (elem.dupli_type == 'GROUP'):

                    subgroup = row.operator("powerlib.toggle_subgroup",
                    text="Visible", icon='RESTRICT_VIEW_OFF')
                    subgroup.display = "NONE"
                    subgroup.item_name = elem.name
                    subgroup.group_name = group.name
                else:
                    subgroup = row.operator("powerlib.toggle_subgroup",
                    text="Hidden", icon='RESTRICT_VIEW_ON')
                    subgroup.display = "GROUP"
                    subgroup.item_name = elem.name
                    subgroup.group_name = group.name

                resolution = str(elem.dupli_group.name)[-3:]
                if resolution in {'_hi', '_lo'}:
                    res = resolution[-2:].upper()

                    subgroup = row.operator("powerlib.toggle_subgroup_res",
                    text=res, icon='FILE_REFRESH')
                    subgroup.item_name = elem.name
                    subgroup.group_name = group.name

            row = layout.row(align=True)
            group = row.operator("powerlib.toggle_group",
            text="Show All", icon='RESTRICT_VIEW_OFF')
            group.display = "showall"
            group.group_name = group_name

            group = row.operator("powerlib.toggle_group",
            text="Hide All", icon='RESTRICT_VIEW_ON')
            group.display = "hideall"
            group.group_name = group_name


def hello(self, n):
    print("a " + n)


class ToggleSubgroupRes(bpy.types.Operator):
    bl_idname = "powerlib.toggle_subgroup_res"
    bl_label = "Powerlib Toggle Soubgroup Res"
    item_name = bpy.props.StringProperty()
    group_name = bpy.props.StringProperty()

    def execute(self, context):

        group_name = self.group_name
        item_name = self.item_name
        obj = bpy.data.objects[item_name]

        print(obj)

        print("-- changing " + str(item_name) + " to ")

        dupgroup = obj.dupli_group
        dupgroup_name = obj.dupli_group.name

        root = dupgroup_name[:-2]
        ext = dupgroup_name[-2:]
        if ext == 'hi':
            new_group = root + "lo"
        elif ext == 'lo':
            new_group = root + "hi"

        else:
            new_group = dupgroup  # if error, do not change dupligroup

        print ("dupligroup = " + str(dupgroup.name))
        print ("extension = " + ext)
        print ("root = " + root)
        print ("new_group = " + new_group)

        if bpy.data.groups[dupgroup_name].library:
            # link needed object
            filepath = bpy.data.groups[dupgroup_name].library.filepath

            print(filepath)
            with bpy.data.libraries.load(filepath, 
            link=True) as (data_from, data_to):
                data_to.groups.append(new_group)

        try: 
            obj.dupli_group = bpy.data.groups[new_group]
        except:
            self.report({'WARNING'}, "Group %s not found" % new_group.upper())

        return {'FINISHED'}


class ToggleGroupOperator(bpy.types.Operator):
    bl_idname = "powerlib.toggle_group"
    bl_label = "Powerlib Toggle Group"
    display = bpy.props.StringProperty()
    group_name = bpy.props.StringProperty()
    #objects = bpy.props.CollectionProperty()

    def execute(self, context):

        display = self.display
        grp_name = self.group_name
        group_objs = bpy.data.groups[grp_name].objects

        for elem in group_objs:
            if display == 'showall':
                elem.dupli_type = "GROUP"
                print("Powerlib: SHOW " + elem.name)
            elif display == 'hideall':
                elem.dupli_type = "NONE"
                print("Powerlib: HIDE " + elem.name)
            else:
                print("nothing")

        return {'FINISHED'}


class ToggleSubgroupOperator(bpy.types.Operator):
    bl_idname = "powerlib.toggle_subgroup"
    bl_label = "Powelib Toggle Subgroup"
    display = bpy.props.StringProperty()
    item_name = bpy.props.StringProperty()
    group_name = bpy.props.StringProperty()

    def execute(self, context):

        display = self.display
        obj_name = self.item_name
        grp_name = self.group_name

        print("Powerlib: " + obj_name + " is being set to " + display)
        #print(obj_name)
        #hello(context, display)

        bpy.data.groups[grp_name].objects[obj_name].dupli_type = display
        return {'FINISHED'}


class LoadLibrarySubgroup(bpy.types.Operator):
    bl_idname = "powerlib.load_library_group"
    bl_label = "Load Library Subgroup"


def register():
    bpy.utils.register_class(LoadLibrarySubgroup)
    bpy.utils.register_class(ToggleSubgroupRes)
    bpy.utils.register_class(ToggleGroupOperator)
    bpy.utils.register_class(ToggleSubgroupOperator)
    bpy.utils.register_class(PowerlibPanel)


def unregister():
    bpy.utils.unregister_class(LoadLibrarySubgroup)
    bpy.utils.unregister_class(ToggleSubgroupRes)
    bpy.utils.unregister_class(ToggleGroupOperator)
    bpy.utils.unregister_class(ToggleSubgroupOperator)
    bpy.utils.unregister_class(PowerlibPanel)

if __name__ == "__main__":
    register()
