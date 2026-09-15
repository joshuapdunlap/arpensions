export interface FinancialRecord {
  id: string; agency: string; accountScope: string; amount: number; currency: 'USD';
  basis: 'par'|'funding'|'market-value-with-accrued'|'authorization';
  stage: 'holding'|'funding'|'purchase'|'processing'|'canceled'|'authorization'|'derived-residual';
  effectiveDate: string; sourceIds: string[]; parentFundingId?: string; securityId?: string; overlapsRecordIds?: string[];
}
export type MeasureKind = 'direct-evidence'|'mixed-funding'|'same-day-holdings';

/** An explicit selection is essential: a ledger includes events and later observations of those events. */
export function assembleMeasure(records: FinancialRecord[], ids: string[], kind: MeasureKind) {
  if (!ids.length || new Set(ids).size !== ids.length) throw new Error('Select distinct record IDs');
  if (new Set(records.map(r=>r.id)).size !== records.length) throw new Error('Duplicate ledger record ID');
  const selected = ids.map(id=>{const r=records.find(r=>r.id===id);if(!r)throw new Error(`Unknown record ${id}`);return r});
  const eligible = kind==='mixed-funding'?['holding','purchase','derived-residual','funding']:kind==='same-day-holdings'?['holding']:['holding','purchase','derived-residual'];
  const securities = new Set<string>();
  for(const row of selected){
    if(!eligible.includes(row.stage)) throw new Error(`${row.stage} is not eligible for ${kind}`);
    if(row.currency!=='USD'||!Number.isFinite(row.amount)||row.amount<0) throw new Error('Invalid USD amount');
    if(!row.sourceIds.length||!/^\d{4}-\d{2}-\d{2}$/.test(row.effectiveDate)) throw new Error('A dated source is required');
    if(row.parentFundingId&&ids.includes(row.parentFundingId)) throw new Error('Double counting manager funding and its asset');
    if(row.overlapsRecordIds?.some(id=>ids.includes(id))) throw new Error('Double counting overlapping portfolio observations');
    if(row.securityId&&securities.has(row.securityId)) throw new Error('Double counting observations of one security');
    if(row.securityId)securities.add(row.securityId);
    if(kind==='direct-evidence'&&row.basis!=='par')throw new Error('Direct evidence uses par, not market value or manager funding');
  }
  const dates=[...new Set(selected.map(r=>r.effectiveDate))].sort();
  if(kind==='same-day-holdings'&&dates.length!==1)throw new Error('Holdings must have the same observation date');
  const amount=selected.reduce((sum,r)=>sum+Math.round(r.amount*100),0)/100;
  const label=kind==='mixed-funding'?'Mixed measure: securities and full manager funding':kind==='same-day-holdings'?`Observed holdings on ${dates[0]}`:`Direct-security evidence floor${dates.length>1?' from different record dates':''}`;
  return {amount,label,mixedDates:dates.length>1,dates,sourceIds:[...new Set(selected.flatMap(r=>r.sourceIds))],records:selected};
}
