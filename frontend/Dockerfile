FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files (uses package*.json so build doesn't fail if lockfile is missing)
COPY package*.json ./

# Install dependencies including devDependencies (needed for Vite in dev mode)
RUN npm ci --include=dev || npm install

# Copy source
COPY . .

# Expose port (Vite dev)
EXPOSE 5173

# Run dev server inside container (development mode)
CMD ["npx", "--yes", "vite", "--host"]
