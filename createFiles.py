# Fill in Synapse Project

import synapseclient
from synapseclient import Project, Folder, File
import sys

# genes = ["MSN", "CD44", "CAPN2", "EPHX2", "MDK", "SYK", "FCER1G", "SFRP1", "PRDX6", "PRDX1", "RABEP1", "SDC4", "GPNMB", "C4A", "NDUFS2", "CNN3", "SMOC1", "CTSH", "PLEC", "SNX32", "STX4"]
genes = ["MSN", "CD44"]
core = "Structural Biology"
fileFormat = "pdf"
category = "TEP"
last_name = "Final"

syn = synapseclient.Synapse()
syn.login(rememberMe=True)

id = syn.findEntityId('TREAD_AD_POC_0.4', parent=None)

# finds the folder described in the filename, and returns the syn_id of that 
def findFolderInProject(parentID, remainingPath):

    currentFolderName = remainingPath.split('-')[0]
    currentID = syn.findEntityId(currentFolderName, parent=parentID)

    if currentID is None:
        return "Couldn't find the location for this path"
    
    if len(remainingPath.split('-')) == 2:
        return currentID
    else:
        return findFolderInProject(currentID, '-'.join(remainingPath.split('-')[1:]))


def createFileInSynapse(pathToFile, nameInSynapse, parentID, gene):
    syn.store(File(path=pathToFile, name=nameInSynapse, parent=parentID, gene=gene, core=core, fileFormat=fileFormat, category=category))


def buildName(nameOfGene, nameOfCore, nameOfFormat, nameOfCategory, nameOfFile):
    return f'Genes-{nameOfGene}-{nameOfCore.replace(" ", "_")}_Core-{nameOfCategory}-{nameOfGene}_{nameOfCategory}_{nameOfFile}.{nameOfFormat}'


for gene in genes:
    name = buildName(gene, core, fileFormat, category, last_name)
    last_parent_id = findFolderInProject(id, name)
    
    if last_parent_id != None:
        f = open(name.split('-')[-1], "x")
        f.write("kljhdsfkljdshfkljdsfs")
        f.close()
    else:
        sys.exit("Couldn't find directory")
    

    ann = {"Gene": gene, "Core": core, "Format": fileFormat, "Category": category}

    createFileInSynapse('./'+name.split('-')[-1], name.split('-')[-1], last_parent_id, gene)
    print("Created file in synapse")
