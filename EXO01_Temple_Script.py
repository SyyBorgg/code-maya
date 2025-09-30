import maya.cmds as cmds

def duplicate_and_move(name,x,y,z):
    cmds.select(cmds.duplicate(name))
    cmds.move(x,y,z)

def array_line(name,n,x,y,z,offx,offy,offz):
    for i in range(n):
        duplicate_and_move(name,x+offx*i,y+offy*i,z+offz*i)
         
def array_square(name,nL,nP,offsetx,offsetz,posinitx,posinity,posinitz):

    array_line(name,nL,posinitx,posinity,posinitz,offsetx,0,0)
    array_line(name,nL,posinitx,posinity,posinitz+offsetz*(nP-1),offsetx,0,0)

    
    array_line(name,nP-2,posinitx,posinity,posinitz+offsetz,0,0,offsetz)
    array_line(name,nP-2,posinitx+offsetx*(nL-1),posinity,posinitz+offsetz,0,0,offsetz)
        
#Construction la colonne
cmds.polyCylinder(n='colonne',h=10)

#Rescale colonne
cmds.select('colonne')
cmds.scale(0.5,0.5,0.5)
cmds.move(0,2.5,0)
#Rescale Face d'en haut
cmds.select('colonne.f[21]')
cmds.scale(0.7,0.7,0.7)
cmds.select( clear=True )

#array_line('colonne',6,-5,2.5,0.0,2.0,0.0,0.0)

array_square('colonne',6,13,2.0,2.0,4,4,4)


