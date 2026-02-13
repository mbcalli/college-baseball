#!/bin/bash
# Deploy FastAPI to AWS Lambda with platform-specific builds

set -e

echo "📦 Creating Lambda deployment package..."

# Clean up old builds
rm -rf lambda_package lambda_package.zip

# Create package directory
mkdir -p lambda_package

# Copy source code
echo "Copying source code..."
cp -r src/college_baseball lambda_package/

# Install dependencies for Lambda Linux environment
echo "Installing dependencies for Linux x86_64..."
pip3 install \
    --target lambda_package \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.11 \
    --only-binary=:all: \
    --upgrade \
    pandas numpy sqlalchemy pydantic pydantic-settings \
    fastapi mangum psycopg2-binary

# Remove unnecessary files to reduce size
echo "Cleaning up..."
cd lambda_package
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
cd ..

# Create ZIP file
echo "Creating ZIP file..."
cd lambda_package
zip -r9 ../lambda_package.zip . -q
cd ..

echo "✓ Package created: lambda_package.zip ($(du -h lambda_package.zip | cut -f1))"
echo ""
echo "Upload lambda_package.zip to AWS Lambda"
