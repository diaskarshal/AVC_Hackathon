#!/bin/bash

# BuildFlow Setup Script
echo "🚀 Setting up BuildFlow ERP System..."

# Create backend directory structure
echo "📁 Creating backend directory structure..."
mkdir -p backend/app/{models,schemas,routes,services,middleware,utils,exceptions}
mkdir -p backend/tests
mkdir -p backend/alembic/versions

# Create __init__.py files
echo "📝 Creating __init__.py files..."
touch backend/app/__init__.py
touch backend/app/models/__init__.py
touch backend/app/schemas/__init__.py
touch backend/app/routes/__init__.py
touch backend/app/services/__init__.py
touch backend/app/middleware/__init__.py
touch backend/app/utils/__init__.py
touch backend/app/exceptions/__init__.py
touch backend/tests/__init__.py

# Create frontend directory structure
echo "📁 Creating frontend directory structure..."
mkdir -p frontend/{public,src/{components,pages,services,utils}}

# Copy .env.example to .env
echo "⚙️  Setting up environment variables..."
cd backend
if [ -f .env.example ]; then
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
else
    echo "⚠️  .env.example not found, skipping..."
fi
cd ..

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy all the code files from the artifacts into their respective locations"
echo "2. Run: docker-compose up --build"
echo "3. Access the API at http://localhost:8000/docs"
echo ""
echo "Happy coding! 🎉"