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
    "name": "Camera Selector",
    "description": "Control panel for activating "
    "the cameras available in a scene",
    "author": "Francesco Siddi",
    "version": (0, 5),
    "blender": (2, 63, 5),
    "location": "Properties Panel",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy
from bpy.props import (FloatProperty, BoolProperty, 
FloatVectorProperty, StringProperty, EnumProperty)


class CameraSelectorPanel(bpy.types.Panel):
    bl_label = "Camera Selector"
    bl_idname = "SCENE_PT_cameraselector"
    bl_context = "scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        cameras = sorted([o for o in scene.objects if o.type == 'CAMERA'],
                         key = lambda o: o.name)
        
        if len(cameras) > 0:
            for camera in cameras:
                row = layout.row(align=True)
                btn = row.operator("cameraselector.set_scene_camera", 
                text=camera.name, icon='OUTLINER_DATA_CAMERA')
                btn.chosen_camera = camera.name

                btn = row.operator("cameraselector.add_camera_marker", 
                text='', icon='MARKER')
                btn.chosen_camera = camera.name
        else:
            layout.label("No cameras in this scene") 
        

class SetSceneCamera(bpy.types.Operator):
    bl_idname = "cameraselector.set_scene_camera"
    bl_label = "Set Scene Camera"
    bl_description = "Set chosen camera as the scene's active camera."

    chosen_camera = bpy.props.StringProperty()
    select_chosen = False
    
    def execute(self, context):
        chosen_camera = bpy.data.objects.get(self.chosen_camera, None)
        scene = context.scene
        if not chosen_camera:
            self.report({'ERROR'}, "Camera %s not found.")
            return {'CANCELLED'}

        if self.select_chosen:
            for o in context.selected_objects:
                o.select = False
            for c in [o for o in scene.objects if o.type == 'CAMERA']:
                c.hide = (c != chosen_camera)
            chosen_camera.select = True
            scene.objects.active = chosen_camera
        scene.camera = chosen_camera

        return {'FINISHED'}

    def invoke(self, context, event):
        if event.ctrl: self.select_chosen = True

        return self.execute(context)


class AddCameraMarker(bpy.types.Operator):
    bl_idname = "cameraselector.add_camera_marker"
    bl_label = "Add Camera Marker"
    bl_description = "Add a timeline marker bound to chosen camera."

    chosen_camera = bpy.props.StringProperty()

    def execute(self, context):
        chosen_camera = bpy.data.objects.get(self.chosen_camera, None)
        scene = context.scene
        if not chosen_camera:
            self.report({'ERROR'}, "Camera %s not found.")
            return {'CANCELLED'}

        current_frame = scene.frame_current
        marker = None
        for m in reversed(sorted(filter(lambda m: m.frame <= current_frame,
                                        scene.timeline_markers),
                                 key = lambda m: m.frame)):
            marker = m
            break
        if marker and (marker.camera == chosen_camera):
            # Cancel if the last marker at or immediately before
            # current frame is already bound to the camera.
            return {'CANCELLED'}

        marker_name = "F_%02d_%s" % (current_frame, self.chosen_camera)
        if marker and (marker.frame == current_frame):
            # Reuse existing marker at current frame to avoid
            # overlapping bound markers.
            marker.name = marker_name
        else:
            marker = scene.timeline_markers.new(marker_name)
        marker.frame = scene.frame_current
        marker.camera = chosen_camera
        marker.select = True

        for other_marker in [m for m in scene.timeline_markers if m != marker]:
            other_marker.select = False

        return {'FINISHED'}


def register():
    bpy.utils.register_class(SetSceneCamera)
    bpy.utils.register_class(AddCameraMarker)
    bpy.utils.register_class(CameraSelectorPanel)
    
def unregister():
    bpy.utils.unregister_class(SetSceneCamera)
    bpy.utils.unregister_class(AddCameraMarker)
    bpy.utils.unregister_class(CameraSelectorPanel)
    
if __name__ == "__main__":
    register()
