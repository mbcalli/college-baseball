#!/bin/bash
# Deploy FastAPI to AWS Lambda

set -e

echo "📦 Creating Lambda deployment package..."

# Clean up old builds
rm -rf lambda_package lambda_package.zip

# Create package directory
mkdir -p lambda_package

# Copy source code
echo "Copying source code..."
cp -r src/college_baseball lambda_package/

# Install dependencies into package
echo "Installing dependencies..."
uv pip install \
  --target lambda_package \
  --python-version 3.11 \
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
find . -type f -name "*.so" -delete
cd ..

# Create ZIP file
echo "Creating ZIP file..."
cd lambda_package
zip -r9 ../lambda_package.zip . -q
cd ..

echo "✓ Package created: lambda_package.zip ($(du -h lambda_package.zip | cut -f1))"
echo ""
echo "Next steps:"
echo "1. Go to AWS Lambda Console"
echo "2. Create a new function (Python 3.11)"
echo "3. Upload lambda_package.zip"
echo "4. Set handler to: college_baseball.api.handler"
echo "5. Set environment variable DATABASE_URL to your RDS connection string"
