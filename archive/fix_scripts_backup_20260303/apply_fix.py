# -*- coding: utf-8 -*-
"""
修复文章解析逻辑 - 使用更简单的方法
"""

# 读取文件
with open('toutiao_article_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复1: improve_article_draft 方法
old_code_1 = """            for i, line in enumerate(lines):
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.strip() == "---":
                    continue
                elif title:  # 已找到标题后,其余内容为正文
                    body_lines.append(line)

            body = '\\n'.join(body_lines).strip()

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else "今日头条文章"

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length,
                'source': 'draft_improvement'
            }

        except Exception as e:
            print(f"[ERROR] 草稿完善失败: {e}")
            return None

    def generate_article_with_ai(self, theme, target_length=2000, style='standard'):"""

new_code_1 = """            for i, line in enumerate(lines):
                stripped_line = line.strip()

                # 查找标题行
                if stripped_line.startswith("标题:"):
                    title = stripped_line.replace("标题:", "").strip()
                    found_title = True
                    continue

                # 跳过分隔符和空行
                if stripped_line == "---" or stripped_line.startswith("---") or not stripped_line:
                    continue

                # 跳过占位符文字(如"[完善后的正文内容]")
                if stripped_line.startswith("[") and stripped_line.endswith("]"):
                    started_body = True
                    continue

                # 如果已经找到标题,开始收集正文
                if found_title:
                    started_body = True

                if started_body:
                    body_lines.append(line)

            body = '\\n'.join(body_lines).strip()

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else "今日头条文章"

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length,
                'source': 'draft_improvement'
            }

        except Exception as e:
            print(f"[ERROR] 草稿完善失败: {e}")
            return None

    def generate_article_with_ai(self, theme, target_length=2000, style='standard'):"""

content = content.replace(old_code_1, new_code_1)

# 添加新的变量定义
old_code_2 = """            # 解析标题和正文
            lines = content.split('\\n')
            title = ""
            body_lines = []"""

new_code_2 = """            # 解析标题和正文
            lines = content.split('\\n')
            title = ""
            body_lines = []
            found_title = False
            started_body = False"""

content = content.replace(old_code_2, new_code_2)

# 修复2: generate_article_with_ai 方法 - 同样的修复
old_code_3 = """            for i, line in enumerate(lines):
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.strip() == "---":
                    continue
                elif title:  # 已找到标题后,其余内容为正文
                    body_lines.append(line)

            body = '\\n'.join(body_lines).strip()

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else f"关于{theme}的思考"

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length
            }

        except Exception as e:
            print(f"[ERROR] AI生成失败: {e}")
            return None

    def generate_article_images(self, theme, article_content="", image_style="realistic"):"""

new_code_3 = """            for i, line in enumerate(lines):
                stripped_line = line.strip()

                # 查找标题行
                if stripped_line.startswith("标题:"):
                    title = stripped_line.replace("标题:", "").strip()
                    found_title = True
                    continue

                # 跳过分隔符和空行
                if stripped_line == "---" or stripped_line.startswith("---") or not stripped_line:
                    continue

                # 跳过占位符文字(如"[正文内容]")
                if stripped_line.startswith("[") and stripped_line.endswith("]"):
                    started_body = True
                    continue

                # 如果已经找到标题,开始收集正文
                if found_title:
                    started_body = True

                if started_body:
                    body_lines.append(line)

            body = '\\n'.join(body_lines).strip()

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else f"关于{theme}的思考"

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length
            }

        except Exception as e:
            print(f"[ERROR] AI生成失败: {e}")
            return None

    def generate_article_images(self, theme, article_content="", image_style="realistic"):"""

content = content.replace(old_code_3, new_code_3)

# 写回文件
with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("修复完成!")
