import os, re

# 1. Change menu name -> @NOLITE
draw_path = 'project/ImGuiDrawView.mm'
if os.path.exists(draw_path):
    with open(draw_path, 'r') as f:
        content = f.read()
    content = re.sub(r'@minhiosne|@elbasanlliu1010|@MONTA|@NOLITE', '@NOLITE', content)
    with open(draw_path, 'w') as f:
        f.write(content)
    print('Patched menu name -> @NOLITE')

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
    if 'apiclient_set_token' not in content:
        old_block = (
            '        if (!extraInfo) {\n'
            '            extraInfo = [PubgLoad new];\n'
            '        }\n'
            '        [extraInfo initTapGes];\n'
            '        [extraInfo initTapGes2];\n'
            '\n'
            '        // K\u00edch ho\u1ea1t Menu v\u00e0 c\u00e1c h\u00e0m li\u00ean quan\n'
            '        MenDeal = true; \n'
            '        kick_hacker_delayed(); '
        )
        new_block = (
            '        apiclient_set_token("nV27GCsmVC/45wmNlAwcxK216pvJs5GILvWY3SXAlsCNi0nwolEDstMEOrlEsxHyiUUj4M/7hRwYD6VApIf9c3kkgQYy6dWE/B69+eT5F0g=");\n'
            '        apiclient_paid(^{\n'
            '            if (!extraInfo) {\n'
            '                extraInfo = [PubgLoad new];\n'
            '            }\n'
            '            [extraInfo initTapGes];\n'
            '            [extraInfo initTapGes2];\n'
            '            MenDeal = true;\n'
            '            kick_hacker_delayed();\n'
            '        });'
        )
        if old_block in content:
            content = content.replace(old_block, new_block)
            print('Patched PubgLoad.mm with API auth (exact match)')
        else:
            content = re.sub(
                r'        if \(!extraInfo\) \{.*?kick_hacker_delayed\(\);',
                '        apiclient_set_token("nV27GCsmVC/45wmNlAwcxK216pvJs5GILvWY3SXAlsCNi0nwolEDstMEOrlEsxHyiUUj4M/7hRwYD6VApIf9c3kkgQYy6dWE/B69+eT5F0g=");\n        apiclient_paid(^{\n            if (!extraInfo) {\n                extraInfo = [PubgLoad new];\n            }\n            [extraInfo initTapGes];\n            [extraInfo initTapGes2];\n            MenDeal = true;\n            kick_hacker_delayed();\n        });',
                content, flags=re.DOTALL
            )
            print('Patched PubgLoad.mm with API auth (regex)')
    else:
        # Already patched - just update the token
        content = re.sub(r'apiclient_set_token\("[^"]*"\)', 'apiclient_set_token("nV27GCsmVC/45wmNlAwcxK216pvJs5GILvWY3SXAlsCNi0nwolEDstMEOrlEsxHyiUUj4M/7hRwYD6VApIf9c3kkgQYy6dWE/B69+eT5F0g=")', content)
        print('Updated API token in PubgLoad.mm')
    with open(pubg_path, 'w') as f:
        f.write(content)

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
        print('Patched Makefile')

print('All patches done!')
