import { test } from 'node:test';
import assert from 'node:assert/strict';
import { assembleMeasure, type FinancialRecord } from '../src/lib/financial.ts';

const record = (id: string, changes: Partial<FinancialRecord> = {}): FinancialRecord => ({
  id, agency: 'atrs', accountScope: 'Reams account', amount: 9_900_000,
  currency: 'USD', basis: 'par', stage: 'purchase', effectiveDate: '2026-02-17',
  sourceIds: ['source'], ...changes,
});
test('direct evidence can include a completed pension-manager acquisition', () => {
  assert.equal(assembleMeasure([record('bond')], ['bond'], 'direct-evidence').amount, 9_900_000);
});

test('conditional residuals require an explicit assumption and cannot become direct holdings', () => {
  const residual=record('residual',{stage:'derived-residual',amount:50_000_000});
  assert.throws(()=>assembleMeasure([residual],['residual'],'historical-comparison'),/assumption/i);
  residual.assumption='Scheduled maturity completed with no other transactions.';
  assert.equal(assembleMeasure([residual],['residual'],'historical-comparison').amount,50_000_000);
  assert.throws(()=>assembleMeasure([residual],['residual'],'direct-evidence'),/not eligible/i);
  residual.effectiveDate=null;
  assert.throws(()=>assembleMeasure([residual],['residual'],'historical-comparison'),/dated source/i);
});
test('processing and canceled instructions cannot enter confirmed direct evidence', () => {
  for (const stage of ['processing', 'canceled', 'authorization', 'funding'] as const)
    assert.throws(() => assembleMeasure([record('pending', {stage})], ['pending'], 'direct-evidence'));
});
test('a manager account and its underlying bond cannot be counted together', () => {
  const rows = [record('funding', {stage: 'funding', basis: 'funding', amount: 50_000_000}), record('bond', {parentFundingId: 'funding'})];
  assert.throws(() => assembleMeasure(rows, ['funding', 'bond'], 'mixed-funding'), /double.count/i);
});
test('mixed record dates and transaction events cannot become same-day holdings', () => {
  const rows = [record('a', {stage: 'holding'}), record('b', {stage: 'holding', effectiveDate: '2026-09-07'})];
  const measure = assembleMeasure(rows, ['a', 'b'], 'direct-evidence');
  assert.equal(measure.mixedDates, true);
  assert.match(measure.label, /different record dates/);
  assert.throws(() => assembleMeasure(rows, ['a', 'b'], 'same-day-holdings'));
  assert.throws(() => assembleMeasure([record('trade')], ['trade'], 'same-day-holdings'));
});
test('duplicate IDs and multiple observations of one security are rejected', () => {
  assert.throws(() => assembleMeasure([record('a')], ['a', 'a'], 'direct-evidence'));
  assert.throws(() => assembleMeasure([record('a', {securityId:'bond'}), record('b', {securityId:'bond'})], ['a','b'], 'direct-evidence'));
  assert.throws(() => assembleMeasure([record('a')], ['missing'], 'direct-evidence'));
});
