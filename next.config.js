/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { webpack }) => {
    config.resolve.fallback = {
      "cohere-ai": false,
      "crypto": false,
      "fs": false
    };

    return config;
  }
}

module.exports = nextConfig
