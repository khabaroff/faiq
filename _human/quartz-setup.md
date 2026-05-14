# Quartz Setup & Deployment

This guide explains how to deploy the `public/` folder using [Quartz](https://quartz.jzhao.xyz/).

## Directory Mapping
The `public/` folder in this repository is a valid Obsidian vault and serves as the content source for Quartz.

- `public/sources/` -> Original articles
- `public/summaries/` -> Structured summaries
- `public/tools/` -> Tool wiki pages
- `public/techniques/` -> Technique wiki pages

## Deployment Steps

1. **Install Quartz** (one-time):
   ```bash
   git clone https://github.com/jackyzha0/quartz.git /opt/quartz
   cd /opt/quartz
   npm install
   ```

2. **Configure Symlink**:
   Point Quartz to our `public/` directory:
   ```bash
   rm -rf /opt/quartz/content
   ln -s /path/to/faiq/public /opt/quartz/content
   ```

3. **Build & Publish**:
   ```bash
   npx quartz build
   # Copy public/ to your web server or use Quartz's built-in deployment
   ```

## CI/CD Pipeline
The recommended approach is to run `npx quartz build` after every successful `run_all` completion if the state has changed.
