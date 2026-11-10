"""Every authored catalog entry must support a URL-only preview without rewriting its fields."""
import hashlib
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import ci

class CurrentCatalogTests(unittest.TestCase):
    def test_url_only_edit_preserves_every_other_character_for_every_entry(self):
        readme=Path('README.md').read_text()
        for entry in ci.entries(readme):
            with self.subTest(id=entry['id'],name=entry['name']):
                url='https://example.invalid/freshness/'+entry['id']
                data=dict(catalogSha='a'*40,readme=readme,readmeHash=hashlib.sha256(readme.encode()).hexdigest(),entries=[entry])
                row=dict(id=entry['id'],action='update',reason='Synthetic URL-only regression.',evidence=[dict(url=url,observation='Fixture.')],limitations=[],blockers=[],newName=None,newUrl=url,newDescription=None)
                proposals,_=ci.previews(data,dict(results=[row]),'unchanged')
                if not entry.get('editable',True):
                    self.assertEqual(proposals,[])
                    continue
                self.assertEqual(len(proposals),1)
                lines=readme.splitlines(keepends=True)
                index=int(entry['id'])-1
                lines[index]=lines[index].replace(']('+entry['url']+')',']('+url+')',1)
                self.assertEqual(proposals[0]['patch'],ci.patch_text(readme,''.join(lines)))

    def test_new_malformed_fields_still_rejected(self):
        readme='# Tools\n- [Original (name) ](https://example.com) - Original description. \n'
        entry=ci.entries(readme)[0]
        data=dict(catalogSha='a'*40,readme=readme,readmeHash=hashlib.sha256(readme.encode()).hexdigest(),entries=[entry])
        for key,value in [('newName',' Bad'),('newName','Bad\nName'),('newDescription',' Bad'),('newDescription','Bad\nDescription')]:
            with self.subTest(field=key,value=value):
                row=dict(id=entry['id'],action='update',reason='Fixture.',evidence=[dict(url='https://example.com',observation='Fixture.')],limitations=[],blockers=[],newName=None,newUrl='https://changed.example',newDescription=None)
                row[key]=value
                with self.assertRaises(ValueError):ci.previews(data,dict(results=[row]),'unchanged')

    def test_new_parenthesized_name_is_valid_markdown_label(self):
        text='# Tools\n- [AVD](https://example.com) - Description.\n'
        entry=ci.entries(text)[0]
        data=dict(catalogSha='a'*40,readme=text,readmeHash=hashlib.sha256(text.encode()).hexdigest(),entries=[entry])
        row=dict(id=entry['id'],action='update',reason='Official name.',evidence=[dict(url='https://example.com',observation='Official name.')],limitations=[],blockers=[],newName='Arista AVD (Architect, Validate, Deploy)',newUrl=None,newDescription=None)
        proposals,_=ci.previews(data,dict(results=[row]),'unchanged')
        expected=text.replace('[AVD]','[Arista AVD (Architect, Validate, Deploy)]')
        self.assertEqual(proposals[0]['patch'],ci.patch_text(text,expected))
        for invalid in ['Bad[Label]','Bad<Label>','Bad\x00Name','Bad\x7fName']:
            row['newName']=invalid
            with self.subTest(name=invalid),self.assertRaises(ValueError):
                ci.previews(data,dict(results=[row]),'unchanged')
