FROM node:20-alpine as develop-stage

WORKDIR /app

COPY package*.json ./

RUN yarn global add @quasar/cli

COPY . .

EXPOSE 9000

CMD yarn install && yarn dev --port 9000
