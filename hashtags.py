'''
Task_2
Yihui Lu
20200412
'''

import random, copy
from hashtag_structures import *
from timeit import default_timer as timer


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def read_tweets(tweet_file):
    '''
    read_tweets(str) --> list of Tweets
    Open and read the given file with tweet data, and return a list of Tweet objects
    representing the file's data.
    '''
    tweets = []
    in_file = open(tweet_file)
    for line in in_file:
        line=line.rstrip().split("|")
        text = line[0]
        hts = line[1].split(",")
        tweets.append(Tweet(text, hts))
    in_file.close()
    return tweets



def read_hashtags(hashtag_file):
    '''
    read_hashtags(str) --> Hashtag_List
    Open and read the given file with hashtags, and return a Hashtag_List of
    Hashtag_Record objects representing the file's data.
    '''
    hashtags = Hashtag_List()
    in_file = open(hashtag_file)
    for line in in_file:
        line=line.rstrip()
        tag = Hashtag_Record(line)   
        hashtags.append(tag)
    in_file.close()
    return hashtags


def insert_tweet(structure, tweet):
    '''
    insert_tweet(structure, Tweet) --> None
    Inserts the given Tweet into the given data structure, by adding it to
    each of the Tweet's hashtags' records.
    '''    
    hashtag_strings = tweet.get_hashtags()
    for tag in hashtag_strings:
        #We need to wrap the hashtag string in a Record object for comparisons
        #that take place within the retrieve() process
        ht_record = Hashtag_Record(tag)
        found_record = structure.retrieve(ht_record)
        if found_record != None:
            #we found it, so mutate the found record.
            #note that mutating ht_record would NOT work here because it's not
            #the record that is actually IN the structure, but found_record IS
            found_record.add_tweet(tweet)
        else:
            #this was a new hashtag found in this Tweet, so add it
            ht_record.add_tweet(tweet)
            structure.insert(ht_record)



def get_tweets(structure, hashtag, output=False):
    '''
    get_tweets(structure, Hashtag_Record, bool) --> list of Tweets
    Returns the list of all Tweets for the given Hashtag_Record,
    or None if that hashtag isnt present.
    Optional bool argument will print out the tweets when True.
    '''
    ht_record = structure.retrieve(hashtag)
    if ht_record != None:
        if output:
            print("Tweets for #{}:".format(hashtag.get_tag()))
            for t in ht_record.get_tweets():
                print(t)
            print()
        
        return ht_record.get_tweets()
    else:
        return None


def get_hashtags(structure, tweet):
    '''
    get_hashtags(structure, str) --> Hashtag_List
    Returns a list of all list of all Hashtag_Records that correspond to
    hashtags that were used in a Tweet with the given text.
    '''
    htl = Hashtag_List()
    l = structure.as_list()
    for i in l: 
        for j in i.get_tweets(): #for each Tweet in each Hashtag_Record
            if tweet == j.get_text(): #given text and text of the Tweet is the same
                htl.append(i)
    return htl

    
    
#===============================================================================

if __name__ == "__main__":

    #=== READ IN THE TWEET & HASHTAG FILES =====================================
    
    #-== PLAIN HASHTAG_RECORDS FILE FOR INSERTS ==-
    #replace with whatever master hashtag file you wish to use.
    HASHTAG_FILE = "hashtags_input.txt"
    all_hashtags = read_hashtags(HASHTAG_FILE)  #list of Hashtag_Records
    random.shuffle(all_hashtags) #randomizing the hashtags is more authentic
    
    #-== TWEET FILE ==-
    #replace with whatever tweet file you wish to use.
    #TWEET_FILE = "tweets_input_small.txt"
    TWEET_FILE = "tweets_input.txt"
    all_tweets = read_tweets(TWEET_FILE)  #list of Tweets
    random.shuffle(all_tweets) #randomizing the Tweets is more authentic
    
       
    
    #-== HASHTAG_RECORDS FILE FOR LOOKUPS ==-
    #replace with whatever hashtag lookup file you wish to use.
    #HASHTAG_LOOKUP_FILE = "hashtag_lookups_input_small.txt" 
    HASHTAG_LOOKUP_FILE = "hashtag_lookups_input.txt"
    some_hashtags = read_hashtags(HASHTAG_LOOKUP_FILE)  #list of Hashtag_Records
    random.shuffle(some_hashtags) #randomizing the hashtags is more authentic

    


    #=== CONSTRUCT THE DATA STRUCTURES =========================================
    HIGH_LOAD_FACTOR = 20
    structure_HTL = Hashtag_LinkedList()
    structure_HTT = Hashtag_BSTree()
    structure_HTT_balanced = Hashtag_BSTree()
    structure_HHT = Hashtag_HashTable(101, True)
    structure_HHTsmall = Hashtag_HashTable(len(all_hashtags)//HIGH_LOAD_FACTOR, False) #much smaller, for comparison
    
    

    #=== INSERTS ===============================================================
    #Using the 'all_hashtags' list of hashtags, insert each as a record
    #into the specific structure data structure.
    #Time the process, and produce output.
    #Repeat for each of the data structures, timing each separately.

    
    print("-== INSERTING {} HASHTAGS INTO STRUCTURES ==-".format(len(all_hashtags)))
    structures = [structure_HTL, structure_HTT, structure_HTT_balanced, structure_HHT, structure_HHTsmall]
    labels = ["Hashtag_LinkedList", "Hashtag_BSTree", "Hashtag_BSTree(Balanced)", "Hashtag_HashTable", "Hashtag_HashTable(small)"]


    for i in range(len(structures)):
        #we make a deep copy of the list of all Hashtag_Records because if we
        #dont, they would get shared amongst all the structures (aliasing), and
        #thus get mutated multiple times (once for each structure we test) 
        all_hashtags_copy = copy.deepcopy(all_hashtags)
        start = timer()
        for tag in all_hashtags_copy:
            structures[i].insert(tag)
            
        #apply the balance() operation to the balanced tree, only after ALL inserts
        #re-balancing each time would be brutally slow
        if structures[i] == structure_HTT_balanced:
            structure_HTT_balanced.balance()
        end = timer()
        print("{} time: {:.4f}".format(labels[i], end - start))
        
        

   
    #=== RETRIEVALS ============================================================
    print("\n-== INSERT_TWEETS() with {} Tweets ==-".format(len(all_tweets)))
    #start at structure 1 since using a linked list would be too slow.
    #change to 0 if you want to also test linked list, but then you should
    #also use the SMALL tweets input file!
    for i in range(1, len(structures)):
        start = timer()
        for tweet in all_tweets:
            insert_tweet(structures[i], tweet)
        end = timer()
        print("{} time: {:.4f}".format(labels[i], end - start))

    
    print("\n-== GET_TWEETS() for {} Hashtags ==-".format(len(some_hashtags)))
    for i in range(0, len(structures)):
        start = timer()
        for tag in some_hashtags:
            tweets_for_this_ht = get_tweets(structures[i], tag, False)
        end = timer()
        print("{} time: {:.4f}".format(labels[i], end - start))
    
    

    
    #=== FULL TRAVERSALS =======================================================
    print("\n-== GET_TOP_HASHTAG() for all STRUCTURES ==-")
    for i in range(0, len(structures)):
        start = timer()
        top = structures[i].get_top_hashtag()
        end = timer()
        print("{} time: {:.4f}".format(labels[i], end - start))
        print("  Top Hashtag: {}".format(top))
        print("  Return type: {}".format(type(top)))

    
    print("\n-== AS_LIST() for all STRUCTURES ==-")
    for i in range(0, len(structures)):
        start = timer()
        alist = structures[i].as_list()
        end = timer()
        print("{} time: {:.4f}".format(labels[i], end - start))
        print("  {} items, first 20: {}".format(len(alist), alist[:20]))
        print("  Return type: {}".format(type(alist)))
    
    
    
    print("\n-== GET_HASHTAGS() for all STRUCTURES ==-")
    tweet_text = "It's a goner for us, tom"
    for i in range(0, len(structures)):
        start = timer()
        tags_for_tweet = get_hashtags(structure_HTT, tweet_text)    
        end = timer()
        print("{} time: {:.4f}".format(labels[i], end - start))
        print("  Hashtags ({}): {}".format(len(tags_for_tweet), tags_for_tweet))
        print("  Return type: {}".format(type(tags_for_tweet)))
    
    
   
    #=== HASHTAG_LIST EXTRAS ===================================================
    print("\n-== HASHTAG_LIST EXTRAS ==-")
    start = timer()
    alist = structure_HTT.as_list().sorted_by_num_tweets()
    end = timer()
    print("sorting_by_num_tweets() time: {:.4f}".format(end - start))
    print("  {} items, first 20: {}".format(len(alist), alist[:20]))
    print("  Return type: {}".format(type(alist)))

        



    #LINKED_LIST EXTRAS
    print("\n-== LINKED_LIST EXTRAS ==-")
    NUM_TO_CHECK = 3
    first_few = []
    for n in range(0, NUM_TO_CHECK):
        first_few.append(str(structure_HTL.get_nth(n)))
    print("First {}:".format(NUM_TO_CHECK))
    print("--->".join(first_few))
    structure_HTL.reverse()
    last_few = []
    for n in range(len(all_hashtags)-NUM_TO_CHECK, len(all_hashtags)):
        last_few.append(str(structure_HTL.get_nth(n)))
    print("Last {} after reversing:".format(NUM_TO_CHECK))
    print("--->".join(last_few))
    

    #BINARY SEARCH TREE EXTRAS
    print("\n-== BINARY SEARCH TREE EXTRAS ==-")    
    leaves = structure_HTT.get_leaves()
    num_1_child = structure_HTT.count_one_child()
    print("Normal Tree:")
    print("  Depth: {}, Average Depth: {}, {} Leaves, {} With 1 Child".format(structure_HTT.depth(), structure_HTT.average_depth(), len(leaves), num_1_child))
    print("  get_leaves() return type: {}".format(type(leaves)))

    print("Balanced Tree:")
    leaves = structure_HTT_balanced.get_leaves()
    num_1_child = structure_HTT_balanced.count_one_child()
    print("  Depth: {}, Average Depth: {}, {} Leaves, {} With 1 Child".format(structure_HTT_balanced.depth(), structure_HTT_balanced.average_depth(), len(leaves), num_1_child))
    print("  get_leaves() return type: {}".format(type(leaves)))
    

    #HASHTABLE EXTRAS
    print("\n-== HASHTABLE EXTRAS ==-")
    largest = structure_HHT.get_largest_bucket()
    over_lf_percent = structure_HHT.get_percent_above_load_factor()
    lf = structure_HHT.load_factor()
    print("Scaling Hashtable:")
    print("  LF: {}, %over LF: {}, Largest ({}) = {}".format(lf, over_lf_percent, largest.size(), largest))
    
    largest = structure_HHTsmall.get_largest_bucket()
    over_lf_percent = structure_HHTsmall.get_percent_above_load_factor()
    lf = structure_HHTsmall.load_factor()
    print("Non-Scaling Hashtable:")
    print("  LF: {}, %over LF: {}, Largest ({} tweets) = {}".format(lf, over_lf_percent, largest.size(), largest))
    print("  Return type from get_largest_bucket(): {}".format(type(largest)))


