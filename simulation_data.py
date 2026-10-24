SCENARIOS = {
    "bank-alert": {
        "subject": "Action required: Your account is on hold",
        "sender_name": "Harbor Bank Support",
        "sender_address": "support@harborbank-alerts.com",
        "avatar": "H",
        "paragraphs": [
            "Hello,",
            "We detected unusual activity on your account and "
            "temporarily restricted your access.",
            "You must verify your account within 24 hours to "
            "prevent further restrictions.",
        ],
        "link_text": "Verify my account",
        "closing": (
            "For your security, please complete verification "
            "before contacting support."
        ),
        "choices": {
            "follow": {
                "label": "Follow the email’s link",
                "points": 0,
                "feedback": (
                    "This link could lead to a fake banking website. "
                    "Open your bank’s app yourself or call the "
                    "number on your card."
                ),
            },
            "report": {
                "label": "Report as scam",
                "points": 10,
                "feedback": (
                    "You avoided the suspicious link and flagged "
                    "the message. The deadline and pressure to avoid "
                    "support were warning signs."
                ),
            },
            "contact": {
                "label": "Contact the bank independently",
                "points": 10,
                "feedback": (
                    "You chose to check through a trusted channel. "
                    "Use your bank’s app or the number on your card."
                ),
            },
        },
    },
}