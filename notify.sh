#!/bin/bash
# This script sends a notification to a Microsoft Teams channel when a pull request is created or updated.
# It uses the Microsoft Teams webhook URL provided as an environment variable.

AUTHOR_AVATAR_URL=$(curl -s https://api.github.com/users/$PR_AUTHOR | jq -r .avatar_url)

if [[ "$IS_MERGED" == "true" ]]; then
  BADGE_TEXT="Merged"
  BADGE_STYLE="Accent"
elif [[ "$PR_STATUS" == "closed" ]]; then
  BADGE_TEXT="Closed"
  BADGE_STYLE="Attention"
else
  BADGE_TEXT="Opened"
  BADGE_STYLE="Good"
fi

cat <<EOF > payload.json
{
   "type":"message",
   "attachments":[
      {
         "contentType":"application/vnd.microsoft.card.adaptive",
         "content":{
            "\$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
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
                                    "url": "${BOT_IMAGE_URL}",
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
                                    "wrap": true
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "**${REPO}**",
                                    "wrap": true,
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
                                    "text": "${BADGE_TEXT}",
                                    "size": "Large",
                                    "style": "${BADGE_STYLE}",
                                    "shape": "Rounded",
                                    "appearance": "Tint"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "TextBlock",
                    "text": "#${PR_NUMBER} - ${PR_TITLE}",
                    "wrap": true,
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
                                    "url": "${AUTHOR_AVATAR_URL}",
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
                                    "text": "**${PR_AUTHOR}** wants to merge **${COMMITS}** commits",
                                    "size": "Large",
                                    "wrap": true,
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
                                    "text": "**Head:** ${HEAD_REF}",
                                    "wrap": true,
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "**Base:** ${BASE_REF}",
                                    "wrap": true,
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "**Files:** ${CHANGED_FILES}",
                                    "wrap": true,
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "**Changes**: 🟢 +${ADDITIONS} / 🔴 -${DELETIONS}",
                                    "wrap": true,
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
                    "url": "${PR_URL}"
                }
            ],
            "msTeams": {
                "width": "full"
            }
        }
      }
   ]
}
EOF
cat payload.json
curl -H "Content-Type: application/json" -d @payload.json "$WEBHOOK_URL"
        
