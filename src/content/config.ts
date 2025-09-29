import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    course: z.string().optional(),
    readTime: z.string().optional(),
    imageType: z.number().optional().default(1),
  }),
});

export const collections = {
  posts,
};
