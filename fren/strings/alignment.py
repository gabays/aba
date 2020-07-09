# Needleman-Wunsch Algorithm

from itertools import product
from .distance import levenshtein
from .utils import init_matrix


def needleman_wunsch(a, b, scores = (4, -1, -1), submat = {}, mode = 'word'): 
    """Returns alignment of sequences a and b.

    :param scores: Scores for match award, mismatch penalty and gap penalty
    :type scores: tuple (match, mismatch, gap)
    """

    # unpack score parameters
    _, _, gap_penalty = scores

    # init matrix
    rows, cols, matrix = init_matrix(a, b, factor = gap_penalty)

    # fill matrix
    for x, y in product(range(1, rows), range(1, cols)):
        # compute values from top, left, and top-left diagonal cells
        match = matrix[x-1][y-1] + score(a[x-1], b[y-1], scores, submat, mode)
        insert = matrix[x][y-1] + gap_penalty
        delete = matrix[x-1][y] + gap_penalty
        # store maxs
        matrix[x][y] = max(match, delete, insert)

    # init traceback
    align_a = []
    align_b = []
    x = len(a)
    y = len(b)

    # traceback
    while x > 0 or y > 0:
        # retrieve scores
        current_score = matrix[x][y]
        topleft_score = matrix[x-1][y-1]
        left_score = matrix[x][y-1]
        top_score = matrix[x-1][y]
        # find origin cell, append corresponding elements, advance
        if (x > 0 and y > 0
            and current_score == topleft_score + score(a[x-1], b[y-1], scores, submat, mode)):
            # origin is top-left
            align_a.append(a[x-1])
            align_b.append(b[y-1])
            x = x-1
            y = y-1
        elif y > 0 and current_score == left_score + gap_penalty:
            # origin is left
            align_a.append('¤')
            align_b.append(b[y-1])
            y = y-1
        elif x > 0 and current_score == top_score + gap_penalty:
            # origin is top
            align_a.append(a[x-1])
            align_b.append('¤')
            x = x-1
        else:
            raise ValueError('Traceback failed')

    # reverse sequence order
    align_a = align_a[::-1]
    align_b = align_b[::-1]

    return (align_a, align_b)

def score(a, b, scores, submat, mode):
    # unpack score parameters
    match_award, mismatch_penalty, gap_penalty = scores
    # make all lowercase
    a = a.lower()
    b = b.lower()
    # match
    if (a == b
     or a == '&' and b == 'et'):
        return match_award
    # substitution matrix
    elif (a in submat and b in submat[a]):
      return submat[a][b]
    # gap
    elif a == '¤' or b == '¤':
        return gap_penalty
    # mismatch
    elif (mode == 'words' and len(a) >= 1 and len(b) >= 1):
        dist = levenshtein(a, b, costs = (1, 1, 2), submat = submat)
        if (dist < min(len(a), len(b)) and dist < 4):
            return match_award - dist
        else:
            return mismatch_penalty
    else:
        return mismatch_penalty