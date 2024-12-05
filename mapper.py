#!/usr/bin/env python3
import sys

# Input format: movieId,tagId,relevance
for line in sys.stdin:
    fields = line.strip().split(',')
    if len(fields) == 3:
        movie_id, tag_id, relevance = fields
        try:
            relevance = float(relevance)
            # Output: tagId \t movieId:relevance
            print(f"{tag_id}\t{movie_id}:{relevance}")
        except ValueError:
            continue
