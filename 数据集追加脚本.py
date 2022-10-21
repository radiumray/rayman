import os
dataDir = 'trafficLight'
prefix = 'traffic_light_'


path = os.path.abspath('.')
lst = os.listdir(dataDir)
path = path + '/' + dataDir
print(lst)
for name in lst:
    if name == 'classes.txt':
        continue
    newName = prefix+ name
    path_name = path + '/'+ name
    path_newName = path + '/' + newName
    is_exists = os.path.exists(path_name)
    if is_exists is False:
        print('file path is error')
        break
    os.rename(path_name, path_newName)
    print(path_newName)
