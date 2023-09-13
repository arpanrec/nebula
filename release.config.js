module.exports = {
  branches: ["main"],
  tagFormat: "${version}",
  plugins: [
    "@semantic-release/commit-analyzer",
    {
      preset: "angular",
    },
    [
      "@semantic-release/exec",
      {
        prepareCmd: 'sed -i "s\\^version.*\\version: ${nextRelease.version}\\g\" galaxy.yml',
      },
    ],
  ],
};
