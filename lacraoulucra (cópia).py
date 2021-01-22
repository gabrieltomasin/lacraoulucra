import requests
import time
import tweepy

#START API
auth = tweepy.OAuthHandler()#AUTHENTICATION STRING HERE
auth.set_access_token()#ACCESS TOKEN STRING HERE
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
#CHECAR ID GUARDADO
while True:
    try:
        sinceid_guardado = open("sinceid.txt" , "r")
        sinceid_guardado = sinceid_guardado.read()
        sinceid_guardado = sinceid_guardado.split()
        sinceid = int(sinceid_guardado[0])
    except:sinceid = None
#LISTA DE MENÇÕES
    time.sleep(30)
    mentionlist = api.mentions_timeline(since_id=sinceid, count=5)




    try:
        recent_mention = mentionlist[0]
        recent_mention_id = recent_mention.id_str
        if sinceid == None or sinceid < int(recent_mention_id):
            sinceid = int(recent_mention_id)
            sinceid_guardado = open("sinceid.txt" , 'w+')
            sinceid_guardado.write(recent_mention_id)
            sinceid_guardado.close()
    except:pass




    #PEGAR NOME DO FILME NO TWEET
    for mention in mentionlist:
        tweet = mention.text.split()
        if tweet[-1].lower() == "lucrou?":
            print(mention.text)
            tweet.pop(-1)
            while tweet[0].startswith('@'): tweet.pop(0)
            moviename = ' '.join(map(str, tweet))
            #PEGAR ID DO FILME
            url = "https://imdb-api.com/pt-BR/API/SearchTitle/k_f5om16yw/%s" % (moviename,)
            print(url)
            payload = {}
            headers= {}
            response = requests.request("GET", url, headers=headers, data = payload)
            id = response.json()['results'][0]['id']
            #PEGAR OS LUCROS DO FILME
            url = 'https://imdb-api.com/pt-BR/API/Title/k_f5om16yw/%s' % (id,)
            response = requests.request("GET", url, headers=headers, data = payload)
            montante = response.json()['boxOffice']['cumulativeWorldwideGross']
            if len(montante) < 2:
                api.update_status(status = '@' + mention.user.screen_name + ' Desculpe, mas o IMDB não possui todas as informações sobre os lucros dessa produção', in_reply_to_status_id = mention.id)
                continue
            montante = montante.replace('$','')
            montante = montante.replace(',','')
            while montante.isdigit() is False: montante = montante[:-1]
            try: montante = int(montante)
            except: pass
            gasto = response.json()['boxOffice']['budget']
            if len(gasto) < 2:
                api.update_status(status = '@' + mention.user.screen_name + ' Desculpe, mas o IMDB não possui todas as informações sobre os lucros dessa produção', in_reply_to_status_id = mention.id)
                continue
            gasto = gasto.replace('$','')
            gasto = gasto.replace(',','')
            while gasto.isdigit() is False: gasto = gasto[:-1]
            try: gasto = int(gasto)
            except: pass
            print("montante:", montante)
            print("gasto:", gasto)
            try:
                lucro = montante - gasto
                print("\nLUCRO:", lucro)
            except: pass
            if lucro > 0: api.update_status(status = '@' + mention.user.screen_name + ' Esta produção lucrou $'+str(lucro)+',00. O lacre lucrou dessa vez', in_reply_to_status_id = mention.id)
            else: api.update_status(status = '@' + mention.user.screen_name + ' Esta produção lucrou $'+str(lucro)+',00. O lacre não lucrou dessa vez', in_reply_to_status_id = mention.id)
        else: print("tweet não contém 'lucrou?'")
