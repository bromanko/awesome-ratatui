"""Exercise the real validators with an intentionally invalid synthetic catalog."""
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import ci
import checks

with tempfile.TemporaryDirectory() as temp:
    repo = Path(temp)
    text = '# Test catalog\n\n- [Example](https://example.com) - A tool.\n'
    (repo/'README.md').write_text(text)
    (repo/'typos.toml').write_text('')
    (repo/'.lycheeignore').write_text('^https://example\\.com\n')
    subprocess.run(['git','init','-q',str(repo)],check=True)
    subprocess.run(['git','-C',str(repo),'add','.'],check=True)
    subprocess.run(['git','-C',str(repo),'-c','user.name=Test','-c','user.email=test@example.com',
                    '-c','commit.gpgsign=false','commit','-qm','Synthetic validation fixture'],check=True)
    sha=ci.git(repo,'rev-parse','HEAD').strip()
    data=dict(catalogSha=sha,readme=text,readmeHash=hashlib.sha256(text.encode()).hexdigest(),entries=ci.entries(text))
    raw=dict(results=[dict(id='3',action='update',reason='Synthetic spelling failure.',evidence=[dict(url='https://example.com',observation='Fixture')],limitations=[], blockers=[], newName="Renamed",newUrl=None,newDescription='A teh tool.')])
    proposal=ci.previews(data,raw,'unchanged')[0][0]
    validator=checks.Validator(repo,sha,text,repo/'output')
    try:
        result=validator.validate(proposal,data['entries'][0])
        assert result['passed'] is False,result
        assert result['patched']['spelling'] != 0,result
        assert result['patched']['lint'] != -1,result
        assert result['patched']['links'] in (0,2),result
        assert result['links']['unverified'] == ['https://example.com/'],result
        # A real successful link must supply per-link evidence, not just a total.
        (repo/'target.md').write_text('Existing target.\n')
        (repo/'link-fixture.md').write_text('[Target](target.md)\n')
        linked = checks.run(['lychee','--verbose','--no-progress','--format','json','link-fixture.md'],repo,validator.env)
        parsed = checks.links(linked,repo)
        assert checks.compare_links(dict(errors=[]),parsed,['file://CATALOG/target.md'])['passed'],parsed
        print('Real validators completed; bad spelling/formatting and excluded destination held the synthetic proposal.')
    finally:
        validator.close()
