# Contribution Guide

If you would like to contribute to development, please pull the latest version of development, create a local branch with a descriptive name, write your code, and push the branch to the repository. After this, create a pull request for your feature branch to the development branch. Please do not create PRs against the master branch.

## An Example Workflow
Let's say you've found a bug you think you can fix or thought of a feature you want to add to the project. Please start or join a conversation using GitHub's issues feature to discuss it. Once you've gotten the go-ahead to implement your changes, you'll want to do the following:

// TODO: Make a setup doc
First setup the project, follow the steps outlined in [the local setupguide](LINK_TO_SETUP_DOC).

Then, think of a meaningful but short name for what you're about to build and use that name to create a new branch. Here's an example:

```
$> git checkout -b my-cool-branch-name
```

Write your code and make meaningful commits along the way (you're encouraged to rebase to make a coherrent history). Here's a quick example:

```
# Write some code
$> git commit -am "Add new class to a module"
# Make some more changes
$> git commit -am "Add test for new class"
```

If you need help with Git, this repository's author created a three-article series for beginner to professional-level version control:
* [The bare-basics of Git (installation, adding, committing)](https://erikscode.space/index.php/2021/03/26/professional-version-control-with-git-pt-1-the-basics/)
* [Collaboration Git (cloning and pull requests)](https://erikscode.space/index.php/2021/04/05/professional-version-control-with-git-pt-2-collaboration/)
* [Advanced Git techniques (rebasing and bisecting)](https://erikscode.space/index.php/2021/04/16/professional-version-control-with-git-pt-3-rebase-and-bisect/)

## Test Your Changes

// TODO: Add guidance for testing

## Issue Label Guide

// TODO: Create issue labels and some information about them
