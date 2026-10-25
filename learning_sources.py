"""Reading links and explanations; no database changes required."""

TOPIC_GUIDANCE = {1: {'title': 'Passwords and account protection',
     'why': 'We emphasize long, random, unique passwords and an extra sign-in check because each '
            'protects against a different way an account can be attacked.',
     'sources': [{'title': 'CISA: Strong passwords (PDF)',
                  'url': 'https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-Passwords-Tip-Sheet.pdf'},
                 {'title': 'CISA: Phishing-resistant MFA (PDF)',
                  'url': 'https://www.cisa.gov/sites/default/files/2023-01/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf'}]},
 2: {'title': 'Protecting personal information',
     'why': 'We encourage checking who is asking and why they need the information. A familiar '
            'logo or HTTPS connection alone does not establish that a request is trustworthy.',
     'sources': [{'title': 'FTC: Sharing and privacy online',
                  'url': 'https://consumer.ftc.gov/articles/heads-up'},
                 {'title': 'CISA: Recognize and report phishing (PDF)',
                  'url': 'https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-Phishing-Tip-Sheet.pdf'},
                 {'title': 'FTC: Online shopping',
                  'url': 'https://consumer.ftc.gov/articles/online-shopping'}]},
 3: {'title': 'Recognizing and responding to scams',
     'why': 'Urgency and unusual requests are reasons to pause and verify independently. Recovery '
            'steps depend on whether you exposed a password, downloaded software, or sent money.',
     'sources': [{'title': 'CISA: Recognize and report phishing (PDF)',
                  'url': 'https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-Phishing-Tip-Sheet.pdf'},
                 {'title': 'FTC: Recognize and avoid phishing',
                  'url': 'https://consumer.ftc.gov/articles/how-recognize-avoid-phishing-scams'},
                 {'title': 'FTC: What to do if you were scammed',
                  'url': 'https://consumer.ftc.gov/articles/what-do-if-you-were-scammed'}]},
 4: {'title': 'Safer browsing and downloads',
     'why': 'We recommend trusted downloads and prompt updates because software flaws can expose '
            'your device. HTTPS protects the connection but does not guarantee an honest seller.',
     'sources': [{'title': 'CISA: Software updates (PDF)',
                  'url': 'https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-Software-Updates-Tip-Sheet.pdf'},
                 {'title': 'FTC: Online shopping',
                  'url': 'https://consumer.ftc.gov/articles/online-shopping'},
                 {'title': 'FTC: Malware protection and removal',
                  'url': 'https://consumer.ftc.gov/articles/malware-how-protect-against-detect-and-remove-it'}]},
 5: {'title': 'Shopping and payments',
     'why': 'We encourage checking the seller and payment protections before buying. Payments to '
            'scammers can be difficult to reverse, but contacting your provider quickly may help.',
     'sources': [{'title': 'FTC: Online shopping',
                  'url': 'https://consumer.ftc.gov/articles/online-shopping'},
                 {'title': 'FTC: Buying from an online marketplace',
                  'url': 'https://consumer.ftc.gov/articles/buying-online-marketplace'},
                 {'title': 'FTC: What to do if you were scammed',
                  'url': 'https://consumer.ftc.gov/articles/what-do-if-you-were-scammed'}]},
 6: {'title': 'Sharing and connecting online',
     'why': 'Privacy settings and thoughtful sharing help you control who sees your information. '
            'Verify unusual requests from familiar accounts through another contact method.',
     'sources': [{'title': 'FTC: Sharing and privacy online',
                  'url': 'https://consumer.ftc.gov/articles/heads-up'},
                 {'title': 'CISA: Recognize and report phishing (PDF)',
                  'url': 'https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-Phishing-Tip-Sheet.pdf'}]}}

RESEARCH = [{'title': 'Anti-Phishing Phil',
  'citation': 'Sheng et al. · SOUPS · 2007',
  'finding': 'In this study, people who played a 15-minute educational game improved '
             'fraudulent-website identification more than participants in reading-based '
             'conditions.',
  'connection': 'Interactive practice can be a useful teaching approach. This older study '
                'evaluated a different game, not Wayfinder.',
  'url': 'https://kilthub.cmu.edu/articles/journal_contribution/Anti-Phishing_Phil_The_Design_and_Evaluation_of_a_Game_That_Teaches_People_Not_to_Fall_for_Phish/6621128/1'},
 {'title': 'Phish and Tips: Phishing Awareness and Education for Older Adults',
  'citation': 'Kazamia et al. · HAISA · 2024',
  'finding': 'In a simulated-inbox study with 37 participants, more than half demonstrated '
             'improved understanding of detection strategies and increased confidence.',
  'connection': 'Realistic practice is relevant to our simulations. This small study does not '
                'establish long-term protection or validate our app.',
  'url': 'https://openresearch.surrey.ac.uk/esploro/outputs/conferencePaper/Phish-and-Tips-Phishing-Awareness-and/99912166002346'},
 {'title': 'Categorizing Human Phishing Difficulty: A Phish Scale',
  'citation': 'Steves, Greene, and Theofanos · Journal of Cybersecurity · 2020',
  'finding': 'Phishing difficulty depends on warning signs and how closely the message fits the '
             'recipient’s situation. Click rates alone can misrepresent exercise difficulty.',
  'connection': 'Our scenarios provide context, such as whether you expect a delivery. A practice '
                'score is not a measure of your overall resistance to scams.',
  'url': 'https://csrc.nist.gov/pubs/journal/2020/09/categorizing-human-phishing-detection-difficulty-a/final'},
 {'title': 'Understanding the Efficacy of Phishing Training in Practice',
  'citation': 'Liu et al. · IEEE Symposium on Security and Privacy · 2025',
  'finding': 'An eight-month randomized study involving over 19,500 healthcare employees found '
             'limited benefits from the workplace training approaches examined.',
  'connection': 'Research findings are mixed. Training is only one part of safety, alongside '
                'independent verification, account protection, and software updates.',
  'url': 'https://www.sysnet.ucsd.edu/~voelker/pubs/phishtrain-oakland25.pdf'}]
