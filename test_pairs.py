def make_pairs(u, o):
    u_ratings = {}
    for r in u.ratings:
        u_ratings[r.movie_id] = r 

    paired_ratings = []
    for o_rating in o.ratings:
        u_score = u_ratings.get(o_rating.movie_id)
        if u_score: 
            paired_ratings.append((u_score.score, o_rating.score))

    return paired_ratings