"""Toon look for previs: two-band toon fill that keeps every material's colour, plus the
blender-npr-eevee skill's inverted-hull outline (navy) on the character parts."""
import importlib.util
from pathlib import Path

import bpy

SKILL = Path.home() / '.claude-personal/skills/blender-npr-eevee/scripts/build_eevee_npr.py'
OUTLINE_PARTS = ('body', 'ear', 'cup', 'band', 'L')


def _skill():
    spec = importlib.util.spec_from_file_location('build_eevee_npr', SKILL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def toonify(mat, shadow=0.8, cut=0.42):
    """Replace the Principled output with: light (white diffuse -> Shader to RGB -> constant ramp) x base colour."""
    nt = mat.node_tree
    bsdf = nt.nodes.get('Principled BSDF')
    if bsdf is None:
        return
    out = nt.nodes['Material Output']
    diff = nt.nodes.new('ShaderNodeBsdfDiffuse')
    s2r = nt.nodes.new('ShaderNodeShaderToRGB')
    bw = nt.nodes.new('ShaderNodeRGBToBW')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation = 'CONSTANT'
    ramp.color_ramp.elements[0].color = (shadow, shadow, shadow, 1)
    ramp.color_ramp.elements[1].position = cut
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    mul = nt.nodes.new('ShaderNodeMix')
    mul.data_type, mul.blend_type = 'RGBA', 'MULTIPLY'
    mul.inputs['Factor'].default_value = 1.0
    em = nt.nodes.new('ShaderNodeEmission')
    nt.links.new(diff.outputs[0], s2r.inputs[0])
    nt.links.new(s2r.outputs['Color'], bw.inputs[0])
    nt.links.new(bw.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs['Color'], mul.inputs['A'])
    base = bsdf.inputs['Base Color']
    if base.is_linked:
        nt.links.new(base.links[0].from_socket, mul.inputs['B'])
    else:
        mul.inputs['B'].default_value = base.default_value
    nt.links.new(mul.outputs['Result'], em.inputs['Color'])
    nt.links.new(em.outputs[0], out.inputs['Surface'])


def apply(width=0.011, navy=(0.004, 0.012, 0.045, 1.0)):
    scn = bpy.context.scene
    scn.render.engine = 'BLENDER_EEVEE'
    scn.view_settings.view_transform = 'Standard'
    scn.view_settings.exposure = 0.0
    for m in bpy.data.materials:
        if m.use_nodes and not m.name.startswith('screen_') and m.name not in ('eye', 'shine'):
            toonify(m)
    sk = _skill()
    outline_mat = sk.build_outline_material(navy)
    group = sk.build_outline_group(outline_mat, width=width, noise_scale=5.0, wobble_amount=0.0)
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name.split('.')[0].rstrip('-1').startswith(OUTLINE_PARTS):
            sk._ensure_outline_modifier(o, group, outline_material=outline_mat, width=width, noise_scale=5.0, wobble_amount=0.0)
