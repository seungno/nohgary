import maya.cmds as cmds
import os
import shutil

top_grop =  cmds.ls(sl=1)
origin_path_list = []
temp_top_name = ""
for i in top_grop:
    temp_top_name =  cmds.ls(i, assemblies=1)
top_name = temp_top_name[0].split("_")[1]
print(top_name)



overlap_remove = []
selShapes = cmds.listRelatives(top_grop, allDescendents=1)
# gpuCacheShapes = cmds.ls(selShapes, long=True, type='gpuCache')

for i in selShapes:
    filepath = cmds.getAttr(i + '.cacheFileName')
    if filepath not in overlap_remove:
        overlap_remove.append(filepath)
for j in overlap_remove:
    aa = "".join(j)
    filename = aa.split('/')[-1]

#H:\HeroRiseMan\Reference\Background\AncientKingdomINT\GPU\
    origin_path = "H:\HeroRiseMan\Reference\Background"+"\{0}".format(top_name)+"\GPU"+"\{0}".format(filename)
    # origin_path = "P:\DinoPowers\Reference\Background"+"\{0}".format(top_name)+"\GPU"+"\{0}".format(filename)
    origin_path_list.append(origin_path)
    # copy_path = "D:\DinoPowers_convert\DinoPowers"+"\{0}".format(top_name)+"\source"+"\{0}".format(filename)
    copy_path = "D:\HeroRiseMan_convert\HeroRiseMan\SET\Prop\GPU"+"\{0}".format(filename)
    copy_pathB = "D:\HeroRiseMan_convert\HeroRiseMan"+"{0}".format(top_name)+"\source"+"\{0}".format(filename)
    
#D:\HeroRiseMan_convert\HeroRiseMan\SET\ALL_house
#D:\HeroRiseMan_convert\HeroRiseMan\SET\Prop\GPU
    # print(origin_path)
    if not os.path.isfile(origin_path):
        if os.path.isfile(copy_path):
            shutil.copy(copy_path,origin_path)
        elif not  os.path.isfile(copy_path):
            shutil.copy(copy_pathB,origin_path)


refine_path = "H:\HeroRiseMan\Reference\Background"+"\{0}".format(top_name)+"\GPU"

for j in selShapes:
    
    filepath = cmds.getAttr(j + '.cacheFileName')
    aa = "".join(filepath)
    refine_path_name = aa.split("/")[-1]
    cmds.setAttr(j+'.cacheFileName',"{0}/{1}".format(refine_path,refine_path_name),type='string' )
        

    


    


