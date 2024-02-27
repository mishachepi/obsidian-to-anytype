# obsidian-to-anytype
This script help to migrate from Obsidian to Anytype.  
This script converted your Wiki-links and both type of Markdown links (relative and not relative) to one format of Markdown links: Markdown links with relative path.
This output format suit for AnyType.
- Part1: bringing existing Markdown links to one format for future processing
- Part2: changing [[wiki-links]] to [markdown-links](markdown-links.md)
- Part3: createing relative path for all links and creating new if not exist. And creating Folders links (Folders links contain links to all included files)
- Part4: just changing " " to "%20" for Markdown standart

### How to use
- Create backup
- Copy to_anytype.py to root of obsidian workspace
- Execute to_anytype.py from root of Obsidian workspace.

### todo
- save metatags
    - maybe convert to anyblocks
