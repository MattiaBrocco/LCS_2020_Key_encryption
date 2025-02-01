import random
import hashlib
import numpy as np
from collections import Counter

class complete_decryption:
    
    def letter_freqs(self, t):
        self.t = t
        """
        This function creates a dictionary such that its keys are the letters,
        and its values the frequencies of occurence in the input text.
        """
        dict_counter = {}
        for char in t:
            if char not in dict_counter:
                dict_counter[char] = 0 
            dict_counter[char] += 1
        return dict_counter
    
    
    def decrittore(key, t):
        """
        This functions MAPS the cipher with the corresponding
        letter of the corpus letters' frequency. This is possible
        because the two strings are sorted on frequency.
        """
        CORPUS = "ETAONIHSRDLUWCMFGYPBVKXJQZ".lower() # extracted from the frequency analysis
        Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
        dictEA = dict(zip(key, CORPUS))
        decrypted = ""
        for char in t:
            if char not in Alphabet:
                decrypted += char
            else:
                decrypted += dictEA[char]
    
        return decrypted
    
    
    def decrypter(self, key, t):
        self.key = key
        self.t = t
        """
        This functions MAPS the cipher with the corresponding
        letter of the corpus letters' frequency. This is possible
        because the two strings are sorted on frequency.
        """
        CORPUS = "ETAONIHSRDLUWCMFGYPBVKXJQZ" # extracted from the frequency analysis
        Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        dictEA = dict(zip(key, CORPUS))
        decrypted = ""
        for char in t:
            if char not in Alphabet:
                decrypted += char
            else:
                decrypted += dictEA[char]
    
        return decrypted

    def bigram_analysis(self, t):
        self.t = t
        """
        This function exploits the Counter library, which
        by definition return a dictionary, where Ks are
        bigrams, and Vs are their respective frequency.
        """
        BigrtoFreq = Counter(t[idx : idx + 2] for idx in range(len(t) - 1))
    
        # Give a score to each bigram (score = np.log(bigram's frequency) )
        BigrtoFreq = dict(zip(BigrtoFreq.keys(), [round(np.log(v), 10)
                                                  for k,v in BigrtoFreq.items()]))
        
        # Bigrams are finally ordered by decreasing frequency
        BigrtoFreq = {k: v for k, v in sorted(BigrtoFreq.items(),
                                              key = lambda item: item[1], reverse = True)}   
    
        return BigrtoFreq
  
    
    def ciphertext_decrypter(self, key, t):
        self.key = key
        self.t = t
        """
        This function is specifically for getting the hash
        check right! It is the lowercase version of "decrypter".
        This function was necessary, since the hash is computed
        on the pure ciphertext (with no punctuation removed). Accordingly,
        this function aims at preserving all the properties of the text
        given as input. All the other inputs to the for loop are
        converted into lowercase as well, to serve the abovementioned purpose.
        """
        key = key.lower()
        corpus = "ETAONIHSRDLUWCMFGYPBVKXJQZ".lower() # extracted from the frequency analysis
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
        dictEA = dict(zip(key, corpus ))
        
        decrypted = ""
        for char in t:
            if char not in alphabet:
                decrypted += char
            else:
                decrypted += dictEA[char]
            
        return decrypted
    

    # Frequency analysis function

    def freq_analysis(self, text):
        self.text = text
        """
        Returns a string of the alphabet letters with len == 26,
        arranged in order of most frequently occurring in the input text.
        It is based on the "cipher_freqs" function.
        """
        # Recap the frequencies in the cipher (K letters, V frequencies)
        letterToFreq = self.letter_freqs(text)

        # The dictionary is then converted to a list of tuples
        # (letter, frequency) that are sorted according to frequency    
        freqPairs = list(letterToFreq.items())
        freqPairs.sort(key = lambda x:x[1], reverse = True)
        
        # The final string is created in such a way that
        # letter sare ordered by frequency
        freqOrder = [pair[0] for pair in freqPairs]    

        return ''.join(freqOrder)
    
    def candidate_plain_score(self, t, corpus):
        self.t = t
        self.corpus = corpus
        # Recall the previous function to generate a
        # dict and get only the list of the keys
        cand_BI_freq = self.bigram_analysis(t)
        Corpus_BI_freq = self.bigram_analysis(corpus)
        
        bigrams_in_cand = list(cand_BI_freq.keys())

        # Get the score (log(freq)) of the bigrams in the corpus
        # for every bigram found in the candidate plaintext.
        # Added a check (if) for those bigrams that are not in the corpus
        scores_corpus_bigrams_in_cand = [Corpus_BI_freq[bi] for bi in bigrams_in_cand
                                        if bi in Corpus_BI_freq.keys()]

        # Assign to every bigram of the candidate plaintext
        # the score that that biagram has in the corpus
        dict_scores_corpus_bigrams_in_cand = dict(zip(bigrams_in_cand,
                                                    scores_corpus_bigrams_in_cand))

        # The overall score of the candidate plain text is
        # computed as the sum of all the values in the above dict
        return sum(dict_scores_corpus_bigrams_in_cand.values())
    

    def key_improver(self, k, first_candidate, text, corpus):
        self.k = k
        self.first_candidate = first_candidate
        self.text = text
        """
        This function gets the first key as an input. Then, for every character
        in the key, it swaps that character with the following one and stores
        the new key.
        
        Then, for every key found, the score of that key is compared with the
        one obtained with the first key. The output of the function will finally
        be a list of tuples (number of iteration, key) of only those keys that
        produce a better score than the first key.
        """
        F_Key_L = list(k)
        List_swap = []
        for n in range(len(F_Key_L)-1):
            F_Key_L2 = F_Key_L.copy()
            # swapping (item assigment) is not possible for string, so we used a list
            F_Key_L2[n], F_Key_L2[n+1] = F_Key_L2[n+1], F_Key_L2[n]
            List_swap += [ "".join(F_Key_L2) ]
        
        First_Score = self.candidate_plain_score(first_candidate, corpus)
        best_from_swap = []
        for e, nk in enumerate(List_swap): # keep the iteration number and the key
            new_try = self.decrypter(nk, text)
            new_score = self.candidate_plain_score(new_try, corpus)
            if new_score > First_Score: # winning scores
                best_from_swap += [ (e, nk) ] # return list of tuples
            else:
                continue
        """
        RECURSIVE ATTEMPT
        for nk in List_swap: #for e, nk in enumerate(List_swap):
            new_try = dec.decrypter(nk, text)
            new_score = candidate_plain_score(new_try)
            if new_score > First_Score:
                print(nk)
                #best_from_swap += [ nk ]
                #improved_key = key_improver(nk)
                return key_improver(nk)
        """
        return best_from_swap
    

    def brute_force(self, key0, list_of_keys, text, corpus, correct_hash, ciphertext):
        self.text = text
        self.key0 = key0
        self.corpus = corpus
        self.ciphertext = ciphertext
        self.list_of_keys = list_of_keys
        self.correct_hash = correct_hash
        """
        This function, starting from the initial key found from frequency
        analysis on letters, iterates for every element of the list of new
        keys found in order to detect the right hash (in the first place),
        or at least to find an improvement of the original key.
        
        If the hash is found the function interrupts the loop and returns
        the right key, otherwise it returns the improvement found.
        """
        best_key = key0
        best_cand = self.decrypter( key0, text )
        max_score = self.candidate_plain_score(best_cand, corpus)
        for key in list_of_keys:
            candidate = self.decrypter( key, text )
            score = self.candidate_plain_score(candidate, corpus)
            candidate_for_hash = self.ciphertext_decrypter(key, ciphertext) # to get the hask check right
            # we are sure that encoding is "utf-8" after professor Maccari's tutorial
            utf8_dig = hashlib.sha256( bytes(candidate_for_hash, "utf-8") ).hexdigest()
            if utf8_dig == correct_hash:
                return key
            elif score > max_score:
                max_score = score
                best_key = key
                best_cand = candidate
        return best_key.lower()
    

    def gradient_descent_brute_force(self, key0, text, corpus, correct_hash, ciphertext, max_iterations=1000):
        self.text = text
        self.key0 = key0
        self.corpus = corpus
        self.ciphertext = ciphertext
        self.correct_hash = correct_hash

        def mutate_key(key):
            """Randomly modifies the key slightly to explore new candidates"""
            key_list = list(key)
            idx1, idx2 = random.sample(range(len(key)), 2)  # Swap two random elements
            key_list[idx1], key_list[idx2] = key_list[idx2], key_list[idx1]
            return "".join(key_list)

        best_key = key0
        best_cand = self.decrypter(best_key, text)
        max_score = self.candidate_plain_score(best_cand, corpus)
        
        for _ in range(max_iterations):
            new_key = mutate_key(best_key)
            candidate = self.decrypter(new_key, text)
            score = self.candidate_plain_score(candidate, corpus)

            # Hash check
            candidate_for_hash = self.ciphertext_decrypter(new_key, ciphertext)
            utf8_dig = hashlib.sha256(bytes(candidate_for_hash, "utf-8")).hexdigest()
            if utf8_dig == correct_hash:
                return new_key  # Found the correct key

            # If the new key improves the score, accept it
            if score > max_score:
                max_score = score
                best_key = new_key

        return best_key.lower()