import investigation from '../data/investigation.json';
import {assembleMeasure,type FinancialRecord} from './financial';
export interface Source {
  title: string; agency: string; date: string; locator: string; originalFile: string;
  recordUrl: string; assetUrl?: string; summary: string; treatment: string;
  documentType: string; subject: string;
  [key: string]: unknown;
}
export const data = investigation;
export const financialRecords = investigation.financialRecords as FinancialRecord[];
export const financialRecord = (id:string) => {const record=financialRecords.find(r=>r.id===id);if(!record)throw new Error(`Missing financial record ${id}`);return record};
export const directMeasure=assembleMeasure(financialRecords,['treasury_derived_residual','apers_september_holding','atrs_february_purchase'],'direct-evidence');
export const mixedMeasure=assembleMeasure(financialRecords,['treasury_derived_residual','apers_september_holding','atrs_january_funding'],'mixed-funding');
export const sources = investigation.sources as Record<string, Source>;
export const money = (amount: number, digits = 0) => new Intl.NumberFormat('en-US', {style:'currency',currency:'USD',maximumFractionDigits:digits}).format(amount);
export const dateLabel = (date: string) => new Date(date.length === 10 ? date+'T12:00:00Z' : date).toLocaleDateString('en-US', {month:'long',day:'numeric',year:'numeric',timeZone:'UTC'});
export const sourceLink = (id: string) => sources[id]?.recordUrl || '/documents/';
