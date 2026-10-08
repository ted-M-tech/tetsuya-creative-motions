import {test} from 'node:test';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
test('LP bundle preserves edits, pins dependencies and rolls back failed updates',()=>{
 execFileSync('python3',[fileURLToPath(new URL('./lp_skill_installer_test.py',import.meta.url))],{stdio:'pipe'});
});
