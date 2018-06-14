"use strict";
// Copyright 2017, Pulumi Corporation.  All rights reserved.
Object.defineProperty(exports, "__esModule", { value: true });
const cloud = require("@pulumi/cloud");
const sourcePort = 5555;
let workers = new cloud.Service("ts-app-workers", {
    containers: {
        worker: {
            build: "../spamdetector",
            memory: 100,
            ports: [{ port: sourcePort, external: true }]
        }
    },
    replicas: 1
});
exports.workerURL = workers.endpoints.apply(e => e["worker"][sourcePort].hostname);
// todo: get leader dns and connect a pool of workers
//# sourceMappingURL=index.js.map