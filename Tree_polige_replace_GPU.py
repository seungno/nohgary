import maya.mel as mel
import re
import maya.cmds as cmds
import os
def Fun_folige_cleanUP_A():
    get_name = cmds.ls(sl=1, type ="transform")
    if get_name:
        for k, grp in enumerate(get_name):
            if "_C_0" not in grp:
                grp_rename = cmds.rename(grp, grp+"_C_0")
                get_name[k] = grp_rename
                objlist =  cmds.listRelatives(grp_rename, c=1, f=1)
                for i, name in enumerate(objlist):
                    cmds.rename(name, "{0}_{1:04d}".format(grp,i))
            
    if not get_name:
        rootName =cmds.ls(assemblies=1, v=1)
        get_names =  cmds.listRelatives(rootName, c=1)
        for grp in get_names:
            objlist =  cmds.listRelatives(grp, c=1, f=1)
            if objlist:
                get_name.append(grp)
                for i, name in enumerate(objlist):
                    cmds.rename(name, "{0}_{1:04d}".format(grp,i))
    ro = cmds.ls(assemblies=1, v=1)
    cmds.setAttr(ro[0]+".rotate", -0,0,0,type="double3")
    return get_name		
            
                    
                    

def import_gpu(file_Directory="",gpu_name=""):    
    if  "_C_0" in gpu_name:
        strip_name = gpu_name.rstrip("_C_0")
        file_name = "{0}.abc".format(strip_name)
        full_path = os.path.join(file_Directory, file_name)
    
        if os.path.exists(full_path):
            print('File {0} Exists : True'.format(full_path))
            createNode = cmds.createNode("gpuCache", name=strip_name+'_GPU') 
            cacheParent = cmds.listRelatives(createNode, p=1, pa=1)    
            cacheParent = cmds.rename(cacheParent, createNode+"_transform")
            cmds.setAttr("|"+createNode+"_transform"+"|"+createNode+'.cacheFileName',full_path,type='string' )
            return createNode
        if not os.path.exists(full_path):
            print("not exists File : {0}".format(full_path))
    else:
        print("not match name")
    return None     
    
                 
for j in Fun_folige_cleanUP_A():
    get_gpu_name = import_gpu("D:/HeroRiseMan_convert/HeroRiseMan/SET/set_tree/GPU",j)
    if get_gpu_name:
        sel_name = "{}_transform".format(get_gpu_name)
        cmds.select(j,hi=1)     
        cmds.select(j,d=1) 
        cmds.select(sel_name,add=1)      
        mel.eval("replaceObjects 1 1 2 0")
        cmds.setAttr(j+".rotate", -90,0,0,type="double3")        
    else :
        continue


        
        

        
        
 
    
        


    




    

    
        
		
    
        




    
        

 
 





    


     






    
    
        
        
			
	
			

			


			 
		
	



		
		






