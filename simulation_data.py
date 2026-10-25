SCENARIOS = {
    "bank-alert": {
        "sources": [{"title": "CISA: Recognize and report phishing", "url": "https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-Phishing-Tip-Sheet.pdf"}],
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
        "closing": (
            "For your security, please complete verification "
            "before contacting support."
        ),
        "interactions": {
            "verify-account": {
                "label": "Verify my account",
                "feedback": [
                    "This could lead to a fake banking website.",
                    "Open your bank’s app yourself to check the alert.",
                ],
            },
        },
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
    "delivery-fee": {
        "sources": [{"title": "FTC: Fake shipping notifications", "url": "https://consumer.ftc.gov/consumer-alerts/2023/12/fake-shipping-notification-emails-text-messages-what-you-need-know-holiday-season"}],
        "subject": "Delivery paused: $1.25 fee needed today",
        "sender_name": "QuickShip Delivery",
        "sender_address": "support@quickship-alerts.example",
        "avatar": "Q",
        "paragraphs": [
            "Hello,",
            "We could not deliver your package because your address needs to be confirmed. "
            "Pay a $1.25 redelivery fee by 8 p.m. today or your package will be returned.",
        ],
        "closing": "QuickShip Delivery Team",
        "interactions": {
            "pay-delivery-fee": {
                "label": "Confirm your address and pay",
                "feedback": [
                    "The displayed destination is https://quickship-fee.example/confirm. "
                    "This practice link stays inside the simulation.",
                    "Entering your address and card details on a fake delivery page could expose "
                    "personal and payment information. Check through the store or delivery app you already use.",
                ],
            },
        },
        "choices": {
            "check-order": {
                "label": "Check the order through the store or delivery app I already use",
                "points": 10,
                "feedback": "This lets you check the package without trusting the email’s link. "
                            "If you weren’t expecting a package, there may be nothing to check.",
            },
            "report": {
                "label": "Report the message as phishing or spam, then delete it",
                "points": 10,
                "feedback": "Reporting can help your email service catch similar messages. "
                            "If you are expecting a package, check its status through a trusted route first.",
            },
            "pay": {
                "label": "Follow the link and enter my address and card details to pay",
                "points": 0,
                "feedback": "The link could lead to a fake page that steals your personal or payment information.",
            },
        },
        "clues": "The small fee, deadline, and request to update delivery details are reasons to check "
                 "independently. Those clues do not prove a message is fake by themselves.",
    },
    "tech-support": {
        "sources": [{"title": "FTC: Tech support scams", "url": "https://consumer.ftc.gov/articles/how-spot-avoid-and-report-tech-support-scams"}],
        "type": "popup",
        "context": "While browsing a website, this warning suddenly appears. You did not open your security software.",
        "decision_prompt": "How would you handle this browser warning?",
        "subject": "URGENT: Viruses found — call now",
        "sender_name": "BrightShield Device Support",
        "sender_address": "alerts@brightshield-warning.example",
        "avatar": "B",
        "paragraphs": [
            "Security notice: We found 7 dangerous viruses on your computer. "
            "Your files may be locked in 10 minutes.",
            "Call our support team now at 555-0105. Do not close this message or shut down your computer.",
        ],
        "closing": "BrightShield Security Team",
        "interactions": {
            "call-support": {
                "label": "Call support: 555-0105 (simulated)",
                "feedback": [
                    "No call was placed. In this scenario, the number connects to the scammer.",
                    "They could ask you to install software or grant remote access. "
                    "Use security software you already trust or contact support through a website you know is genuine; search ads may show fake support numbers.",
                ],
            },
            "download-tool": {
                "label": "Download repair tool",
                "feedback": [
                    "Nothing was downloaded. A repair tool offered by an unexpected warning could be unsafe.",
                    "Use security software already installed on your device or find help through a trusted source.",
                ],
            },
            "close-warning": {
                "label": "Close the warning",
                "dismiss": True,
                "feedback": [
                    "You closed the simulated warning without calling or downloading anything.",
                    "In a real browser, use the browser’s own tab-close control rather than buttons supplied "
                    "by a suspicious page. If concerned, check with security software you already trust.",
                ],
            },
        },
        "choices": {
            "close-and-scan": {
                "label": "Close the warning and scan with security software already on my device",
                "points": 10,
                "feedback": "A warning that pressures you to call is suspicious. Running a scan through "
                            "software you already trust, after updating it, is a safer way to check for a problem.",
            },
            "trusted-help": {
                "label": "Ask someone I trust or contact official support using known contact details",
                "points": 10,
                "feedback": "This gives you a way to check the warning without relying on its phone number.",
            },
            "grant-access": {
                "label": "Call the number and follow instructions to install software or grant access",
                "points": 0,
                "feedback": "A scammer could use remote access to view information on your device "
                            "or charge you for a problem that does not exist.",
            },
        },
        "clues": "The message creates fear and a short deadline, tells you not to close it, "
                 "and directs you to its own phone number. Check the claim through a trusted channel.",
    },
    "library-notice": {
        "sources": [{"title": "CISA: Recognize and report phishing", "url": "https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-Phishing-Tip-Sheet.pdf"}],
        "context": "You requested The Secret Garden from Maple Street Library and chose to receive email notices.",
        "subject": "Your library hold is ready",
        "sender_name": "Maple Street Library",
        "sender_address": "holds@maplestreetlibrary.example",
        "avatar": "M",
        "paragraphs": [
            "Hello, Maya,",
            "The book you requested, The Secret Garden, is ready for pickup at Maple Street Library. "
            "Please collect it by November 2 and bring your library card.",
        ],
        "closing": "No reply is needed. If you have questions, contact the library "
                   "using the phone number on your library card.",
        "interactions": {},
        "choices": {
            "collect": {
                "label": "Go to the library and collect the book with my library card",
                "points": 10,
                "feedback": "This matches a request you made, and the message does not ask you "
                            "to pay or share private information.",
            },
            "check-hold": {
                "label": "Check my hold through the library app or call the number on my library card",
                "points": 10,
                "feedback": "This confirms the notice through a route you trust. "
                            "It is a good choice if you are unsure about the email.",
            },
            "report": {
                "label": "Report and delete it immediately just because it arrived by email",
                "points": 0,
                "feedback": "You avoid interacting with the message, but may miss a book you requested. "
                            "Email can carry legitimate notices too. Use the context and verify if uncertain.",
            },
        },
        "clues": "You requested this specific book and opted into notices. The email names the pickup "
                 "location, asks for no payment or login, and suggests a contact method you already have. "
                 "An email address alone cannot prove who sent a message.",
    },
    "family-emergency": {
        "type": "sms",
        "subject": "A family member needs help",
        "context": "An unfamiliar number texts you, claiming to be your adult child. You have their usual number saved.",
        "sender_name": "Unknown number",
        "sender_detail": "Not in your contacts",
        "avatar": "?",
        "decision_prompt": "How would you respond to this text?",
        "messages": [
            {"from": "them", "text": "Hi, it’s me. My phone broke, so I’m borrowing this number."},
            {"from": "them", "text": "I’m stuck and need $200 right now. Please buy gift cards and send photos of the codes."},
            {"from": "them", "text": "Please don’t call or tell anyone. I’m embarrassed and need this sorted quickly."},
        ],
        "interactions": {
            "send-codes": {
                "label": "Send gift-card codes (simulate)",
                "feedback": [
                    "No codes were sent. Sharing gift-card codes could let someone spend the balance.",
                    "A claim about a broken phone does not establish identity. Contact your family member using the number you already have.",
                ],
            },
            "call-saved-number": {
                "label": "Call their saved number (simulate)",
                "feedback": [
                    "In this scenario, your family member answers and says they did not send the request. No real call was placed.",
                    "You checked independently instead of trusting the new number.",
                ],
            },
        },
        "choices": {
            "send": {"label": "Send the codes quickly because it sounds urgent", "points": 0,
                     "feedback": "Urgency is not proof of identity. Gift-card codes can give a scammer access to the money."},
            "verify": {"label": "Call my family member using their saved number", "points": 10,
                       "feedback": "A contact method you already know helps you check whether the request is really theirs."},
            "ask-family": {"label": "Pause and ask another trusted family member to help verify", "points": 10,
                           "feedback": "A second trusted person can help check the story before you send money. You do not have to keep the request secret."},
        },
        "clues": "An unfamiliar number, urgency, secrecy, and a request for gift-card codes all give you reasons to stop and verify.",
        "sources": [{"title": "FTC: Fake emergency scams", "url": "https://consumer.ftc.gov/articles/scammers-use-fake-emergencies-steal-your-money"}],
    },
    "marketplace-payment": {
        "type": "chat",
        "subject": "A bargain with a payment shortcut",
        "context": "You are buying a used tablet through a marketplace that offers its own checkout. You have not paid yet.",
        "platform": "MarketSquare · Buyer chat",
        "sender_name": "Taylor · Seller",
        "sender_detail": "Listing: Used tablet · $120",
        "avatar": "T",
        "decision_prompt": "What would you do before paying?",
        "messages": [
            {"from": "you", "text": "Hi! Is the tablet still available? Can I use the marketplace checkout?"},
            {"from": "them", "text": "Yes! I can ship today. Checkout is broken, though. Send $120 to my payment-app account instead."},
            {"from": "them", "text": "Mark it as a payment to friends. That avoids the fees. Someone else wants it, so pay in the next 10 minutes."},
        ],
        "interactions": {
            "pay-outside": {
                "label": "Use the seller’s payment shortcut (simulate)",
                "feedback": [
                    "No money moved. Moving payment outside the marketplace can mean losing its purchase protections.",
                    "A claim that checkout is broken is a reason to check with the platform, not to rush payment.",
                ],
            },
            "open-platform-help": {
                "label": "Check marketplace help (simulate)",
                "feedback": [
                    "This fictional marketplace says its purchase protection requires its own checkout and has eligibility limits.",
                    "In real marketplaces, read the applicable protections and exclusions before buying.",
                ],
            },
        },
        "choices": {
            "platform": {"label": "Use the marketplace checkout after checking its purchase protections", "points": 10,
                         "feedback": "Keeping payment within the platform avoids the seller’s shortcut. Check coverage; it is not a guarantee against every problem."},
            "shortcut": {"label": "Send the money as a friends payment before someone else buys it", "points": 0,
                         "feedback": "You would be trusting the seller’s claim and may lose purchase protections by paying outside the platform."},
            "walk-away": {"label": "Decline the deal and report the suspicious payment request", "points": 10,
                          "feedback": "You can walk away from a purchase when the seller pressures you to bypass the platform."},
        },
        "clues": "The seller wants to bypass checkout, classify a purchase as a friends payment, and hurry you with another buyer.",
        "sources": [{"title": "FTC: Buying from an online marketplace", "url": "https://consumer.ftc.gov/articles/buying-online-marketplace"}],
    },
    "social-prize": {
        "type": "chat",
        "subject": "You have won a prize!",
        "context": "You follow a travel page on social media but did not enter a prize draw. A different account sends you this message.",
        "platform": "SocialCircle · Message request",
        "sender_name": "Suntrail Rewards Team",
        "sender_detail": "@suntrail-prize-help · Not an account you follow",
        "avatar": "S",
        "decision_prompt": "How would you handle this prize message?",
        "messages": [
            {"from": "them", "text": "Congratulations! You were selected for a free weekend getaway from Suntrail Travel."},
            {"from": "them", "text": "Pay a $35 processing fee to release your prize. We need your card details today."},
            {"from": "them", "text": "Claim it at suntrail-prize.example/claim. Keep this message private so nobody takes your spot!"},
        ],
        "interactions": {
            "claim-prize": {
                "label": "Claim the prize (simulate)",
                "feedback": [
                    "No site opened and no payment was made. A prize message that asks you to pay to receive the prize is a scam warning.",
                    "Do not provide card details to release a supposed free prize.",
                ],
            },
            "inspect-profile": {
                "label": "Inspect the sender profile",
                "feedback": [
                    "The handle is @suntrail-prize-help, not the travel page you follow. A familiar name or copied image does not prove who sent a message.",
                    "Check through the organization’s known website or established account rather than links from this sender.",
                ],
            },
        },
        "choices": {
            "report": {"label": "Report and block the account without paying", "points": 10,
                       "feedback": "You avoided the fee and flagged the account. Having to pay to receive a prize is a strong warning sign."},
            "pay-fee": {"label": "Pay the small fee to receive the free trip", "points": 0,
                        "feedback": "A small fee can still be a scam. You could lose the payment and expose your card information."},
            "verify": {"label": "Check independently with the travel company before responding", "points": 10,
                       "feedback": "Use a website or contact method you know belongs to the company. Do not use the message’s link or send money."},
        },
        "clues": "You did not enter a draw. A different account asks for payment and card details, adds a deadline, and requests secrecy.",
        "sources": [{"title": "FTC: Fake prize scams", "url": "https://consumer.ftc.gov/articles/fake-prize-sweepstakes-and-lottery-scams"}],
    },
    "appointment-reminder": {
        "sources": [{"title": "CISA: Recognize and report phishing", "url": "https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-Phishing-Tip-Sheet.pdf"}],
        "type": "sms",
        "subject": "Your appointment reminder",
        "context": "You booked a haircut at Willow Salon for tomorrow at 2 p.m. and opted into text reminders. It is also in your calendar.",
        "sender_name": "Willow Salon",
        "sender_detail": "Appointment reminder",
        "avatar": "W",
        "decision_prompt": "What is a reasonable response to this reminder?",
        "messages": [
            {"from": "them", "text": "Hi Jordan, a reminder that your haircut at Willow Salon is tomorrow at 2 p.m."},
            {"from": "them", "text": "No reply or payment is needed. If you need to change the booking, use the contact details on your booking confirmation."},
        ],
        "interactions": {
            "check-calendar": {
                "label": "Check my calendar (simulate)",
                "feedback": [
                    "Your fictional calendar shows Willow Salon, tomorrow at 2 p.m. This matches the booking you made.",
                    "The context supports the reminder. A sender name alone would not prove it is genuine.",
                ],
            },
        },
        "choices": {
            "report": {"label": "Report it as a scam only because it is a text message", "points": 0,
                       "feedback": "Text messages can be legitimate. This reminder matches a booking you made and asks for no payment or private information."},
            "attend": {"label": "Keep my planned appointment; no reply is needed", "points": 10,
                       "feedback": "That fits the booking you made. You do not need to send information or money in response."},
            "confirm": {"label": "If unsure, contact the salon using my original booking confirmation", "points": 10,
                       "feedback": "Using contact details you already have lets you verify independently instead of relying on the text’s display name."},
        },
        "clues": "The time matches your calendar, you opted into reminders, and the text asks for neither payment nor sensitive information.",
    },
}
