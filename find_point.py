# Author: Li

def amor(player_map):
    def safe_find():
        def find_mime(x,y):
            return player_map[x,y]=='♥'

        def click(x,y):
            if player_map[x,y]=='□':
                safe_point.append([1,x,y])

        for i in range(1,row+1):
            for j in range(1,column+1):
                try:
                    if int(player_map[i,j])>0:
                        if sum([find_mime(i-1,j-1),find_mime(i-1,j),find_mime(i-1,j+1),find_mime(i,j-1),find_mime(i,j+1),find_mime(i+1,j-1),find_mime(i+1,j),find_mime(i+1,j+1)])==int(player_map[i,j]):
                            click(i-1,j-1)
                            click(i-1,j)
                            click(i-1,j+1)
                            click(i,j-1)
                            click(i,j+1)
                            click(i+1,j-1)
                            click(i+1,j)
                            click(i+1,j+1)
                except:
                    pass

        for i in range(1,row+1):
            for j in range(1,column+1):
                if player_map[i,j]=='2' and player_map[i-1,j]=='1' and player_map[i+1,j]=='1' :
                    if player_map[i,j-1]=='□':
                        safe_point.append([1,i,j-1])
                    if player_map[i,j+1]=='□':
                        safe_point.append([1,i,j+1])
                if player_map[i,j]=='2' and player_map[i,j-1]=='1' and player_map[i,j+1]=='1' :
                    if player_map[i-1,j]=='□':
                        safe_point.append([1,i-1,j])
                    if player_map[i+1,j]=='□':
                        safe_point.append([1,i+1,j])
              
    def mime_find():
        def judge(x,y):
            return ((player_map[x,y]=='□')|(player_map[x,y]=='♥'))
        def judge1(x,y):
            if player_map[x,y]=='□':
                mime_point.append([0,x,y])
        for i in range(1,row+1):
            for j in range(1,column+1):
                try :
                    if int(player_map[i,j])>0:
                        if sum([judge(i-1,j-1),judge(i-1,j),judge(i-1,j+1),judge(i,j-1),judge(i,j+1),judge(i+1,j-1),judge(i+1,j),judge(i+1,j+1)])==int(player_map[i,j]):
                                judge1(i-1,j-1)
                                judge1(i-1,j)
                                judge1(i-1,j+1)
                                judge1(i,j-1)
                                judge1(i,j+1)
                                judge1(i+1,j-1)
                                judge1(i+1,j)
                                judge1(i+1,j+1)
                except:
                    pass

    def unsure_find():
        def count(x,y): 
            a=sum([player_map[x-1,y-1]=='□',player_map[x-1,y]=='□',player_map[x-1,y+1]=='□',player_map[x,y-1]=='□',player_map[x,y+1]=='□',player_map[x+1,y-1]=='□',player_map[x+1,y]=='□',player_map[x+1,y+1]=='□'])
            return a

        def r_pick(x,y):
            gg=1
            for i in range(x-1,x+2):
                if gg==1:
                    for j in range(y-1,y+2):
                        if player_map[i,j]=='□':
                            if suround(i,j)==1:
                                unsure_point.append([2,i,j])
                                gg=0
                                break
                else:
                    break
            return not gg
        
        def suround(x,y):
            xc=[]
            flag=1
            xc.append(player_map[x-1,y-1])
            xc.append(player_map[x-1,y])
            xc.append(player_map[x-1,y+1])
            xc.append(player_map[x,y-1])
            xc.append(player_map[x,y+1])
            xc.append(player_map[x+1,y-1])
            xc.append(player_map[x+1,y])
            xc.append(player_map[x+1,y+1])
            
            for i in range(1,9):
                if str(i) in xc:
                    flag=0
                    break
            
            return flag
        one_ex=0

        if one_ex==0:
            mm=1                        
            for i in range(1,row+1):
                if mm==1:
                    for j in range(1,column+1):
                        if player_map[i,j]=='1':                    
                            s=count(i,j)
                            if s>4 and r_pick(i,j):
                            
                                one_ex=1
                            
                                mm=0
                                break
                else:
                    break
                    
        if one_ex==0:
            ff=1
            for i in range(1,row+1):
                if ff==1:
                    for j in range(1,column+1):
                        if (player_map[i,j] == '□') and suround(i,j):
                            one_ex=1
                            unsure_point.append([2,i,j])
                            ff=0
                            break
                else:
                    break
        if one_ex==0:
            ff=1
            for i in range(1,row+1):
                if ff==1:
                    for j in range(1,column+1):
                        if player_map[i,j] == '□':
                            unsure_point.append([2,i,j])
                            ff=0
                            break
                else:
                    break
    def main():
        safe_find()
        mime_find()
        back_list=safe_point.copy()+mime_point.copy()
        if len(safe_point)==0 and len(mime_point)==0:
            unsure_find()
            back_list=unsure_point.copy()
        return back_list

    def list_cheak(p):
        x=[]
        for i in p:
            if i not in x:
                x.append(i)
        return x

    safe_point=[]
    mime_point=[]
    unsure_point=[]

    size=player_map.shape
    row=int(size[0])-2
    column=int(size[1])-2
    
    return list_cheak(main())