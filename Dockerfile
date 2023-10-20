# Copyright (c) TribuFu. All Rights Reserved.

FROM node:18-alpine AS base
VOLUME /config
VOLUME /saved

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /src
COPY package.json lerna.json yarn.lock ./
COPY ./package.json ./package.json
COPY ./next.config.js ./next.config.js
COPY ./next-i18next.config.js ./next-i18next.config.js
RUN yarn --frozen-lockfile

FROM base AS build
WORKDIR /src
COPY --from=deps /src/node_modules ./node_modules
COPY . ./.
WORKDIR /src/.
ENV NEXT_TELEMETRY_DISABLED 1
RUN yarn build

FROM base AS final
WORKDIR /app
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=build --chown=nextjs:nodejs /src/node_modules ./node_modules
COPY --from=build --chown=nextjs:nodejs /src/.next ./.next
COPY --from=build --chown=nextjs:nodejs /src/package.json ./package.json
COPY --from=build --chown=nextjs:nodejs /src/next.config.js ./next.config.js
COPY --from=build --chown=nextjs:nodejs /src/public ./public
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
USER nextjs
EXPOSE ${PORT}
CMD ["yarn", "start"]
