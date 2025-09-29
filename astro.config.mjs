// @ts-check
import { defineConfig } from 'astro/config';
import astroExpressiveCode from 'astro-expressive-code';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  base: '/~andres.cruz/',
  site: 'https://computacion.cs.cinvestav.mx',
  markdown: {
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      theme: 'vitesse-dark',
      wrap: true,
    },
  },
  integrations: [
    astroExpressiveCode({
      themes: ['vitesse-dark'],
    }),
  ],
});
