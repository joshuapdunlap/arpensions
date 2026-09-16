import manifest from '../data/public-assets.json';
export interface PublicAsset {
  assetUrl: string; sha256: string; pages: number; reviewedAt: string;
  originalFile: string; originalLocator: string; treatment: string;
  previews: {url:string;width:number;height:number;caption:string}[];
  transcript: string;
  transcriptScope?: string;
  tables?: {caption:string;columns:string[];rows:string[][];note:string}[];
  originalSha256?: string;
  format?: 'pdf'|'email-text';
}
export const assets=manifest as Record<string,PublicAsset>;
