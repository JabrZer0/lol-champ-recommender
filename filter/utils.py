

def get_WLR_sims(profile_to_check, profiles_list):
    
    cos_sims = []
    for i in range(len(profiles_list)):
        w0 = list(profile_to_check['NormalizedWLR'])
        w1 = list(profiles_list[i]['NormalizedWLR'])
        cos_sims.append(1 - distance.cosine(w0, w1))
    
    return cos_sims

def get_recs(WLR_sims, profiles, champs):
    WLR_scores= []
    
    for i in range(len(WLR_sims)):
        WLR_score = list(profiles[i]['NormalizedWLR'] * WLR_sims[i])
        WLR_scores.append(WLR_score)
    
    WLR_scores = [*zip(*WLR_scores)]
    WLR_scores = [sum(x) for x in WLR_scores]
    result = pd.DataFrame({'Champ': champs, 'Recommendation': WLR_scores}).set_index('Champ').sort_values('Recommendation',ascending=False)
    
    return result

# define the functions needed for messing with the profile dataframe

def get_wins(row):
    item = row['Played'].split(' ')[0]
    if item[-1] == 'W':
        return int(item[:-1])
    else: return 0

def get_losses(row):
    item = row['Played'].split(' ')[-3]
    if item[-1] == 'L':
        return int(item[:-1])
    else: return 0

def get_KDA(row):
    item = row['KDA'].split(' ')[-1][:-2]
    if item == 'Perfe': return float(10)
    return float(item)

def get_top_bot(recs):
    top = round(recs[:5],2).reset_index().values.tolist()
    bottom = round(recs[-5:],2).reset_index().values.tolist()
    bottom = bottom[::-1]
    return [top, bottom]

def recommend_from_summoner_name(sum_name, region, profiles, champs):
    sum_name = sum_name.replace(' ','+')
    
    # get the summoner profile from op.gg
    url = 'http://' + region + '.op.gg/summoner/champions/userName=' + sum_name
    #     try:
    page = requests.get(url).content
    profile = pd.read_html(page)[0]
    truncated_profile = profile[['Champion','Played','KDA']]

    user_profile = truncated_profile

    user_profile['Wins'] = truncated_profile.apply(lambda row: get_wins(row), axis=1)
    user_profile['Losses'] = truncated_profile.apply(lambda row: get_losses(row), axis=1)
    user_profile['Games'] = truncated_profile.apply(lambda row: get_wins(row) + get_losses(row), axis=1)
    user_profile['WLR'] = truncated_profile.apply(lambda row: get_wins(row) / (get_wins(row) + get_losses(row)), axis=1)
    user_profile['KDA'] = truncated_profile.apply(lambda row: get_KDA(row), axis=1)
    user_profile = user_profile.set_index('Champion')
    user_profile = user_profile.drop('Played',1)

    user_profile['NormalizedKDA'] = 0
    user_profile['NormalizedWLR'] = 0

    for champ in champs:
        if champ in list(user_profile.index) and user_profile.loc[champ]['Games'] > 1:
            a = user_profile.loc[champ, :]['WLR']
            b = a - 0.5
            c = user_profile.loc[champ, :]['KDA']

            if c < 1 and c > 0:
                d = -1 / c
            else:
                d = c

            user_profile['NormalizedKDA'][champ] = d
            user_profile['NormalizedWLR'][champ] = b

        else: # if the champ hasn't been played, initialize to 0
            user_profile.loc[champ] = [0,0,0,0,.5,0,0]

    user_profile['NormalizedKDA'] = [y / max([abs(x) for x in list(user_profile['NormalizedKDA'])]) for y in user_profile['NormalizedKDA']]
    user_profile['NormalizedWLR'] = [y / max([abs(x) for x in list(user_profile['NormalizedWLR'])]) for y in user_profile['NormalizedWLR']]

    user_profile = user_profile.sort_index()
    for i in range(len(profiles)):
        profiles[i] = profiles[i].sort_index()
        
    WLR_sims = get_WLR_sims(user_profile,profiles)
    return get_recs(WLR_sims, profiles, champs)

def get_img_paths(champ, champ_img_conv):
	output = "http://ddragon.leagueoflegends.com/cdn/9.4.1/img/champion/" + champ_img_conv[champ] + ".png"
	return output
