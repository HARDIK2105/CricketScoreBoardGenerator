import re
from win10toast import ToastNotifier
import bs4,requests,time

class Cricbuzz:




	url='http://www.cricbuzz.com/cricket-match/live-scores'
#Cricbuzz url for live section
	
	try:#When no package is sent from the 'url' (in case of no internet connection or denied permission)
		res=requests.get(url)
		res.raise_for_status()
		soup=bs4.BeautifulSoup(res.text,'html.parser')
	except Exception as exc:
		print('There was a problem: %s' % (exc))
		exit()
	



	def display_all_scheduled_matches(self):
#list of all matches including domestic and international
		score=self.soup.find_all('li',{'class':'cb-lst-mtch cb-lst-dom'})
		for i in score:
			print(i.text.ljust(70)+' '*5+i.find('a').get('href').ljust(120))
		    



	
	def matches(self):
#Gives the matches that are displayed in the header menu of cricbuzz
		menu_bar=self.soup.find_all('a',class_='cb-mat-mnu-itm cb-ovr-flo')
		matches=[]
		match_urls=[] 

		for i in list(menu_bar):
			#print(i.string)
			matches.append(i.text)
			match_urls.append(i.get('href'))
		return matches,match_urls
		#returns match names and their urls with the same index

	def live_matches(self):
 #Gives the list of live matches 
		matches,match_urls=self.matches()
		live_matches_urls=[]
		live_match=[]

		#Regular expression to find the live matches from the return list of 'matches' function
		live=re.compile(r'Live')
		for i in range(len(matches)):
			if(live.search(matches[i])!=None):
				live_matches_urls.append(match_urls[i])
				live_match.append(matches[i])

		
		try:#If there are no live matches currently going on 
			if(len(live_match)==0):
				raise Exception('No current live matches')
			for n in range(len(live_match)):
				print(str(n+1)+" "+live_match[n])
			
			i=int(input('Give the no of live match to be displayed'))
			return live_matches_urls,live_match,i
#Return the list of live mathces ,live urls,and the opted live match to be displayed

		except Exception as err:
			print(str(err)+'\nTry again after some time')
			return 'no url','no live matches',0
#Returning false url,false match name,and ambigious index of the match

	def show_live_score(self,score_of_url,score_of_match,j):
		#To show the live score of the jth match from the list returned from function 'live_matches'
		flag=0
		while flag!=1:

			


			score_url='https://www.cricbuzz.com'+score_of_url[j-1]#URL of the desired match to be notified
			try:
				ret=requests.get(score_url)
				ret.raise_for_status()
				soup=bs4.BeautifulSoup(ret.text,'html.parser')
			except Exception as exc:
			
				exit()
			toaster=ToastNotifier()
			#For windows only


			won=re.compile(r'won')#Regular expression to recognise the completion of current displayed match 

			if(won.search(score_of_match[j-1])!=None):
				flag=1
				score=soup.find('div',{'class':'cb-col cb-col-67 cb-scrs-wrp'})
				ans=soup.find('div',{'class':'cb-col cb-col-100 cb-min-stts cb-text-mom'})
				
#Display changes once the match is completed ,so final score is displayed here,whose string is different from the live
				final=score.text.split()
				print(final)
				final_score=''
				for i in final:
				    final_score=final_score+i+' '
				    if(i=='Ovs)'):
				        final_score=final_score+'\n'
				final_score=final_score+'\n'+ans.text.strip()
				toaster.show_toast(score_of_match[j-1],final_score, duration=5)

				break
				

			
			in_progress=soup.find('div',{'class':'cb-text-inprogress'})
			bat_board=soup.find('div',{'class':'cb-min-bat-rw'})
			fielding_board=soup.find('div',{'class':'cb-col cb-col-67 cb-scrs-wrp'})



			z=fielding_board.text.split()[0:4]

			field=''
			for i in z:
				field=field+i+' '

			a=bat_board.text.split()
			bat=''
			for i in a:
				bat=bat+i+' '


				
			display=field+'\n'+bat+'\n'+in_progress.text.strip()


			
      
			toaster.show_toast(score_of_match[j-1],display, duration=5)
 #First parameter is the Header containing name of the live match,Second paremeter is the notification content to be displayed
      			while toaster.notification_active(): time.sleep(0.1)
			

			time.sleep(10)


z=Cricbuzz()
l,m,i=z.live_matches()
z.show_live_score(l,m,i)









		



