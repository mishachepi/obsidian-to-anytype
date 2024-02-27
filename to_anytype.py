import os
import re

"""
This script converted your Wiki-links and both type of Markdown links (relative and not relative) to one format of Markdown links: Markdown links with relative path.
This output format suit for AnyType.
Part1: bringing existing Markdown links to one format for future processing
Part2: changing [[wiki-links]] to [markdown-links](markdown-links.md)
Part3: createing relative path for all links and creating new if not exist. And creating Folders links (Folders links contain links to all included files)
Part4: just changing " " to "%20" for Markdown standart
"""

base_path = '.'
newfiles_folder = 'newnoteflow'

# Part1
def preprocess_md_links(file_path):
    """Preprocess Markdown links: replace %20 with spaces and remove relative paths."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()

        # Replace %20 with spaces
        contents = re.sub(r'%20', ' ', contents)

        # Remove relative paths, keeping only the file name
        def remove_relative_path(match):
            name, path = match.groups()
            filename = os.path.basename(path)
            return f"[{name}]({filename})"

        contents = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', remove_relative_path, contents)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(contents)
    except Exception as e:
        print(f"Error preprocessing Markdown links in file {file_path}: {e}")

# Part2
def replace_wiki_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()

        def replace_function(match):
            link_content = match.group(1)
            if link_content.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.md')):
                return f"[{link_content}]({link_content})"
            else:
                return f"[{link_content}]({link_content}.md)"

        pattern = r'\[\[(.*?)\]\]'
        updated_contents = re.sub(pattern, replace_function, contents)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_contents)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


# Part3
def find_file(name, search_path):
    for root, dirs, files in os.walk(search_path):
        if name in files:
            return os.path.join(root, name)
    return None

def create_if_not_exists(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"Creating new markdown file: {file_path}")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('')
        else:
            print("file found, udpdate link")
    except Exception as e:
        print(f"Error creating file {file_path}: {e}")

def update_links_and_create_directory_index(file_path, base_path):
    try:
        print(f"Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()

        def replace_link(match):
            is_image, name, link = match.groups()
            print("link:", link)
            if link.startswith("http:") or link.startswith("https:") or link.startswith("onenote:"):
                print(f"External link found, skipping: {link}")
                return match.group(0)

            print(f"Processing link: {link}")
            found_path = find_file(link, base_path)
            if found_path:
                print(f"File found for link: {link}")
                relative_path = os.path.relpath(found_path, start=os.path.dirname(file_path))
            else:
                print(f"File not found for link: {link}")
                if is_image == '':
                    newfiles_path = os.path.join(base_path, newfiles_folder, link)
                    create_if_not_exists(newfiles_path)
                    relative_path = os.path.relpath(newfiles_path, start=os.path.dirname(file_path))
                else:
                    print(f"Keeping original link for image: {link}")
                    relative_path = link
            return f"{is_image}[{name}]({relative_path})"

        pattern = r'(!?)\[([^\]]+)\]\(([^)]+)\)'
        updated_contents = re.sub(pattern, replace_link, contents)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_contents)
        print(f"Finished processing file: {file_path}")
    except Exception as e:
        print(f"Error updating links in file {file_path}: {e}")

def create_directory_index(dir_path):
    try:
        index_file_path = os.path.join(dir_path, os.path.basename(dir_path) + '.md')
        if not os.path.exists(index_file_path):
            links = []
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    links.append(f"- [{item}]({os.path.abspath(os.path.join(item_path, item + '.md'))})")
                elif item.endswith('.md') and item != os.path.basename(dir_path) + '.md':
                    links.append(f"- [{os.path.splitext(item)[0]}]({os.path.abspath(item_path)})")
            with open(index_file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(links))
    except Exception as e:
        print(f"Error creating index file in {dir_path}: {e}")

# Part4
def update_md_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        updated_contents = re.sub(pattern, lambda m: f'[{m.group(1)}]({m.group(2).replace(" ", "%20")})', contents)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_contents)
    except Exception as e:
        print(f"Error updating Markdown links in file {file_path}: {e}")

def confirm_execution(part):
    response = input(f"Do you want to execute the script part '{part}'? (yes/no): ").lower()
    return response in ["yes"]

### Main
if confirm_execution("1. Preprocessing .md links. Changeing .md links to one format"):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                preprocess_md_links(os.path.join(root, file))
    print("Preprocessing of Markdown links completed.")

if confirm_execution("2. Replacing wiki-links with md-links"):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                replace_wiki_links(os.path.join(root, file))
    print("Wiki-links to md-links replacement completed.")

if confirm_execution("3. Making links relative and creating directory indexes"):
    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            create_directory_index(os.path.join(root, dir))
        for file in files:
            if file.endswith('.md'):
                update_links_and_create_directory_index(os.path.join(root, file), base_path)
    print("Links updating and directory indexes creation completed.")

if confirm_execution("4. Updating Markdown links: replace spaces to %20"):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                update_md_links(os.path.join(root, file))
    print("Markdown links update completed.")
