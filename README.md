<h1 align="center">
~~Starfield~~ GTA Substance Painter DDS Exporter
</h1>

<p align="center">
	<img src="https://staticdelivery.nexusmods.com/mods/4187/images/4891/4891-1696725885-1834762162.png" width=50% height=50%>
</p>

## Original author
https://github.com/emomilol1213/Substance-Painter-DDS-Exporter

# Installation: 
Extract the starfield-dds-exporter.py into your Substance Painter Plugin folder:
<pre>
C:\Users\username\Documents\Adobe\Adobe Substance 3D Painter\python\plugins
</pre>

(Can also be found using the Python > Plugins Folder button in the top row)

## Plugin
<p align="center">
	<img src="https://imgur.com/azPxKZ0.png" width=100% height=100%>
</p>

## Features

- Choose format type for each map type
<img src="https://imgur.com/1cLr4iS.png" width=75% height=50%>

 - **DXT5** - Higher quality texture with transparency (alpha) but size is a bit bigger (just use this for most things really)
 
 - **DXT1** - No transparency format, also lowers the quality and can cause artifacts, smaller size than DXT5 though
 
 - **None** - Will not export that DDS texture
- Export only DDS (Skip/Delete PNGs on export)
- Help dialog if you are clueless
- Some other changes...

## Export preset (IMPORTANT): 
Move the GTA 5.spexp file to this folder: 
<pre>
C:\Users\username\Documents\Adobe\Adobe Substance 3D Painter\assets\export-presets
</pre>

OR

Make sure you use specific suffixes in your export template, like this: 

![](https://imgur.com/PwW9juz.png)

## Enable the Starfield-DDS-Exporter under the Python menu
First time running the plugin it will ask you what folder the Texconv.exe is located in via a UI pop-up. This will create a Starfield-DDS-Exporter-PluginSettings.ini in the plugin folder with the settings saved.

![plugin widget](https://staticdelivery.nexusmods.com/mods/4187/images/4891/4891-1696725603-1907132508.png)
Dockable widget with output terminal and basic settings

# Dependencies:
Microsoft Texconv (Download and extract to whatever folder you want)

https://github.com/Microsoft/DirectXTex/wiki/Texconv

# Compatibility
Developed and tested with Substance Painter 7.3.1 (2021)

## Support
For support, please use this repository's GitHub Issues tracking service. Feel free to send me an email if you use and like the plugin.

Copyright (c) 2023 Emil Eldstål
::