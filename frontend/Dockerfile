FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

# Install production dependencies
COPY package.json package-lock.json* ./
RUN npm ci --only=production

# Copy pre-built Next.js output (built locally to avoid Docker memory issues)
COPY public ./public
COPY .next ./.next
COPY next.config.js ./

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

EXPOSE 3000
ENV PORT=3000
CMD ["npx", "next", "start"]
