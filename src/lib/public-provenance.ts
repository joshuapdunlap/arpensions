const windowsPath = /^[A-Za-z]:/;
const encodedSeparator = /%(?:2f|5c)/i;
const encodedAbsolutePath = /^%(?:2f|5c)/i;
const privateRoot = /(?:^|[^A-Za-z0-9_]|%(?:2f|5c))raw(?:[\\/]|%(?:2f|5c)|$)/i;

export const exposesPrivatePath = (value: unknown): boolean => {
  if (typeof value !== 'string' || !value.trim()) return true;
  const candidate=value.trim();
  return candidate.startsWith('/') || candidate.startsWith('\\') || encodedAbsolutePath.test(candidate) || windowsPath.test(candidate) || privateRoot.test(candidate);
};

export const isPublicOriginalFilename = (value: unknown): value is string =>
  !exposesPrivatePath(value) && !(value as string).includes('/') && !(value as string).includes('\\') && !encodedSeparator.test(value as string) && value !== '.' && value !== '..';

export const requirePublicOriginalFilename = (value: unknown, context: string): string => {
  if (!isPublicOriginalFilename(value)) throw new Error(`${context} must be a public filename, not a private path`);
  return value;
};

export const requirePublicLocator = (value: unknown, context: string): string => {
  if (exposesPrivatePath(value)) throw new Error(`${context} exposes a private path`);
  return value as string;
};
