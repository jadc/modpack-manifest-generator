# Modpack manifest.json Generator
# by Jad Chehimi

import requests
import json
import sys

# Prepare headers with unique user-agent
headers = {'User-Agent': 'modmanifestgen'}

# Reads manifest template
with open('manifest-template.json') as m:
    manifest = json.load(m)

# Check if version is configured in manifest
if manifest['minecraft']['version'] == '':
    print('Error. There is no Minecraft version specified in the manifest.json')
    exit()

# Determines latest forge modloader version depending on mc version
modLoaderData = requests.get('https://addons-ecs.forgesvc.net/api/v2/minecraft/modloader', headers=headers)
for key in modLoaderData.json():
    if(key['latest'] == True):
        if(key['gameVersion'] == manifest['minecraft']['version']):
            modLoaders = []
            modLoaders.append({"id":key['name'], "primary":True})
            manifest['minecraft']["modLoaders"] = modLoaders

# Reads file from drag and drop or first argument, otherwise emods.txt
if(len(sys.argv) > 1):
    i = open(sys.argv[1], 'r')
else:
    try:
        i = open('mods.txt')
    except FileNotFoundError:
        print('Error. Default mods list (mods.txt) not found; either create it or use another file in the argument/drag and drop.')
        exit()

# Prepares output file
mods = {
    'files': []
}

# Mod log function
line = 0

def log(s):
    global line
    print('LINE #' + str(line).zfill(4) + ': ' + s)

# For every mod id
for projectID in i:
    line += 1

    # Remove whitespace
    projectID = projectID.strip()

    # Skip blank lines
    if not projectID:
        continue

    # Skip comments
    if projectID.startswith('#'):
        print(projectID)
        continue

    # API GET Request
    req = requests.get('https://addons-ecs.forgesvc.net/api/v2/addon/' + projectID, headers=headers)

    # Skip non-existent mods
    if req.status_code == 404:
        log('Failed to add mod. Not found.')
        continue

    data = req.json()

    # Gets mod name
    modname = data['name']

    # Gets file id for latest build in desired mc version
    for key in data['gameVersionLatestFiles']:

        buildExists = False
        # If mod has desired mc version
        if key['gameVersion'] == manifest['minecraft']['version']:
            # Prepares json for mod
            mod = {}
            mod['alias'] = modname + ' (' + key['projectFileName'] + ')'
            mod['projectID'] = int(projectID)
            mod['fileID'] = key['projectFileId']
            mod['required'] = True

            mods['files'].append(mod)
            log('Added [' + modname + '] (' + key['projectFileName'] + ')')
            buildExists = True
            break
        
    if not buildExists:
        log('Failed to add [' + modname + '], no build for MC ' + manifest['minecraft']['version'])

# Add files object to manifest
manifest['files'] = mods['files']

# Output manifest json to file (with beautify)
with open('manifest.json', 'w') as o:
    json.dump(manifest, o, sort_keys=True, indent=4)

print('Done. Press ENTER to close this window.')

# Pause to allow viewing of logs
input()
