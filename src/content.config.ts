import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob, file } from 'astro/loaders';
import investigation from './data/investigation.json';

const date = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);
const sourceSchema = z.looseObject({
  title: z.string(), agency: z.string(), date: z.string(), locator: z.string(), originalFile: z.string(),
  documentType: z.string().min(1), subject: z.string().min(1),
  recordUrl: z.string().regex(/^(\/|https:\/\/)/), assetUrl: z.string().optional(), summary: z.string(), treatment: z.string(),
});
const pageSchema = z.object({
  title: z.string(), description: z.string(), permalink: z.string().startsWith('/'),
  section: z.string().optional(), eyebrow: z.string().optional(),
  template: z.enum(['article','policy','evidence','agency','action','updates','people']),
  agency: z.string().optional(), sourceIds: z.array(z.string().refine(id=>id in investigation.sources,'Unknown source reference')).default([]), reviewedAt: date, updatedAt: date,
});
const pages = defineCollection({loader: glob({pattern:'**/*.md',base:'./src/content/pages'}),schema:pageSchema});
const findings = defineCollection({loader: glob({pattern:'findings/*.md',base:'./src/content/pages'}),schema:pageSchema});
const updates = defineCollection({loader: glob({pattern:'news/*.md',base:'./src/content/pages'}),schema:pageSchema});
const sources = defineCollection({loader:file('src/data/investigation.json', {parser: (text) => Object.entries(JSON.parse(text).sources).map(([id,value]) => ({id,...value as object}))}),schema:sourceSchema});
const claims = defineCollection({loader:file('src/data/publication-matrix.json'), schema:z.object({
  claim:z.string(), sourceIds:z.array(z.string()), locator:z.string(), scope:z.string(), asOf:z.string(),
  interpretation:z.string(), boundary:z.string(), pages:z.array(z.string()),
})});
const financialRecords = defineCollection({loader:file('src/data/investigation.json',{parser:text=>JSON.parse(text).financialRecords}),schema:z.object({
  agency:z.string(),accountScope:z.string(),amount:z.number().nonnegative(),currency:z.literal('USD'),
  basis:z.enum(['par','funding','market-value-with-accrued','authorization']),
  stage:z.enum(['holding','funding','purchase','processing','canceled','authorization','derived-residual']),
  effectiveDate:date,sourceIds:z.array(z.string()).min(1),parentFundingId:z.string().optional(),securityId:z.string().optional(),overlapsRecordIds:z.array(z.string()).optional(),
})});
const policyVersions = defineCollection({loader:file('src/data/investigation.json',{parser:text=>[{id:'2026-09-15',...JSON.parse(text).policy}]}),schema:z.object({title:z.string(),status:z.string(),session:z.string(),reviewedAt:date,briefUrl:z.string(),summary:z.string()})});
export const collections = {pages,findings,updates,sources,claims,financialRecords,policyVersions};
