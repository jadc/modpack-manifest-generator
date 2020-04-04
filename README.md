# Modpack manifest.json Generator
A small python script that automatically generates a `manifest.json` file for you simply from a list of Curseforge mod project IDs.

It automatically downloads the latest release of forge and each mod for your desired Minecraft version.

## Instructions
1. Open `mods.txt`, and write the Project ID of each mod you want, seperating each one with a new line.  
   ![Project ID](https://i.imgur.com/sSSJuMi.png)

   Your mods.txt should look something like this.  
   ![mods.txt example](https://i.imgur.com/dZvwVFV.png)

2. Edit `manifest-template.json` to your liking. Ensure `version` is set to the desired Minecraft version of the modpack.  
   a. If you are planning to have an overrides folder, add `"overrides": "overrides"`

3. Generate the manifest.json by double-clicking `generate.pyc` with Python installed.  
   *(alternatively, run it in terminal if you know how)*

4. A manifest.json should now be in the directory.  
   Move that to your modpack folder, zip it up, and your modpack should import into MultiMC perfectly.

### Other Files
You can alternatively use other files instead of the mods.txt.  
Simply just drag and drop the file onto `generate.pyc`, or state it as the first argument in a command.

## Releases
The released are simply minified versions of the source code. If you don't know what that means, don't worry, just click the link below.

[Download the latest release](https://github.com/jadc/modpack-manifest-generator/releases)
