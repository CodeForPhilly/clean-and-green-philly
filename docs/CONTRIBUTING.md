# Guidelines for contributing

## Overview

🎉 First off, thanks for taking the time to contribute! 🎉 Clean & Green Philly wouldn't be possible without volunteers like you.

This document will outline guidelines for contributing to the Clean & Green Philly [codebase](https://github.com/CodeForPhilly/vacant-lots-proj).

Before contributing, we encourage you to read our [LICENSE](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/LICENSE) and [README](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/README.md) files. If you have any questions not answered by the content of this repository, please contact us via [our Slack channel](https://codeforphilly.slack.com/archives/C05H9QBMP96).

## Quickstart Checklist

To ensure smooth contributions to the Clean & Green Philly project, please follow these steps:

- [ ] **Join the Slack channel**: [#clean-and-green-philly](https://codeforphilly.slack.com/archives/C05H9QBMP96)
- [ ] **Read the [README](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/README.md)**
- [ ] **Attend a meeting**: Check Slack for meeting times and join our regular meetings
- [ ] **Find an issue**: Look through the [issues page](https://github.com/CodeForPhilly/vacant-lots-proj/issues) and comment on one you'd like to work on
- [ ] **Fork the repository**:
  - Navigate to [our GitHub repository](https://github.com/CodeForPhilly/clean-and-green-philly)
  - Create a fork of the repository by clicking the "Fork" button in the top right corner of the page
  - Clone your fork of the repository to your local machine using `git clone`
  - Keep your fork up to date with the original repository by following the instructions [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo#keep-your-fork-synced)
- [ ] **Set up your local environment**: Follow instructions in the [SETUP](/docs/SETUP) folder
- [ ] **Make sure you're up-to-date with the `staging` branch** To maintain repo organization and protection, merges to main are not allowed. All changes must be made through pull requests to the `staging` branch.
- [ ] **Create a new branch**:
  - Name it `<github-username>/<issue-number>-<kebab-case-description>`
  - Example: `vimusds/1069-fix-territory-on-mobile`
- [ ] **Work on the issue**: Make your changes, commit them, and push to your branch
- [ ] **Commit Message Format**: Follow the Conventional Commits format to maintain a clean and meaningful git history.

  ```
  <type>[optional scope]: <description>
  ```

  Where:

  - `<type>` is one of: feat, fix, docs, style, refactor, test, chore, ci, perf, build
  - `[optional scope]` is the area of the codebase affected (e.g., component name)
  - `<description>` is a concise description of the change

  **Examples:**

  - `fix: resolve data fetching issue`
  - `feat(FilterView): add new method for conditional filtering`
  - `docs: update the pull request template`

- [ ] **Open a Pull Request (PR)**: Use the provided template, tag relevant issues, and provide testing instructions. Make sure the base branch of the PR is set to `base: staging`.
- [ ] **Ensure all checks pass**: Fix any errors and re-check
- [ ] **Tag reviewers**: Find appropriate reviewers from the [CODEOWNERS](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/.github/CODEOWNERS) file
- [ ] **Close the issue**: Once your PR is merged, comment on the issue to close it, tagging the relevant reviewer(s)
- [ ] **Follow deployment process**: Your changes will be reviewed, merged into the main branch, and eventually deployed to production

## Joining the regular meetings

We hold weekly meetings via Zoom, plus the monthly in-person Code for Philly hack night. During these meetings, we cover recent progress, next steps for the week, and any outstanding challenges. Participating in these meetings is the best way to get up to speed on the project. The best way to find out about when they're happening is joining the [#clean-and-green-philly](https://codeforphilly.slack.com/archives/C05H9QBMP96) channel on the [Code for Philly](https://www.codeforphilly.org/) [Slack](https://www.codeforphilly.org/chat/).

## How can I contribute?

### Find an issue

We welcome all kinds of contributions, big or small. The best way to start is to look through the [issues page](https://github.com/CodeForPhilly/vacant-lots-proj/issues) to see what's available to be working on. If you're not sure which issue to tackle, consider filtering them by tags or asking in the [Slack channel](https://codeforphilly.slack.com/archives/C05H9QBMP96).

Once you've found an issue you'd like to work on, please comment on it to let us know you're interested. We'll do our best to assign it to you ASAP.

### Being fair

If you're unable to complete the issue in a timely manner (a week or two), please let us know so we can reassign it. If we see an issue with no activity for 3 or more days, we'll reach out via GitHub and Slack to the person to whom it's assigned. If there is no activity at all on the issue for 1 week, we'll reassign it. If there is some activity (e.g., a draft PR or a message to let us know that you're out of town), then you're free to continue working on the issue for another week. However, in the interest of avoiding bottlenecks and giving everyone a fair chance to contribute, we ask that everyone try to complete all issues within 2 weeks of assignment.

### Local setup

For info on how to get the codebase setup, see the [SETUP](/docs/SETUP) folder, which contains instructions for setting up the front end, back end, and full stack, depending on your interest. If you have questions about the process, please ask in the [Slack channel](https://codeforphilly.slack.com/archives/C05H9QBMP96).

## Open an Issue

To report a bug, request a feature, or suggest an enhancement, please open an issue on the [issues page](https://github.com/CodeForPhilly/vacant-lots-proj/issues). We ask that you provide as much detail as possible, including steps to reproduce the issue, expected behavior, and any relevant screenshots or logs. We provide issue templates to help guide you through this process.

## Contribute to Documentation

As this project grows, building our documentation is an important part of making sure it's accessible and sustainable. We welcome contributions to our documentation, ranging from refining existing content for better clarity, adding examples and tutorials for complex features, to ensuring inclusivity in language and presentation. In particular, we welcome suggestions for any of the documents in [docs](../docs) and [SETUP](/docs/SETUP).

## Suggesting Something Else

Got an idea for another way in which you could contribute to our project? Maybe you want to write an article for us, or help us with research or graphic design. If you have an idea for a way to improve the project that we aren't currently including, [reach out via Slack](https://codeforphilly.slack.com/archives/C05H9QBMP96) and let us know how you'd like to get involved.
