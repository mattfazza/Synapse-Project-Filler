# Fill in Synapse Project

import synapseclient
from synapseclient import File
from pathlib import Path
import json
import sys


# ingest json file into variable
def ingestJSON(filePath):
    try:
        with open(filePath) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        sys.exit("Could not find file")
    except json.decoder.JSONDecodeError:
        sys.exit("Please provide a valid JSON file")
    except Exception:
        sys.exit("An error has occurred.")


# finds the folder described in the filename, and returns the syn_id of that
def findFolderInProject(parentID, remainingPath, syn):

    currentFolderName = remainingPath.split('-')[0]
    currentID = syn.findEntityId(currentFolderName, parent=parentID)

    if currentID is None:
        return "Couldn't find the location for this path"

    if len(remainingPath.split('-')) == 2:
        return currentID
    else:
        return findFolderInProject(currentID, '-'.join(remainingPath.split('-')[1:]), syn)


def createFileInSynapse(pathToFile, nameInSynapse, parentID, gene, fileCreationObj, syn):
    syn.store(File(path=pathToFile, name=nameInSynapse, parent=parentID, gene=gene, core=fileCreationObj['core'], fileFormat=fileCreationObj['fileFormat'], category=fileCreationObj['category']))


def buildName(nameOfGene, nameOfCore, nameOfFormat, nameOfCategory, nameOfFile):
    return f'Genes-{nameOfGene}-{nameOfCore.replace(" ", "_")}_Core-{nameOfCategory}-{nameOfGene}_{nameOfCategory}_{nameOfFile}.{nameOfFormat}'


def populate(fileCreationObj, syn):

    # find project synId first
    projectId = syn.findEntityId(fileCreationObj['project'], parent=None)

    for gene in fileCreationObj['genes']:
        name = buildName(gene, fileCreationObj['core'], fileCreationObj['fileFormat'], fileCreationObj['category'], fileCreationObj['last_name'])
        last_parent_id = findFolderInProject(projectId, name, syn)

        if last_parent_id is not None:
            f = open(name.split('-')[-1], "x")
            f.write("kljhdsfkljdshfkljdsfs")
            f.close()
        else:
            sys.exit("Couldn't find directory")

        createFileInSynapse('./'+name.split('-')[-1], name.split('-')[-1], last_parent_id, gene, fileCreationObj, syn)
        print(f"Created file {name.split('-')[-1]} in synapse")


def preparePopulation(path, synObj=None):

    populateConfig = ingestJSON(path)

    if synObj is None:
        syn = synapseclient.Synapse()
        syn.login(rememberMe=True)
    else:
        syn = synObj

    populate(populateConfig, syn)


def main():
    relativePath = Path(__file__).parent / sys.argv[1]
    preparePopulation(relativePath)


if __name__ == "__main__":
    main()
