import tokenizer # awwww yeah
import sqlite3
import codecs
import collections
import sys
import matplotlib.pyplot as plt
import numpy

def get_categories(fileName):
    with codecs.open(fileName) as f:
        cate_dict = collections.defaultdict(set)
        current_topic = ""
        for line in f:
            if line[0] != '\n':
                if line[0] == '#':
                    current_topic = line[2:].strip()
                else:
                    cate_dict[current_topic].add(line.strip())
        return cate_dict

def get_domains_for_search(curs, table, search, rank_cutoff=11):
    sql = 'select url from %s where search=? and rank < ?' % table
    url_tups = curs.execute(sql, (search, rank_cutoff))
    return [u[0] for u in url_tups]

def get_bing_results(curs, search, rank_cutoff=11):
    return get_domains_for_search(curs, 'search_bingrank', search, rank_cutoff=rank_cutoff)

def get_pop_rank_results(curs, search, rank_cutoff=11):
    return get_domains_for_search(curs, 'search_poprank', search, rank_cutoff=rank_cutoff)

def make_counters_for_category(category, search_set, curs):
    bing_counter = collections.Counter()
    pop_counter = collections.Counter()
    for search in search_set:
        bing_results = get_bing_results(curs, search)
        pop_results = get_pop_rank_results(curs, search)
        for b_res, pop_res in zip(bing_results, pop_results):
            b_dom = tokenizer.get_tokens(b_res)[1]
            pop_dom = tokenizer.get_tokens(pop_res)[1]
            bing_counter[b_dom] += 1
            pop_counter[pop_dom] += 1

    b_hist_data = []
    b_hist_labels = []
    for domain, count in pop_counter.most_common(10):
        b_hist_data.append(count)
        b_hist_labels.append(domain)


    plt.bar(range(len(b_hist_data)), b_hist_data, align='center', color='red')
    plt.xticks(range(len(b_hist_data)), b_hist_labels, size='small', rotation=90)
    plt.legend(loc=3)
    plt.suptitle('Most Popular Domains for PopRank in %s' % category)
    plt.show()
    return (bing_counter, pop_counter)

def get_ranks(curs):
    sql = """select b.rank, p.rank from search_bingrank as b 
             join search_poprank as p on p.search=b.search and p.url=b.url"""
    rows = curs.execute(sql)
    return rows.fetchall()

def get_ranks_for_topic(curs, search):
    sql = """select b.rank, p.rank from search_bingrank as b 
             join search_poprank as p on p.search=b.search and p.url=b.url
             where b.search=?"""
    rows = curs.execute(sql, search)
    return rows.fetchall()

def get_ranks_for_topics(curs, search_list):
    sql = """select b.rank, p.rank from search_bingrank as b 
             join search_poprank as p on p.search=b.search and p.url=b.url
             where b.search in (%s)""" % ','.join('?'*len(search_list))

    rows = curs.execute(sql, list(search_list))
    return rows.fetchall()


def get_corrcoeff(category_file, db_file):
    db_conn = sqlite3.connect(db_file)
    curs = db_conn.cursor()
    categories = get_categories(category_file)

    for key, topic_set in categories.iteritems():
        ranks = get_ranks_for_topics(curs, topic_set)
        bing_ranks = numpy.array([r[0] for r in ranks])
        pop_ranks = numpy.array([r[1] for r in ranks])
        print key
        print numpy.corrcoef([bing_ranks, pop_ranks])


def make_hists(category_file, db_file):
    db_conn = sqlite3.connect(db_file)
    curs = db_conn.cursor()
    categories = get_categories(category_file)

    totals_bing = collections.Counter()
    totals_pop = collections.Counter()

    for category, search_set in categories.iteritems():
        bing_counter, pop_counter = make_counters_for_category(category, search_set, curs)
        totals_bing[category] = len(list(bing_counter.keys()))/len(search_set)
        totals_pop[category] = len(list(pop_counter.keys()))/len(search_set)


    hist_data = []
    hist_data2 = []
    hist_labels = []
    hist_labels2 = []
    for key, count in totals_pop.most_common(6):
        hist_data.append(count)
        hist_labels.append(key)

    plt.bar(range(len(hist_data)), hist_data, align='center', color='red', label='PopRank Domain Count')
    plt.xticks(range(len(hist_data)), hist_labels, size='small', rotation=90)
    
    for key, count in totals_bing.most_common(6):
        hist_data2.append(count)
        hist_labels2.append(key)

    plt.bar(range(len(hist_data2)), hist_data2, align='center', color='blue', label="Bing Domain Count")
    plt.xticks(range(len(hist_data2)), hist_labels2, size='small', rotation=90)

    plt.legend(loc=3)
    plt.suptitle('Unique Domain Per Search By Category')
    plt.show()



if __name__ == '__main__':
    print get_corrcoeff(sys.argv[1], sys.argv[2])


