const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);

config.resolver.assetExts = [
  ...config.resolver.assetExts,
  'png', 'jpg', 'jpeg', 'svg', 'webp'
];

module.exports = config;
