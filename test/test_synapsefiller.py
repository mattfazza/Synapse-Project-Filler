import pytest
import synapseclient
from pathlib import Path
from src import synapsefiller as sf

relativePath = Path(__file__).parent

syn = synapseclient.Synapse()
syn.login(rememberMe=True)

def test_jsonIngest(capsys):
    with pytest.raises(SystemExit) as emptyPath_e:
        sf.ingestJSON(relativePath)
    assert emptyPath_e.type == SystemExit

    with pytest.raises(SystemExit) as badPath_e:
        sf.ingestJSON(relativePath / './badPath.json')
    assert badPath_e.type == SystemExit
    assert badPath_e.value.args[0] == "Could not find file"

    assert sf.ingestJSON(relativePath / './config.json')['project'] == 'TREAD_AD_POC_0.4'

def test_findFolderInProject():
    assert sf.findFolderInProject('syn23652349', 'MSNx-', syn) == "Couldn't find the location for this path"
    assert sf.findFolderInProject('syn23652349', '', syn) == "Couldn't find the location for this path"
    assert sf.findFolderInProject('syn23652349', 'MSN-', syn) == 'syn23652350'
    
def test_buildName():
    assert sf.buildName('MSN', 'Structural Biology', 'pdf', 'TEP', 'Final') == 'Genes-MSN-Structural_Biology_Core-TEP-MSN_TEP_Final.pdf'