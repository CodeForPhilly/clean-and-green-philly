# Setup Instructions

## Overview

If you are planning to focus on front end development for Clean & Green Philly and do not need to run any of the Python code, follow the installation and setup instructions below.

## Installation

### NVM (Windows Only)

If you are running Windows, you will need to [install NVM for Windows](https://github.com/coreybutler/nvm-windows/blob/master/README.md). Under 'Assets', [nvm-setup.exe](https://github.com/coreybutler/nvm-windows/releases) is straightforward. Node.js and nvm ship with Linux and macOS and therefore do not need to be installed for people using those OS.

## Setup

### Fork the Repository

1. Navigate to [our GitHub repository](https://github.com/CodeForPhilly/vacant-lots-proj).
2. Create a fork of the repository by clicking the "Fork" button in the top right corner of the page. This will create a copy of the repository in your own GitHub account.
3. Clone your fork of the repository to your local machine using `git clone`.

Note: make sure to keep your fork up to date with the original repository by following the instructions [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo#keep-your-fork-synced).

### Nextjs App

Navigate to the root directory of the repository. Install dependencies by running `npm i`. Then, run the development server with `npm run dev`. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result. Congrats! You're all set up.

### MapTiler

You'll need to set up a free [MapTiler](https://www.maptiler.com/) and get an API key. Once you have this, set it as en environment variable called `NEXT_PUBLIC_MAPTILER_KEY`.

#### Formatting

For js/ts, install [Prettier](https://prettier.io/) and enable it for your [editor](https://prettier.io/docs/en/editors.html). For VSCode, enable [Format on Save](https://www.robinwieruch.de/how-to-use-prettier-vscode/) for best experience.
