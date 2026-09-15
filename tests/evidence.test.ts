import {test} from 'node:test';
import assert from 'node:assert/strict';
import data from '../src/data/investigation.json';
import {assembleMeasure, type FinancialRecord} from '../src/lib/financial.ts';
const records=data.financialRecords as FinancialRecord[];
const get=(id:string)=>records.find(r=>r.id===id)!;
test('portfolio observations cannot double count their earlier purchase or statement',()=>{
  assert.throws(()=>assembleMeasure(records,['apers_october_purchase','apers_september_holding'],'direct-evidence'),/overlapping/i);
  assert.throws(()=>assembleMeasure(records,['treasury_june_holding','treasury_derived_residual'],'direct-evidence'),/overlapping/i);
});
test('September reconciled totals use distinct eligible records',()=>{
  const direct=assembleMeasure(records,['treasury_derived_residual','apers_september_holding','atrs_february_purchase'],'direct-evidence');
  assert.equal(direct.amount,84_900_000);assert.equal(direct.mixedDates,true);
  assert.equal(assembleMeasure(records,['treasury_derived_residual','apers_september_holding','atrs_january_funding'],'mixed-funding').amount,125_000_000);
});
test('historical APERS purchase and later holding remain distinguishable',()=>{
  assert.equal(get('apers_october_purchase').amount,15_000_000);
  assert.equal(get('apers_september_holding').amount,25_000_000);
  assert.equal(get('apers_september_holding').effectiveDate,'2026-09-07');
});
test('ATRS settlement, cancellation and parent funding are explicit',()=>{
  assert.equal(get('atrs_january_funding').effectiveDate,'2026-01-02');
  assert.equal(get('atrs_february_purchase').effectiveDate,'2026-02-17');
  assert.equal(get('atrs_february_purchase').amount,9_900_000);
  assert.equal(get('atrs_february_purchase').parentFundingId,'atrs_january_funding');
  assert.equal(get('atrs_canceled_issuance').stage,'canceled');
  assert.equal(get('treasury_processing').stage,'processing');
});
test('July composition is market value plus accrued income, not par or funding',()=>{
  const total=data.accountComposition.reduce((sum,row)=>sum+Math.round(row.amount*100),0)/100;
  assert.equal(total,50_446_757.95);
  assert.ok(Math.abs(data.accountComposition.reduce((sum,row)=>sum+row.share,0)-100)<0.0001);
  assert.equal(new Set(data.accountComposition.map(r=>r.asOf)).size,1);
});
test('every financial and timeline source resolves',()=>{
  for(const row of [...data.financialRecords,...data.timeline])for(const id of row.sourceIds)assert.ok(id in data.sources,`${row.id}: ${id}`);
});
