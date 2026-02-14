#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scratch 3.0 项目生成器
可以创建包含角色、脚本、声音和资源的 .sb3 文件
"""

import json
import zipfile
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional


class ScratchProjectGenerator:
    """Scratch 3.0 项目生成器"""

    def __init__(self):
        self.targets = []
        self.extensions = []
        self.monitors = []
        self.meta = {
            "semver": "3.0.0",
            "vm": "0.2.0",
            "agent": "Mozilla/5.0"
        }

    def add_stage(self, name: str = "Stage",
                  width: int = 480,
                  height: int = 360,
                  tempo: int = 60,
                  video_state: str = "on",
                  rotation_style: str = "none"):
        """添加舞台背景"""
        stage = {
            "isStage": True,
            "name": name,
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "blocks": {},
            "comments": {},
            "currentCostume": 0,
            "costumes": [
                {
                    "assetId": self._generate_md5(),
                    "name": "backdrop1",
                    "md5ext": self._generate_md5() + ".png",
                    "dataFormat": "png",
                    "rotationCenterX": width // 2,
                    "rotationCenterY": height // 2,
                    "bitmapResolution": 1
                }
            ],
            "sounds": [],
            "volume": 100,
            "layerOrder": 0,
            "tempo": tempo,
            "videoTransparency": 50,
            "videoState": video_state,
            "textToSpeechLanguage": None,
            "stageWidth": width,
            "stageHeight": height,
            "textureMap": {},
            "runtime": 2000
        }
        self.targets.append(stage)
        return self

    def add_sprite(self, name: str,
                  x: int = 0,
                  y: int = 0,
                  size: int = 100,
                  visible: bool = True,
                  rotation_style: str = "all around"):
        """添加角色"""
        sprite = {
            "isStage": False,
            "name": name,
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "blocks": {},
            "comments": {},
            "currentCostume": 0,
            "costumes": [
                {
                    "assetId": self._generate_md5(),
                    "name": "costume1",
                    "bitmapResolution": 1,
                    "md5ext": self._generate_md5() + ".png",
                    "dataFormat": "png",
                    "rotationCenterX": 48,
                    "rotationCenterY": 50
                }
            ],
            "sounds": [],
            "volume": 100,
            "layerOrder": len(self.targets),
            "visible": visible,
            "x": x,
            "y": y,
            "size": size,
            "direction": 90,
            "draggable": False,
            "rotationStyle": rotation_style,
            "physicsEnabled": False
        }
        self.targets.append(sprite)
        return sprite

    def add_block(self, sprite: Dict, block_id: str, opcode: str,
                  fields: Dict = None, inputs: Dict = None,
                  next: Optional[str] = None, parent: Optional[str] = None):
        """添加积木到角色"""
        if "blocks" not in sprite:
            sprite["blocks"] = {}

        block = {
            "opcode": opcode,
            "next": next,
            "parent": parent,
            "inputs": inputs or {},
            "fields": fields or {},
            "shadow": False,
            "topLevel": False
        }
        sprite["blocks"][block_id] = block
        return block_id

    def add_simple_script(self, sprite: Dict, blocks: List[Dict]):
        """添加简单脚本（积木链）"""
        if "blocks" not in sprite:
            sprite["blocks"] = {}

        prev_block_id = None
        first_block_id = None

        for block_config in blocks:
            block_id = self._generate_md5()
            if first_block_id is None:
                first_block_id = block_id

            # 添加积木
            self.add_block(
                sprite,
                block_id,
                block_config.get("opcode", ""),
                block_config.get("fields", {}),
                block_config.get("inputs", {}),
                None,  # next 会在后面设置
                prev_block_id  # parent 是前一个积木
            )

            # 设置前一个积木的 next
            if prev_block_id:
                sprite["blocks"][prev_block_id]["next"] = block_id

            prev_block_id = block_id

        # 设置第一个积木为顶级积木
        if first_block_id:
            sprite["blocks"][first_block_id]["topLevel"] = True

    def add_variable(self, sprite: Dict, name: str, value: float = 0, is_cloud: bool = False):
        """添加变量"""
        if "variables" not in sprite:
            sprite["variables"] = {}
        var_id = self._generate_md5()
        sprite["variables"][var_id] = [name, value, is_cloud]
        return var_id

    def add_sound(self, sprite: Dict, name: str,
                  data: bytes = None,
                  rate: int = 48000,
                  sample_count: int = 0):
        """添加声音"""
        if "sounds" not in sprite:
            sprite["sounds"] = []

        sound_id = self._generate_md5()
        sound = {
            "assetId": sound_id,
            "name": name,
            "dataFormat": "wav",
            "rate": rate,
            "sampleCount": sample_count,
            "md5ext": sound_id + ".wav"
        }
        sprite["sounds"].append(sound)
        return sound_id

    def _generate_md5(self) -> str:
        """生成随机MD5字符串"""
        import hashlib
        import random
        data = str(random.random()).encode()
        return hashlib.md5(data).hexdigest()

    def build_project_json(self) -> Dict:
        """构建项目JSON"""
        return {
            "targets": self.targets,
            "monitors": self.monitors,
            "extensions": self.extensions,
            "meta": self.meta
        }

    def save(self, filename: str):
        """保存为 .sb3 文件"""
        project_json = self.build_project_json()

        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 写入 project.json
            zf.writestr('project.json', json.dumps(project_json))

            # 添加占位图片（实际使用时应该替换为真实图片）
            for target in self.targets:
                for costume in target.get('costumes', []):
                    # 创建一个最小的 PNG 文件
                    png_data = self._create_placeholder_png()
                    zf.writestr(costume['md5ext'], png_data)

        print(f"[成功] Scratch 项目已保存: {filename}")

    def _create_placeholder_png(self, width: int = 1, height: int = 1) -> bytes:
        """创建占位符PNG（1x1透明像素）"""
        # 最小的PNG文件（1x1透明像素）
        return base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
        )


def create_hello_world_project(filename: str = "hello_world.sb3"):
    """创建一个简单的Hello World项目"""
    gen = ScratchProjectGenerator()

    # 添加舞台
    gen.add_stage("My Stage")

    # 添加角色
    sprite = gen.add_sprite("Sprite1", x=0, y=0)

    # 添加变量
    gen.add_variable(sprite, "counter", 0)

    # 添加脚本：当绿旗被点击时
    gen.add_simple_script(sprite, [
        {
            "opcode": "event_whenflagclicked",
            "fields": {},
            "inputs": {}
        },
        {
            "opcode": "control_repeat",
            "fields": {},
            "inputs": {
                "TIMES": [1, [4]]  # 重复4次
            }
        },
        {
            "opcode": "motion_movesteps",
            "fields": {},
            "inputs": {
                "STEPS": [1, [10]]  # 移动10步
            }
        },
        {
            "opcode": "looks_say",
            "fields": {},
            "inputs": {
                "MESSAGE": [1, ["Hello Scratch!"]]  # 说"Hello Scratch!"
            }
        },
        {
            "opcode": "control_wait",
            "fields": {},
            "inputs": {
                "DURATION": [1, [1]]  # 等待1秒
            }
        },
        {
            "opcode": "motion_turnright",
            "fields": {},
            "inputs": {
                "DEGREES": [1, [90]]  # 右转90度
            }
        }
    ])

    gen.save(filename)
    return filename


def create_animation_project(filename: str = "animation.sb3"):
    """创建一个动画项目"""
    gen = ScratchProjectGenerator()

    # 添加舞台
    gen.add_stage("Animation Stage")

    # 添加角色
    sprite = gen.add_sprite("Bouncing Ball", x=0, y=0)

    # 添加脚本：弹跳动画
    gen.add_simple_script(sprite, [
        {
            "opcode": "event_whenflagclicked",
            "fields": {},
            "inputs": {}
        },
        {
            "opcode": "control_forever",
            "fields": {},
            "inputs": {}
        },
        {
            "opcode": "motion_movesteps",
            "fields": {},
            "inputs": {
                "STEPS": [1, [10]]
            }
        },
        {
            "opcode": "motion_ifonedgebounce",
            "fields": {},
            "inputs": {}
        },
        {
            "opcode": "control_wait",
            "fields": {},
            "inputs": {
                "DURATION": [1, [0.1]]
            }
        }
    ])

    gen.save(filename)
    return filename


def create_music_project(filename: str = "music.sb3"):
    """创建一个音乐项目"""
    gen = ScratchProjectGenerator()

    # 添加舞台
    gen.add_stage("Music Stage")

    # 添加角色
    sprite = gen.add_sprite("Music Player", x=-150, y=0)

    # 添加脚本：播放音符
    gen.add_simple_script(sprite, [
        {
            "opcode": "event_whenflagclicked",
            "fields": {},
            "inputs": {}
        },
        {
            "opcode": "control_repeat",
            "fields": {},
            "inputs": {
                "TIMES": [1, [8]]  # 重复8次
            }
        },
        {
            "opcode": "music_playDrumForBeats",
            "fields": {
                "DRUM": [1, "1 (snare drum)"]
            },
            "inputs": {
                "BEATS": [1, [0.5]]
            }
        },
        {
            "opcode": "control_wait",
            "fields": {},
            "inputs": {
                "DURATION": [1, [0.5]]
            }
        }
    ])

    gen.save(filename)
    return filename


if __name__ == "__main__":
    import sys

    print("="*80)
    print("Scratch 3.0 项目生成器")
    print("="*80)
    print()

    # 创建示例项目
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("[1/3] 创建 Hello World 项目...")
    hello_path = str(output_dir / "hello_world.sb3")
    create_hello_world_project(hello_path)

    print("\n[2/3] 创建动画项目...")
    anim_path = str(output_dir / "animation.sb3")
    create_animation_project(anim_path)

    print("\n[3/3] 创建音乐项目...")
    music_path = str(output_dir / "music.sb3")
    create_music_project(music_path)

    print()
    print("="*80)
    print("[完成] 所有项目已生成到 output/ 目录")
    print("="*80)
    print()
    print("生成的文件:")
    print(f"1. {hello_path}")
    print(f"2. {anim_path}")
    print(f"3. {music_path}")
    print()
    print("[提示] 可以在 https://scratch.mit.edu/editor 导入这些项目")
    print()
