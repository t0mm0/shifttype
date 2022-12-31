min_length = 5
max_length = 7
with open('short.txt') as short:
    for word_length in range(min_length + 1, max_length + 2):
        short.seek(0)
        words_short = [line for line in short if len(line) == word_length]
        out_name = 'common_{}.txt'.format(word_length - 1)
        with open(out_name, 'w') as out:
            out.writelines(words_short)
            print('wrote {} words to {}'.format(len(words_short), out_name))
        with open('long.txt') as long:
            all_words_long = [line for line in long if len(line) == word_length]
            words_long = set(all_words_long).difference(set(words_short))
            out_name = 'uncommon_{}.txt'.format(word_length - 1)
            with open(out_name, 'w') as out:
                out.writelines(sorted(words_long))
                print('wrote {} words to {}'.format(len(words_long), out_name))
