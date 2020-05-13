# The player either had matches the day before or not, and we compare the difference in elo between
# yesterday and the last day the user played.


##############
### Images ####
##############

# No games played
images_0 = ['no_games.jpeg']

# +40 elo points
images_a = ['great_image_1.jpeg', 'great_image_2.jpg', 'great_image_3.jpg', 'great_image_4.jpg', 'great_image_5.jpg']

# 15 to 40 elo points
images_b = ['good_image_1.gif', 'good_image_2.jpg', 'good_image_3.jpeg', 'good_image_4.jpg', 'good_image_5.jpg']

# -15 to 15 elo points
images_c = ['calm_image_1.jpg', 'calm_image_2.jpg', 'calm_image_3.jpg', 'calm_image_4.jpg', 'calm_image_5.jpg']

# -15 to -40 elo points
images_d = ['bad_image_1.jpg', 'bad_image_2.jpg', 'bad_image_3.jpg', 'bad_image_4.jpg', 'bad_image_5.jpeg']

# more than -40 elo points
images_e = ['crisis_image_1.jpg', 'crisis_image_2.jpg', 'crisis_image_3.jpg', 'crisis_image_4.jpg', 'crisis_image_5.jpg']


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
            '{username} climbs {diff_rating} points!']

# 15 to 40 elo points
titles_b = ['Grandmaster {username} keeps going',
            'Good day for grandmaster {username}',
            'Steady improvement by master {username}',
            'Grandmaster {username} does his thing',
            'Master {username} fulfilling high expectations']

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
           'have to retreat into their own mediocre chess matches, awaiting for the master\'s comeback.  ',
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
           '.  Grinding the opponents down methodically is how you make the ELO balance in your favor. '
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
            'level.  With decent chess, those dark old days of week-long parties seem forgotten, and the results are '
            'there to prove it.  Playing the game is a routine, and the chess professor was on schedule yesterday.',
           'When he doesn\'t find the perfect move, {username} still seems to pull off his chess compass and play '
           'a solid defense, making life hard for the opponent.  However, the fans want to see more risky play, and '
           'find out how high can this superstar player fly.',
           'After appearing in Forbes as the 8th most highest paid celebrity in the world, yesterday was another '
           'day at the chess laboratory for {username}.  Like a mechanical turk, the grandmaster played with good '
           'technique, but ultimately no sparks of that persistence that makes him climb the charts.',
           'The audience has been yawning yesterday, dreaming of those days where excitement was the daily menu.  '
           'As the servers of chess.com were at full capacity, the rating of {username} did not move much, and maybe '
           ' that\'s a good thing, maintaining this level of chess is not an easy feat. ',
           ]

# -15 to -40 elo points
sen_1_d = ['Alarms went off yesterday at the {username} headquarters.  Counterattacks are his hallmark, but if you get '
            'distracted in the middle in this circuit of players, your chances of winning go down significantly. '
            'It was not a disaster, but the fans were disappointed with the performance yesterday.',
           'That feeling of preparing the popcorn, only to watch a terrible movie, we have all been there.  And '
           'yesterday, all chess fans of superstar {username} had this exact same feeling.  Like a rock sinking in the '
           ' water, the rating went down, and some signs of desperation were visible in the best player of the last decade.',
           'Blunders are like flowers that grow in {username}\'s garden after a truck of fertilizer is poured in.  '
           'Except they ain\'t beautiful, nor they smell any good.  It could have been worse, but some sparks of the '
           'superstar\'s brilliance avoided the disaster.  Terrain has been lost, and will not be easy to recover',
           'Once nicknamed the emperor of chess, it seems that the empire has turned against the ruling tyrant, '
           'showing little to no respect for the master\'s skills.  One match after the other, one blunder after the '
           'other, it is only due to some luck that the day was not a complete disaster',
           ]

# more than -40 elo points
sen_1_e = ['The tsunami has hit hard on {username}\'s coast.  One wave after the other, opponents humiliated the player'
            ' we once called the Elvis of chess.  The rumours say that he has been infected with the coronavirus, '
            'herpes and HIV simultaneously after visiting a shady brothel in the outskirts of the city, abusing low '
           'quality drugs, hence his low performance.',
           'What is wrong with {username}?  Is it the drug addictions that have returned after all this time?  Is it '
           'the media pressure after having been found out having an affair? Or perhaps '
           'the photographs found of him kissing a homeless man drinking cheap wine?',
           'The blunder man, the bad opening guy, the \"oh, I had bad connection\" excuse.  This all found place in a '
           'single individual yesterday: {username}.  The level of chess displayed was distasteful, and we all want '
           'our money back sir.  And disinfect the money you give us please, in case it\'s contagious.',
           'No, it was not a horror movie, nor was it a bad dream you had last night.  It really happened, and it was '
           'awful.  The best player of the decade has collapsed, one defeat after the next {username} kept on playing '
           'trying to recover the lost ground, but to no avail as his mediocre play led the path for a rough patch',
           ]

###############
##Sentence 2 ##
###############

# How many rating points were won/lost
# nr of matches won and lost last day
# diff_rating, abs_diff_rating, matches_won, matches_drawn, matches_lost
# if no matches: current rating + date of last play, highest rating + date of that.
# rating_last_play, date_last_play
# can also use max_yesterday and max_day_before

# No games played
sen_2_0 = ['The last time we saw {username} on the board was on {date_last_play}, achieving a maximum elo of '
            '{rating_last_play}. Who knows what the future holds. ',
           'If this is the last we see of {username}, he leaves us with a rating of {rating_last_play} on '
           '{date_last_play}']

sen_2_record = ['Achieving an all-time-high of {max_yesterday} points, the master broke his own record.  Fantastic '
                'day for {username}, having played {matches_played_y} matches, with a tally of {matches_won_y} victories, '
                '{matches_lost_y} defeats, and {matches_drawn_y} draws. This equates to a net gain of {abs_diff_rating}'
                'points, and a new record.']

# +40 elo points
sen_2_a = ['Climbing to a rating of {max_yesterday} points, we witnessed a fantastic display of how to play the game of'
            ' chess by the leyend we know as {username}.  In total we saw {matches_played_y} matches, of which '
           '{matches_won_y} resulted in victories, {matches_lost_y} were defeats, and {matches_drawn_y} ended in draw. '
           'An impressive rating climb of {abs_diff_rating} points'
           ]

# 15 to 40 elo points
sen_2_b = ['Showing some solid chess, yesterday {username} increased rating by {abs_diff_rating} points.  Currently at '
           '{max_yesterday} points in the ranking, {matches_won_y} matches won yesterday out of a total of '
           '{matches_played_y} games.  The other ones resulted in {matches_lost_y} defeats and {matches_drawn_y} draws.'
           ]

# -15 to 15 elo points
sen_2_c = ['Let\'s dive into the stats.  Currently at '
           '{max_yesterday} points in the ranking, {matches_won_y} matches won yesterday out of a total of '
           '{matches_played_y} games.  The other ones resulted in {matches_lost_y} defeats and {matches_drawn_y} draws.'
           ]

# -15 to -40 elo points
sen_2_d = ['Not a good day for {username} yesterday, losing a total of {abs_diff_rating} points.  Currently at '
           '{max_yesterday} points in the ranking, {matches_won_y} matches won yesterday out of a total of '
           '{matches_played_y} games.  The other ones resulted in {matches_lost_y} defeats and {matches_drawn_y} draws.'
           ]

# more than -40 elo points
sen_2_e = ['Sinking to a rating of {max_yesterday} points, we witnessed a poor display of how to play the game of'
            ' chess by the leyend we know as {username}.  In total we saw {matches_played_y} matches, of which '
           '{matches_won_y} resulted in victories, {matches_lost_y} were defeats, and {matches_drawn_y} ended in draw. '
           'An total crash resulting in the loss of {abs_diff_rating} points'
           ]




###############
##Sentence 3: quote ##
###############



# No games played
sen_3_0 = [' \" What am I supposed to do during the quarantine if my favourite player is offline?\" said Magnus Carlsen'
           ', in tears, to ESPN yesterday evening']

sen_3_record = ['\" I have never seen such a show of talent in the last 3 decades! \" said Kasparov to CNN']

# +40 elo points
sen_3_a = ['\" Brilliant chess by {username}, top performance!\" twitted Magnus Carlsen yesterday evening'
           ]

# 15 to 40 elo points
sen_3_b = ['\"He is getting better.  Will he be the best player in history some day? We\'ll see. \" said Lionel Messi'
           ' to Fox Sports yesterday evening']

# -15 to 15 elo points
sen_3_c = ['\"Decent chess, but we want to see more from {username} \" said a fan yesterday to the media'
           ]

# -15 to -40 elo points
sen_3_d = ['\" The boat is sinking, will {username} be able to recover? Let\'s see what happens tomorrow. \" said'
           ' ex-world champion Karpov to Fox Sports'
           ]

# more than -40 elo points
sen_3_e = ['\" I will definitely have nightmares tonight.  I am absolutely horrified by the terrible chess. \" said '
           'Garry Kasparov to CNN yesterday'
           ]




# html.H4(
#     'These were not bad performances from the opponents but not bad gets you nowhere against the gold '
#     'standard in world chess. There were chances for the rival sides, even after {username}’s first '
#     'checkmate, and there simply was no player of quality to overcome the cunning skills of our '
#     'present era’s chess star. That was the difference in the end. {username}’s sniper vision overwhelmed'
#     ' the board once and again, leaving little room to chance.'
#         .format(username=username_input)
# ),
# html.Br(),
# html.Br(),
# html.H4(
#     'If the second checkmate was not a masterpiece, then the third one was the consequence of a rock '
#     'solid opening and then an inaccuracy on the rival’s part in the middle game, just as the match was'
#     'starting to open up to complex tactical variants.'
#         .format(username=username_input)
# ),
# html.Br(),
# html.Br(),
# html.H4(
#     '{username} reached his highest rating of {best_elo} on {date_best}, so he is currently '
#     '{diff_with_max} points {above_below} the record.  The universe of chess is eagerly awaiting the '
#     'next matches to see if {username} can keep climbing the rating ladder or if the competitive '
#     'pressure will make him stumble.'
#         .format(username=username_input, date_best='2019-01-01', diff_with_max='200', best_elo='2800',
#                 above_below='above')
# ),

