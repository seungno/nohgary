import maya.cmds as cmds
top_grop =  cmds.ls(sl=1)
origin_path_list = []
temp_top_name = ""
for i in top_grop:
    temp_top_name =  cmds.ls(i, assemblies=1)
top_name = temp_top_name[0].split("_")[2]
overlap_remove = []
selShapes = cmds.listRelatives(top_grop, allDescendents=1)
print(selShapes)
for i in selShapes:
    cmds.rename(i, "{0}_{1}".format(i,top_name))




    