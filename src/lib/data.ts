import investigation from '../data/investigation.json';
import {assembleMeasure,type FinancialRecord} from './financial';
export interface Source {
  title: string; agency: string; date: string|null; dateType: string; dateNote: string; receivedDate?: string; locator: string; originalFile: string;
  recordUrl: string; assetUrl?: string; summary: string; treatment: string;
  documentType: string; subject: string;
  [key: string]: unknown;
}
export const data = investigation;
export const financialRecords = investigation.financialRecords as FinancialRecord[];
export const financialRecord = (id:string) => {const record=financialRecords.find(r=>r.id===id);if(!record)throw new Error(`Missing financial record ${id}`);return record};
export const directMeasure=assembleMeasure(financialRecords,['treasury_derived_residual','apers_september_holding','atrs_february_purchase'],'historical-comparison');
export const mixedMeasure=assembleMeasure(financialRecords,['treasury_derived_residual','apers_september_holding','atrs_january_funding'],'mixed-funding');
export const sources = investigation.sources as Record<string, Source>;
export const money = (amount: number, digits = 0) => new Intl.NumberFormat('en-US', {style:'currency',currency:'USD',maximumFractionDigits:digits}).format(amount);
export const dateLabel = (date: string|null) => date?new Date(date.length === 10 ? date+'T12:00:00Z' : date).toLocaleDateString('en-US', {month:'long',day:'numeric',year:'numeric',timeZone:'UTC'}):'Date not established';
export const sourceDateLabels:Record<string,string>={document:'Document date',message:'Message date',decision:'Decision date',meeting:'Meeting date','packet':'Board packet date',transaction:'Transaction date','account-as-of':'Account as of','period-end':'Reporting period end','scheduled-maturity':'Scheduled post date',signature:'Signature date',verified:'Reference checked',unknown:'Document date'};
export const sourceDateLabel=(source:Source)=>`${sourceDateLabels[source.dateType]||'Source date'}: ${source.date||'not shown'}`;
export const sourceLink = (id: string) => sources[id]?.recordUrl || '/documents/';
