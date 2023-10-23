__author__ = "Emil Eldstål"
__copyright__ = "Copyright 2023, Emil Eldstål"
__version__ = "0.1.1"

from PySide2 import QtWidgets
from PySide2.QtCore import Qt

import substance_painter.ui
import substance_painter.event

import os
import configparser
import subprocess

def config_ini(overwrite):
    # Get the path to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the StarfieldPluginSettings.ini file
    ini_file_path = os.path.join(script_dir, "Starfield-DDS-Exporter-PluginSettings.ini")            
    
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Check if the INI file exists
    if os.path.exists(ini_file_path):
        # Read the INI file
        config.read(ini_file_path)
        
        # Check if the section and key exist
        if 'General' in config and 'TexConvDirectory' in config['General']:
            # Check if the value is empty
            if not config['General']['TexConvDirectory']:
                # Let's the user choose where TexConv is if not configured
                config['General']['TexConvDirectory'] = choose_texconv_folder()
            if overwrite:
                # Let's the user choose where TexConv is if using overwrite button
                config['General']['TexConvDirectory'] = choose_texconv_folder()

            # Assign the TexConvDirectory value to the TexConvPath variable
            TexConvPath = config['General']['TexConvDirectory']
        else:
            TexConvPath = choose_texconv_folder()
            # If the section or key doesn't exist, create it and set the value
            config['General'] = {}
            config['General']['TexConvDirectory'] = TexConvPath
            print("Starfield DDS Exporter Plugin: TexConvDirectory value set or updated in StarfieldPluginSettings.ini")

        # Write the updated configuration back to the INI file
        with open(ini_file_path, 'w') as configfile:
            config.write(configfile)
    else:
        TexConvPath = choose_texconv_folder()
        # If the INI file doesn't exist, create it and set the value
        with open(ini_file_path, 'w') as configfile:
            config['General'] = {}
            config['General']['TexConvDirectory'] = TexConvPath
            config.write(configfile)

    return TexConvPath

def choose_texconv_folder():
    path = QtWidgets.QFileDialog.getExistingDirectory(
    substance_painter.ui.get_main_window(),"Choose Texconv directory")
    return path +"/texconv.exe"

def convert_png_to_dds(texconvPath, sourcePNG, overwrite, format_choice):
    # Replace backslashes with forward slashes in the provided paths
    texconvPath = texconvPath.replace('\\', '/')
    sourceFolder = os.path.dirname(sourcePNG)
    sourceFolder = sourceFolder.replace('\\', '/')
    outputFolder = sourceFolder + "/DDS/"

    isExist = os.path.exists(outputFolder)
    if not isExist:
        # Create the DDS directory if it does not exist
        os.makedirs(outputFolder)
        print("Created DDS subfolder")

    # for filename in os.listdir(sourceFolder):
    filename = sourcePNG
    if filename.endswith(".png"):
        sourceFile = os.path.splitext(filename)[0]
        suffix = sourceFile.split('_')[-1]
        suffix = suffix.rstrip('_')

        outputFile = sourceFile + ".dds"

        if format_choice == "DXT1":
            format_option = "BC1_UNORM"
        elif format_choice == "DXT5":
            format_option = "BC3_UNORM"
        else:
            format_option = "BC1_UNORM"  # default in case of an unexpected value

        if overwrite:
            overwrite_option = "-y"
        else:
            overwrite_option = ""

        if outputFile:
            texconv_cmd = [
                texconvPath,
                "-nologo", overwrite_option,
                "-o", outputFolder,
                "-f", format_option,
                os.path.join(sourceFolder, filename)
            ]
            texconv_cmd_str = subprocess.list2cmdline(texconv_cmd)

            try:
                subprocess.run(texconv_cmd_str, shell=True, check=True)
                print(f"Successfully converted {filename} to {outputFile}")
            except subprocess.CalledProcessError:
                print(f"Failed to convert {filename}")

class StarfieldDDSPlugin:
    def __init__(self):
        # Export boolean whether to add DDS creation or not
        self.export = True
        # Overwrites existing DDS files if checked
        self.overwrite = True

        self.export_png = False  # Default is to export PNGs

        # Plugin Version
        self.version = "0.1.1"

        # Create a dock widget to report plugin activity.
        self.log = QtWidgets.QTextEdit()
        self.window = QtWidgets.QWidget()
        self.TexConvPath = config_ini(False)

        layout = QtWidgets.QVBoxLayout()
        sub_layout = QtWidgets.QHBoxLayout()

        checkbox = QtWidgets.QCheckBox("Export DDS files")
        checkbox.setChecked(True)
        checkbox.setToolTip("Enable this to automatically export textures in DDS format after regular export.")

        checkbox_png_export = QtWidgets.QCheckBox("Export PNG files")
        checkbox_png_export.setChecked(False)
        checkbox_png_export.setToolTip("Enable this to export PNG textures (regular export).")

        checkbox_overwrite = QtWidgets.QCheckBox("Overwrite DDS files")
        checkbox_overwrite.setChecked(True)
        checkbox_overwrite.setToolTip("Enable this to overwrite existing DDS files with the new exports.")

        button_texconv = QtWidgets.QPushButton("Texconv Folder")
        button_texconv.setToolTip("Select the directory where 'texconv.exe' resides.")

        button_clear = QtWidgets.QPushButton("Clear Log")
        button_clear.setToolTip("Clear the current log messages.")

        button_help = QtWidgets.QPushButton("Help")


        version_label = QtWidgets.QLabel("Version: {}".format(self.version))

        # Adds buttons to sub-layout
        sub_layout.addWidget(checkbox)
        sub_layout.addWidget(checkbox_overwrite)
        sub_layout.addWidget(checkbox_png_export)
        sub_layout.addWidget(button_texconv)
        sub_layout.addWidget(button_clear)
        sub_layout.addWidget(button_help)


        # LEV TEST

        # Define map types
        self.map_types = ["diffuse", "normal", "specular", "alpha"]
        
        # Dictionary to store combo boxes for each map type
        self.map_format_comboboxes = {}
        
        # Create combo boxes for each map type
        for map_type in self.map_types:
            combobox = QtWidgets.QComboBox()
            
            # If the map_type is "alpha", only add "DXT5" and "None"
            if map_type == "alpha":
                combobox.addItems(["None", "DXT5"])
            else:
                combobox.addItems(["DXT5", "DXT1", "None"])

            self.map_format_comboboxes[map_type] = combobox
                
            # Add a label and combo box to the layout
            map_label = QtWidgets.QLabel(f"{map_type.capitalize()} Format:")
            format_layout = QtWidgets.QHBoxLayout()
            format_layout.addWidget(map_label)
            format_layout.addWidget(combobox)
            layout.addLayout(format_layout)
        # LEV END TEST

        # Adds all widgets to main layout
        layout.addLayout(sub_layout)
        layout.addWidget(self.log)
        layout.addWidget(version_label)

        self.window.setLayout(layout)
        self.window.setWindowTitle("Starfield DDS Auto Converter")

        self.log.setReadOnly(True)

        # Connects buttons to click events
        checkbox.stateChanged.connect(self.checkbox_export_change)
        checkbox_overwrite.stateChanged.connect(self.checkbox_overwrite_change)
        checkbox_png_export.stateChanged.connect(self.checkbox_png_export_change)
        button_texconv.clicked.connect(self.button_texconv_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_help.clicked.connect(self.show_help_dialog)


        # Adds Qt as dockable widget to Substance Painter
        substance_painter.ui.add_dock_widget(self.window)

        self.log.append("TexConv Path: {}".format(self.TexConvPath))

        connections = {
            substance_painter.event.ExportTexturesEnded: self.on_export_finished
        }
        for event, callback in connections.items():
            substance_painter.event.DISPATCHER.connect(event, callback)

    def button_texconv_clicked(self):
        self.TexConvPath = config_ini(True)
        self.log.append("New TexConv Path: {}".format(self.TexConvPath))

    def button_clear_clicked(self):
        self.log.clear()

    def checkbox_png_export_change(self,state):
        if state == Qt.Checked:
            self.export_png = True
        else:
            self.export_png = False

    def checkbox_export_change(self,state):
        if state == Qt.Checked:
            self.export = True
        else:
            self.export = False

    def checkbox_overwrite_change(self,state):
        if state == Qt.Checked:
            self.overwrite = True
        else:
            self.overwrite = False

    def show_help_dialog(self):
        message = (
            "Starfield DDS Auto Converter\n\n"
            "1. Set the path to 'texconv.exe' using 'Choose Texconv location'.\n"
            "2. Choose your desired DDS formats using the dropdown menus.\n"
            "3. When exporting from Substance Painter, DDS files will be automatically generated."
        )
        QtWidgets.QMessageBox.information(self.window, "Help", message)

    def texconv_exists(self):
        return os.path.exists(self.TexConvPath)

    def __del__(self):
        # Remove all added UI elements.
        substance_painter.ui.delete_ui_element(self.log)
        substance_painter.ui.delete_ui_element(self.window)

    def on_export_finished(self, res):
        if not self.texconv_exists():
            QtWidgets.QMessageBox.critical(self.window, "DDS Exporter", "texconv.exe not found in the specified directory. Skipping DDS export.")
            return

        expected_suffixes = ["diffuse", "normal", "specular", "alpha"]
        exported_suffixes = [file_path.split('_')[-1].split('.')[0] for file_list in res.textures.values() for file_path in file_list]

        for suffix in expected_suffixes:
            if suffix not in exported_suffixes:
                QtWidgets.QMessageBox.warning(self.window, "Export Warning", f"The '{suffix}' suffix is missing in the exported textures. Please ensure it's present in your export template. e.g 't_$textureSet_diffuse'")

        # Logging the export results
        self.log.append(res.message)
        self.log.append("Exported files:")

        for file_list in res.textures.values():
            for file_path in file_list:
                # Extract the map type from the filename
                map_type = file_path.split('_')[-1].split('.')[0]
                
                # Check if the map type is recognized
                if map_type not in self.map_format_comboboxes:
                    self.log.append(f"Unrecognized map type: {map_type}. Skipping...")
                    continue

                # Fetch the chosen format for this map type
                chosen_format = self.map_format_comboboxes[map_type].currentText()

                # If chosen format is "None", skip the conversion
                if chosen_format == "None":
                    self.log.append(f"Skipping conversion for {file_path} as per user choice.")
                    continue

                # Log the conversion attempt
                self.log.append(f"Converting {file_path} using format {chosen_format}...")

                # Convert the file using the chosen format
                convert_png_to_dds(self.TexConvPath, file_path, self.overwrite, chosen_format)
                    
                # Log the converted file
                dds_file_path = file_path[:-3] + "dds" # Changed "DDS" to "dds" for correct extension
                if os.path.exists(dds_file_path):
                    self.log.append(f"Successfully converted to {dds_file_path}")
                else:
                    self.log.append(f"Failed to convert {file_path}")
                                # Delete the PNG after conversion if the option is unchecked
                if not self.export_png:
                    try:
                        os.remove(file_path)
                        self.log.append(f"Removed PNG: {file_path}")
                    except Exception as e:
                        self.log.append(f"Error removing PNG: {file_path}. Reason: {str(e)}")

    def on_export_error(self, err):
        self.log.append("Export failed.")
        self.log.append(repr(err))

STARFIELD_DDS_PLUGIN = None

def start_plugin():
    """This method is called when the plugin is started."""
    print ("Starfield DDS Exporter Plugin Initialized")
    global STARFIELD_DDS_PLUGIN
    STARFIELD_DDS_PLUGIN = StarfieldDDSPlugin()

def close_plugin():
    """This method is called when the plugin is stopped."""
    print ("Starfield DDS Exporter Plugin Shutdown")
    global STARFIELD_DDS_PLUGIN
    del STARFIELD_DDS_PLUGIN

if __name__ == "__main__":
    start_plugin()
