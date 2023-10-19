#!/usr/bin/env python
# coding: utf-8

# ##### <center>  <img src="https://images.squarespace-cdn.com/content/v1/551a19f8e4b0e8322a93850a/1602020393443-L6M0DGZK4C75DRNR7GZH/Title_Animation.gif"  width=600> [[1]](#źr)
# 
# 
# 

# <h2 class="alert alert-block alert-danger">  
# Projekt ten przedstawia mój tok myślenia oraz opinie! Wersja z czystą analizą dostępna jest na:    
# </h2>

# ## Jako osoba która pracowała na kuchni i dla której temat jedzenia jako część kultury jest niezwykle fascynujący, w tym notatniku zajmę się analizą bazy danych z WHO na temat konsumpcji produktów na świecie. Moim planem jest odpowiedzieć na pytania, jakie produkty są najpopularniejsze i na co to wskazuje, jakie są różnice między kobietami i mężczyznami oraz jak te dane można by wykorzystać tworząc menu do restauracji. Myślę, że w tych danych jest wiele ciekawych informacji, które można wykorzystać do odpowiedzenia na wspomniane pytania jak i do pogłębienie wiedzy na temat tredów konsumcyjnych w różnych rejonach świata.
# ## może bardziej pojśc w to że czym różni się otwarcie restauracji w Europie niż na świecie? że czy różnica między kobietami i mężczyznami by sprawiała że profilowanie restauracji pod płeć ma sens? czy celowanie w ogólnoświatowe gusta ma sens czy lepiej iśc w lokalne? myśle że w to i na podstawie tego podsumowania i wnioski
# ### 📝 Plan jest następujący:
# 1. Sprawdzę jak skonstruowana jest baza danych, jakie informacje i typy danych znajdują sie w kolumnach.
# 1. Z tą wiedzą pozbędę się kolumn, które na pewno nie będą mi potrzebne no chyba, że takich nie będzie.
# 1. Następnie dokonam analizy, gdzie znajdują sie puste dane oraz gdzie jest największe ryzyko ich znajdowania się, a potem pozbędę sie ich.
# 1. Sprawdzę z jakich krajów i kontynentów jest najwięcej danych, żeby ocenić ich używalnośc w globalnej skali.
# 1. Kolejną rzeczą będzie wyciagniecie danych dla produktów spożywanych na całym świecie, w Europie oraz to samo dla mężczyzn i kobiet na świecie i w Europie.
# 1. Na koniec podsumuję co udało się osiągnąć, jakie były wyzwania, problemy, błędy, sukcesy.
# ### Taki jest plan ale co napotkam na tej drodze to się okaże. Liczę na to że będzie ciekawie! 

# # <font  color='289C4E'>Spis treści:<font><a class='anchor' id='top'></a> 📕
# 1. [Wczytywanie danych](#hello)
# 1. [Usuwanie niepotrzebnych kolumn](#del_col)
# 1. [Ujednolicanie danych](#stand)
# 1. [Usuwanie duplikatów i pustych danych](#del_dup)
# 1. [Wyciąganie informacji z kolumn Consumers_Mean, Consumers_Median, Total_Mean, Total_Median](#colinfo)
# 1. [Sprawdzanie z jakich krajów pochodzą dane](#kraje)
# 1. [Problem z kolumną AgeClass](#ageclass)
# 1. [Wykres: Ilość badanych na przestrzeni lat](#sub_over_time)
#     1. [Wnioski](#sub_over_time_wnio)
# 1. [Wykres: Ilość badanych dla poszczególnych krajów](#country_sub)
#     1. [Wnioski](#country_sub_wnio)
# 1. [Tworzenie kolumn z kodami i nazwami kontynentów](#kont)
# 1. [Wykres: Procentowy udział badanych patrząc na kontynent](#kont_sub)
#     1. [Wnioski](#kont_sub_wnio)
# 1. [Wykres: Najpopularniejsze produkty na Świecie](#food_world)
# 1. [Wykres: Najpopularniejsze produkty w Europie](#food_eu) 
# 1. [Wykresy: Porównanie wykresów najpopularniejsze produkty na świecie i w Europie](#food_world_eu)
#     1. [Wnioski](#food_world_eu_wnio)
# 1. [Wykresy: Najpopularniejsze produkty dla mężczyzn i kobiet na Świecie](#food_world_gen) 
#     1. [Wnioski](#food_world_gen_wnio)
# 1. [Wykresy: Najpopularniejsze produkty dla mężczyzn i kobiet w Europie](#food_eu_gen)    
#     1. [Wnioski](#food_eu_gen_wnio)    
# 1. [Podsumowanie](#Podsumowanie)    
# 1. [Możliwe zakłamania](#risk)
# 1. [Źródła](#źr)   
#     

# In[102]:


# import bibliotek oraz ustawienia
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import pycountry_convert as pc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from dash import dcc, html, Input, Output
from jupyter_dash import JupyterDash
import plotly.io as pio
pio.renderers.default = "notebook_connected" # bez tego nie wyswietlają mi sie wykresy kiedy eksportuje je do htmla
plt.style.use('fivethirtyeight')


# # Wczytywanie danych <a id="hello"></a>[&uarr;](#top) [[2]](#źr)

# In[103]:


food = pd.read_csv("fullcifocoss.csv", on_bad_lines='skip', sep=';', skipinitialspace = True)  # wczytanie danych do dataframe pozbywając sie rzędów, które mają za dużo pól oraz spacji
pd.set_option('display.max_columns', None) # sprawiam, że można przejrzeć wszystkie kolumny, ponieważ by deafault ilość wyświetlanych kolumn jest ograniczona
food.head()


# # Usuwanie niepotrzebnych kolumn <a id="del_col"></a>[&uarr;](#top)

# In[104]:


food.drop(columns=food.loc[:, 'Consumers_P05':'Consumers_Standard_deviation'], inplace=True)
food.drop(columns=food.loc[:, 'Total_P05':'ExtBWValue'], inplace=True)
food = food.drop(['BW'], axis=1)
food.head(10)


# In[105]:


food.shape


# ### Sprawdzę czy typy danych w kolumnach się zgadzają

# In[106]:


food.dtypes


# ### Wszystkie kolumny mają dobre typy danych

# ### Ze względów estetycznych ustawię by dane miały dwie liczby po przecinku. Jest to moja preferencja, a w razie potrzeby wrócenie do ustawień deafaultych nie będzie problematyczne.

# In[107]:


pd.set_option('display.float_format', lambda x: '%.2f' % x)
food.head()


# ### <a id="stand"></a>[&uarr;](#top) Również rzuca mi się w oczy to że female i male w kolumnie Gender zaczynają się z małej litery a All z dużej. Przypomina mi to o tym żeby ujednolicić stringi. Zrobię to dla wszystkich kolumn zawierających stringi poza FoodCode bo mogło by w przyszłosci mieć to znaczenie podczas wczytywania kodów.

# In[108]:


food.loc[:, 'Country'] = food.loc[:, 'Country'].str.title()
food.loc[:, 'FoodName'] = food.loc[:, 'FoodName'].str.title()
food.loc[:, 'AgeClass'] = food.loc[:, 'AgeClass'].str.title()
food.loc[:, 'SourceAgeClass'] = food.loc[:, 'SourceAgeClass'].str.title()
food.loc[:, 'Gender'] = food.loc[:, 'Gender'].str.title()
food.head()


# ### Wszystko bardzo ładnie się udalo i mam ujednolicone stringi.

# # <a class="anchor" id="del_dup">Usuwanie duplikatów i pustych danych.</a> [&uarr;](#top)

# In[109]:


food.shape


# In[110]:


food = food.drop_duplicates()


# In[111]:


food.shape


# In[112]:


544686-519881


# ### Tym prostym sposobem pozbyłem się 24805 duplikatów.

# ### Przy użyciu biblioteki missingno oraz metody isna sprawdzam, gdzie znajdują sie puste dane.
# 

# In[113]:


msno.bar(food)


# In[114]:


food.isna().sum()


# ### Zarówno na wykresie jak i w tabeli widać, że FoodName i FoodCode mają puste wartości, wiec zajmuję sie usunięciem tych rzędów. (na razie nie zajmuję sie innymi kolumnami z pustymi watościami, bo nie wiem czy będą użyteczne).

# In[115]:


null_data = food[food.isnull().any(axis=1)]
null_data.tail(5) # NaN w FoodCode widać dopiero na 50 ale dla wygody pozostaje default


# In[116]:


food.loc[527540]


# ### Teraz widać, że zarówno w kolumnie FoodName i FoodCode puste dane są opisane jako NaN. Dodatkowo w kolumnie FoodCode widzę, że jest kod znacząco dłuższy od innych, które na razie widziałem i znajduje się on zawsze tam gdzie jest pusta wartość dla FoodName. Na podstawie tego decyduję, żę dobrym rozwiązaniem jest usunięcie rzędów w których FoodName ma wartości NaN bo nawet jeżeli kody są dobre to bez wiedzy jaki produkt one oznaczją są one bezużyteczne. Następnie zobaczę czy po tym nadal pozostaną długie kody i puste wartości w FoodCode. Prawdopodobnym powodem pustych danych jest błednie podany kod produktu co skutkuje tym, że nie ma również nazwy produktu ale to się okaże dalej.

# In[117]:


food = food.dropna(subset=['FoodName'])


# In[118]:


food.isna().sum()      


# ### Usuwanie pustych danych powiodło się. Poprzez usuwanie pustych danych z FoodName usnąłem też przy okazji puste dane z FoodCode. Teraz chcę sprawdzić czy długość kodu miała znaczenie. Zrobię to najpierw na przykładzie kodu który widziałem czyli fa6adbfab52e8a77f23df411f59c2150 oraz sprawdzając kody o długości większej niż 5 czyli standardowej długości, którą widziałem. 

# In[119]:


food.loc[food['FoodCode'] == "fa6adbfab52e8a77f23df411f59c2150"]


# In[120]:


temp = food['FoodCode'].str.len() > 5
temp.value_counts()


# ### Wychodzi na to, że pozbyłem się kodu fa6adbfab52e8a77f23df411f59c2150, ale kody o długości większej niż 5 nadal istnieją i jest ich znacząco mniej, więc sprawdzę teraz czy one są poprawne, chociaż na razie wszystko wskazuje na to, że nie powinno być z nimi problemu.

# In[121]:


checkpoint = food #tworzę checkpoint żeby móc łatwo wrócić do wersji przed sortowaniem
food['CodeLen'] = food['FoodCode'].str.len()
food.sort_values(by=['CodeLen'])


# In[122]:


temp = food.loc[food['FoodCode'] == "a93a0316b93a7c2af9305e90012af119"]
len(temp)


# ### Moje przypuszczenia zostały potwierdzone, puste dane nie są zależne od długości kodu, więc w tych kwestiach nie ma o co się martwić. 

# ### <a id="colinfo"></a>[&uarr;](#top) Teraz zajmę się kolumnami Consumers_Mean, Consumers_Median, Total_Mean, Total_Median. Jako że nie mam legendy to nie wiem co dokładnie one znaczą i zakładanie co znaczą oraz wiara że posiadają dobre wartości może być zgubna

# In[123]:


food = checkpoint # powrót do checkpointa
food.head()


# ### martwi mnie kwestia że Total_Median, Consumers_Median mają wartości 0,kiedy mediana nie powinna w takim przypadku mięc zerowych wartości

# In[124]:


food['Consumers_Mean'].loc[food['Consumers_Mean'] == 0].count() ,food['Consumers_Median'].loc[food['Consumers_Median'] == 0].count(),food['Total_Mean'].loc[food['Total_Mean'] == 0].count(),food['Total_Median'].loc[food['Total_Median'] == 0].count()


# In[125]:


food['Consumers_Mean'].count()


# ### Total_median ma prawie 500 000 wartości 0. Totalnie dyskfalifikuje to używalność używalność tej kolumny. podobnie z Total_mean, niezależnie co ona znaczy niemożliwe żeby aż w 1/4 wyników miała tym bardziej że one występują w rzedach które mają dane. Dla mnie wyklucza to totalnie używalność tych kolumn. 

# ### Consumers_Mean i Consumers_Median mają mniej zerowych wartości ale nadal dużo ale spróbuję na przykładzie chin dla oat grain sprawdzić czy te wartości może mają jakiś sens.

# In[126]:


food_all = food.loc[food['Gender'] == "All"]
food_all_oat = food_all.loc[food_all['FoodName'] == "Oat Grain"]
food_all_oat_ch = food_all_oat.loc[food_all_oat['Country'] == "China"]
food_all_oat_ch


# ### Tutaj pojawiło się pare ciekawych rzeczy. Po pierwse to to żę dane są podwojone dla wszystkich kolumn nie licząc Consumers_Mean, Consumers_Median, Total_Mean, Total_Median. Dodatkowo polowa danych z Consumers_median i total_mean ma wartości NaN. Na tym przykładzie widać że Consumers_Median i Total_Median sa dla mnie bezużytecznymi kolumnami bo niektórych przypadkach nie dadzą mi w ogóle informacji wiec już teraz moge ustalić ze ich się pozbywam wiec jedynie consumers mean może być użyteczne i to to sprawdzę czy posiada sensowne wartości. Tylko martwi mnie to żę dane są podowjone, a dane consumers mean dwa razy są różne prawdopodobnie ta kolumna też do wyrzucenia jest. 

# In[127]:


food.isna().sum()


# ### Czyli dochądzą kolejne bezużyteczne dane w tych kolumnach.

# In[128]:


food_all_oat_ch['Consumers_Mean'].iloc[0] 


# In[129]:


1157/66172*100 # procent konsumentów z całej puli badanych 


# In[130]:


66172/1157 #liczba badanych podzielona przez liczbę konsumentów


# In[131]:


(1.12+66172)/1157 # połączona liczba badanych podzielona przez liczbę konsumentów


# In[132]:


food_all_oat_ch['Consumers_Mean'].iloc[1:7].sum() # suma średnich dla rzędów 1-6


# In[133]:


food_all_oat_ch['Consumers_Mean'].iloc[1:7].mean() # średnia ze średnich


# In[134]:


food_all_oat_ch['Number_of_consumers'].iloc[:7].mean() # średnia z pierwszyć 7 rzędów


# In[135]:


food_all_oat_ch['Number_of_consumers'].iloc[0]/food_all['Number_of_consumers'].iloc[1:7].sum() # wartość dla all podzielona przez sume wartości rzędów 1-6


# ### Żadne obliczenia nie daja takiej wartości jaka jest w kolumnie Consumers_Mean, więc albo są to jakieś inne dane, np. średnia ilość gramów spożywanego produktu przez ankietowanych albo coś zupełnie innego, ale bez odpowiedniej wiedzy nie można tego założyć. Znaczy to, że tych kolumn też trzeba sie pozbyć, gdyż nawet gdyby były pomocne, mogą one zawierać fałszywe wartości.
# ### Usuwam więc: Consumers_Mean, Consumers_Median, Total_Mean, Total_Median i dodatkowo CodeLen które i tak już nie będzie użyteczne dla mnie.

# In[136]:


food.shape


# In[137]:


food = food.drop(['Consumers_Mean', 'Consumers_Median', 'Total_Mean', 'Total_Median', 'CodeLen'], axis=1)
food.shape


# ### Wszystko poszło dobrze, pozbyłem się 5 kolumn, więc teraz czas na usuwanie duplikatów, zrobię to za pomocą drop.duplicates bo tak jak widziałem dane były podwojone i jedyne kolumny które uniemożliwiały usunięcie duplikatów przy wczesniejszym przywołaniu dropduplicates wiec samo to powinno bozbyc się niepotrzebnych danych

# In[138]:


food.shape


# In[139]:


food = food.drop_duplicates()
food.shape


# In[140]:


544032-272016


# ### Tak jak wczesniej zauważyłem dane były podwojone w całej bazie danych, więc bardzo dobrze, że to zauważyłem, bo inaczej mogło by to mocno zakłamać wyniki.
# ### <a id="kraje"></a>[&uarr;](#top) Sprawdzam z jakich krajów są dane dla wszystkich płci

# In[141]:


food_all = food.loc[food['Gender'] == "All"]
food_fem = food.loc[food['Gender'] == "Female"]
food_men = food.loc[food['Gender'] == "Male"]


# ### jeszcze przed tym dla upewnienia się sprawdze czy sumują się dobrze rzędy czy czegoś nie straciłem podczas przypisywania

# In[142]:


food_all['Country'].count() + food_fem['Country'].count() + food_men['Country'].count() - food['Country'].count()


# ### takie same ilości więc super

# In[143]:


food['Country'].nunique()


# In[144]:


food_all['Country'].nunique()


# In[145]:


food_fem['Country'].nunique()


# In[146]:


food_men['Country'].nunique()


# ### Niestety dane dla mężczyzn są z mniejszej ilości krajów, więc należy wziąć to pod uwagę przy analizie.
# ### Sprawdzę jakie kraje są zawarte w tych danych, czy all. fem mają takie same kraje oraz jakich krajów nie ma w men.

# In[147]:


food_all['Country'].unique()


# In[148]:


food_fem['Country'].unique()


# In[149]:


food_men['Country'].unique()


# In[150]:


np.setxor1d(food_fem['Country'].unique(), food_all['Country'].unique()) # używam setxor1d z biblioteki numpy żeby sprawdzić czy te same kraje są dla fem i all


# In[151]:


np.setxor1d(food_fem['Country'].unique(), food_men['Country'].unique()) # sprawdzam jakich krajów nie posiadają mężczyźni


# ### Jako że jestem przy temacie krajów to sprawdzę czy jest Polska tutaj

# In[152]:


food_all.loc[food_all['Country'] == "Poland"]


# ### Niestety nie ma jej więc wnioski będę wyciągać dla Europy.

# ### <a id="ageclass"></a>[&uarr;](#top) Będę chciał dane sprawdzać dla wszystkich group wiekowych bez rozdzielania dokładnie na grupy więc sprawdzę czy gdy tak filtruje to wszystko jest dobrze.

# In[153]:


food_all_all = food_all.loc[food_all['AgeClass'] == "All"]
food_fem_all = food_fem.loc[food_fem['AgeClass'] == "All"]
food_men_all = food_men.loc[food_men['AgeClass'] == "All"]
food_all_all.head()


# In[154]:


food_all_all['Country'].nunique()


# In[155]:


food_fem_all['Country'].nunique()


# In[156]:


food_men_all['Country'].nunique()


# ### O i tutaj jest duży problem przy takim rozdzieleniu ilości krajów są inne niż wczesniej sprawdzałem czyli muszę znaleźć inne rozwiązanie bo wynika z tego że ageclass all nie jest dla wszystkich krajów, niektóre kraje nie mają tego zgrupowanego

# In[157]:


np.setxor1d(food_all['Country'].unique(), food_all_all['Country'].unique())


# ### tak wstępnie patrząc to wydzhodi na to że z Europy kraje nie mją ageclass All. Na przykładzie Francji sprawdzę jak to dokładnie wygląda.

# In[158]:


food_fr = food.loc[food['Country'] == "France"] 
food_fr['AgeClass'].unique()
food_fr


# In[159]:


food_fr_wine = food_fr.loc[food_fr['FoodName'] == "Soft Drink, Flavoured With Herbs"] 
food_fr_wine.sort_values(by='SourceAgeClass')


# ### oznacza to że muszę znaleźć inny sposob na przedstawienie danych dla wszystkich grup wiekowych. rozwiązaniem może być nieużywanie ageclass all a za to samemu grupować dane dla danego produktu wykożystując to że każde badanie ma unikalną ilość badanych, jest tu ryzko że madania będą miały taka samą ilośc badanych ale na razie nie widzę innej opcji
# ### jako żenie będę rodzielać danych na konkretne grupy wiekowe to sama ich suma mi wystarczy wiec pozbycie sie all i zsumowanie wszystkich wartości robiąc to na podstawie tego że każde badanie ma inną ilośc badanych to nie powinno być tu problemu ale upewnię się
# ### widać że dane female+male=All więc wszystko się pod tym wzgledem zgadza oznacza to że przy rodzielaniu na płcie wszytko idzie dobrze. 

# In[160]:


food_all['Number_of_subjects'].nunique()


# ### znaczy to ze jest grupując tak dane będą z 243 badań brane czyli jest to dobra próba badanych. może znajdę lepszy sposob ale na razie wydaje sie to być najlepsze. 
# ### sprawdzę jeszcze na przykładzie chin dla oat grain czy wszystkie wartości dodane do siebie dają tą samą wartość co dla Ageclass All. 

# In[161]:


food_all_oat = food_all.loc[food_all['FoodName'] == "Oat Grain"]
food_all_oat_ch = food_all_oat.loc[food_all_oat['Country'] == "China"]

food_all_oat_ch


# In[162]:


food_all_oat_ch['Number_of_consumers'].iloc[1:].sum()-food_all_oat_ch['Number_of_consumers'].iloc[0]


# ### wynik jest 0 więc znaczy to że sumy są dobre. Czyli podsumowując moim pomysłem jest usunięcie rzędów z ageclass all i potem samodzielnei grupować dane wykorzstując zależnośc że badania mają różne ilości badanych. czyli teraz usuwam rzędy z ageclass all i wstępnie sprawdzę czy to dobrze działa

# In[163]:


food_fr = food_fr.loc[food_fr['Gender'] == "All"] 
food_fr['Number_of_subjects'].unique().sum() # chyba to będzie rozwiązaniem


# In[164]:


food_ctry = food_all.groupby(['Country','Number_of_subjects']).sum().reset_index()
food_ctry = food_ctry.groupby(['Country']).sum().reset_index()
food_ctry.loc[food_ctry['Country'] == "France"]


# In[165]:


food_ctry['Country'].nunique()


# ### wychodzi na to że ta metoda daję dobrą ilość badnaych wczęsniej zakłądana i nic nei trace w ten sposób a ilość krajów jest dobra

# In[166]:


sub_over_time = food_all.groupby(['Year', 'Number_of_subjects']).sum().reset_index()
sub_over_time = sub_over_time.groupby(['Year']).sum().reset_index()
sub_over_time['Number_of_subjects'].sum()


# In[167]:


mask = food['AgeClass']== 'All'
food = food[~mask]


# In[168]:


food_all = food.loc[food['Gender'] == "All"]
food_fem = food.loc[food['Gender'] == "Female"]
food_men = food.loc[food['Gender'] == "Male"]


# In[169]:


food_all.count() + food_fem.count() + food_men.count() - food.count() 


# ### wychodzi 0 czyli wszystko jest dobrze i nie ma strat

# In[170]:


food_all['Country'].nunique()


# In[171]:


food_fem['Country'].nunique()


# In[172]:


food_men['Country'].nunique()


# ### ilości krajów się zgadzają
# ### chyba wszystkie dane są wyczyszczone i uporządkowane żeby móc robić wykresy, wiem jak osiągnąć najbardziej zbliżony do rzeczywistości wynik wiec wiec wszystko powinno być fine
# ### sprawdzam przy jakim grupowaniu suma Number_of_subjects jest najwieksza i z tej będę kożystac. tak samo będę robić przy innych wykresach

# In[173]:


sub_over_time = food_all.groupby(['Year', 'Number_of_subjects','SourceAgeClass']).sum().reset_index()
sub_over_time = sub_over_time.groupby(['Year']).sum().reset_index()
sub_over_time['Number_of_subjects'].sum()


# # 📊 Wykres: Ilość badanych na przestrzeni lat.<a id="sub_over_time"></a> [&uarr;](#top)

# In[174]:


hello = px.line(sub_over_time, x="Year", y="Number_of_subjects", title="over time", labels={'Number_of_subjects':'Number of Subjects', 'FoodName': 'Food Names' } , hover_data={'Number_of_subjects':':,'})
hello.show()


# # Wnioski <a id="sub_over_time_wnio"></a> [&uarr;](#top)

# ### Jak widać dane są głównie z 202 i 2010. Najwyraźniej wtedy było albo najwieksze badanie albo najwiecej badań. 

# In[175]:


food_2002 = food_all.loc[food_all['Year'] == 2002]
food_2002 = food_2002.groupby(['Number_of_subjects','SourceAgeClass']).sum().reset_index()
food_2002['Number_of_subjects'].unique()


# In[176]:


food_2010 = food_all.loc[food_all['Year'] == 2010]
food_2010 = food_2010.groupby(['Number_of_subjects','SourceAgeClass']).sum().reset_index()
food_2010['Number_of_subjects'].unique()


# ### jak widać głównie tutaj miały znaczenie duże badania ale również było troche tych badań wiec jest to zawsze plus bo zwiększa to wiarygodność i zmiejsza błąd z badań(jak to ianczej nazwać?)

# In[177]:


food_ctry = food_all.groupby(['Country', 'Number_of_subjects','SourceAgeClass','AgeClass']).sum().reset_index()
food_ctry = food_ctry.groupby(['Country', 'Number_of_subjects','SourceAgeClass']).sum().reset_index()
food_ctry = food_ctry.groupby(['Country']).sum().reset_index().sort_values(by='Number_of_subjects', ascending=False)

food_ctry['Number_of_subjects'].sum()


# # 📊 Wykres: Ilość badanych dla poszczególnych krajów.<a id="country_sub"></a>[&uarr;](#top)

# In[178]:


#testowanie dwustronnego suwaka

app = JupyterDash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(
        min=0,
        max=food_ctry['Number_of_subjects'].count(), # max i min wartości możliwe do wyświetlenia
        step=1,
        id='my-range-slider',
		value=[0,food_ctry['Number_of_subjects'].count()], #wartości wyswietlane na początku
    )
    
])

@app.callback( #porozumiewanie się graphu z suwakiem
    Output("graph-with-slider", "figure"), 
    Input('my-range-slider', 'value'))
def update_bar_chart(value): #funkcja updateująca wykres
    v1=value[0]
    v2=value[1] #dzięki takiemu rozdzieleniu mogę przekazać wartości do iloc
    dff = food_ctry.iloc[v1:v2] # wybieram z jakiego przedziału dane mają się pokazywać po nr rzędów
    fig = px.bar(dff, x="Country", y="Number_of_subjects", title="Number of subjects per country", labels={'Number_of_subjects':'Number of subjects', 'Country': 'Countries' },hover_data={'Number_of_subjects':':,'})
    fig.update_xaxes(tickangle=40) #pochylenie nazw na x żeby było łatwiej czytać 
    return fig
if __name__ == '__main__':
    app.run_server(mode='inline', port="8005") #mode inline po to żeby wyswietlało się w notebooku, a nie poza. Port dla każdego wykresu korzystającego z JupyterDash będzie inny bo 
    #inaczej pokazuje się ten sam wykres gdziekolwiek był użyty JupyterDash


# ### <a id="country_sub_wnio"></a>[&uarr;](#top) Na wykresie bardzo dobrze widać jak duża jest dysproporcja, co do ilości osób w zależności od kraju. Znaczy to, że wyciągnięte wnioski mogą być zachwiane i należy o tym pamiętać podczas analizy.
# ### Dla dokładności sprawdzę jak duża jest ta dysproporcja i jak rozkłada się to pod względem kontynentów.

# In[179]:


top5 = food_ctry['Number_of_subjects'].iloc[0:5].sum()
top5


# In[180]:


rest = food_ctry['Number_of_subjects'].iloc[5:].sum()
rest


# In[181]:


top5/rest


# ### Jak widać top 5 krajów ma 1.65 razy więcej badanych niż reszta krajów, jest to bardzo duża dysporporcja, lecz nie dyskredytuje to od razu analizy wszystkich danych.
# # Tworzenie kolumny z kodami i nazwami kontynentów. <a id="kont"></a>[&uarr;](#top)
# ### Rozbicie na kontynenty, pozwoli zobaczyć jak użyteczna będzie globalna analiza i czy nie lepiej będzie analizować, każdy kontynent odrębnie. Użyję do tego biblioteki pycountry_convert.

# In[182]:


def convert(row): # funkcja przypisująca kod kontynentu w zależności od kraju
    cn_code = pc.country_name_to_country_alpha2(row.Country, cn_name_format="default")
    conti_code = pc.country_alpha2_to_continent_code(cn_code)
    return conti_code


# ### Trzeba zamienić nazwy kilku krajów, bo biblioteka pycountry_convert korzysta z innych nazw krajów niż te które są w dataframe.

# In[183]:


continent = food
ctry_change = {
	'Republic Of Korea' : 'South Korea',
    'Bolivia (Plurinational State Of)' : 'Bolivia',
    'United States Of America' : 'United States of America',
    "Lao People'S Democratic Republic" : "Lao People's Democratic Republic",
    "Democratic Republic Of The Congo" : "Democratic Republic of the Congo"
}
continent = continent.replace(ctry_change)


# In[184]:


continent['ContinentCode'] = continent.apply(convert, axis=1)
continent


# ### Mam kody kontynentów, więc niby można by tak to zostawić ale uważam, że dużo ładniej i czytelniej jest jak będą też widoczne nazwy kontynentów.

# In[185]:


continent['ContinentCode'].unique()


# In[186]:


conti_names = {	# stworzenie słownika dla kontynentów, żeby móc zamienić kody kontynentów na nazwy kontynentów
				'AS' : 'Asia',
				'EU' : 'Europe',
                'NA' : 'North America',
                'SA' : 'South America',
                'AF' : 'Africa'
                }
continent['Continent'] = continent['ContinentCode'].map(conti_names)
continent


# In[187]:


continent['Continent'].unique()


# ### Jak widać wszystko ładnie się udało, więc mogę przypisać continent do food i ponownie stworzyć dataframes dla każdej płci.

# In[188]:


food = continent

food_all = food.loc[food['Gender'] == "All"]
food_fem = food.loc[food['Gender'] == "Female"]
food_men = food.loc[food['Gender'] == "Male"]


# In[189]:


food_con = food_all.groupby(['Country','SourceAgeClass','ContinentCode','Number_of_subjects']).sum().reset_index()
food_con = food_con[['ContinentCode','Number_of_subjects']].sort_values(by='Number_of_subjects', ascending=False)

food_con.sum()


# ### Ilość subjectów jest taka jak wczesniej czyli 312217 wiec super

# ###  Niestety kontynenty też są zgrupowane, więc muszę odciać wszystko poza pierwszymi literami kodu, co pozwoli to dobrze podsumować.
# 

# In[190]:


food_con['ContinentCode'] = food_con['ContinentCode'].apply(lambda x: x[0:2])
food_con = food_con.groupby(['ContinentCode']).sum().reset_index().sort_values(by='Number_of_subjects', ascending=False)
food_con


# ### Wszystko poszło dobrze, więc mogę teraz wizualizować, tylko jeszcze dodam nazwy kontynentów.

# In[191]:


food_con['Continent'] = food_con['ContinentCode'].map(conti_names)
food_con


# # 📊 Wykres: Procentowy udział badanych patrząc na kontynent.<a id="kont_sub"></a> [&uarr;](#top)

# In[192]:


fig = px.pie(food_con, values='Number_of_subjects', names='Continent', title='Percent of subjects per Continents',color_discrete_sequence=px.colors.sequential.RdBu, hover_data={'Number_of_subjects':':,'})
fig.show()


# ### <a id="kont_sub_wnio"></a> [&uarr;](#top) Na tym wykresie widać, ze rozłożenie badancyh między kontynentami nie jest takie złe. Wiadomo Afryka najgorzej wypada i gdyby chcieć wyciągnąć informacje dla Afryki, to można to robić tylko dla Afryki i nie sugerować się ogólnymi wynikami. Natomiast reszta kontynentów nawet równo się rozkłada, nadal dla dokładnych informacji należy sprawdzać konkretne kontynenty ale i tak już ogólna analiza może dać sensowne informacje.

# ### Teraz czas na sprawdzenie najpopularniejszych produktów

# In[193]:


most_consumed_all = food_all.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)
most_consumed_fem = food_fem.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)
most_consumed_men = food_men.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)
most_consumed_all[['FoodName','Number_of_consumers']].head(10)


# # 📊 Wykres: Najpopularniejsze produkty na świecie. <a id="food_world"></a>[&uarr;](#top)

# In[194]:


app = JupyterDash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(
        min=0,
        max=75, 
        step=1,
        id='my-range-slider',
		value=[0,30], 
    )
    
])

@app.callback( 
    Output("graph-with-slider", "figure"), 
    Input('my-range-slider', 'value'))
def update_bar_chart(value):
    v1=value[0]
    v2=value[1] 
    dff = most_consumed_all.iloc[v1:v2] 
    fig = px.bar(dff, x="FoodName", y="Number_of_consumers", 
       	title="Most popular foods in the World", 
       	labels={'Number_of_consumers':'Number of comsumers', 'FoodName': 'Food Names' },
      	color_discrete_sequence=["green"],
        hover_data={'Number_of_consumers':':,'})
    fig.update_xaxes(tickangle=40) 
    return fig
if __name__ == '__main__':
    app.run_server(mode='inline', port="8006") 


# # 📊 Wykres: Najpopularniejsze produkty w Europie. <a id="food_eu"></a>[&uarr;](#top)

# In[195]:


food_all = food.loc[food['Gender'] == "All"]
food_all_eu = food_all.loc[food_all['Continent'] == "Europe"]
most_consumed_all_eu = food_all_eu.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)


# In[196]:


app = JupyterDash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(
        min=0,
        max=75, 
        step=1,
        id='my-range-slider',
		value=[0,30], 
    )
    
])

@app.callback( 
    Output("graph-with-slider", "figure"), 
    Input('my-range-slider', 'value'))
def update_bar_chart(value): 
    v1=value[0]
    v2=value[1] 
    dff = most_consumed_all_eu.iloc[v1:v2] 
    fig = px.bar(dff, x="FoodName", y="Number_of_consumers", 
       title="Most popular food in Europe", 
       labels={'Number_of_consumers':'Number of comsumers', 'FoodName': 'Food Names' },
      	color_discrete_sequence=["blue"],
        hover_data={'Number_of_consumers':':,'})
    fig.update_xaxes(tickangle=40)
    return fig
if __name__ == '__main__':
    app.run_server(mode='inline',port="8015") 


# ### Dla wygody porównywania dodamn te wykresy obok siebie.

# # 📊 Wykresy: Porównanie wykresów najpopularniejsze produkty na świecie i w Europie <a id="food_world_eu"></a>[&uarr;](#top)

# In[197]:


app = JupyterDash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(
        min=0,
        max=75, 
        step=1,
        id='my-range-slider',
		value=[0,30], 
    )
    
])

@app.callback( 
    Output("graph-with-slider", "figure"), 
    Input('my-range-slider', 'value'))
def update_bar_chart(value): 
    v1=value[0]
    v2=value[1] 
    dff_world = most_consumed_all.iloc[v1:v2] 
    dff_eu = most_consumed_all_eu.iloc[v1:v2]
    first_line = go.Bar(x=dff_eu["FoodName"], y=dff_eu["Number_of_consumers"], name="Europe", marker=dict(color='blue'), hovertemplate = 'Number of consumers=%{y:,}')
    second_line = go.Bar(x=dff_world["FoodName"], y=dff_world["Number_of_consumers"], name="World", marker=dict(color='green'), hovertemplate = 'Number of consumers=%{y:,}')
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(first_line,row=1, col=1)
    fig.add_trace(second_line,row=1, col=2)
    fig.update_layout(title_text="Most popular foods for Europe and World")
    fig.update_xaxes(tickangle=40) 
    
    return fig
if __name__ == '__main__':
    app.run_server(mode='inline', port="8007") 


# ### <a id="food_world_eu_wnio"></a>[&uarr;](#top) Porównując dwa wykresy widać, że Europa zamiast płatków śniadaniowych na pierszym miejscu ma wodę z kranu. Może to być połączone z wyższym bezpieczeństwem wody z kranu w Europie [[3]](#źr). Następnie należy sie zastanowić nad wysokim miejscem pieczywa białego, cebuli, marchewki, masła, kurczaka, pomidorów, czosnku, oliwy z oliwek i mleka. Powodem może być duży wpływ Francji i Włoch na kuchnię Europy.
# ### Mleko które też jak widać częściej jest spożywane w Europie niż w reszcie świata, co może wynikać z mniejszej nietoleracji laktozy w Europie [[5]](#źr). Wysokie miejsce margaryny, soli i cukru może tłumaczyć częste zachorowania na wysokie ciśnienie tętnicze[[4]](#źr).

# # 📊 Wykresy: Najpopularniejsze produkty u mężczyzn i kobiet. <a id="food_world_gen"></a>[&uarr;](#top)

# In[198]:


app = JupyterDash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(
        min=0,
        max=75, 
        step=1,
        id='my-range-slider',
		value=[0,30], 
    )
    
])

@app.callback(
    Output("graph-with-slider", "figure"), 
    Input('my-range-slider', 'value'))
def update_bar_chart(value): 
    v1=value[0]
    v2=value[1] 
    dff_men = most_consumed_men.iloc[v1:v2] 
    dff_fem = most_consumed_fem.iloc[v1:v2]
    first_line = go.Bar(x=dff_men["FoodName"], y=dff_men["Number_of_consumers"], name="Male", hovertemplate = 'Number of consumers=%{y:,}')
    second_line = go.Bar(x=dff_fem["FoodName"], y=dff_fem["Number_of_consumers"], name="Female", hovertemplate = 'Number of consumers=%{y:,}')
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(first_line,row=1, col=1)
    fig.add_trace(second_line,row=1, col=2)
    fig.update_layout(title_text="Most popular foods for men and women")
    fig.update_xaxes(tickangle=40) 
    return fig
if __name__ == '__main__':
    app.run_server(mode='inline',port="8008") 


# ### <a id="food_world_gen_wnio"></a>[&uarr;](#top) Nie ma dużej różnicy między płciami jedynie kobiety mają na wyższym miejscu płatki śniadaniowe oraz warzywa i ryż, a natomiast mężczyźni mają na wyższym miejscu białą mąkę, białe pieczywo i mięso wieprzowe.

# # Wykresy: najpopularniejsze produkty dla mężczyzn i kobiet w Europie. <a id="food_eu_gen"></a>[&uarr;](#top)

# In[199]:


food_fem_eu = food_fem.loc[food_fem['Continent'] == "Europe"]
food_men_eu = food_men.loc[food_men['Continent'] == "Europe"]
most_consumed_fem_eu = food_fem_eu.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)
most_consumed_men_eu = food_men_eu.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)

app = JupyterDash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(
        min=0,
        max=75, 
        step=1,
        id='my-range-slider',
		value=[0,30], 
    )
    
])

@app.callback( 
    Output("graph-with-slider", "figure"), 
    Input('my-range-slider', 'value'))
def update_bar_chart(value): #funkcja updateująca wykres
    v1=value[0]
    v2=value[1] 
    dff_men = most_consumed_men_eu.iloc[v1:v2] 
    dff_fem = most_consumed_fem_eu.iloc[v1:v2]
    first_line = go.Bar(x=dff_men["FoodName"], y=dff_men["Number_of_consumers"], name="Male", hovertemplate = 'Number of consumers=%{y:,}')
    second_line = go.Bar(x=dff_fem["FoodName"], y=dff_fem["Number_of_consumers"], name="Female", hovertemplate = 'Number of consumers=%{y:,}')
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(first_line,row=1, col=1)
    fig.add_trace(second_line,row=1, col=2)
    fig.update_layout(title_text="Most popular foods for men and women in EU")
    fig.update_xaxes(tickangle=40) 
    return fig
if __name__ == '__main__':
    app.run_server(mode='inline',port="8009") 


# ### <a id="food_eu_gen_wnio"></a>[&uarr;](#top) W Europie podobnie jak na świecie małe różnice między płciami. Jedynie mężczyźni spożywają wiecej mięsa kurczaka oraz soli. Największa różnica jest w przypadku mięsa wieprzowego, u kobiet wypada z top15 a u mężczyzn zajmuje 10 miejsce. Kobiety jedynie spożywają więcej cukru.

# # Podsumowanie 🧠 <a id="Podsumowanie"></a>[&uarr;](#top)
# ### Jak widać nawet w bazach danych branych z renomowanych źródeł znajdują sie puste dane, błędy i niejasności. To jak dużą część tego notatnika zajmowało czyszczenie danych i obchodzenie problemów pokazuje jak przydatna jest czysta i dobrze zbudowana baza danych.
# ### Z uporządkowanych danych dało się wywnioskować to, że: 
# 1. Na świecie płatki śniadaniowe, mięso wieprzowe, ryż są bardziej popularne niż w Europie
# 1. W Europie bardziej popularne niż na świecie są mięso z kurczaka, mleko, ryż, margaryna, oliwa z oliwek, banany, masło
# 1. Woda z kranu jest popularniejsza w Europie niż na świecie
# 1. Nie ma wielu różnic między płciami jeżeli chodzi o spożywane produkty
# 1. Mężczyźni w Europie spożywają wiecej mięsa wieprzowego oraz soli od kobiet
# 1. Kobiety w Europie spożywają więcej cukru od mężczyzn
# ### Mam nadzieję, że była to przyjemna lektura i pokazała ciekawe zależności w świecie jedzenia. Do zobaczenia.

# # Możliwe zakłamania: ⚠️<a id="risk"></a>[&uarr;](#top)
# 1. Założenie, że każde badanie ma różną ilość badanych i w ten sposób grupowanie badanych.
# 1. Brak grupy wiekowej All dla wszystkich krajów.
# 1. Własne opinie i przeświadczenia.
# 1. Brak legendy do bazy danych.
# 1. Dane mężczyzn są z mniejszej ilości krajów.
# 1. Brak Polski i sprawdzanie dlanych dla Europy

# # Źródła:📱  [&uarr;](#top) <a id="źr"></a>
# 1. Gif: https://www.slynyrd.com/blog/2020/9/30/pixelblog-30-food 
# 1. Baza danych: https://apps.who.int/foscollab/Download/DownloadConso
# 1. Dane na temat jakości wody na świecie: https://worldpopulationreview.com/country-rankings/water-quality-by-country
# 	1. https://vividmaps.com/tap-water-safe-to-drink/
# 1. Badania na temat wpływu soli i cukru na ciśnienie tętnicze: https://sci-hub.se/10.1007/s00424-014-1677-x
# 	1. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4896734/
#     1. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6770596/
# 1. Dane na temat nietolerancji laktozy na świecie: https://worldpopulationreview.com/country-rankings/lactose-intolerance-by-country
