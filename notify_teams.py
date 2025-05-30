#!/usr/bin/env python3

import os
import json
import requests
from typing import Dict, Any

def get_author_avatar(author: str) -> str:
    """Get the avatar URL for a GitHub user."""
    response = requests.get(f"https://api.github.com/users/{author}")
    response.raise_for_status()
    return response.json()["avatar_url"]

def get_badge_info(is_merged: str, pr_status: str) -> tuple[str, str]:
    """Get badge text and style based on PR status."""
    if is_merged.lower() == "true":
        return "Merged", "Accent"
    elif pr_status.lower() == "closed":
        return "Closed", "Attention"
    return "Opened", "Good"

def create_adaptive_card(
    bot_image_url: str,
    repo: str,
    pr_number: str,
    pr_title: str,
    pr_author: str,
    author_avatar_url: str,
    commits: str,
    head_ref: str,
    base_ref: str,
    changed_files: str,
    additions: str,
    deletions: str,
    pr_url: str,
    badge_text: str,
    badge_style: str,
) -> Dict[str, Any]:
    """Create the adaptive card JSON payload."""
    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                    "speak": "New pull request opened",
                    "type": "AdaptiveCard",
                    "version": "1.5",
                    "body": [
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "Image",
                                            "url": bot_image_url,
                                            "size": "Medium",
                                            "style": "RoundedCorners"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "**Pull Request Notifier**",
                                            "wrap": True
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"**{repo}**",
                                            "wrap": True,
                                            "color": "Good"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "Badge",
                                            "text": badge_text,
                                            "size": "Large",
                                            "style": badge_style,
                                            "shape": "Rounded",
                                            "appearance": "Tint"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "TextBlock",
                            "text": f"#{pr_number} - {pr_title}",
                            "wrap": True,
                            "size": "ExtraLarge",
                            "weight": "Bolder",
                            "color": "Accent"
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "Image",
                                            "url": author_avatar_url,
                                            "size": "Small",
                                            "style": "Person"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": f"**{pr_author}** wants to merge **{commits}** commits",
                                            "size": "Large",
                                            "wrap": True,
                                            "spacing": "Small"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": f"**Head:** {head_ref}",
                                            "wrap": True,
                                            "spacing": "Small"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"**Base:** {base_ref}",
                                            "wrap": True,
                                            "spacing": "Small"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"**Files:** {changed_files}",
                                            "wrap": True,
                                            "spacing": "Small"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"**Changes**: 🟢 +{additions} / 🔴 -{deletions}",
                                            "wrap": True,
                                            "spacing": "Small"
                                        }
                                    ],
                                    "verticalContentAlignment": "Center"
                                }
                            ]
                        }
                    ],
                    "msteams": {
                        "width": "full"
                    },
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "View pull request",
                            "url": pr_url
                        }
                    ],
                    "msTeams": {
                        "width": "full"
                    }
                }
            }
        ]
    }

def main():
    # Get environment variables
    webhook_url = os.environ["WEBHOOK_URL"]
    bot_image_url = os.environ["BOT_IMAGE_URL"]
    repo = os.environ["REPO"]
    pr_url = os.environ["PR_URL"]
    pr_title = os.environ["PR_TITLE"]
    pr_author = os.environ["PR_AUTHOR"]
    head_ref = os.environ["HEAD_REF"]
    base_ref = os.environ["BASE_REF"]
    commits = os.environ["COMMITS"]
    changed_files = os.environ["CHANGED_FILES"]
    additions = os.environ["ADDITIONS"]
    deletions = os.environ["DELETIONS"]
    pr_number = os.environ["PR_NUMBER"]
    pr_status = os.environ["PR_STATUS"]
    is_merged = os.environ["IS_MERGED"]

    # Get author avatar
    author_avatar_url = get_author_avatar(pr_author)

    # Get badge info
    badge_text, badge_style = get_badge_info(is_merged, pr_status)

    # Create payload
    payload = create_adaptive_card(
        bot_image_url=bot_image_url,
        repo=repo,
        pr_number=pr_number,
        pr_title=pr_title,
        pr_author=pr_author,
        author_avatar_url=author_avatar_url,
        commits=commits,
        head_ref=head_ref,
        base_ref=base_ref,
        changed_files=changed_files,
        additions=additions,
        deletions=deletions,
        pr_url=pr_url,
        badge_text=badge_text,
        badge_style=badge_style,
    )

    # Print payload for debugging
    print(json.dumps(payload, indent=2))

    # Send to Teams
    response = requests.post(
        webhook_url,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()

if __name__ == "__main__":
    main() 