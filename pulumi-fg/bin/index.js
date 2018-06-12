"use strict";
// Copyright 2017, Pulumi Corporation.  All rights reserved.
Object.defineProperty(exports, "__esModule", { value: true });
const cloud = require("@pulumi/cloud");
let workers = new cloud.Service("ts-app-workers", {
    containers: {
        worker: {
            build: "./testapp",
            memory: 100,
            ports: [{ port: 80, external: true }]
        }
    },
    replicas: 1
});
exports.workerURL = workers.endpoints.apply(e => e["worker"][80].hostname);
//# sourceMappingURL=index.js.map