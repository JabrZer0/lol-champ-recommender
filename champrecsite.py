import pickle
import logging
from scipy.spatial import distance
import requests
import pandas as pd

logging.basicConfig(filename='data/info.log', filemode='a+', format='%(levelname)s - %(message)s', level=logging.INFO)

# turn off warnings from pandas
pd.options.mode.chained_assignment = None

from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from forms import RecommendForm
app = Flask(__name__)

conf = open("data/conf.txt", "r")
app.config['SECRET_KEY'] = conf.read()


champ_img_conv = {'Aatrox': 'Aatrox',
 'Ahri': 'Ahri',
 'Akali': 'Akali',
 'Alistar': 'Alistar',
 'Amumu': 'Amumu',
 'Anivia': 'Anivia',
 'Annie': 'Annie',
 'Ashe': 'Ashe',
 'Aurelion Sol': 'AurelionSol',
 'Azir': 'Azir',
 'Bard': 'Bard',
 'Blitzcrank': 'Blitzcrank',
 'Brand': 'Brand',
 'Braum': 'Braum',
 'Caitlyn': 'Caitlyn',
 'Camille': 'Camille',
 'Cassiopeia': 'Cassiopeia',
 "Cho'Gath": 'Chogath',
 'Corki': 'Corki',
 'Darius': 'Darius',
 'Diana': 'Diana',
 'Dr. Mundo': 'DrMundo',
 'Draven': 'Draven',
 'Ekko': 'Ekko',
 'Elise': 'Elise',
 'Evelynn': 'Evelynn',
 'Ezreal': 'Ezreal',
 'Fiddlesticks': 'FiddleSticks',
 'Fiora': 'Fiora',
 'Fizz': 'Fizz',
 'Galio': 'Galio',
 'Gangplank': 'Gangplank',
 'Garen': 'Garen',
 'Gnar': 'Gnar',
 'Gragas': 'Gragas',
 'Graves': 'Graves',
 'Hecarim': 'Hecarim',
 'Heimerdinger': 'Heimerdinger',
 'Illaoi': 'Illaoi',
 'Irelia': 'Irelia',
 'Ivern': 'Ivern',
 'Janna': 'Janna',
 'Jarvan IV': 'JarvanIV',
 'Jax': 'Jax',
 'Jayce': 'Jayce',
 'Jhin': 'Jhin',
 'Jinx': 'Jinx',
 "Kai'Sa": 'Kaisa',
 'Kalista': 'Kalista',
 'Karma': 'Karma',
 'Karthus': 'Karthus',
 'Kassadin': 'Kassadin',
 'Katarina': 'Katarina',
 'Kayle': 'Kayle',
 'Kayn': 'Kayn',
 'Kennen': 'Kennen',
 "Kha'Zix": 'Khazix',
 'Kindred': 'Kindred',
 'Kled': 'Kled',
 "Kog'Maw": 'KogMaw',
 'LeBlanc': 'Leblanc',
 'Lee Sin': 'LeeSin',
 'Leona': 'Leona',
 'Lissandra': 'Lissandra',
 'Lucian': 'Lucian',
 'Lulu': 'Lulu',
 'Lux': 'Lux',
 'Malphite': 'Malphite',
 'Malzahar': 'Malzahar',
 'Maokai': 'Maokai',
 'Master Yi': 'MasterYi',
 'Miss Fortune': 'MissFortune',
 'Mordekaiser': 'Mordekaiser',
 'Morgana': 'Morgana',
 'Nami': 'Nami',
 'Nasus': 'Nasus',
 'Nautilus': 'Nautilus',
 'Neeko': 'Neeko',
 'Nidalee': 'Nidalee',
 'Nocturne': 'Nocturne',
 'Nunu & Willump': 'Nunu',
 'Olaf': 'Olaf',
 'Orianna': 'Orianna',
 'Ornn': 'Ornn',
 'Pantheon': 'Pantheon',
 'Poppy': 'Poppy',
 'Pyke': 'Pyke',
 'Quinn': 'Quinn',
 'Rakan': 'Rakan',
 'Rammus': 'Rammus',
 "Rek'Sai": 'RekSai',
 'Renekton': 'Renekton',
 'Rengar': 'Rengar',
 'Riven': 'Riven',
 'Rumble': 'Rumble',
 'Ryze': 'Ryze',
 'Sejuani': 'Sejuani',
 'Shaco': 'Shaco',
 'Shen': 'Shen',
 'Shyvana': 'Shyvana',
 'Singed': 'Singed',
 'Sion': 'Sion',
 'Sivir': 'Sivir',
 'Skarner': 'Skarner',
 'Sona': 'Sona',
 'Soraka': 'Soraka',
 'Swain': 'Swain',
 'Sylas': 'Sylas',
 'Syndra': 'Syndra',
 'Tahm Kench': 'TahmKench',
 'Taliyah': 'Taliyah',
 'Talon': 'Talon',
 'Taric': 'Taric',
 'Teemo': 'Teemo',
 'Thresh': 'Thresh',
 'Tristana': 'Tristana',
 'Trundle': 'Trundle',
 'Tryndamere': 'Tryndamere',
 'Twisted Fate': 'TwistedFate',
 'Twitch': 'Twitch',
 'Udyr': 'Udyr',
 'Urgot': 'Urgot',
 'Varus': 'Varus',
 'Vayne': 'Vayne',
 'Veigar': 'Veigar',
 "Vel'Koz": 'Velkoz',
 'Vi': 'Vi',
 'Viktor': 'Viktor',
 'Vladimir': 'Vladimir',
 'Volibear': 'Volibear',
 'Warwick': 'Warwick',
 'Wukong': 'MonkeyKing',
 'Xayah': 'Xayah',
 'Xerath': 'Xerath',
 'Xin Zhao': 'XinZhao',
 'Yasuo': 'Yasuo',
 'Yorick': 'Yorick',
 'Zac': 'Zac',
 'Zed': 'Zed',
 'Ziggs': 'Ziggs',
 'Zilean': 'Zilean',
 'Zoe': 'Zoe',
 'Zyra': 'Zyra'}

profiles = pickle.load(open( "data/analyzed_profiles.pickle", "rb" ))
champs = pickle.load(open( "data/champs.pickle", "rb" ))


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


@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def home():
	form = RecommendForm()
	if form.validate_on_submit():

		try:
			print("************* Form submitted. Running code for: " + str(form.sum_name.data))
			logging.info(form.sum_name.data + ', ' + form.region_id.data)

			personal_results = recommend_from_summoner_name(form.sum_name.data, form.region_id.data, profiles, champs)
			personal_results = get_top_bot(personal_results)
			for result in personal_results[0]:
				result.append(get_img_paths(result[0], champ_img_conv))
			for result in personal_results[1]:
				result.append(get_img_paths(result[0], champ_img_conv))

			return render_template('home.html', form=form, results=personal_results)

		except ValueError:
			logging.error('ValueError on ' + form.sum_name.data + ', ' + form.region_id.data)
			print("*************No tables found for " + form.sum_name.data + " in region " + form.region_id.data)
			err = "The Recommender couldn't find any data for " + form.sum_name.data + " in " + form.region_id.data + ". Make sure you entered your info correctly."
			return render_template('home.html', form=form, err=err)

		except ZeroDivisionError:
			logging.error('ZeroDivisionError on ' + form.sum_name.data + ', ' + form.region_id.data)
			print("*************No suitable champions found for " + form.sum_name.data + " in region " + form.region_id.data)
			err = "It looks like " + form.sum_name.data + " in " + form.region_id.data + " doesn't have enough games from the current season. Make sure you update your op.gg page and consider playing more games if you only have a few listed there."
			return render_template('home.html', form=form, err=err)


		except:
			logging.error('Unknown error on ' + form.sum_name.data + ', ' + form.region_id.data)
			print("*************Something unknown went wrong")
			err = "Something went wrong. Maybe I shouldn't have coded the Recommender as minions..."
			return render_template('home.html', form=form, err=err)

	return render_template('home.html', form=form)

# @app.route('/results')
# def results():
# 	return render_template('results.html', champions=champions, title='Jabr')

# @app.route('/about')
# def about():
# 	return render_template('about.html')


if __name__ == '__main__':
	app.run(threaded=True)
