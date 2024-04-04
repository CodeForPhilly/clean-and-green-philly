/** @type {import('next').NextConfig} */
const nextConfig = {};

module.exports = {
  serverRuntimeConfig: {
    PROJECT_ROOT: __dirname,
  },
  images: {
    domains: ["storage.googleapis.com"],
  },
  async redirects() {
    return [
      {
        source: "/map",
        destination: "/find-properties",
        permanent: true,
      },
    ];
  },
};
