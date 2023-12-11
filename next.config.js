/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { webpack }) => {
    config.resolve.fallback = {
      "cohere-ai": false,
      "crypto": false,
      "fs": false
    };

    return config;
  },
  rewrites: async () => {
    return [
      {
        source: "/apii/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/apii/:path*"
            : "/apii/",
      },
      {
        source: "/docs",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/docs"
            : "/apii/docs",
      },
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/openapi.json"
            : "/apii/openapi.json",
      },
    ];
  },
  env: {
    vrijednost: 'my-value',
  },
}

module.exports = nextConfig
