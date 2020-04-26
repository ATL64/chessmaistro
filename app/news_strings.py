# The player either had matches the day before or not, and we compare the difference in elo between
# yesterday and the last day the user played.


##############
### Title ####
##############

# No games played
titles_0 = ['{username} enjoying vacation',
            '{username} takes a rest',
            'We miss you, {username}',
            '\"Party first, chess second\", says {username}',
            '{username}\'s retirement rumours grow ']

# +40 elo points
titles_a = ['Stellar performance by {username}',
            'Magical {username}',
            '\"The machine\" {username}',
            '{username} goes to the moon',
            '{username} climbs {pts_diff_day_before} points!']

# 15 to 40 elo points
titles_b = ['{username} keeps going',
            'Good day for {username}',
            'Steady improvement by master {username}',
            '{username} does his thing',
            '{username} fulfilling high expectations']

# -15 to 15 elo points
titles_c = ['\"Just another day at the chess office\", says GM {username}',
            'Stable in the rating charts',
            'Calm waters in planet {username}',
            'Chill in the comfort zone'
            ]

# -15 to -40 elo points
titles_d = ['{username} loses {diff_rating} points',
            '{username} sliding down',
            'Ouch, {username} lost focus',
            '{username} in slow decline',
            '{username} hangs out with Mr. Blunder']

# more than -40 elo points
titles_e = ['{username} in crisis',
            'Disaster day for {username}',
            'Is this the end of {username}?',
            '{username} brain meltdown as he loses {diff_rating} points',
            '{username}\'s poor performance tied to drug abuse']


###############
##Sentence 1 ##
###############

# No games played
sen_1_0 = ['Not much action in the chess Arena yesterday, as {username} enjoys vacations in his luxury mansion'
            'in the Amalfi coast in Italy.  Every great mind needs inspiration, but the fans are calling for '
            'more activity as they have become addicted to the show.',
           'Can life be more boring than the days when {username} does not play chess?  Fans and experts'
           'have to retreat into their own mediocre chess matches, awaiting for the master\'s return.  ',
           'The question now is: when will the Jedi return?']

# +40 elo points
sen_1_a = ['There are those days when {username} can win 8 games in a row, or humiliate an opponent '
            'mid-demolition with a novelty move but even when he does not grind the other side into the dust, '
            'it still feels that ultimately {username} inhabits a different planet to lesser mortals. ',
           'Magic, style, killer instincts.  What else can we ask from a chess player? We are fortunate to live in this'
           ' era of extraordinary chess, and {username} is the one who started the revolution. After the revolution '
           'comes the tyranny, and this is how the opponents felt yesterday: tyrannized. ',
           'The world of chess is still rubbing its eyes after yesterday\'s display of quality from grandmaster'
           '{username}.  What seemed like a dream for the spectator, was really a nightmare for the opponents. '
           'Millions of people gathered at the world\'s biggest capitals to celebrate the victory. ',
           'The batman of chess is back, and no one\'s safe anymore. Even the Joker was sad while {username} '
           'kept all the laughing to himself. BAM went the bishop, WHAM went the dark knight, POW went the queen.  '
           'Chess was a boxing ring yesterday and only one player remained intact.'
           ]

# 15 to 40 elo points
sen_1_b = ['No big fireworks yesterday at the chess factory, but even in the dullest of days, {username} can'
            ' manage to cash in a bag of points for the rating.  Going up the ladder is tough business and these kind of'
            ' days make a big difference.  Small improvements in the rating add up in the long run.',
           'Moving up is never easy, but chess superstar {username} has an elevator that keeps going towards the skies'
           '.  Grinding the opponents down methodically is how you make the elo balance in your favor.'
           'And yesterday was no exception, as most opponents could not cope with the masterful gambits.',
           'The ship sails forward in the sea of the unknown, and the captain of the enterprise has a name:'
           ' {username}.  We have seen nervous opponents yesterday, blundering their pieces left and right, most likely'
           ' due to the sheer pressure of facing one of the most brilliant players of all time .',
           'Autopilot is all he needs in days like this.  Like a sophisticated jet plane, {username} cruises through'
           ' the sky, gradually gaining altitude.  In some cases, the opponents seemed like birds trying to catch up'
           ' to the airplane that just took off.',
           ]

# -15 to 15 elo points
sen_1_c = ['Not much movement today in the rankings, but {username} had to put some effort to maintain a competitive '
            'level.   '
            'it still feels that ultimately {username} inhabits a different planet to lesser mortals. ',
           'Magic, style, killer instincts.  What else can we ask from a chess player? We are fortunate to live in this'
           'era of extraordinary chess, and {username} is the one who started the revolution. After the revolution'
           'comes the tyranny, and this is how the opponents felt yesterday: tyrannized. ',
           'The world of chess is still rubbing its eyes after yesterday\'s display of quality from grandmaster'
           '{username}.  What seemed like a dream for the spectator, was really a nightmare for the opponents. '
           'Millions of people gathered at the world\'s biggest capitals to celebrate the victory. ',
           'The batman of chess is back, and no one\'s safe anymore. Even the Joker was sad while {username} '
           'kept all the laughing to himself. BAM went the bishop, WHAM went the dark knight, POW went the queen.  '
           'Chess was a boxing ring yesterday and only one player remained intact.',
           ]

sen_1_d = ['There are those days when {username} can win 8 games in a row, or humiliate an opponent '
            'mid-demolition with a novelty move but even when he does not grind the other side into the dust, '
            'it still feels that ultimately {username} inhabits a different planet to lesser mortals. ',
           'Magic, style, killer instincts.  What else can we ask from a chess player? We are fortunate to live in this'
           'era of extraordinary chess, and {username} is the one who started the revolution. After the revolution'
           'comes the tyranny, and this is how the opponents felt yesterday: tyrannized. ',
           'The world of chess is still rubbing its eyes after yesterday\'s display of quality from grandmaster'
           '{username}.  What seemed like a dream for the spectator, was really a nightmare for the opponents. '
           'Millions of people gathered at the world\'s biggest capitals to celebrate the victory. ',
           'The batman of chess is back, and no one\'s safe anymore. Even the Joker was sad while {username} '
           'kept all the laughing to himself. BAM went the bishop, WHAM went the dark knight, POW went the queen.  '
           'Chess was a boxing ring yesterday and only one player remained intact.',
           ]

sen_1_e = ['There are those days when {username} can win 8 games in a row, or humiliate an opponent '
            'mid-demolition with a novelty move but even when he does not grind the other side into the dust, '
            'it still feels that ultimately {username} inhabits a different planet to lesser mortals. ',
           'Magic, style, killer instincts.  What else can we ask from a chess player? We are fortunate to live in this'
           'era of extraordinary chess, and {username} is the one who started the revolution. After the revolution'
           'comes the tyranny, and this is how the opponents felt yesterday: tyrannized. ',
           'The world of chess is still rubbing its eyes after yesterday\'s display of quality from grandmaster'
           '{username}.  What seemed like a dream for the spectator, was really a nightmare for the opponents. '
           'Millions of people gathered at the world\'s biggest capitals to celebrate the victory. ',
           'The batman of chess is back, and no one\'s safe anymore. Even the Joker was sad while {username} '
           'kept all the laughing to himself. BAM went the bishop, WHAM went the dark knight, POW went the queen.  '
           'Chess was a boxing ring yesterday and only one player remained intact.',
           ]
