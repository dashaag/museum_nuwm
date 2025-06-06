# Stage 1: Build the React application
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json and lock file
# Use wildcard for lock file to support npm, yarn, pnpm
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

# Install dependencies based on the lock file found
# This example assumes npm. If using yarn or pnpm, adjust accordingly.
RUN if [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    elif [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    else echo "Lockfile not found or npm install needed." && npm install; fi

COPY . .

# Set build arguments for Vite (if needed, e.g., API base URL)
# ARG VITE_API_BASE_URL=/api
# ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

# Stage 2: Serve the built application with a lightweight server
FROM node:18-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=build /app/dist /app/dist

EXPOSE 5173

# Serve the 'dist' folder. Vite builds to 'dist' by default.
# The -l flag tells serve to listen on all interfaces, important for Docker
CMD ["serve", "-s", "dist", "-l", "tcp://0.0.0.0:5173"]
