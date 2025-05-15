# Notify PR to Microsoft Teams

![License](https://img.shields.io/badge/license-Apache%202.0-blue)

This GitHub Action sends an Adaptive Card notification to a Microsoft Teams channel when a pull request is created or updated. It is designed to be used across multiple repositories and provides rich PR metadata, including author avatar, PR status, changed files, and commit count.

## 🚀 Features

- Sends a Microsoft Teams Adaptive Card
- Displays PR title, author, branch info, commit count, changed files
- Supports PR status badges (open, merged, closed)
- Easily reusable across repositories

## 📦 Usage

### Step 1: Add to Your Workflow

```yaml
- name: Compute added/removed lines for notification
  id: diff
  run: |
    PR_DATA=$(gh pr view "$PR_NUMBER" --json additions,deletions -q '.')
    ADDITIONS=$(echo "$PR_DATA" | jq '.additions')
    DELETIONS=$(echo "$PR_DATA" | jq '.deletions')
    echo "additions=$ADDITIONS" >> $GITHUB_OUTPUT
    echo "deletions=$DELETIONS" >> $GITHUB_OUTPUT
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
- name: Notify Microsoft Teams
  uses: your-org/notify-pr-teams-action@v1
  with:
    webhook_url: ${{ secrets.TEAMS_WEBHOOK_URL }}
    bot_image_url: https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png
    repo: ${{ github.repository }}
    pr_url: ${{ github.event.pull_request.html_url }}
    pr_title: ${{ github.event.pull_request.title }}
    pr_author: ${{ github.event.pull_request.user.login }}
    head_ref: ${{ github.event.pull_request.head.ref }}
    base_ref: ${{ github.event.pull_request.base.ref }}
    commits: ${{ github.event.pull_request.commits }}
    changed_files: ${{ github.event.pull_request.changed_files }}
    additions: ${{ steps.diff.outputs.additions }}
    deletions: ${{ steps.diff.outputs.deletions }}
    pr_number: ${{ github.event.pull_request.number }}
    pr_status: ${{ github.event.pull_request.state }}
    is_merged: ${{ github.event.pull_request.merged }}

