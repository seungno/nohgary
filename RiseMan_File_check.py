import os
def File_check(file_name = " ", folder= " "):
    

    BG_folder =  file_name.split("_")[1]
    my_file_path = "D:\HeroRiseMan_convert\HeroRiseMan\{0}\{1}.txt".format(BG_folder,file_name)
    aa= "D:\HeroRiseMan_convert\HeroRiseMan\SET"
    Path  = "{0}\{1}\GPU".format(aa,folder)
    temp_list = []
    Result_List = []
    
    with open(my_file_path) as f:
            lines = f.readlines()
    for i in lines:
        if "StaticMesh=StaticMesh" in i :
            temp_name = i.split("/")[-1].split(".")[0]
            temp_list.append(temp_name)
    File_Name_List =  set(temp_list)
    extension = "abc"
    for Name in File_Name_List:
        Full_Name = "{0}.{1}".format(Name,extension)
        File_Path = "{0}\{1}".format(Path,Full_Name)
        
        if not os.path.isfile(File_Path):
            Result_List.append(Full_Name)

                
    return Result_List
print(File_check("BG_MinoaCityPrime_mountain","Prop")  )  