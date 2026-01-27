#!/usr/bin/env node

/**
 * Unzip Chrome extension (.crx) files
 * Usage: node unzip-crx.mjs <crx-file-path> [destination]
 *
 * If destination is not provided, extracts to the same directory as the crx file
 */

import { execFileSync } from 'child_process';
import { existsSync, mkdirSync } from 'fs';
import { dirname, basename, join, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: node unzip-crx.mjs <crx-file-path> [destination]');
    console.error('  crx-file-path: Path to the .crx file');
    console.error('  destination: Optional output directory (defaults to crx file directory)');
    process.exit(1);
  }

  const crxPath = resolve(args[0]);

  if (!existsSync(crxPath)) {
    console.error(`Error: File not found: ${crxPath}`);
    process.exit(1);
  }

  if (!crxPath.endsWith('.crx')) {
    console.error('Error: File must have .crx extension');
    process.exit(1);
  }

  // Default destination: same directory as crx file, folder named after crx file (without extension)
  const crxDir = dirname(crxPath);
  const crxName = basename(crxPath, '.crx');
  const destination = args[1] ? resolve(args[1]) : join(crxDir, crxName);

  // Ensure @tomjs/unzip-crx is installed
  try {
    await import('@tomjs/unzip-crx');
  } catch {
    console.log('Installing @tomjs/unzip-crx...');
    execFileSync('npm', ['install', '@tomjs/unzip-crx'], {
      stdio: 'inherit',
      cwd: __dirname
    });
  }

  // Import and run unzip
  const { default: unzip } = await import('@tomjs/unzip-crx');

  // Create destination directory if it doesn't exist
  if (!existsSync(destination)) {
    mkdirSync(destination, { recursive: true });
  }

  console.log(`Extracting: ${crxPath}`);
  console.log(`Destination: ${destination}`);

  try {
    await unzip(crxPath, destination);
    console.log('✅ Successfully extracted crx file');
  } catch (error) {
    console.error('❌ Failed to extract crx file:', error.message);
    process.exit(1);
  }
}

main();
