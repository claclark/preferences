#!/usr/bin/env python3

import argparse
import random
import sys

from prefj import prefj
from prefj import load_qrels


def load_judgments(filename):
    judgments = {}
    with open(filename) as jf:
        for line in jf:
            fields = line.rstrip().split()
            if len(fields) == 3:
                (topic, a, b) = fields
                best = a
            else:
                (topic, a, b, best) = fields
            if a == b or (a != best and b != best):
                print('Bad judgment: ', line, file=sys.stderr)
            else:
                if a < b:
                    pair = ' '.join((a, b))
                else:
                    pair = ' '.join((b, a))
                if topic not in judgments:
                    judgments[topic] = {}
                if pair not in judgments[topic]:
                    judgments[topic][pair] = []
                judgments[topic][pair].append(best)
    return judgments


def random_judgment(judgments, pair):
    if pair in judgments:
        best = random.choice(judgments[pair])
    else:
        docnos = pair.split()
        best = random.choice(docnos)
    return ' '.join((pair, best))


def random_judgments(judgments, requests):
    rj = []
    for request in requests:
        rj.append(random_judgment(judgments, request))
    return rj


def sim(topic, qrels, judgments):
    p = prefj(topic, qrels)
    requests = p.requests()
    while len(requests) > 0:
        p.add(random_judgments(judgments, requests))
        requests = p.requests()
    p.dump_log()
    return len(p.log)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      description='Simulate top-k preferences')
    parser.add_argument('qrels', type=str, help='TREC-style qrels')
    parser.add_argument('prefs', type=str, help='Preferences for simulation')
    args = parser.parse_args()

    qrels = load_qrels(args.qrels)
    if len(qrels) == 0:
        sys.exit(0)
    judgments = load_judgments(args.prefs)
    total = 0
    for topic in qrels:
        if topic in judgments:
            total += sim(topic, qrels[topic], judgments[topic])
        else:
            fake = {}
            total += sim(topic, qrels[topic], fake)
    #print('TOTAL', total)
