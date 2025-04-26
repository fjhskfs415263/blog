
import os
import re
import shutil

# 配置路径
posts_dir = r"D:\code\blog\terminal_website\content\posts"
attachments_dir = r"D:\work\write\obsidian vault\Attachments"
static_images_dir = r"D:\code\blog\terminal_website\static\images"

# 确保 static/images 目录存在
os.makedirs(static_images_dir, exist_ok=True)

# 统计用
total_files_processed = 0
total_images_copied = 0

print("开始处理Markdown文件...\n")

for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"处理文件：{filename}")
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # !!! 这里改了 !!! 支持 ![[xxx.jpg]]
        images = re.findall(r'!\[\[([^]]*\.(?:png|jpg|jpeg|gif))\]\]', content)
        print(f"  找到 {len(images)} 张图片")

        for image in images:
            # 替换成标准 Markdown 图片链接
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"![[{image}]]", markdown_image)
            
            # 拷贝图片
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)
                print(f"    ✅ 已复制图片：{image}")
                total_images_copied += 1
            else:
                print(f"    ⚠️ 找不到图片，跳过：{image}")

        # 保存回原Markdown
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        
        total_files_processed += 1

print("\n处理完成 ✅")
print(f"总共处理了 {total_files_processed} 个Markdown文件")
print(f"总共复制了 {total_images_copied} 张图片")
