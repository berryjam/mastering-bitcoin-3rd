import re
import sys
import os

def convert_hint_blocks(text):
    # 将 GitBook hint 块转为标准 Markdown blockquote，兼容 Pandoc 输出
    def repl(m):
        style = m.group(1)
        content = m.group(2).strip()
        style_map = {
            "info": "信息",   
            "warning": "警告",  
            "danger": "注意"   
        }
        prefix = style_map.get(style, style)
        # 每行加 > 前缀，首行加类型
        lines = content.splitlines()
        if lines:
            lines[0] = f"**{prefix}：** " + lines[0]
        content = "\n".join([f"> {line}" for line in lines])
        return content + "\n"
    return re.sub(r'{% hint style="(\w+)" %}([\s\S]*?){% endhint %}', repl, text)

def convert_figure_img(text):
    # 只识别图片 src 路径，全部替换为 .gitbook/assets/xxx，caption 只取 <p>...</p> 内容
    def repl(m):
        src = m.group(1)
        filename = os.path.basename(src)
        new_src = f'.gitbook/assets/{filename}'
        figcaption = m.group(2)
        # 只取 <p>...</p> 里的内容作为 caption
        p_match = re.search(r'<p>([\s\S]*?)</p>', figcaption, re.IGNORECASE)
        caption = p_match.group(1).strip() if p_match else ''
        return f'![{caption}]({new_src})\n'
    return re.sub(
        r'<figure>\s*<img [^>]*src="([^"]+)"[^>]*>\s*<figcaption>([\s\S]*?)</figcaption>\s*</figure>',
        repl,
        text,
        flags=re.IGNORECASE
    )

def main():
    content = sys.stdin.read()
    content = convert_hint_blocks(content)
    content = convert_figure_img(content)
    sys.stdout.write(content)

if __name__ == "__main__":
    main()
