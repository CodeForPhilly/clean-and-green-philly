# Guidelines for contributing

## Overview

This document will outline guidelines for contributing to the Clean & Green Philly [codebase](https://github.com/CodeForPhilly/vacant-lots-proj).

## Joining the regular meetings

We host weekly meetings both in person and remotely. This is largely where we make decisions and set up collaborative pairing sessions to get large chunks of work done.

The best way to find out about our meetings is joining the [#clean-and-green-philly](https://codeforphilly.slack.com/archives/C05H9QBMP96) channel on the [Code for Philly](https://www.codeforphilly.org/) [Slack](https://www.codeforphilly.org/chat/).

## Issues

We use issues to describe our needs and track our work. Writing clear and descriptive issues help make sure our teammates are able to understand the task and complete the work.

We also use issues for tracking our own team needs (e.g. adding documentation).

### Add an issue

Navigate to our [issues page on Github](https://github.com/CodeForPhilly/vacant-lots-proj/issues) and hit the big green `New` button.

## Making code changes

Changes to our codebase should always address an [issue](https://github.com/CodeForPhilly/vacant-lots-proj/issues) and need to be requested to be merged by submitting a pull request that will be reviewed by at least the team lead or tech lead.

### Choose an issue

Look through the [issues page](https://github.com/CodeForPhilly/vacant-lots-proj/issues) in the repo.

Find a task that has no current assignees and sounds like a task that either you can confidently take on yourself or involves a new language, framework, or design that you want learn.

For the latter it is best to pair on this with a team member experienced with that thing you want to learn. 

### Commit your work

Any good work with code involves good commit messages.

The best commit messages read like instructions on how to recreate the code being committed.

Individual commits should be small chunks of work included together as one step in the process.

### Push your work up to the remote repo

When you have completed your work and made good commit messages that read like clear instructions, you will want to push your work up to our remote repository on Github.

```sh
# Make a matching remote branch to push to
# Note: While it is usually `origin`, the remote repo may be named a different alias on your machine
git push --set-upstream origin <new-branch-name>

# Once you have set up a remote branch continue to push changes with:
git push
```

### Create a pull request

In order to merge your work to the `develop` branch you must create a pull request.

Often Github will put up a notification that a new branch has been pushed and give a green "Make a PR" button on any page of the repo. If you don't see this you can go to the [pull requests tab](https://github.com/CodeForPhilly/vacant-lots-proj/pulls) and hit the big green `New` button.

There is a template to follow to make sure that reviewers have enough context about the changes you made and what they fix.

It is vital to provide clear instructions how to test the changes you made.

Please also make sure you tag the issue you are addressing. You can do this when writing the PR by writing `#<number>` in the `Does this close any currently open issues` section.

```md
<!-- For example, for a PR addressing issue #13 -->
Closes #13
```

To make sure reviewers know to review it, finish up by assigning either the team lead or two team members in the 'reviewers' tab in the sidebar or under the PR text depending on your view.

### Reviewed work

The reviewer(s) will either ask for changes or approve the PR.

If changes are requested, please make the changes in your branch and push them up to Github when ready.

```bash
# Tip: If you are fixing something from a particular commit, you can create a !fixup commit with
git commit --fixup <sha-for-commit>

# Then, when approved, before you merge you can use:
git rebase -i --autosquash develop
# to squash your !fixup commits into their corresponding commits and make sure your branch is up to date with develop
```

Once you have pushed up your fixes, let your reviewer know and they will follow up and look again. This may loop a few times.

Once your changes are approved, you can hit the `merge` button to merge to the `develop` branch (unless specified otherwise).

Please also delete the branch from Github (you'll be prompted).

### Update changelog

We keep a changelog following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. In the unreleased section add the following line to one of the sections within unreleased:

```md

### Added

- Add your PR title [#1](https://github.com/CodeForPhilly/vacant-lots-proj/pull/1)

```

You would use your PR's title, the number of your PR, and the link to that PR. There are a few sections: `Added, Changed, Deprecated, Removed, Fixed, Security`, and you should add your line to the section that best matches what your PR is contributing.

### Clean up

Once you've merged your work go back to your terminal

```sh
# Go to the develop branch
git checkout develop

# Pull down the changes you merged
git pull

# Delete the branch from your local machine
git branch -d <new-branch-name>
```

## Creating a release

See the [RELEASES.md](https://github.com/CodeForPhilly/vacant-lots-proj/blob/develop/RELEASES.md) for an explanation of this process
