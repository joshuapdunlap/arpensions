import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
export function assessRelease(status,digest){
  const errors=[];
  if(status.externalPetitionAligned!==true||!status.petitionVerifiedAt||!status.petitionVerifiedBy)errors.push('External petition description, letter, subscription settings and confirmation require Joshua’s verified alignment. See docs/petition-revision.md.');
  if(status.publicationApproved!==true||!status.approvedBy)errors.push('Joshua’s approval of this concrete website release is required.');
  if(status.approvedSourceDigest!==digest)errors.push('The reviewed source digest does not match this candidate. Approval cannot carry over to changed content or code.');
  return errors;
}
export function candidateDigest(root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..')){
  const names=execFileSync('git',['ls-files','--cached','--others','--exclude-standard','-z'],{cwd:root,encoding:'utf8'}).split('\0').filter(Boolean);
  const digest=createHash('sha256');
  for(const name of [...new Set(names)].sort()){
    if(name==='release-status.json')continue;
    const file=path.join(root,name);if(!fs.existsSync(file))continue;
    const stat=fs.lstatSync(file);if(stat.isDirectory())continue;
    // Git applies this repository's text/binary attributes before hashing. The
    // same candidate therefore has one fingerprint on Windows and Linux,
    // including extensionless text such as LICENSE. This does not write objects.
    const content=stat.isSymbolicLink()?fs.readlinkSync(file):execFileSync('git',['hash-object','--path',name,'--',name],{cwd:root,encoding:'utf8'}).trim();
    digest.update(name.replaceAll('\\','/')+'\0');digest.update(content);digest.update('\0');
  }
  return digest.digest('hex');
}
