// Shared display helpers for public pages.

// The five safeguards, worded exactly as on /the-act/ and /legislators/.
// The dated PDF brief still uses the older requirement names in investigation.json.
export const safeguards = [
  {title: 'Explain repayment risk', detail: 'Prepare a written credit analysis before agreeing to the investment.'},
  {title: 'Compare the options', detail: 'Show how reasonable alternatives compare on risk, expected return and access to the money.'},
  {title: 'Explain the exit', detail: 'Describe restrictions on selling or transferring the investment before maturity.'},
  {title: 'Make the financial case', detail: "Explain why this investment serves members' interests and fits the pension portfolio."},
  {title: 'Publish the record', detail: 'Post the analysis and decision within 30 calendar days of the binding commitment, showing whether the transaction has settled.'},
];

const shortMonths = ['Jan.', 'Feb.', 'March', 'April', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'];

// Metadata date style used in labels, tables and lists: "Sept. 7, 2026".
export const metaDate = (iso: string | null | undefined) => {
  if (!iso || !/^\d{4}-\d{2}-\d{2}/.test(iso)) return iso || '';
  const [y, m, d] = iso.slice(0, 10).split('-').map(Number);
  return `${shortMonths[m - 1]} ${d}, ${y}`;
};

// Glossary anchors for financial bases shown in tables.
export const basisTerms: Record<string, {label: string; href: string}> = {
  par: {label: 'Par value', href: '/glossary/#par'},
  funding: {label: 'Manager funding', href: '/glossary/#manager-funding'},
};

export const isExternal = (href: string) => /^(https?:)?\/\//.test(href) || href.startsWith('mailto:');
