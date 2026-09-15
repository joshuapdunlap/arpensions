import fs from 'node:fs';
import {assessRelease,candidateDigest} from './release-policy.mjs';
const status=JSON.parse(fs.readFileSync(new URL('../release-status.json',import.meta.url),'utf8'));
const digest=candidateDigest();
if(process.argv.includes('--fingerprint')){console.log(digest);process.exit(0)}
const errors=assessRelease(status,digest);
if(errors.length){console.error('Release remains staged.\n'+errors.map(e=>'• '+e).join('\n'));process.exit(1)}
console.log(`Recorded campaign alignment and publication approval match candidate ${digest}.`);
