from flask import Flask,request,render_template
import pickle
import requests
from patsy import dmatrices

movies=pickle.load(open('model/movies_list.pkl','rb'))
similarity=pickle.load(open('model/similarity_list.pkl','rb'))

current_movie_id=0
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
   
        
    data = requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path



def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    print(index)
    distance=sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x:x[1])
    recommended_movies_name=[]
    recommended_movies_poster=[]

   
    current_movie_id=movies.iloc[index].movie_id
    print("😂😊🤦‍♀️👍😎😎😉😉😉😎👍😁")
    print(current_movie_id)

    current_movie_poster=fetch_poster(current_movie_id)

    for i in distance[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name,recommended_movies_poster,current_movie_poster,current_movie_id


app = Flask(__name__)

@app.route("/")
def hello():
    movies_list=movies['title'].values
    return render_template('index.html', movies_list=movies_list)


@app.route("/about")
def about():
    
    return render_template('about.html')




@app.route("/recommendation",methods=['GET','POST'])
def recommendation():
    movies_list=movies['title'].values
    if request.method=='POST':
        try:
            if request.form:
                movies_name=request.form['movies']
                recommended_movies_name,recommended_movies_poster,current_movie_poster,current_movie_id=recommend(movies_name)

                with open('integer.pkl', 'wb') as file:
                    pickle.dump(current_movie_id, file)
                
                
                
                print(type(recommended_movies_name[0]))
              
                print(recommended_movies_name[0])




                return render_template('film.html',movies_name=recommended_movies_name, poster=recommended_movies_poster, movies_list=movies_list,current_movie_poster=current_movie_poster,current_movie_id=current_movie_id)

        except Exception as e:
            error={'error':e}
            return render_template('film.html',movies_list=movies_list,error=error)  
    
    else:
        return render_template('film.html',movies_list=movies_list)
    


@app.route("/videos")
def videos():
    
    print("videos call ho raha hai")

    with open('integer.pkl', 'rb') as file:
        pick_value = pickle.load(file)
        print(pick_value)
        current_movie_id=pick_value


    print("🐱‍👓🐱‍💻🐱‍🏍🐱‍💻")
    print(current_movie_id)
    


    
    return render_template('video.html', current_movie_id=current_movie_id)










if __name__=='__main__':
    app.debug=True
    app.run()