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
        prepare:
          "echo ${nextRelease.version} ${branch.name} ${commits.length} ${Date.now()} > version.txt",
      },
    ],
  ],
};
