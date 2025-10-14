import maya.cmds as cmds
import time

# Fonction pour générer un nom unique
def get_unique_name(base_name):
    timestamp = int(time.time())
    return f"{base_name}_{timestamp}"

# Dupliquer et déplacer un mesh + nommage de la copie
def duplicate_and_move(name, x, y, z):
    cmds.select(cmds.duplicate(name))
    cmds.move(x, y, z)

# Tracer une ligne de colonnes avec une distance (offset égal sur chaque axe)
def array_line(name, n, x, y, z, offx, offy, offz):
    for i in range(n):
        duplicate_and_move(name, x + offx * i, y + offy * i, z + offz * i)

# Tracer un rectangle avec nL en nombre de colonnes en largeur et nP idem en longueur (profondeur)
def array_square(name, nL, nP, offsetx, offsetz, posinitx, posinity, posinitz):
    array_line(name, nL, posinitx, posinity, posinitz, offsetx, 0, 0)
    array_line(name, nL, posinitx, posinity, posinitz + offsetz * (nP - 1), offsetx, 0, 0)
    array_line(name, nP - 2, posinitx, posinity, posinitz + offsetz, 0, 0, offsetz)
    array_line(name, nP - 2, posinitx + offsetx * (nL - 1), posinity, posinitz + offsetz, 0, 0, offsetz)

# Fonction principale pour construire le temple
def build_temple(temple_name):


    # Construction de l'ordre
    # Colonnes
    colonne_name = f"{temple_name}_colonne"
    cmds.polyCylinder(n=colonne_name, h=10, sa=30)
    cmds.group(colonne_name, n=f"{temple_name}_colonnes")
    # Rescale colonne entière
    cmds.select(colonne_name)
    cmds.scale(0.5, 0.5, 0.5)
    cmds.move(0, 2.5, 0)
    # Rescale Face d'en haut
    cmds.select(f'{colonne_name}.f[31]')
    cmds.scale(0.7, 0.7, 0.7)
    cmds.select(clear=True)
    # Récupérer diamètre de la base de la colonne
    bbox_colonne_name = f"{temple_name}_bbox_colonne"
    cmds.duplicate(colonne_name, n=bbox_colonne_name, rr=True)
    cmds.select(bbox_colonne_name)
    cmds.geomToBBox(single=True, shaderColor=[0.5, 0.5, 0.5])
    bbox_colonne = cmds.geometryAttrInfo(f'{bbox_colonne_name}.outMesh', bb=True)
    diam_colonne = bbox_colonne[1] - bbox_colonne[0]

    # Abaques
    abaque_name = f"{temple_name}_abaque"
    cmds.polyCube(n=abaque_name)
    cmds.group(abaque_name, n=f"{temple_name}_abaques")
    # Rescale abaque
    cmds.select(abaque_name)
    cmds.scale(1.45, 0.24, 1.45)
    cmds.move(0, 0.24, 0)

    # Echines
    echine_name = f"{temple_name}_echine"
    cmds.polyCylinder(n=echine_name, sx=30, sy=2, h=0.5)
    cmds.group(echine_name, n=f"{temple_name}_echines")
    # Rescale echine
    cmds.select(echine_name)
    cmds.scale(0.55, 0.45, 0.55)
    # Rescale 2 faces echine
    cmds.select(f'{echine_name}.f[61]')
    cmds.scale(1.22, 1, 1.22)
    cmds.select(f'{echine_name}.f[60]')
    cmds.scale(0.7, 1, 0.7)
    # Bevel echine
    cmds.select(f'{echine_name}.f[61]')
    # cmds.polyBevel('echine.e[60:89]', segments=4, offset=0.05 )
    cmds.polyExtrudeFacet(f'{echine_name}.f[61]', off=0.1)

    # Utiliser les noms uniques pour les appels à array_square
    array_square(colonne_name, 6, 13, 2.0, 2.0, -5, 2.5, -12)
    array_square(abaque_name, 6, 13, 2.0, 2.0, -5, 4.58, -12)
    array_square(echine_name, 6, 13, 2.0, 2.0, -5, 4.36, -12)

    # Supprimer les meshs d'origine
    cmds.delete(colonne_name)
    cmds.delete(bbox_colonne_name)
    cmds.delete(abaque_name)
    cmds.delete(echine_name)

    # Récupérer bbox du groupe de colonnes
    bbox_colonnes_name = f"{temple_name}_bbox_colonnes"
    bbox_echines_name = f"{temple_name}_bbox_echines"
    cmds.duplicate(f"{temple_name}_colonnes", n=bbox_colonnes_name, rr=True)
    cmds.duplicate(f"{temple_name}_echines", n=bbox_echines_name, rr=True)
    cmds.select(bbox_colonnes_name, bbox_echines_name)
    cmds.group(bbox_colonnes_name, bbox_echines_name, n=f"{temple_name}_temple_int")
    cmds.geomToBBox(single=True, shaderColor=[0.5, 0.5, 0.5])
    bbox_temple_int = cmds.geometryAttrInfo(f'{temple_name}_temple_int.outMesh', bb=True)

    # Construction des escaliers
    cmds.duplicate(f"{temple_name}_temple_int", n=f"{temple_name}_escaliers1", rr=True)
    # Calculs dimensions bbox colonnes + dimensions bloc int + dimensions escaliers
    print(bbox_temple_int)
    l_temple_int = bbox_temple_int[1] - bbox_temple_int[0]
    p_temple_int = bbox_temple_int[5] - bbox_temple_int[4]
    NL = l_temple_int - (diam_colonne * 2)
    NP = p_temple_int - (diam_colonne * 3.5)
    coefL = NL / l_temple_int
    coefP = NP / p_temple_int
    # Scale le bloc interieur
    cmds.select(f"{temple_name}_temple_int")
    cmds.scale(coefL, 1, coefP)

    # Construction des escaliers
    cmds.select(f"{temple_name}_escaliers1")
    cmds.scale(1, 0.05, 1)
    cmds.duplicate(f"{temple_name}_escaliers1", n=f"{temple_name}_escaliers2", rr=True)
    cmds.duplicate(f"{temple_name}_escaliers2", n=f"{temple_name}_escaliers3", rr=True)
    cmds.select(f"{temple_name}_escaliers1", f"{temple_name}_escaliers2", f"{temple_name}_escaliers3")
    cmds.group(n=f"{temple_name}_escaliers")
    # Reset coordonnées escaliers1
    cmds.makeIdentity(f"{temple_name}_escaliers1", apply=True, t=True, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(f"{temple_name}_escaliers1", apply=False, t=True, r=True, s=True, n=False, pn=True)
    # Recuperer hauteur marche
    bbox_escalier = cmds.geometryAttrInfo(f'{temple_name}_escaliers1.outMesh', bb=True)
    print(bbox_escalier)
    h_escalier = bbox_escalier[3] - bbox_escalier[2]

    # Construction de l'architrave
    architrave_name = f"{temple_name}_architrave"
    cmds.duplicate(f"{temple_name}_abaques", n=architrave_name, rr=True)
    cmds.select(architrave_name)
    cmds.geomToBBox(single=True, shaderColor=[0.5, 0.5, 0.5])
    bbox_architrave = cmds.geometryAttrInfo(f'{architrave_name}.outMesh', bb=True)
    hauteur_bas_architrave = bbox_architrave[3]
    # Placer architrave au dessus des abaques
    cmds.select(architrave_name)
    cmds.move(0, -bbox_architrave[2], 0)
    cmds.makeIdentity(architrave_name, apply=True, t=True, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(architrave_name, apply=False, t=True, r=True, s=True, n=False, pn=True)
    cmds.move(0, hauteur_bas_architrave, 0)
    # Scaler architrave
    cmds.scale(1, 3, 1)
    # Appliquer Scale + Reset
    cmds.makeIdentity(architrave_name, apply=True, t=False, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(architrave_name, apply=False, t=False, r=True, s=True, n=False, pn=True)
    bbox_architrave = cmds.geometryAttrInfo(f'{architrave_name}.outMesh', bb=True)

    # Creation de la Taenia
    taenia_name = f"{temple_name}_taenia"
    cmds.duplicate(architrave_name, n=taenia_name, rr=True)
    cmds.select(taenia_name)
    # Placer Taenia au dessus de l'architrave
    cmds.move(0, hauteur_bas_architrave + bbox_architrave[3], 0)
    cmds.scale(1.005, 0.15, 1.005)
    # Appliquer Scale Taenia
    cmds.makeIdentity(taenia_name, apply=True, t=False, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(taenia_name, apply=False, t=False, r=True, s=True, n=False, pn=True)
    bbox_taenia = cmds.geometryAttrInfo(f'{taenia_name}.outMesh', bb=True)

    # Creation de la Frise
    frise_name = f"{temple_name}_frise"
    cmds.duplicate(architrave_name, n=frise_name, rr=True)
    cmds.select(frise_name)
    # Placer Frise au dessus de l'architrave
    cmds.move(0, hauteur_bas_architrave + bbox_architrave[3] + bbox_taenia[3], 0)
    cmds.scale(1, 1.4, 1)
    # Appliquer Scale Frise
    cmds.makeIdentity(frise_name, apply=True, t=False, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(frise_name, apply=False, t=False, r=True, s=True, n=False, pn=True)
    bbox_frise = cmds.geometryAttrInfo(f'{frise_name}.outMesh', bb=True)

    # Creation de la Corniche Horizontale
    # Corniche Part 1
    corniche_p1_name = f"{temple_name}_corniche_p1"
    cmds.duplicate(taenia_name, n=corniche_p1_name, rr=True)
    cmds.select(corniche_p1_name)
    # Placer Corniche_p1 au dessus de la Frise
    cmds.move(0, hauteur_bas_architrave + bbox_architrave[3] + bbox_taenia[3] + bbox_frise[3], 0)
    cmds.scale(1.03, 0.9, 1)
    # Appliquer Scale Corniche Part 1
    cmds.makeIdentity(corniche_p1_name, apply=True, t=False, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(corniche_p1_name, apply=False, t=False, r=True, s=True, n=False, pn=True)
    bbox_corniche_p1 = cmds.geometryAttrInfo(f'{corniche_p1_name}.outMesh', bb=True)

    # Corniche Part 2
    corniche_p2_name = f"{temple_name}_corniche_p2"
    cmds.duplicate(corniche_p1_name, n=corniche_p2_name, rr=True)
    cmds.select(corniche_p2_name)
    # Placer Corniche au dessus de Corniche Part 1
    cmds.move(0, hauteur_bas_architrave + bbox_architrave[3] + bbox_taenia[3] + bbox_frise[3] + bbox_corniche_p1[3], 0)
    cmds.scale(1.006, 1, 1.006)
    # Appliquer Scale Corniche Part 2
    cmds.makeIdentity(corniche_p2_name, apply=True, t=False, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(corniche_p2_name, apply=False, t=False, r=True, s=True, n=False, pn=True)
    bbox_corniche_p2 = cmds.geometryAttrInfo(f'{corniche_p2_name}.outMesh', bb=True)

    # Contruction du fronton
    fronton_name = f"{temple_name}_fronton"
    cmds.duplicate(corniche_p2_name, n=fronton_name)
    cmds.select(fronton_name)
    cmds.move(0, hauteur_bas_architrave + bbox_architrave[3] + bbox_taenia[3] + bbox_frise[3] + bbox_corniche_p1[3] + bbox_corniche_p2[3], 0)
    cmds.makeIdentity(fronton_name, apply=True, t=False, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(fronton_name, apply=False, t=False, r=True, s=True, n=False, pn=True)
    cmds.scale(1, 20, 1)
    cmds.select(f'{fronton_name}.vtx[6]', f'{fronton_name}.vtx[5]', r=True)
    cmds.polyMergeVertex(am=True)
    cmds.select(f'{fronton_name}.vtx[6]', f'{fronton_name}.vtx[4]', r=True)
    cmds.polyMergeVertex(am=True)

    # Contruction de la corniche rampante
    corniche_rampante_name = f"{temple_name}_corniche_rampante"
    cmds.duplicate(fronton_name, n=corniche_rampante_name, rr=True)
    cmds.select(fronton_name)
    cmds.scale(1, 20, 0.97)
    cmds.select(f'{corniche_rampante_name}.f[0]', f'{corniche_rampante_name}.f[1]', f'{corniche_rampante_name}.f[3]')
    cmds.delete()
    cmds.select(corniche_rampante_name)
    cmds.polyExtrudeFacet(f'{corniche_rampante_name}.f[0:1]', lt=[0, 0, 0.3], ch=1, kft=True, pvx=0, pvy=8.373272657, pvz=0, d=1, twt=0, tp=1, off=0, tk=0, sma=30)

    # Déplacer toute la structure au dessus des escaliers
    cmds.select(all=True)
    cmds.select(f"{temple_name}_escaliers", d=True)
    cmds.group(n=f"{temple_name}_temple")
    cmds.makeIdentity(f"{temple_name}_temple", apply=True, t=True, r=True, s=True, n=False, pn=True)
    cmds.makeIdentity(f"{temple_name}_temple", apply=False, t=True, r=True, s=True, n=False, pn=True)
    cmds.move(0, h_escalier * 3, 0)
    cmds.select(f"{temple_name}_escaliers1")
    cmds.move(0, h_escalier * 2, 0)
    cmds.select(f"{temple_name}_escaliers2")
    cmds.scale(1.05, 1, 1.05, r=True)
    cmds.move(0, h_escalier, 0)
    cmds.select(f"{temple_name}_escaliers3")
    cmds.scale(1.1, 1, 1.1, r=True)

    # Placer tous les éléments dans le groupe principal
    temple_elements = [
        f"{temple_name}_colonnes",
        f"{temple_name}_abaques",
        f"{temple_name}_echines",
        f"{temple_name}_temple_int",
        f"{temple_name}_escaliers",
        architrave_name,
        taenia_name,
        frise_name,
        corniche_p1_name,
        corniche_p2_name,
        fronton_name,
        corniche_rampante_name
    ]
    for element in temple_elements:
        cmds.parent(element, temple_group)

# Générer un nouveau temple avec un nom unique
temple_name = get_unique_name("temple")
build_temple(temple_name)
temple_group = cmds.group(n=temple_name, em=True)