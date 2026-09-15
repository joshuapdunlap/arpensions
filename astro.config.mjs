import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://arpensions.org',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
  devToolbar: { enabled: false },
});
