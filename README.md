<h1 align="center" style="font-size:100%;"> 
Progetto APMD 
  <p> Anno accademico: 2021-2022</p>
  <p style="font-size:50%;"> di Giuseppe Martinelli & Sindi Ruci</p>
</h1>
<b>Costruzione del grafo</b>:
<p>La prima parte del progetto si concentra sulla costruzione di un grafo bipartito dai dati che sono stati forniti dal docente, in particolare abbiamo utilizzato la libreria <i>pandas</i> per quanto riguarda il caricamento e l'analisi dei dati dal file fornito. Il dataframe dei dati caricati da file sono stati analizzati linearamente attraverso il seguente codice:
<pre><code>
for x, y in zip(data[0], data[1]):
  build_dictionaries_and_graph(x, y)
</code></pre>
La scelta di iterare in questo modo il dataframe di pandas non è dettata dal caso, infatti abbiamo condotto un indagine sui metodi e le euristiche più efficienti per questo scopo. Da questa analisi abbiamo concluso che il metodo migliore (e presentato dal codice di sopra) è quello delle <i>list comprehension</i> che ci permettono di girare i contenuti del dataframe in una decina di secondi (parte della documentazione che abbiamo visionato risiede in questi links: <a href="url">https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas</a>, <a href="url">https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#essential-basic-functionality</a>).</p>
<p>Dopo il caricamento e l'analisi dei dati abbiamo costruito diverse strutture dati che ci potessero permettere di poter tenere traccia di diverse informazioni. Infatti dal momento in cui ogni nodo del grafo è identificato da un id univoco dobbiamo <mark>tener traccia della coppia <id,film/attore></mark> in modo tale da poter identificare quel nodo. Le strutture create sono state le seguenti:
<dl>
<dt><b>actor_dic = {}</b></dt><dd>Dizionario che tiene traccia dell'attore e del suo id univoco (ogni nodo del grafo ha un id)</dd>
<dt><b>movie_dic = {}</b></dt><dd>Dizionario che tiene traccia dell'film e del suo id univoco</dd>
<dt><b>reverse_movie = {}</b></dt><dd>Dizionario ordinato per id attore e nome</dd>
<dt><b>reverse_actor = {}</b></dt><dd>Dizionario ordinato per id film e nome</dd>
<dt><b>movie_actors_dic = {}</b></dt><dd>Dizionario che tiene traccia per ogni film della lista di attori(il loro id) che hanno partecipato a quel film</dd>
<dt><b>edge_list = []</b></dt><dd>Lista contenete tutti gli archi del grafo, dove per arco si modella la partecipazione di un attore ad un determinato film</dd>
</dl>
La costruzione del grafo avviene in circa 60s e viene svolta nella funzione <i>def create_graph(data)</i> dove si ha anche la creazione di tutte le strutture dati di support sopra citate. Con la costruzione del grafo effettuata, siamo passati alla seconda parte del progetto dove ci siamo concentrati sul rispondere alle seguenti domande
<h1>Domande svolte:</h1>
<ol type="I">
<li>Which is the movie with the largest number of actors, considering only the movies up to year x?</li>
<li>Compute exactly the diameter of G</li>
<li>Who is the actor who had the largest number of collaborations? If actor A and B collaborated twice, this count 2.</li>
</ol>
