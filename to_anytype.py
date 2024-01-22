import os
import re

base_path = '.'
newfiles_folder = 'newnoteflow'

def confirm_execution(part):
    response = input(f"Do you want to execute the script part '{part}'? (yes/no): ").lower()
    return response in ["yes"]

def replace_wiki_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
        pattern = r'\[\[(.*?)\]\]'
        updated_contents = re.sub(pattern, lambda m: f"[{m.group(1)}]({m.group(1)}.md)", contents)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_contents)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def find_file(name, search_path):
    for root, dirs, files in os.walk(search_path):
        if name in files:
            return os.path.join(root, name)
    return None

def create_if_not_exists(file_path):
    try:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('')
    except Exception as e:
        print(f"Error creating file {file_path}: {e}")

def update_links_and_create_directory_index(file_path, base_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()

        def replace_link(match):
            is_image, name, link = match.groups()

            # Skip external links
            if link.startswith("http://") or link.startswith("https://"):
                return match.group(0)

            found_path = find_file(link, base_path)
            if found_path:
                # Use relative path
                relative_path = os.path.relpath(found_path, start=os.path.dirname(file_path))
            else:
                # If file not found, create it in newnoteflow folder (for .md files only)
                if is_image == '':
                    newfiles_path = os.path.join(base_path, newfiles_folder, link)
                    create_if_not_exists(newfiles_path)
                    relative_path = os.path.relpath(newfiles_path, start=os.path.dirname(file_path))
                else:
                    # For images, keep original link if file not found
                    relative_path = link
            return f"{is_image}[{name}]({relative_path})"

        pattern = r'(!?)\[([^\]]+)\]\(([^)]+)\)'
        updated_contents = re.sub(pattern, replace_link, contents)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_contents)
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


if confirm_execution("Replace wiki-links with md-links"):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                replace_wiki_links(os.path.join(root, file))
    print("Wiki-links to md-links replacement completed.")

if confirm_execution("Make links relative and create directory indexes"):
    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            create_directory_index(os.path.join(root, dir))
        for file in files:
            if file.endswith('.md'):
                update_links_and_create_directory_index(os.path.join(root, file), base_path)
    print("Links updating and directory indexes creation completed.")

if confirm_execution("Update Markdown links: replace spaces to %20"):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                update_md_links(os.path.join(root, file))
    print("Markdown links update completed.")
