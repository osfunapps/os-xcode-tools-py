from pbxproj import XcodeProject
import os_file_handler.file_handler as fh
import os
###########################################################################
#
# this module meant to inject/remove files in any xcode project
#
###########################################################################
from pbxproj.pbxextensions import ProjectFiles


def build_project(xcodeproj_path, pbxproj_path='project.pbxproj'):
    """
    call this initially. Will create the project object to work with.

    Args:
        xcodeproj_path -> the path to your xcodeproj file
        pbxproj_path -> the path to your pbxproj file (usually just project.pbxproj)
    """
    return XcodeProject.load(xcodeproj_path + '/' + pbxproj_path)


# will create a group. if already exists, return it
def get_or_create_group(project, path_to_group):
    path = os.path.normpath(path_to_group)
    splatted_path = path.split(os.sep)
    last_group = None
    for i in splatted_path:
        last_group = project.get_or_create_group(i, parent=last_group)

        # last_group = project.get_or_create_group(i)

    return last_group
    # parent = project.get_or_create_group(parent_name)
    # return project.get_or_create_group(group_name, parent=parent)


# will add the references of a file into a group
# force = replace if exists
def add_file_to_group(project, file_path, group_obj, force=True):
    project.add_file(file_path, force=force, parent=group_obj)


# will add the references of files into a group
# force = replace if exists
def add_arr_of_files_to_group(project, arr_of_files, group_obj, force=True):
    for file_path in arr_of_files:
        add_file_to_group(project, file_path, group_obj, force)


# remove a whole group
def remove_group(project, group_name):
    return project.remove_group_by_name(group_name)


def remove_file_from_group(project, group, file_name):
    for f in group.children:
        if f._get_comment() == file_name:
            project.remove_file_by_id(f)


# will remove all of the references of files from a given group
def clear_all_files_from_group(project, group_obj):
    while True:
        if len(group_obj.children) == 0:
            project.save()
            return
        for file in group_obj.children:
            project.remove_file_by_id(file)


# will add the ability to inject these array of extensions (add .zip, .xml etc...)
def add_files_extensions_arr(extensions_arr):
    for ext in extensions_arr:
        ProjectFiles._FILE_TYPES[ext] = (ext[1:] + ext, u'PBXResourcesBuildPhase')


# will change the bundle id
def change_bundle_identifier(project, new_bundle_id):
    set_custom_flag(project, 'PRODUCT_BUNDLE_IDENTIFIER', new_bundle_id)


# will set a custom flag to the project
def set_custom_flag(project, key, val):
    project.set_flags(key, val)


# will replace the info.plist file of the project.
# do this if you want to change the display name of the current project, for example.
def replace_info_plist_file(old_info_file, new_info_file):
    fh.copy_file(new_info_file, old_info_file)


# save the changes in the project, otherwise your changes won't be picked up by Xcode
def save_changes(project):
    project.save()
