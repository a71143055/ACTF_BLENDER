"""
ACTF (Android Cyborg Transformers) 3D Design for Blender 4.4
작성자: 정구영
작성일: 2026년 05월 20일
설명: 차세대 로봇 디자인 - 그래핀 폴리머 액정 기반 안드로이드 사이보그
"""

import bpy
import math
from mathutils import Vector, Euler
from bpy.props import FloatProperty, IntProperty, BoolProperty

# =============================================================================
# ACTF 3D Design Class
# =============================================================================
class ACTFDesigner:
    def __init__(self):
        self.clear_scene()
        self.setup_materials()
        
    def clear_scene(self):
        """씬 정리"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
    def setup_materials(self):
        """재질 설정 - 그래핀 폴리머 액정 및 탄소나노튜브"""
        
        # 그래핀 폴리머 액정 재질 (외골격)
        self.mat_graphene = bpy.data.materials.new(name="Graphene_Polymer_Liquid_Crystal")
        self.mat_graphene.use_nodes = True
        nodes = self.mat_graphene.node_tree.nodes
        links = self.mat_graphene.node_tree.links
        
        # 기본 노드 정리
        nodes.clear()
        
        # Principled BSDF
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs['Base Color'].default_value = (0.1, 0.15, 0.2, 1.0)  # 짙은 메탈릭 블루-그레이
        bsdf.inputs['Metallic'].default_value = 0.9
        bsdf.inputs['Roughness'].default_value = 0.3
        bsdf.inputs['IOR'].default_value = 2.4  # 그래핀의 높은 굴절률
        
        # Output
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # 탄소나노튜브 재질 (강화 부품)
        self.mat_nanotube = bpy.data.materials.new(name="Carbon_Nanotube")
        self.mat_nanotube.use_nodes = True
        nodes = self.mat_nanotube.node_tree.nodes
        links = self.mat_nanotube.node_tree.links
        nodes.clear()
        
        bsdf_nt = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf_nt.location = (0, 0)
        bsdf_nt.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)  # 검은색
        bsdf_nt.inputs['Metallic'].default_value = 1.0
        bsdf_nt.inputs['Roughness'].default_value = 0.1
        bsdf_nt.inputs['IOR'].default_value = 2.6
        
        output_nt = nodes.new('ShaderNodeOutputMaterial')
        output_nt.location = (300, 0)
        links.new(bsdf_nt.outputs['BSDF'], output_nt.inputs['Surface'])
        
        # 내골격 재질 (생물학적 구조)
        self.mat_internal = bpy.data.materials.new(name="Internal_Skeleton")
        self.mat_internal.use_nodes = True
        nodes = self.mat_internal.node_tree.nodes
        links = self.mat_internal.node_tree.links
        nodes.clear()
        
        bsdf_int = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf_int.location = (0, 0)
        bsdf_int.inputs['Base Color'].default_value = (0.8, 0.85, 0.9, 1.0)  # 흰색-회색
        bsdf_int.inputs['Metallic'].default_value = 0.3
        bsdf_int.inputs['Roughness'].default_value = 0.5
        
        output_int = nodes.new('ShaderNodeOutputMaterial')
        output_int.location = (300, 0)
        links.new(bsdf_int.outputs['BSDF'], output_int.inputs['Surface'])
        
        # 에너지 코어 재질
        self.mat_energy = bpy.data.materials.new(name="Energy_Core")
        self.mat_energy.use_nodes = True
        nodes = self.mat_energy.node_tree.nodes
        links = self.mat_energy.node_tree.links
        nodes.clear()
        
        emission = nodes.new('ShaderNodeEmission')
        emission.location = (0, 0)
        emission.inputs['Color'].default_value = (0.0, 0.8, 1.0, 1.0)  # 청록색 발광
        emission.inputs['Strength'].default_value = 5.0
        
        output_energy = nodes.new('ShaderNodeOutputMaterial')
        output_energy.location = (300, 0)
        links.new(emission.outputs['Emission'], output_energy.inputs['Surface'])
    
    def create_humanoid_base(self):
        """인간형 기본 구조 생성"""
        # 신체 비율 (미터 단위)
        height = 1.8
        head_radius = 0.12
        neck_radius = 0.05
        torso_width = 0.4
        torso_depth = 0.25
        torso_height = 0.6
        shoulder_width = 0.45
        arm_length = 0.7
        forearm_length = 0.5
        hand_size = 0.12
        pelvis_width = 0.35
        pelvis_depth = 0.2
        pelvis_height = 0.15
        thigh_length = 0.5
        calf_length = 0.5
        foot_length = 0.25
        
        body_parts = {}
        
        # 머리
        bpy.ops.mesh.primitive_uv_sphere_add(radius=head_radius, location=(0, 0, height - head_radius))
        head = bpy.context.active_object
        head.name = "ACTF_Head"
        body_parts['head'] = head
        
        # 목
        bpy.ops.mesh.primitive_cylinder_add(radius=neck_radius, depth=0.1, location=(0, 0, height - head_radius * 2 - 0.05))
        neck = bpy.context.active_object
        neck.name = "ACTF_Neck"
        body_parts['neck'] = neck
        
        # 상체 (흉부)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, height - head_radius * 2 - 0.1 - torso_height / 2))
        torso = bpy.context.active_object
        torso.name = "ACTF_Torso"
        torso.scale = (torso_width, torso_depth, torso_height)
        body_parts['torso'] = torso
        
        # 어깨
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, height - head_radius * 2 - 0.1 - torso_height + 0.1))
        shoulders = bpy.context.active_object
        shoulders.name = "ACTF_Shoulders"
        shoulders.scale = (shoulder_width, 0.15, 0.1)
        body_parts['shoulders'] = shoulders
        
        # 골반
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, height - head_radius * 2 - 0.1 - torso_height - pelvis_height / 2))
        pelvis = bpy.context.active_object
        pelvis.name = "ACTF_Pelvis"
        pelvis.scale = (pelvis_width, pelvis_depth, pelvis_height)
        body_parts['pelvis'] = pelvis
        
        # 왼쪽 팔 상부
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=arm_length, location=(-shoulder_width / 2 - arm_length / 2, 0, height - head_radius * 2 - 0.1 - torso_height + 0.05))
        left_upper_arm = bpy.context.active_object
        left_upper_arm.name = "ACTF_Left_Upper_Arm"
        left_upper_arm.rotation_euler = Euler((0, 0, math.pi / 2))
        body_parts['left_upper_arm'] = left_upper_arm
        
        # 오른쪽 팔 상부
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=arm_length, location=(shoulder_width / 2 + arm_length / 2, 0, height - head_radius * 2 - 0.1 - torso_height + 0.05))
        right_upper_arm = bpy.context.active_object
        right_upper_arm.name = "ACTF_Right_Upper_Arm"
        right_upper_arm.rotation_euler = Euler((0, 0, -math.pi / 2))
        body_parts['right_upper_arm'] = right_upper_arm
        
        # 왼쪽 팔 하부
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=forearm_length, location=(-shoulder_width / 2 - arm_length - forearm_length / 2, 0, height - head_radius * 2 - 0.1 - torso_height + 0.05))
        left_forearm = bpy.context.active_object
        left_forearm.name = "ACTF_Left_Forearm"
        left_forearm.rotation_euler = Euler((0, 0, math.pi / 2))
        body_parts['left_forearm'] = left_forearm
        
        # 오른쪽 팔 하부
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=forearm_length, location=(shoulder_width / 2 + arm_length + forearm_length / 2, 0, height - head_radius * 2 - 0.1 - torso_height + 0.05))
        right_forearm = bpy.context.active_object
        right_forearm.name = "ACTF_Right_Forearm"
        right_forearm.rotation_euler = Euler((0, 0, -math.pi / 2))
        body_parts['right_forearm'] = right_forearm
        
        # 왼쪽 손
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-shoulder_width / 2 - arm_length - forearm_length - hand_size / 2, 0, height - head_radius * 2 - 0.1 - torso_height + 0.05))
        left_hand = bpy.context.active_object
        left_hand.name = "ACTF_Left_Hand"
        left_hand.scale = (hand_size, 0.08, hand_size)
        body_parts['left_hand'] = left_hand
        
        # 오른쪽 손
        bpy.ops.mesh.primitive_cube_add(size=1, location=(shoulder_width / 2 + arm_length + forearm_length + hand_size / 2, 0, height - head_radius * 2 - 0.1 - torso_height + 0.05))
        right_hand = bpy.context.active_object
        right_hand.name = "ACTF_Right_Hand"
        right_hand.scale = (hand_size, 0.08, hand_size)
        body_parts['right_hand'] = right_hand
        
        # 왼쪽 허벅지
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=thigh_length, location=(-0.12, 0, height - head_radius * 2 - 0.1 - torso_height - pelvis_height - thigh_length / 2))
        left_thigh = bpy.context.active_object
        left_thigh.name = "ACTF_Left_Thigh"
        body_parts['left_thigh'] = left_thigh
        
        # 오른쪽 허벅지
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=thigh_length, location=(0.12, 0, height - head_radius * 2 - 0.1 - torso_height - pelvis_height - thigh_length / 2))
        right_thigh = bpy.context.active_object
        right_thigh.name = "ACTF_Right_Thigh"
        body_parts['right_thigh'] = right_thigh
        
        # 왼쪽 종아리
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=calf_length, location=(-0.12, 0, height - head_radius * 2 - 0.1 - torso_height - pelvis_height - thigh_length - calf_length / 2))
        left_calf = bpy.context.active_object
        left_calf.name = "ACTF_Left_Calf"
        body_parts['left_calf'] = left_calf
        
        # 오른쪽 종아리
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=calf_length, location=(0.12, 0, height - head_radius * 2 - 0.1 - torso_height - pelvis_height - thigh_length - calf_length / 2))
        right_calf = bpy.context.active_object
        right_calf.name = "ACTF_Right_Calf"
        body_parts['right_calf'] = right_calf
        
        # 왼쪽 발
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.12, foot_length / 4, height - head_radius * 2 - 0.1 - torso_height - pelvis_height - thigh_length - calf_length - 0.05))
        left_foot = bpy.context.active_object
        left_foot.name = "ACTF_Left_Foot"
        left_foot.scale = (0.1, foot_length, 0.08)
        body_parts['left_foot'] = left_foot
        
        # 오른쪽 발
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.12, foot_length / 4, height - head_radius * 2 - 0.1 - torso_height - pelvis_height - thigh_length - calf_length - 0.05))
        right_foot = bpy.context.active_object
        right_foot.name = "ACTF_Right_Foot"
        right_foot.scale = (0.1, foot_length, 0.08)
        body_parts['right_foot'] = right_foot
        
        return body_parts
    
    def create_internal_skeleton(self, body_parts):
        """내골격 구조 생성 - 줄기세포 배양 및 인공장기 공간"""
        internal_parts = {}
        
        # 척추 (중심 구조)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.5, location=(0, 0, 0.9))
        spine = bpy.context.active_object
        spine.name = "ACTF_Internal_Spine"
        spine.data.materials.append(self.mat_internal)
        internal_parts['spine'] = spine
        
        # 흉곽 (인공장기 공간)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.15, minor_radius=0.02, location=(0, 0, 1.2))
        ribcage = bpy.context.active_object
        ribcage.name = "ACTF_Internal_Ribcage"
        ribcage.rotation_euler = Euler((math.pi / 2, 0, 0))
        ribcage.scale = (1, 0.8, 1)
        ribcage.data.materials.append(self.mat_internal)
        internal_parts['ribcage'] = ribcage
        
        # 두개골 내부 (뇌 이식 공간)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(0, 0, 1.65))
        skull_interior = bpy.context.active_object
        skull_interior.name = "ACTF_Internal_Skull"
        skull_interior.data.materials.append(self.mat_internal)
        internal_parts['skull_interior'] = skull_interior
        
        # 심장 공간
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0, 0.05, 1.15))
        heart_chamber = bpy.context.active_object
        heart_chamber.name = "ACTF_Internal_Heart_Chamber"
        heart_chamber.data.materials.append(self.mat_internal)
        internal_parts['heart_chamber'] = heart_chamber
        
        # 폐 공간
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(-0.08, 0, 1.15))
        left_lung = bpy.context.active_object
        left_lung.name = "ACTF_Internal_Left_Lung"
        left_lung.data.materials.append(self.mat_internal)
        internal_parts['left_lung'] = left_lung
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(0.08, 0, 1.15))
        right_lung = bpy.context.active_object
        right_lung.name = "ACTF_Internal_Right_Lung"
        right_lung.data.materials.append(self.mat_internal)
        internal_parts['right_lung'] = right_lung
        
        # 골반 내부 (줄기세포 배양 공간)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.75))
        pelvis_interior = bpy.context.active_object
        pelvis_interior.name = "ACTF_Internal_Pelvis_Chamber"
        pelvis_interior.scale = (0.2, 0.12, 0.1)
        pelvis_interior.data.materials.append(self.mat_internal)
        internal_parts['pelvis_interior'] = pelvis_interior
        
        return internal_parts
    
    def create_external_armor(self, body_parts):
        """외골격 구조 생성 - 그래핀 폴리머 액정 갑옷"""
        armor_parts = {}
        
        # 머리 헬멧
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(0, 0, 1.68))
        helmet = bpy.context.active_object
        helmet.name = "ACTF_Armor_Helmet"
        helmet.scale = (1, 1.2, 1)
        helmet.data.materials.append(self.mat_graphene)
        armor_parts['helmet'] = helmet
        
        # 흉부 갑옷
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.25))
        chest_armor = bpy.context.active_object
        chest_armor.name = "ACTF_Armor_Chest"
        chest_armor.scale = (0.45, 0.3, 0.35)
        chest_armor.data.materials.append(self.mat_graphene)
        armor_parts['chest_armor'] = chest_armor
        
        # 등 갑옷
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.2, 1.2))
        back_armor = bpy.context.active_object
        back_armor.name = "ACTF_Armor_Back"
        back_armor.scale = (0.4, 0.15, 0.3)
        back_armor.data.materials.append(self.mat_graphene)
        armor_parts['back_armor'] = back_armor
        
        # 어깨 갑옷 (왼쪽)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.35, 0, 1.45))
        left_shoulder_armor = bpy.context.active_object
        left_shoulder_armor.name = "ACTF_Armor_Left_Shoulder"
        left_shoulder_armor.scale = (0.15, 0.2, 0.12)
        left_shoulder_armor.data.materials.append(self.mat_nanotube)
        armor_parts['left_shoulder_armor'] = left_shoulder_armor
        
        # 어깨 갑옷 (오른쪽)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.35, 0, 1.45))
        right_shoulder_armor = bpy.context.active_object
        right_shoulder_armor.name = "ACTF_Armor_Right_Shoulder"
        right_shoulder_armor.scale = (0.15, 0.2, 0.12)
        right_shoulder_armor.data.materials.append(self.mat_nanotube)
        armor_parts['right_shoulder_armor'] = right_shoulder_armor
        
        # 상완 갑옷 (왼쪽)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.4, location=(-0.55, 0, 1.35))
        left_upper_arm_armor = bpy.context.active_object
        left_upper_arm_armor.name = "ACTF_Armor_Left_Upper_Arm"
        left_upper_arm_armor.rotation_euler = Euler((0, 0, math.pi / 2))
        left_upper_arm_armor.data.materials.append(self.mat_graphene)
        armor_parts['left_upper_arm_armor'] = left_upper_arm_armor
        
        # 상완 갑옷 (오른쪽)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.4, location=(0.55, 0, 1.35))
        right_upper_arm_armor = bpy.context.active_object
        right_upper_arm_armor.name = "ACTF_Armor_Right_Upper_Arm"
        right_upper_arm_armor.rotation_euler = Euler((0, 0, -math.pi / 2))
        right_upper_arm_armor.data.materials.append(self.mat_graphene)
        armor_parts['right_upper_arm_armor'] = right_upper_arm_armor
        
        # 전완 갑옷 (왼쪽)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.35, location=(-0.9, 0, 1.35))
        left_forearm_armor = bpy.context.active_object
        left_forearm_armor.name = "ACTF_Armor_Left_Forearm"
        left_forearm_armor.rotation_euler = Euler((0, 0, math.pi / 2))
        left_forearm_armor.data.materials.append(self.mat_graphene)
        armor_parts['left_forearm_armor'] = left_forearm_armor
        
        # 전완 갑옷 (오른쪽)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.35, location=(0.9, 0, 1.35))
        right_forearm_armor = bpy.context.active_object
        right_forearm_armor.name = "ACTF_Armor_Right_Forearm"
        right_forearm_armor.rotation_euler = Euler((0, 0, -math.pi / 2))
        right_forearm_armor.data.materials.append(self.mat_graphene)
        armor_parts['right_forearm_armor'] = right_forearm_armor
        
        # 장갑 (왼쪽)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.15, 0, 1.35))
        left_gauntlet = bpy.context.active_object
        left_gauntlet.name = "ACTF_Armor_Left_Gauntlet"
        left_gauntlet.scale = (0.12, 0.1, 0.12)
        left_gauntlet.data.materials.append(self.mat_nanotube)
        armor_parts['left_gauntlet'] = left_gauntlet
        
        # 장갑 (오른쪽)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(1.15, 0, 1.35))
        right_gauntlet = bpy.context.active_object
        right_gauntlet.name = "ACTF_Armor_Right_Gauntlet"
        right_gauntlet.scale = (0.12, 0.1, 0.12)
        right_gauntlet.data.materials.append(self.mat_nanotube)
        armor_parts['right_gauntlet'] = right_gauntlet
        
        # 골반 갑옷
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.85))
        pelvic_armor = bpy.context.active_object
        pelvic_armor.name = "ACTF_Armor_Pelvic"
        pelvic_armor.scale = (0.4, 0.22, 0.18)
        pelvic_armor.data.materials.append(self.mat_graphene)
        armor_parts['pelvic_armor'] = pelvic_armor
        
        # 대퇴부 갑옷 (왼쪽)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.35, location=(-0.12, 0, 0.6))
        left_thigh_armor = bpy.context.active_object
        left_thigh_armor.name = "ACTF_Armor_Left_Thigh"
        left_thigh_armor.data.materials.append(self.mat_graphene)
        armor_parts['left_thigh_armor'] = left_thigh_armor
        
        # 대퇴부 갑옷 (오른쪽)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.35, location=(0.12, 0, 0.6))
        right_thigh_armor = bpy.context.active_object
        right_thigh_armor.name = "ACTF_Armor_Right_Thigh"
        right_thigh_armor.data.materials.append(self.mat_graphene)
        armor_parts['right_thigh_armor'] = right_thigh_armor
        
        # 하퇴부 갑옷 (왼쪽)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.35, location=(-0.12, 0, 0.25))
        left_calf_armor = bpy.context.active_object
        left_calf_armor.name = "ACTF_Armor_Left_Calf"
        left_calf_armor.data.materials.append(self.mat_graphene)
        armor_parts['left_calf_armor'] = left_calf_armor
        
        # 하퇴부 갑옷 (오른쪽)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.35, location=(0.12, 0, 0.25))
        right_calf_armor = bpy.context.active_object
        right_calf_armor.name = "ACTF_Armor_Right_Calf"
        right_calf_armor.data.materials.append(self.mat_graphene)
        armor_parts['right_calf_armor'] = right_calf_armor
        
        # 부츠 (왼쪽)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.12, 0.08, 0.05))
        left_boot = bpy.context.active_object
        left_boot.name = "ACTF_Armor_Left_Boot"
        left_boot.scale = (0.12, 0.2, 0.1)
        left_boot.data.materials.append(self.mat_nanotube)
        armor_parts['left_boot'] = left_boot
        
        # 부츠 (오른쪽)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.12, 0.08, 0.05))
        right_boot = bpy.context.active_object
        right_boot.name = "ACTF_Armor_Right_Boot"
        right_boot.scale = (0.12, 0.2, 0.1)
        right_boot.data.materials.append(self.mat_nanotube)
        armor_parts['right_boot'] = right_boot
        
        return armor_parts
    
    def create_energy_cores(self):
        """에너지 코어 생성"""
        cores = {}
        
        # 흉부 에너지 코어
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(0, 0.12, 1.25))
        chest_core = bpy.context.active_object
        chest_core.name = "ACTF_Energy_Chest_Core"
        chest_core.data.materials.append(self.mat_energy)
        cores['chest_core'] = chest_core
        
        # 등 에너지 코어
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0, -0.18, 1.2))
        back_core = bpy.context.active_object
        back_core.name = "ACTF_Energy_Back_Core"
        back_core.data.materials.append(self.mat_energy)
        cores['back_core'] = back_core
        
        # 골반 에너지 코어
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(0, 0, 0.85))
        pelvic_core = bpy.context.active_object
        pelvic_core.name = "ACTF_Energy_Pelvic_Core"
        pelvic_core.data.materials.append(self.mat_energy)
        cores['pelvic_core'] = pelvic_core
        
        return cores
    
    def create_joints(self):
        """관절 구조 생성"""
        joints = {}
        
        # 어깨 관절 (왼쪽)
        bpy.ops.mesh.primitive_sphere_add(radius=0.05, location=(-0.3, 0, 1.45))
        left_shoulder_joint = bpy.context.active_object
        left_shoulder_joint.name = "ACTF_Joint_Left_Shoulder"
        left_shoulder_joint.data.materials.append(self.mat_nanotube)
        joints['left_shoulder_joint'] = left_shoulder_joint
        
        # 어깨 관절 (오른쪽)
        bpy.ops.mesh.primitive_sphere_add(radius=0.05, location=(0.3, 0, 1.45))
        right_shoulder_joint = bpy.context.active_object
        right_shoulder_joint.name = "ACTF_Joint_Right_Shoulder"
        right_shoulder_joint.data.materials.append(self.mat_nanotube)
        joints['right_shoulder_joint'] = right_shoulder_joint
        
        # 팔꿈치 관절 (왼쪽)
        bpy.ops.mesh.primitive_sphere_add(radius=0.04, location=(-0.75, 0, 1.35))
        left_elbow_joint = bpy.context.active_object
        left_elbow_joint.name = "ACTF_Joint_Left_Elbow"
        left_elbow_joint.data.materials.append(self.mat_nanotube)
        joints['left_elbow_joint'] = left_elbow_joint
        
        # 팔꿈치 관절 (오른쪽)
        bpy.ops.mesh.primitive_sphere_add(radius=0.04, location=(0.75, 0, 1.35))
        right_elbow_joint = bpy.context.active_object
        right_elbow_joint.name = "ACTF_Joint_Right_Elbow"
        right_elbow_joint.data.materials.append(self.mat_nanotube)
        joints['right_elbow_joint'] = right_elbow_joint
        
        # 고관절 (왼쪽)
        bpy.ops.mesh.primitive_sphere_add(radius=0.06, location=(-0.12, 0, 0.95))
        left_hip_joint = bpy.context.active_object
        left_hip_joint.name = "ACTF_Joint_Left_Hip"
        left_hip_joint.data.materials.append(self.mat_nanotube)
        joints['left_hip_joint'] = left_hip_joint
        
        # 고관절 (오른쪽)
        bpy.ops.mesh.primitive_sphere_add(radius=0.06, location=(0.12, 0, 0.95))
        right_hip_joint = bpy.context.active_object
        right_hip_joint.name = "ACTF_Joint_Right_Hip"
        right_hip_joint.data.materials.append(self.mat_nanotube)
        joints['right_hip_joint'] = right_hip_joint
        
        # 무릎 관절 (왼쪽)
        bpy.ops.mesh.primitive_sphere_add(radius=0.05, location=(-0.12, 0, 0.45))
        left_knee_joint = bpy.context.active_object
        left_knee_joint.name = "ACTF_Joint_Left_Knee"
        left_knee_joint.data.materials.append(self.mat_nanotube)
        joints['left_knee_joint'] = left_knee_joint
        
        # 무릎 관절 (오른쪽)
        bpy.ops.mesh.primitive_sphere_add(radius=0.05, location=(0.12, 0, 0.45))
        right_knee_joint = bpy.context.active_object
        right_knee_joint.name = "ACTF_Joint_Right_Knee"
        right_knee_joint.data.materials.append(self.mat_nanotube)
        joints['right_knee_joint'] = right_knee_joint
        
        return joints
    
    def setup_lighting(self):
        """조명 설정"""
        # 키 라이트
        bpy.ops.light.light_add(type='SUN', location=(5, 5, 10))
        key_light = bpy.context.active_object
        key_light.name = "ACTF_Key_Light"
        key_light.data.energy = 1000
        key_light.rotation_euler = Euler((math.radians(45), 0, math.radians(45)))
        
        # 필 라이트
        bpy.ops.light.light_add(type='SUN', location=(-5, 5, 8))
        fill_light = bpy.context.active_object
        fill_light.name = "ACTF_Fill_Light"
        fill_light.data.energy = 500
        fill_light.rotation_euler = Euler((math.radians(30), 0, math.radians(135)))
        
        # 백 라이트
        bpy.ops.light.light_add(type='SUN', location=(0, -5, 8))
        back_light = bpy.context.active_object
        back_light.name = "ACTF_Back_Light"
        back_light.data.energy = 300
        back_light.rotation_euler = Euler((math.radians(30), 0, math.radians(180)))
        
        # 앰비언트 라이트
        bpy.ops.light.light_add(type='POINT', location=(0, 0, 5))
        ambient_light = bpy.context.active_object
        ambient_light.name = "ACTF_Ambient_Light"
        ambient_light.data.energy = 200
        ambient_light.data.shadow_soft_size = 0.1
    
    def setup_camera(self):
        """카메라 설정"""
        bpy.ops.object.camera_add(location=(4, -4, 2.5))
        camera = bpy.context.active_object
        camera.name = "ACTF_Camera"
        camera.rotation_euler = Euler((math.radians(70), 0, math.radians(45)))
        bpy.context.scene.camera = camera
        
        # 카메라 설정
        camera.data.sensor_fit = 'AUTO'
        camera.data.lens = 50
    
    def setup_scene(self):
        """씬 설정"""
        # 렌더 엔진 설정
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'
        
        # 배경색
        bpy.context.scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.05, 0.05, 0.08, 1)
        
        # 그라운드 플레인
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
        ground = bpy.context.active_object
        ground.name = "ACTF_Ground"
        
        # 그라운드 재질
        ground_mat = bpy.data.materials.new(name="Ground_Material")
        ground_mat.use_nodes = True
        nodes = ground_mat.node_tree.nodes
        nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.1, 0.1, 0.12, 1)
        nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.8
        ground.data.materials.append(ground_mat)
    
    def create_full_design(self):
        """전체 ACTF 디자인 생성"""
        print("ACTF 3D 디자인 시작...")
        
        # 기본 구조 생성
        print("1. 인간형 기본 구조 생성 중...")
        body_parts = self.create_humanoid_base()
        
        # 내골격 생성
        print("2. 내골격 구조 생성 중...")
        internal_parts = self.create_internal_skeleton(body_parts)
        
        # 외골격 생성
        print("3. 외골격 구조 생성 중...")
        armor_parts = self.create_external_armor(body_parts)
        
        # 에너지 코어 생성
        print("4. 에너지 코어 생성 중...")
        energy_cores = self.create_energy_cores()
        
        # 관절 생성
        print("5. 관절 구조 생성 중...")
        joints = self.create_joints()
        
        # 조명 설정
        print("6. 조명 설정 중...")
        self.setup_lighting()
        
        # 카메라 설정
        print("7. 카메라 설정 중...")
        self.setup_camera()
        
        # 씬 설정
        print("8. 씬 설정 중...")
        self.setup_scene()
        
        print("ACTF 3D 디자인 완료!")
        print(f"생성된 부품:")
        print(f"- 기본 구조: {len(body_parts)}개")
        print(f"- 내골격: {len(internal_parts)}개")
        print(f"- 외골격: {len(armor_parts)}개")
        print(f"- 에너지 코어: {len(energy_cores)}개")
        print(f"- 관절: {len(joints)}개")
        
        return {
            'body_parts': body_parts,
            'internal_parts': internal_parts,
            'armor_parts': armor_parts,
            'energy_cores': energy_cores,
            'joints': joints
        }

# =============================================================================
# 메인 실행 함수
# =============================================================================
def main():
    """메인 실행 함수"""
    designer = ACTFDesigner()
    result = designer.create_full_design()
    return result

if __name__ == "__main__":
    main()
