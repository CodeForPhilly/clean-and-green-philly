# Guidelines for contributing

## Overview

🎉 First off, thanks for taking the time to contribute! 🎉 Clean & Green Philly wouldn't be possible without volunteers like you.

This document will outline guidelines for contributing to the Clean & Green Philly [codebase](https://github.com/CodeForPhilly/vacant-lots-proj).

Before contributing, we encourage you to read our [LICENSE](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/LICENSE) and [README](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/README.md) files. If you have any questions not answered by the content of this repository, please contact us via [our Slack channel](https://codeforphilly.slack.com/archives/C05H9QBMP96).

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


## Quickstart

To maintain repo organization and protection, merges to main are not allowed. All changes must be made through pull requests to the `staging` branch. Follow these steps, [example PR](https://github.com/CodeForPhilly/clean-and-green-philly/pull/617) for reference:

1. Have an assigned issue (e.g. [#646](https://github.com/CodeForPhilly/clean-and-green-philly/issues/646))
1. Ensure you're up to date with the `staging` branch
2. Create a new branch
    - Name it `<github-username>`/`<issue-number>`-`<kebab-case-description>`. 
    - Example: `vimusds/1069-fix-territory-on-mobile`.
3. Push changes and open PR: Push your commits and open a PR with the template filled in. 
    - Provide clear instructions on how to test/view your changes
    - Tag the issues you're addressing using `#<number>` in the "Does this close any currently open issues?" section.
4. Ensure your PR passes all checks. If not, resolve the errors and try again.
5. Tag reviewers: Tag a code approver (see [CODEOWNERS](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/.github/CODEOWNERS)) for review.

Once approved and all checks pass, your code will be built in Vercel if it's a frontend change and merged into staging by a reviewer. Now you just need to close your issue!

### Closing your Issue
To close the issue you worked on, add a comment to the issue tagging the appropriate reviewer(s).
- Front-End Issues: Tag @paulhchoi and @thansidwell. If it involves the map, also tag @brandonfcohen1.
- Back-End Issues: Tag @brandonfcohen1.

🎉 Congrats, you finished your contribution!

### What's next?

-  Design review: The design team will review and eventually merge it into main for deployment.
- Deploy to prod: A Clean and Green Philly team member will deploy your changes to the production site.

## Open an Issue

To report a bug, request a feature, or suggest an enhancement, please open an issue on the [issues page](https://github.com/CodeForPhilly/vacant-lots-proj/issues). We ask that you provide as much detail as possible, including steps to reproduce the issue, expected behavior, and any relevant screenshots or logs. We provide issue templates to help guide you through this process.

## Contribute to Documentation

As this project grows, building our documentation is an important part of making sure it's accessible and sustainable. We welcome contributions to our documentation, ranging from refining existing content for better clarity, adding examples and tutorials for complex features, to ensuring inclusivity in language and presentation. In particular, we welcome suggestions for any of the documents in [docs](../docs) and [SETUP](/docs/SETUP).

## Suggesting Something Else

Got an idea for another way in which you could contribute to our project? Maybe you want to write an article for us, or help us with research or graphic design. If you have an idea for a way to improve the project that we aren't currently including, [reach out via Slack](https://codeforphilly.slack.com/archives/C05H9QBMP96) and let us know how you'd like to get involved.
