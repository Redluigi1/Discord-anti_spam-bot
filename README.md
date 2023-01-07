The bot is mainly used to prevent spam in any server. It has the following features - 
(a) It checks for any swear/obcsene words in english or hindi in the server. There are two csv files - eng.csv has bad words in english; hin.csv has bad words in hindi
(b) It makes sure that the frequency of messages sent by users in a channel doesnt exceed a limit. For example, if a user sends 50 messages under one minute, then they are clearly spamming in the server
(c) It has the following commands - 
            add_regex ------ to add a regex check along with the security level
            print_regex ------ to print all the regex checks along with their keys. The keys of the dictionary is the key of the regex. Each key has a two element list. The first element is the security level. The second element is the regex string
            remove_regex ------ to remove a partiular regex check
            pattern_regex ------ to delete all the messages satisfying a certain regex check from the past 24 hours
            
