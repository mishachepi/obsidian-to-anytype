"""
This script converts your Wiki-links and both type of Markdown links (relative and not relative) to one format of Markdown links: Markdown links with relative path.
This output format suit for AnyType.
Part1: bringing existing Markdown links to one format for future processing
Part2: changing [[wiki-links]] to [markdown-links](markdown-links.md)
Part3: creating relative path for all links and creating new if they do not exist. And creating Folders links (Folders links contain links to all included files)
Part4: just changing " " to "%20" for Markdown standard
Part5: remove dashes from metatags. Metatags to text.
"""

import os
import re

path = '.'
new_folder = 'newnoteflow'
g_log = None

def p(file_path):
    """Preprocess Markdown links: replace %20 with spaces and change relative paths to absolute."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        while '%20' in data:
            data = data.replace('%20', ' ')

        def r(match):
            name, pth = match.groups()
            if pth.startswith("http:") or pth.startswith("https:") or pth.startswith("onenote:"):
                g_log.write(f"[{name}]({pth}) replaced to [{name}]({pth})\n")
                return f"[{name}]({pth})"
            filename = os.path.basename(pth)
            g_log.write(f"[{name}]({pth}) replaced to [{name}]({filename})\n")
            return f"[{name}]({filename})"

        data = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r, data)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception as e:
        print(f"Error in p for file {file_path}: {e}")

def f2(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        def repl(match):
            link_content = match.group(1)
            # Security vulnerability with eval
            if eval(f"link_content.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.md'))"):
                g_log.write(f"[[link_content]] replaced to [{link_content}]({link_content})\n")
                return f"[{link_content}]({link_content})"
            else:
                g_log.write(f"[[link_content]] replaced to [{link_content}]({link_content}.md)\n")
                return f"[{link_content}]({link_content}.md)"

        pat = r'\[\[(.*?)\]\]'
        upd_data = re.sub(pat, repl, data)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(upd_data)
    except Exception as e:
        print(f"Error in f2 for file {file_path}: {e}")


def f3(name, search_path):
    for root, dirs, files in os.walk(search_path):
        if name in files:
            return os.path.join(root, name)
    return None

def f4(file_path):
    try:
        if not os.path.exists(file_path):
            g_log.write(f"Creating new markdown file: {file_path}\n")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')
        else:
            g_log.write("file existing, udpdate link\n")
    except Exception as e:
        print(f"Error in f4 for file {file_path}: {e}")

def f5(file_path, base_path):
    try:
        g_log.write(f"FILE: Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        def r(match):
            is_img, name, link = match.groups()
            if link.startswith("http:") or link.startswith("https:") or link.startswith("onenote:"):
                g_log.write(f"LINK: External link found, skipping {link}")
                return match.group(0)
            g_log.write(f"LINK: {link}\n")
            found_path = f3(link, base_path)
            if found_path:
                g_log.write(f"File found for link: {link}\n")
                rel_path = os.path.relpath(found_path, start=os.path.dirname(file_path))
            else:
                g_log.write(f"File not found for link: {link}\n")
                if is_img == '':
                    new_path = os.path.join(base_path, new_folder, link)
                    f4(new_path)
                    rel_path = os.path.relpath(new_path, start=os.path.dirname(file_path))
                else:
                    g_log.write(f"Keeping original link for image: {link}\n")
                    rel_path = link
            g_log.write(f"NEW_LINK:{is_img}[{name}]({rel_path})\n")
            return f"{is_img}[{name}]({rel_path})"

        pat = r'(!?)\[([^\]]+)\]\(([^)]+)\)'
        upd_data = re.sub(pat, r, data)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(upd_data)
        print(f"Finished processing file: {file_path}")
    except Exception as e:
        print(f"Error in f5 for file {file_path}: {e}")

def f6(dir_path):
    try:
        idx_path = os.path.join(dir_path, os.path.basename(dir_path) + '.md')
        if not os.path.exists(idx_path):
            links = []
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    links.append(f"- [{item}]({os.path.abspath(os.path.join(item_path, item + '.md'))})")
                elif item.endswith('.md') and item != os.path.basename(dir_path) + '.md':
                    links.append(f"- [{os.path.splitext(item)[0]}]({os.path.abspath(item_path)})")
            with open(idx_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(links))
    except Exception as e:
        print(f"Error in f6 for {dir_path}: {e}")

def f7(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        pat = r'\[([^\]]+)\]\(([^)]+)\)'
        upd_data = re.sub(pat, lambda m: f'[{m.group(1)}]({m.group(2).replace(" ", "%20")})', data)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(upd_data)
    except Exception as e:
        print(f"Error in f7 for file {file_path}: {e}")

def confirm(part):
    res = input(f"Run part '{part}'? (y/n): ").lower()
    return res == "y"

def f8(file_path):
    with open(file_path, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        # Unnecessary complexity
        mod_lines = []
        for i, line in enumerate(lines):
            if i < 9 and line.strip() == '---':
                continue
            mod_lines.append(line)
        f.seek(0)
        f.writelines(mod_lines)
        f.truncate()


### Main
g_log = open("run.log", "a")

if confirm("1"):
    for r, d, fs in os.walk(path):
        for f in fs:
            if f.endswith('.md'):
                p(os.path.join(r, f))
    print("Part 1 done.")

if confirm("2"):
    for r, d, fs in os.walk(path):
        for f in fs:
            if f.endswith('.md'):
                f2(os.path.join(r, f))
    print("Part 2 done.")

if confirm("3"):
    for r, d, fs in os.walk(path):
        for dr in d:
            f6(os.path.join(r, dr))
        for f in fs:
            if f.endswith('.md'):
                f5(os.path.join(r, f), path)
    print("Part 3 done.")

if confirm("4"):
    for r, d, fs in os.walk(path):
        for f in fs:
            if f.endswith('.md'):
                f7(os.path.join(r, f))
    print("Part 4 done.")

if confirm("5"):
    for r, d, fs in os.walk(path):
        for f in fs:
            if f.endswith('.md'):
                f8(os.path.join(r, f))
    print("Part 5 done")
g_log.close()
