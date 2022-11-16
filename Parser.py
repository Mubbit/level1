

class ParseText:
    def __init__(self):
        self.dir=""
        self.stopwords=pd.DataFrame(columns=['vocab','pos'])
        self.data=[]
        self.parsedData=[]
        self.kkma=None
    #No json
    
    
    #limit    
    def openAllJsonTest(self,dirname,limit=0): #"./2020-02-019.도서자료요약_Sample"
        self.dir+=dirname## get path
        #1) open json file
        jsonobj=[]
        
        for file in os.listdir(dirname):
            if limit<0:
                break
            jsonfd=open(dirname+"/"+file, encoding="utf-8")## get file descriptor
            jsonstr=jsonfd.read()## get str
            jsonobj.append(jsonstr)
            limit-=1
        
        return jsonobj
    #no limit
    def openAllJson(self,dirname): #"./2020-02-019.도서자료요약_Sample"
        self.dir+=dirname## get path
        #1) open json file
        jsonobj=[]
        
        for file in os.listdir(dirname):
 
            jsonfd=open(dirname+"/"+file, encoding="utf-8")## get file descriptor
            jsonstr=jsonfd.read()## get str
            jsonobj.append(jsonstr)

        
        return jsonobj
    
    def organizeFile(self,jsonobj):
		#2) select passages and summaries
        file=json.loads(jsonobj)
        return {'id':file["passage_id"],'passage':file["passage"],'summary':file["summary"]}
    
    #limited
    def organizeFiles(self,dirname):
        jsonobj=self.openAllJson(dirname)
        for i in range(len(jsonobj)):
            self.data.append(self.organizeFile(jsonobj[i]))
            
    #no limit
    def organizeFilesTest(self,dirname,limit=10):
            jsonobj=self.openAllJsonTest(dirname,limit=limit)
            for i in range(len(jsonobj)):
                self.data.append(self.organizeFile(jsonobj[i]))
        
    
    def setStopwords(self,path):#stopwords.txt
        self.kkma=Kkma()
        f=open(path,encoding="utf-8")
        self.stopwords=pd.concat((self.stopwords,pd.DataFrame(self.kkma.pos(f.read()),columns=['vocab','pos'])),axis=0)
    
    def preprocessFile(self,data):
        kkma=Kkma()
        passage=data['passage']
        word_dict=pd.DataFrame(columns=['vocab','pos','mundan_id','sent_id','eojeol_id'])
        for i,mundan in enumerate(passage.split('\n')): #i는 n 번째 문단이라는 뜻
            for j, sent in enumerate(mundan.split('.')):#j 는 n번째 문장이라는 뜻
                for k, word in enumerate(sent.split(' ')):#k는 n번째 어절이라는 뜻 
                    passage_hs=kkma.pos(word) #list in list
                    for hs in passage_hs: #어절 내부의 위치는 기록하지 않는다. 어절은 통째로 뺄 것이기 때문이다. 
                        position=[i,j,k]+list(hs)
                        current=np.reshape(np.array(position),(1,-1))
                        current=pd.DataFrame(current,columns=['mundan_id','sent_id','eojeol_id','vocab','pos'])
                        word_dict=pd.concat((word_dict,current),axis=0)

                

        return word_dict


    def preprocessFiles(self,stoppath,stop=0):
        if stop==0:
            self.setStopwords(stoppath)
        #new passage object with words-->words & PoS tuples / only NNG, VV
        for d in self.data:
            word_PoS_pos=self.preprocessFile(d)
            #품사,stopwords 필터, 재정렬
            filtered=word_PoS_pos[(word_PoS_pos.pos=='NNG')|(word_PoS_pos.pos=='VV')&(~word_PoS_pos['vocab'].isin(list(self.stopwords.vocab)))].reset_index()
            self.parsedData.append(filtered)
        return self.parsedData
    
    def doAll(self,type=0,dr=None,stop=None):
        if type==0:
            dirname=input('dirname of jsonobj directory')
            stoppath=input('dirname of stopwords txt')
        else:#need work
            dirname=dr
            stoppath=stop
        self.organizeFiles(dirname)
        data_stack=self.preprocessFiles(stoppath)
        return data_stack
    def doAllTest(self,dirname,stoppath,limit):

        self.organizeFilesTest(dirname,limit=limit)
        data_stack=self.preprocessFiles(stoppath)
        return data_stack

