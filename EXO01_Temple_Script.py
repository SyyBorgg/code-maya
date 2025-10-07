import maya.cmds as cmds

#Dupliquer et déplacer un mesh + nommage de la copie
def duplicate_and_move(name,x,y,z):
    cmds.select(cmds.duplicate(name))
    cmds.move(x,y,z)

#tracer une ligne de colonnes avec une distance (offset égal sur chaque axe)
def array_line(name,n,x,y,z,offx,offy,offz):
    for i in range(n):
        (duplicate_and_move(name,x+offx*i,y+offy*i,z+offz*i))

#Tracer un rectangle avec nL en nbre de colonnes en largeur et nP idem en loongueur (profondeur)
def array_square(name,nL,nP,offsetx,offsetz,posinitx,posinity,posinitz):

    array_line(name,nL,posinitx,posinity,posinitz,offsetx,0,0)
    array_line(name,nL,posinitx,posinity,posinitz+offsetz*(nP-1),offsetx,0,0)

    array_line(name,nP-2,posinitx,posinity,posinitz+offsetz,0,0,offsetz)
    array_line(name,nP-2,posinitx+offsetx*(nL-1),posinity,posinitz+offsetz,0,0,offsetz)


#Construction de l'ordre
#Colonnes
cmds.polyCylinder(n='colonne',h=10,sa=30)
cmds.group('colonne',n='colonnes')
#Rescale colonne entière
cmds.select('colonne')
cmds.scale(0.5,0.5,0.5)
cmds.move(0,2.5,0)
#Rescale Face d'en haut
cmds.select('colonne.f[31]')
cmds.scale(0.7,0.7,0.7)
cmds.select( clear=True )
#Cannelures maybe
#ptlist = []
#for i in range(0,60,2):
#    ptlist.append('colonne.vtx['+str(i)+']')
#cmds.select(ptlist,r=True)

#Récupérer diamètre de la base de la colonne
cmds.duplicate('colonne',n='bbox_colonne',rr=True)
cmds.select('bbox_colonne')
cmds.geomToBBox(single=True, shaderColor=[0.5,0.5,0.5])
bbox_colonne=cmds.geometryAttrInfo('bbox_colonne.outMesh', bb=True)
diam_colonne=bbox_colonne[1]-bbox_colonne[0]

#Abaques
cmds.polyCube(n='abaque')
cmds.group('abaque',n='abaques')
#Rescale abaque
cmds.select('abaque')
cmds.scale(1.45,0.24,1.45)
cmds.move(0,0.24,0)

#Echines
cmds.polyCylinder(n='echine',sx=30,sy=2,h=0.5)
cmds.group('echine',n='echines')
#Rescale echine
cmds.select('echine')
cmds.scale(0.55,0.45,0.55)
#Rescale 2 faces echine
cmds.select('echine.f[61]')
cmds.scale(1.22,1,1.22)
cmds.select('echine.f[60]')
cmds.scale(0.7,1,0.7)

#Bevel echine
cmds.select('echine.f[61]')
#cmds.polyBevel('echine.e[60:89]', segments=4, offset=0.05 )
cmds.polyExtrudeFacet('echine.f[61]',off=0.1)

#array_line('colonne',6,-5,2.5,0.0,2.0,0.0,0.0)
array_square('colonne',6,13,2.0,2.0,-5,2.5,-12)
array_square('abaque',6,13,2.0,2.0,-5,4.58,-12)
array_square('echine',6,13,2.0,2.0,-5,4.36,-12)

#Supprimer les meshs d'origine
cmds.delete('colonne')
cmds.delete('bbox_colonne')
cmds.delete('abaque')
cmds.delete('echine')

#Récupérer bbox du groupe de colonnes
cmds.duplicate('colonnes',n='bbox_colonnes',rr=True)
cmds.duplicate('echines',n='bbox_echines',rr=True)
cmds.select('bbox_colonnes','bbox_echines')
cmds.group('bbox_colonnes','bbox_echines',n='temple_int')
cmds.geomToBBox(single=True, shaderColor=[0.5,0.5,0.5])
bbox_temple_int=cmds.geometryAttrInfo('temple_int.outMesh', bb=True)

#Construction des escaliers
cmds.duplicate('temple_int',n='escaliers1',rr=True)

#Calculs dimensions bbox colonnes + dimensions bloc int + dimensions escaliers
print (bbox_temple_int)
l_temple_int=bbox_temple_int[1]-bbox_temple_int[0]
p_temple_int=bbox_temple_int[5]-bbox_temple_int[4]

NL=l_temple_int-(diam_colonne*2)
NP=p_temple_int-(diam_colonne*3.5)

coefL=NL/l_temple_int
coefP=NP/p_temple_int

#Scale le bloc interieur
cmds.select('temple_int')
cmds.scale(coefL,1,coefP)

#Construction des escaliers 
cmds.select('escaliers1')
cmds.scale(1,0.05,1)

cmds.duplicate( 'escaliers1', n='escaliers2', rr=True )
cmds.duplicate( 'escaliers2', n='escaliers3', rr=True )
cmds.select('escaliers1','escaliers2','escaliers3')
cmds.group(n='escaliers')

#Reset coordonnées escaliers1
cmds.makeIdentity('escaliers1',apply=True, t=True,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('escaliers1',apply=False, t=True,r=True,s=True,n=False,pn=True)

#Recuperer hauteur marche
bbox_escalier=cmds.geometryAttrInfo('escaliers1.outMesh', bb=True)
print(bbox_escalier)
h_escalier=bbox_escalier[3]-bbox_escalier[2]

#Construction de l'architrave
cmds.duplicate( 'abaques', n='architrave', rr=True )
cmds.select('architrave')
cmds.geomToBBox(single=True, shaderColor=[0.5,0.5,0.5])
bbox_architrave=cmds.geometryAttrInfo('architrave.outMesh', bb=True)
hauteur_bas_architrave=bbox_architrave[3]

#Placer architrave au dessus des abaques
cmds.select('architrave')
cmds.move(0,-bbox_architrave[2],0)
cmds.makeIdentity('architrave',apply=True, t=True,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('architrave',apply=False, t=True,r=True,s=True,n=False,pn=True)
cmds.move(0,hauteur_bas_architrave,0)
#Scaler architrave
cmds.scale(1,3,1)

#Appliquer Scale + Reset 
cmds.makeIdentity('architrave',apply=True, t=False,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('architrave',apply=False, t=False,r=True,s=True,n=False,pn=True)
bbox_architrave=cmds.geometryAttrInfo('architrave.outMesh', bb=True)

#Creation de la Taenia
cmds.duplicate( 'architrave', n='taenia', rr=True )
cmds.select('taenia')

#Placer Taenia au dessus de l'architrave
cmds.move(0,hauteur_bas_architrave+bbox_architrave[3],0)
cmds.scale(1.005,0.15,1.005)

#Appliquer Scale Taenia
cmds.makeIdentity('taenia',apply=True, t=False,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('taenia',apply=False, t=False,r=True,s=True,n=False,pn=True)
bbox_taenia=cmds.geometryAttrInfo('taenia.outMesh', bb=True)

#Creation de la Frise
cmds.duplicate( 'architrave', n='frise', rr=True )
cmds.select('frise')

#Placer Frise au dessus de l'architrave
cmds.move(0,hauteur_bas_architrave+bbox_architrave[3]+bbox_taenia[3],0)
cmds.scale(1,1.4,1)

#Appliquer Scale Frise
cmds.makeIdentity('frise',apply=True, t=False,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('frise',apply=False, t=False,r=True,s=True,n=False,pn=True)
bbox_frise=cmds.geometryAttrInfo('frise.outMesh', bb=True)

#Creation de la Corniche Horizontale
#Corniche Part 1
cmds.duplicate( 'taenia', n='corniche_p1', rr=True )
cmds.select('corniche_p1')

#Placer Corniche_p1 au dessus de la Frise
cmds.move(0,hauteur_bas_architrave+bbox_architrave[3]+bbox_taenia[3]+bbox_frise[3],0)
cmds.scale(1.03,0.9,1)

#Appliquer Scale Corniche Part 1
cmds.makeIdentity('corniche_p1',apply=True, t=False,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('corniche_p1',apply=False, t=False,r=True,s=True,n=False,pn=True)
bbox_corniche_p1=cmds.geometryAttrInfo('corniche_p1.outMesh', bb=True)

#Corniche Part 2
cmds.duplicate( 'corniche_p1', n='corniche_p2', rr=True )
cmds.select('corniche_p2')

#Placer Corniche  au dessus de Corniche Part 1
cmds.move(0,hauteur_bas_architrave+bbox_architrave[3]+bbox_taenia[3]+bbox_frise[3]+bbox_corniche_p1[3],0)
cmds.scale(1.006,1,1.006)

#Appliquer Scale Corniche Part 2
cmds.makeIdentity('corniche_p2',apply=True, t=False,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('corniche_p2',apply=False, t=False,r=True,s=True,n=False,pn=True)
bbox_corniche_p2=cmds.geometryAttrInfo('corniche_p2.outMesh', bb=True)

#Contruction du fronton
cmds.duplicate('corniche_p2', n='fronton')
cmds.select('fronton')
cmds.move(0,hauteur_bas_architrave+bbox_architrave[3]+bbox_taenia[3]+bbox_frise[3]+bbox_corniche_p1[3]+bbox_corniche_p2[3],0)

cmds.makeIdentity('fronton',apply=True, t=False,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('fronton',apply=False, t=False,r=True,s=True,n=False,pn=True)

cmds.scale(1,20,1)

cmds.select('fronton.vtx[6]','fronton.vtx[5]',r=True)
cmds.polyMergeVertex(am=True)
cmds.select('fronton.vtx[6]','fronton.vtx[4]',r=True)
cmds.polyMergeVertex(am=True)

#Contruction de la corniche rampante
cmds.duplicate( 'fronton', n='corniche_rampante', rr=True )
cmds.select('fronton')
cmds.scale(1,20,0.97)

cmds.select('corniche_rampante.f[0]','corniche_rampante.f[1]','corniche_rampante.f[3]')
cmds.delete()
cmds.select('corniche_rampante')
cmds.polyExtrudeFacet('corniche_rampante.f[0:1]',lt=[0,0,0.3],ch=1,kft=True,pvx=0,pvy=8.373272657,pvz=0,d=1,twt=0,tp=1,off=0,tk=0,sma=30,)


#Deplacer toute la structure au dessus des escaliers
cmds.select(all=True)
cmds.select('escaliers',d=True)
cmds.group(n='temple')
cmds.makeIdentity('temple',apply=True, t=True,r=True,s=True,n=False,pn=True)
cmds.makeIdentity('temple',apply=False, t=True,r=True,s=True,n=False,pn=True)
cmds.move(0,h_escalier*3,0)

cmds.select('escaliers1')
cmds.move(0,h_escalier*2,0)

cmds.select('escaliers2')
cmds.scale(1.05,1,1.05, r=True)
cmds.move(0,h_escalier,0)

cmds.select('escaliers3')
cmds.scale(1.1,1,1.1, r=True)

#A faire pour samedi: escaliers: calculer périmètre rectangle colonnes, rajouter +0.5+1+1.5
#Corniche rampante = deux paralleli qui se croisent dans un angle de 15°. + Mirror
#Arcotères extrémité + sommet du fronton + bases (cubes)