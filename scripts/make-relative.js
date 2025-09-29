#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const distDir = path.join(__dirname, '..', 'dist');

console.log('🔧 Converting absolute paths to relative paths...');

// Function to convert absolute paths to relative paths
function convertToRelative(content, filePath) {
  // Get the depth of the current file relative to dist
  const relativePath = path.relative(distDir, filePath);
  const depth = relativePath.split(path.sep).length - 1;
  const prefix = '../'.repeat(depth);
  
  // Convert src="/..." to relative paths
  content = content.replace(/src="\//g, `src="${prefix}`);
  
  // Convert href="/..." to relative paths
  content = content.replace(/href="\//g, `href="${prefix}`);
  
  // Convert action="/..." to relative paths
  content = content.replace(/action="\//g, `action="${prefix}`);
  
  // Convert CSS references to local styles.css
  content = content.replace(/href="[^"]*_astro\/[^"]*\.css"/g, 'href="styles.css"');
  
  // Fix internal links - add trailing slash for directory links
  content = content.replace(/href="([^"\/\.]+)"(?![^<]*>)/g, 'href="$1/"');
  
  // Fix links that should point to index.html
  content = content.replace(/href="([^"]+\/)"(?![^<]*>)/g, 'href="$1index.html"');
  
  return content;
}

// Function to process HTML files
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
      content = convertToRelative(content, filePath);
      fs.writeFileSync(filePath, content);
    }
  }
}

// Function to copy CSS files to all directories
function copyCssFiles() {
  const astroDir = path.join(distDir, '_astro');
  
  if (fs.existsSync(astroDir)) {
    const files = fs.readdirSync(astroDir);
    let cssFile = null;
    
    // Find the CSS file
    for (const file of files) {
      if (file.endsWith('.css')) {
        cssFile = file;
        break;
      }
    }
    
    if (cssFile) {
      const srcPath = path.join(astroDir, cssFile);
      
      // Copy CSS to root
      const rootDestPath = path.join(distDir, 'styles.css');
      console.log(`📋 Copying CSS: ${cssFile} → styles.css`);
      fs.copyFileSync(srcPath, rootDestPath);
      
      // Copy CSS to all subdirectories
      copyCssToSubdirs(distDir, srcPath);
    }
  }
}

// Function to copy CSS to all subdirectories
function copyCssToSubdirs(dir, srcPath) {
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory() && file !== '_astro') {
      const destPath = path.join(filePath, 'styles.css');
      fs.copyFileSync(srcPath, destPath);
      console.log(`📋 Copying CSS to: ${path.relative(distDir, filePath)}/styles.css`);
      
      // Recursively copy to subdirectories
      copyCssToSubdirs(filePath, srcPath);
    }
  }
}

// Main execution
try {
  if (!fs.existsSync(distDir)) {
    console.error('❌ dist directory not found. Run "bun run build" first.');
    process.exit(1);
  }
  
  // Copy CSS files to root
  copyCssFiles();
  
  // Process all HTML files
  processHtmlFiles(distDir);
  
  console.log('✅ Successfully converted all paths to relative!');
  console.log('🎉 Your site is now ready to be opened directly in the browser!');
  
} catch (error) {
  console.error('❌ Error:', error.message);
  process.exit(1);
}
