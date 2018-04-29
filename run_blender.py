import bpy
import sys
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
factor = float(argv[0])
normal_factor = float(argv[1])
file_name = argv[2]

fp = bpy.context.scene.render.filepath
bpy.context.scene.render.filepath = fp + file_name

origin_obj = bpy.context.object.name

bpy.ops.object.modifier_add(type='SMOKE')
bpy.ops.object.material_slot_add()
bpy.ops.object.quick_smoke()


bpy.data.objects['Smoke Domain'].select = True
bpy.context.object.modifiers["Smoke"].domain_settings.use_adaptive_domain = True
bpy.context.object.modifiers["Smoke"].domain_settings.resolution_max = 80
bpy.context.object.modifiers["Smoke"].domain_settings.use_high_resolution = True
bpy.context.object.modifiers["Smoke"].domain_settings.strength = 1
bpy.context.object.modifiers["Smoke"].domain_settings.collision_extents = 'BORDERCLOSED'
bpy.context.object.scale[0] = 5
bpy.context.object.scale[1] = 5
bpy.context.object.scale[2] = 8
bpy.data.objects['Smoke Domain'].select = False

bpy.data.objects['Cube'].select = True

# velocity settings
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.use_initial_velocity = True
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.velocity_factor = factor
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.velocity_normal = normal_factor


#temperature settings
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.temperature = -1

# density settings
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.density = 1
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.keyframe_insert(data_path='density', frame=0)

bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.density = 0
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.keyframe_insert(data_path='density', frame=35)


# color settings
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.smoke_color = (0.7, 0.7, 0.7)
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.keyframe_insert(data_path='smoke_color', frame=0)

bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.smoke_color = (0.148918, 0.283537, 0.7)
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.keyframe_insert(data_path='smoke_color', frame=10)

bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.smoke_color = (0.690755, 0.0858234, 0.7)
bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.keyframe_insert(data_path='smoke_color', frame=15)

# bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.smoke_color = (0.7, 0.7, 0.7)
# bpy.data.objects['Cube'].modifiers["Smoke"].flow_settings.keyframe_insert(data_path='smoke_color', frame=20)


# create keyframes
bpy.context.scene.frame_set(0)
bpy.data.objects['Cube'].location = (0, 0, 7)
bpy.data.objects['Cube'].keyframe_insert(data_path="location", index=-1)

bpy.context.scene.frame_set(10)
bpy.data.objects['Cube'].location = (0, 0, 4)
bpy.data.objects['Cube'].keyframe_insert(data_path="location", index=-1)

scale_box = 0.5
bpy.data.objects['Cube'].scale[0] = scale_box
bpy.data.objects['Cube'].scale[1] = scale_box
bpy.data.objects['Cube'].scale[2] = scale_box

scene = bpy.context.scene
scene.layers = [True] * 20 # Show all layers
for obj in scene.objects:
    if obj.name == 'Cube':
        scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(smoothness=2)
        bpy.ops.object.mode_set(mode='OBJECT')

bpy.context.scene.frame_set(100)
bpy.context.scene.frame_end = 100

bpy.data.objects['Cube'].draw_type = 'SOLID'
bpy.data.objects['Smoke Domain'].draw_type = 'SOLID'

bpy.data.objects["Camera"].hide = True
bpy.data.objects["Lamp"].hide = True

bpy.context.object.hide = True

for area in bpy.data.screens['Default'].areas:
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.show_only_render = True


bpy.ops.screen.animation_play()


def my_handler(scene):
    frame = scene.frame_current
    n = frame
    if n >= 60:
        bpy.ops.render.opengl(write_still=True)
        bpy.ops.screen.animation_cancel()
        bpy.ops.wm.quit_blender()


#bpy.app.handlers.frame_change_pre.append(my_handler)