import os

# 1. Change menu name @minhiosne -> @elbasanlliu1010
draw_path = 'project/ImGuiDrawView.mm'
if os.path.exists(draw_path):
    with open(draw_path, 'r') as f:
        content = f.read()
    content = content.replace('@minhiosne', '@elbasanlliu1010')
    with open(draw_path, 'w') as f:
        f.write(content)
    print('Patched menu name in ImGuiDrawView.mm')

# 2. Patch Helper/Hooks.h - add chrono include
hooks_path = 'project/Helper/Hooks.h'
if os.path.exists(hooks_path):
    with open(hooks_path, 'r') as f:
        content = f.read()
    if '#include <chrono>' not in content:
        content = '#include <chrono>\n' + content
        with open(hooks_path, 'w') as f:
            f.write(content)
        print('Patched Hooks.h')

# 3. Patch Other/dobby_defines.h
dobby_path = 'project/Other/dobby_defines.h'
if os.path.exists(dobby_path):
    with open(dobby_path, 'r') as f:
        content = f.read()
    if '#include <stdint.h>' in content and 'extern "C"' in content:
        content = content.replace('#include <stdint.h>', '')
        content = '#include <stdint.h>\n' + content
        with open(dobby_path, 'w') as f:
            f.write(content)
        print('Patched dobby_defines.h')

# 4. Patch Helper/Monostring.h
mono_path = 'project/Helper/Monostring.h'
if os.path.exists(mono_path):
    with open(mono_path, 'r') as f:
        content = f.read()
    content = content.replace('->template toCPPlist()', '->toCPPlist()')
    with open(mono_path, 'w') as f:
        f.write(content)
    print('Patched Monostring.h')

# 5. Add API authentication to PubgLoad.mm
pubg_path = 'project/Esp/PubgLoad.mm'
if os.path.exists(pubg_path):
    with open(pubg_path, 'r') as f:
        content = f.read()
    if '#import "../API/APIClient.h"' not in content:
        content = '#import "../API/APIClient.h"\n' + content
    old_block = '        if (!extraInfo) {'
    new_block = '''        apiclient_set_token("nV27GCsmVC/45wmNlAwcxHUtWgVuJgTAJTNkZ6q7uk+Ni0nwolEDstMEOrlEsxHyiUUj4M/7hRwYD6VApIf9c3kkgQYy6dWE/B69+eT5F0g=");
        apiclient_paid(^{
            if (!extraInfo) {'''
    if old_block in content and 'apiclient_set_token' not in content:
        content = content.replace(old_block, new_block)
        # Close the apiclient_paid block before the end of dispatch_after
        content = content.replace(
            '        kick_hacker_delayed(); \n        \n        // --- KET THUC PHAN THUC THI ---',
            '        kick_hacker_delayed();\n        });\n        // --- KET THUC PHAN THUC THI ---'
        )
        # simpler close
        content = content.replace('        kick_hacker_delayed(); \n        ', '        kick_hacker_delayed();\n        });\n        ')
    with open(pubg_path, 'w') as f:
        f.write(content)
    print('Patched PubgLoad.mm')

# 6. Patch Makefile to add API linker flag
makefile_path = 'project/Makefile'
if os.path.exists(makefile_path):
    with open(makefile_path, 'r') as f:
        content = f.read()
    if 'API/libAPIClient.a' not in content:
        content = content.replace(
            '$(TWEAK_NAME)_LDFLAGS +=',
            '$(TWEAK_NAME)_LDFLAGS += API/libAPIClient.a'
        )
        with open(makefile_path, 'w') as f:
            f.write(content)
        print('Patched Makefile with API linker flag')

print('All patches done!')
