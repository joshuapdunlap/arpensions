import {test} from 'node:test';
import assert from 'node:assert/strict';
import {assessRelease,candidateDigest} from '../scripts/release-policy.mjs';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
test('approval for one candidate never authorizes a changed candidate',()=>{
  const approved={externalPetitionAligned:true,petitionVerifiedAt:'2026-09-15',petitionVerifiedBy:'reviewer',publicationApproved:true,approvedBy:'reviewer',approvedSourceDigest:'reviewed'};
  assert.equal(assessRelease(approved,'reviewed').length,0);
  assert.match(assessRelease(approved,'changed').join(' '),/does not match/);
  assert.ok(assessRelease({...approved,externalPetitionAligned:false},'reviewed').length>0);
  assert.ok(assessRelease({...approved,publicationApproved:'true'},'reviewed').length>0);
});
test('candidate approval survives Git line-ending normalization but detects changed content',()=>{
  const directory=fs.mkdtempSync(path.join(os.tmpdir(),'arpensions-release-test-'));
  try{
    execFileSync('git',['init','--quiet',directory]);
    fs.writeFileSync(path.join(directory,'.gitattributes'),'* text=auto eol=lf\n*.pdf binary\n');
    fs.writeFileSync(path.join(directory,'LICENSE'),'Reviewed text\r\nSecond line\r\n');
    const windows=candidateDigest(directory);
    fs.writeFileSync(path.join(directory,'LICENSE'),'Reviewed text\nSecond line\n');
    assert.equal(candidateDigest(directory),windows);
    fs.writeFileSync(path.join(directory,'LICENSE'),'Changed text\n');
    assert.notEqual(candidateDigest(directory),windows);
  }finally{
    // Only remove the fresh temporary repository created by this test.
    assert.equal(path.dirname(directory),path.resolve(os.tmpdir()));
    fs.rmSync(directory,{recursive:true});
  }
});
