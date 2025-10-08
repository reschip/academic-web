#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const distDir = path.join(__dirname, '..', 'dist');

console.log('🔧 Preparing site for subdirectory deployment...');

// Function to process HTML files for subdirectory deployment
function processHtmlFiles(dir) {
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      processHtmlFiles(filePath);
    } else if (file.endsWith('.html')) {
      console.log(`📄 Processing: ${path.relative(distDir, filePath)}`);
      
      let content = fs.readFileSync(filePath, 'utf8');
      
      // Fix internal navigation links to include the base path
      content = content.replace(/href="about"/g, 'href="/~andres.cruz/about/"');
      content = content.replace(/href="coursework"/g, 'href="/~andres.cruz/coursework/"');
      content = content.replace(/href="coursework\/ada-tarea-1"/g, 'href="/~andres.cruz/coursework/ada-tarea-1/"');
      content = content.replace(/href="coursework\/ada-tarea-2"/g, 'href="/~andres.cruz/coursework/ada-tarea-2/"');
      content = content.replace(/href="coursework\/ada-tarea-3"/g, 'href="/~andres.cruz/coursework/ada-tarea-3/"');
      
      // Fix links from subdirectories to go back to root
      content = content.replace(/href="\.\.\/about\/"/g, 'href="/~andres.cruz/about/"');
      content = content.replace(/href="\.\.\/coursework\/"/g, 'href="/~andres.cruz/coursework/"');
      content = content.replace(/href="\.\.\/coursework\/ada-tarea-1\/"/g, 'href="/~andres.cruz/coursework/ada-tarea-1/"');
      content = content.replace(/href="\.\.\/coursework\/ada-tarea-2\/"/g, 'href="/~andres.cruz/coursework/ada-tarea-2/"');
      content = content.replace(/href="\.\.\/coursework\/ada-tarea-3\/"/g, 'href="/~andres.cruz/coursework/ada-tarea-3/"');
      
      // Fix links from deeper subdirectories
      content = content.replace(/href="\.\.\/\.\.\/about\/"/g, 'href="/~andres.cruz/about/"');
      content = content.replace(/href="\.\.\/\.\.\/coursework\/"/g, 'href="/~andres.cruz/coursework/"');
      content = content.replace(/href="\.\.\/\.\.\/coursework\/ada-tarea-1\/"/g, 'href="/~andres.cruz/coursework/ada-tarea-1/"');
      content = content.replace(/href="\.\.\/\.\.\/coursework\/ada-tarea-2\/"/g, 'href="/~andres.cruz/coursework/ada-tarea-2/"');
      content = content.replace(/href="\.\.\/\.\.\/coursework\/ada-tarea-3\/"/g, 'href="/~andres.cruz/coursework/ada-tarea-3/"');
      
      // Fix image paths to use absolute paths
      content = content.replace(/src="\.\.\/web-app-manifest-192x192\.png"/g, 'src="/~andres.cruz/web-app-manifest-192x192.png"');
      content = content.replace(/src="\.\.\/image-about\.jpeg"/g, 'src="/~andres.cruz/image-about.jpeg"');
      content = content.replace(/src="\.\.\/favicon\.svg"/g, 'src="/~andres.cruz/favicon.svg"');
      
      // Fix CSS references to use absolute paths
      content = content.replace(/href="\.\.\/_astro\/[^"]*\.css"/g, 'href="/~andres.cruz/_astro/about.C2pHtI6A.css"');
      content = content.replace(/href="\.\.\/styles\.css"/g, 'href="/~andres.cruz/_astro/about.C2pHtI6A.css"');
      content = content.replace(/href="styles\.css"/g, 'href="/~andres.cruz/_astro/about.C2pHtI6A.css"');
      
      fs.writeFileSync(filePath, content);
    }
  }
}

// Main execution
try {
  if (!fs.existsSync(distDir)) {
    console.error('❌ dist directory not found. Run "bun run build" first.');
    process.exit(1);
  }
  
  // Process all HTML files
  processHtmlFiles(distDir);
  
  console.log('✅ Successfully prepared site for subdirectory deployment!');
  console.log('🎉 Your site is now ready for https://computacion.cs.cinvestav.mx/~andres.cruz/');
  
} catch (error) {
  console.error('❌ Error:', error.message);
  process.exit(1);
}


