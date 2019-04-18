# goldenglobes
This project is a tool for extracting award ceremony information given a dataset of tweets related to that ceremony. This initial version focuses on the 2015 Golden Globes to try to determine:

1. Host(s) (for the entire ceremony)
2. Award Names
3. Presenters, mapped to award
4. Nominees, mapped to awards
5. Winners, mapped to awards

Information regarding the dataset:

Sample GG-related tweet:
[{u'id': 554402424728072192, u'text': u'just had to scramble to find a golden globes stream for my brother. :D', u'user': {u'id': 19904553, u'screen_name': u'baumbaTz'}, u'timestamp_ms': u'1421014813011'}, {"text": "What?!? https://t.co/NSPtGtbCvO", "id_str": "950142397194821632"}, ...
]

Tweets for 2015 were collected if they matched the query
track=['gg','golden globes', 'golden globe', 'goldenglobe','goldenglobes','gg2015','gg15','goldenglobe2015','goldenglobe15','goldenglobes2015','goldenglobes15','redcarpet','red carpet','redcarpet15','redcarpet2015','nominees','nominee','globesparty','globesparties' ]

See twitter api "track" parameter for details.
Tweets that are retweets have a text field that begins "RT"
Unicode characters (such as "\ud83d") are usually emoji or non-English letters.
