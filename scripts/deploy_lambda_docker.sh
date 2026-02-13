#!/bin/bash
# Deploy FastAPI to AWS Lambda using Docker for compatibility

set -e

echo "📦 Creating Lambda deployment package with Docker..."

# Clean up old builds
rm -rf lambda_package lambda_package.zip

# Create package directory
mkdir -p lambda_package

# Copy source code
echo "Copying source code..."
cp -r src/college_baseball lambda_package/

# Install dependencies using Docker to match Lambda environment
echo "Installing dependencies (using Docker for Lambda compatibility)..."

docker run --rm \
    -v "$PWD/lambda_package:/var/task" \
    -w /var/task \
    public.ecr.aws/lambda/python:3.11 \
    pip install \
        pandas numpy sqlalchemy pydantic pydantic-settings \
        fastapi mangum psycopg2-binary \
        -t /var/task --no-cache-dir

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
echo "Package is Lambda-compatible! Upload to AWS Lambda now."
