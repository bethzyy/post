# -*- coding: utf-8 -*-
"""测试图片生成"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from article.toutiao_article_generator import ToutiaoArticleGenerator

# 测试内容（包含emoji）
test_content = """阳春三月，春风拂面。

🐷 猪肉呢，得挑那瘦肉，尤其是春天。

🥬 蔬菜要新鲜的。

最后总结一下春季养生之道。"""

gen = ToutiaoArticleGenerator()

print("=" * 60)
print("测试生成4张配图（包含emoji）")
print("=" * 60)

try:
    images = gen.generate_article_images(
        theme="春季食趣",
        article_content=test_content,
        image_style="realistic",
        num_images=4
    )
    print("\n" + "=" * 60)
    print(f"成功生成 {len(images)} 张图片")
    print("=" * 60)
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
