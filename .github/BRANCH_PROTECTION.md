# Branch Protection Rules

This document describes the branch protection rules configured for this repository.

## Master Branch Protection

The `master` branch is protected with the following rules:

### ✅ Required Reviews
- **Pull Request reviews are required** before merging
- **At least 1 approval required** from code owners
- Code owner approval is **required** (see CODEOWNERS file)

### ✅ Code Owners
All changes to any file in the repository require approval from **@Roteus**.

See the [CODEOWNERS](CODEOWNERS) file for the complete list of code owners.

## How to Contribute

1. **Fork the repository** or create a new branch
2. **Make your changes** in your branch
3. **Push your branch** to GitHub
4. **Open a Pull Request** to the `master` branch
5. **Wait for review and approval** from @Roteus
6. Once approved, the PR can be merged

## Configuring Branch Protection in GitHub

To ensure these rules are enforced, configure the following settings in the GitHub repository:

### Steps to Configure:

1. Go to repository **Settings**
2. Navigate to **Branches** (under "Code and automation")
3. Click **Add branch protection rule**
4. For **Branch name pattern**, enter: `master`
5. Enable the following options:
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: **1**
     - ✅ Dismiss stale pull request approvals when new commits are pushed
     - ✅ Require review from Code Owners
   - ✅ **Require status checks to pass before merging** (optional, if you have CI/CD)
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Do not allow bypassing the above settings** (recommended)
   - ✅ **Restrict who can push to matching branches** (optional, for additional security)
6. Click **Create** or **Save changes**

### Additional Recommendations:

- **Include administrators**: Consider not allowing administrators to bypass these rules for maximum security
- **Require linear history**: Enforce a clean commit history by requiring linear history
- **Lock branch**: Prevent any direct pushes (everyone must use Pull Requests)

## Why These Rules?

Branch protection rules help maintain code quality and ensure:
- All changes are reviewed before merging
- No accidental or unauthorized changes to the main branch
- Better collaboration through the PR review process
- Traceability of all changes through PR history

## Questions?

If you have questions about these rules or need help creating a Pull Request, please open an issue or contact @Roteus.
