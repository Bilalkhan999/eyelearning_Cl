#!/bin/bash

# Vercel build script

echo "Installing Git LFS..."
git lfs install

echo "Fetching LFS files..."
git lfs fetch
git lfs checkout

echo "Git LFS status:"
git lfs status

echo "Listing static files:"
ls -la static/images/cn/

echo "Build complete!"
