'use strict';

//implement the file system module of node js
const fs = require('fs');
const torrent = fs.readFileSync('test.torrent');
console.log(torrent.toString('utf8'));
