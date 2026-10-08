import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'scripts/install-lp-skills.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.dest = self.root / 'installed'
        self.dest.mkdir()
        self.packages = self.root / 'packages'
        self.packages.mkdir()
        self.lock = {'version': 1, 'skills': []}
        for name in ['alpha', 'beta']:
            folder = self.packages / name
            folder.mkdir()
            (folder / 'SKILL.md').write_text(f'---\nname: {name}\n---\nOriginal')
            self.lock['skills'].append({'name': name, 'sha256': m.digest(folder)})

    def update(self):
        p = self.packages / 'alpha' / 'reference.md'
        p.write_text('New guidance')
        self.lock['skills'][0]['sha256'] = m.digest(p.parent)

    def test_install_reinstall_and_managed_update(self):
        self.assertEqual(m.install(self.lock, self.packages, self.dest), ['alpha', 'beta'])
        self.assertEqual(m.install(self.lock, self.packages, self.dest), [])
        self.update()
        self.assertEqual(m.install(self.lock, self.packages, self.dest), ['alpha'])
        self.assertTrue(m.check(self.lock, self.dest))

    def test_modified_skill_prevents_every_change(self):
        m.install(self.lock, self.packages, self.dest)
        original = (self.dest / m.RECEIPT).read_bytes()
        (self.dest / 'beta/SKILL.md').write_text('Personal changes')
        self.update()
        with self.assertRaisesRegex(ValueError, 'edited'):
            m.install(self.lock, self.packages, self.dest)
        self.assertFalse((self.dest / 'alpha/reference.md').exists())
        self.assertEqual(original, (self.dest / m.RECEIPT).read_bytes())
        self.assertEqual((self.dest / 'beta/SKILL.md').read_text(), 'Personal changes')

    def test_unmanaged_collision_preserved(self):
        (self.dest / 'beta').mkdir()
        (self.dest / 'beta/SKILL.md').write_text('Existing install')
        with self.assertRaisesRegex(ValueError, 'unmanaged'):
            m.install(self.lock, self.packages, self.dest)
        self.assertFalse((self.dest / 'alpha').exists())

    def test_failure_rolls_back_source_and_receipt(self):
        m.install(self.lock, self.packages, self.dest)
        original = (self.dest / m.RECEIPT).read_bytes()
        old_digest = m.digest(self.dest / 'alpha')
        self.update()
        with patch.object(m.shutil, 'copytree', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                m.install(self.lock, self.packages, self.dest)
        self.assertEqual(m.digest(self.dest / 'alpha'), old_digest)
        self.assertEqual((self.dest / m.RECEIPT).read_bytes(), original)

    def test_symlink_refused_without_touching_target(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'keep').write_text('keep')
        (self.dest / 'alpha').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            m.install(self.lock, self.packages, self.dest)
        self.assertEqual((outside / 'keep').read_text(), 'keep')

    def test_floating_refs_and_traversal_refused(self):
        for item in [dict(name='alpha', path='skill', repo='owner/repo', ref='main'), dict(name='alpha', path='../outside')]:
            p = self.root / 'lock.json'
            p.write_text(json.dumps({'version': 1, 'skills': [item]}))
            with self.assertRaises(ValueError):
                m.read_lock(p)

    def test_local_tampering_rejected_during_staging(self):
        source = self.root / 'source'
        (source / 'skill').mkdir(parents=True)
        (source / 'skill/SKILL.md').write_text('---\nname: alpha\n---')
        staging = self.root / 'staging'
        staging.mkdir()
        lock = {'skills': [{'name': 'alpha', 'path': 'skill', 'sha256': 'incorrect'}]}
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            m.stage(lock, staging, root=source)
        self.assertEqual(list(self.dest.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
