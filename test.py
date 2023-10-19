{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "06c9e60e-dc2e-486a-9279-831c1162c420",
   "metadata": {
    "tags": []
   },
   "source": [
    "##### <center>  <img src=\"https://images.squarespace-cdn.com/content/v1/551a19f8e4b0e8322a93850a/1602020393443-L6M0DGZK4C75DRNR7GZH/Title_Animation.gif\"  width=600> [[1]](#źr)\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3105bfdc-b20d-4ddf-945d-3d4e3dcda0a6",
   "metadata": {},
   "source": [
    "<h2 class=\"alert alert-block alert-danger\">  \n",
    "Projekt ten przedstawia mój tok myślenia oraz opinie! Wersja z czystą analizą dostępna jest na:    \n",
    "</h2>"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d75a1a89-928d-448a-8fba-6cf7674ea406",
   "metadata": {},
   "source": [
    "## Jako osoba która pracowała na kuchni i dla której temat jedzenia jako część kultury jest niezwykle fascynujący, w tym notatniku zajmę się analizą bazy danych z WHO na temat konsumpcji produktów na świecie. Moim planem jest odpowiedzieć na pytania, jakie produkty są najpopularniejsze i na co to wskazuje, jakie są różnice między kobietami i mężczyznami oraz jak te dane można by wykorzystać tworząc menu do restauracji. Myślę, że w tych danych jest wiele ciekawych informacji, które można wykorzystać do odpowiedzenia na wspomniane pytania jak i do pogłębienie wiedzy na temat tredów konsumcyjnych w różnych rejonach świata.\n",
    "## może bardziej pojśc w to że czym różni się otwarcie restauracji w Europie niż na świecie? że czy różnica między kobietami i mężczyznami by sprawiała że profilowanie restauracji pod płeć ma sens? czy celowanie w ogólnoświatowe gusta ma sens czy lepiej iśc w lokalne? myśle że w to i na podstawie tego podsumowania i wnioski\n",
    "### 📝 Plan jest następujący:\n",
    "1. Sprawdzę jak skonstruowana jest baza danych, jakie informacje i typy danych znajdują sie w kolumnach.\n",
    "1. Z tą wiedzą pozbędę się kolumn, które na pewno nie będą mi potrzebne no chyba, że takich nie będzie.\n",
    "1. Następnie dokonam analizy, gdzie znajdują sie puste dane oraz gdzie jest największe ryzyko ich znajdowania się, a potem pozbędę sie ich.\n",
    "1. Sprawdzę z jakich krajów i kontynentów jest najwięcej danych, żeby ocenić ich używalnośc w globalnej skali.\n",
    "1. Kolejną rzeczą będzie wyciagniecie danych dla produktów spożywanych na całym świecie, w Europie oraz to samo dla mężczyzn i kobiet na świecie i w Europie.\n",
    "1. Na koniec podsumuję co udało się osiągnąć, jakie były wyzwania, problemy, błędy, sukcesy.\n",
    "### Taki jest plan ale co napotkam na tej drodze to się okaże. Liczę na to że będzie ciekawie! "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b70a02a1-60ff-4a86-80ad-27951bb8dc92",
   "metadata": {},
   "source": [
    "# <font  color='289C4E'>Spis treści:<font><a class='anchor' id='top'></a> 📕\n",
    "1. [Wczytywanie danych](#hello)\n",
    "1. [Usuwanie niepotrzebnych kolumn](#del_col)\n",
    "1. [Ujednolicanie danych](#stand)\n",
    "1. [Usuwanie duplikatów i pustych danych](#del_dup)\n",
    "1. [Wyciąganie informacji z kolumn Consumers_Mean, Consumers_Median, Total_Mean, Total_Median](#colinfo)\n",
    "1. [Sprawdzanie z jakich krajów pochodzą dane](#kraje)\n",
    "1. [Problem z kolumną AgeClass](#ageclass)\n",
    "1. [Wykres: Ilość badanych na przestrzeni lat](#sub_over_time)\n",
    "    1. [Wnioski](#sub_over_time_wnio)\n",
    "1. [Wykres: Ilość badanych dla poszczególnych krajów](#country_sub)\n",
    "    1. [Wnioski](#country_sub_wnio)\n",
    "1. [Tworzenie kolumn z kodami i nazwami kontynentów](#kont)\n",
    "1. [Wykres: Procentowy udział badanych patrząc na kontynent](#kont_sub)\n",
    "    1. [Wnioski](#kont_sub_wnio)\n",
    "1. [Wykres: Najpopularniejsze produkty na Świecie](#food_world)\n",
    "1. [Wykres: Najpopularniejsze produkty w Europie](#food_eu) \n",
    "1. [Wykresy: Porównanie wykresów najpopularniejsze produkty na świecie i w Europie](#food_world_eu)\n",
    "    1. [Wnioski](#food_world_eu_wnio)\n",
    "1. [Wykresy: Najpopularniejsze produkty dla mężczyzn i kobiet na Świecie](#food_world_gen) \n",
    "    1. [Wnioski](#food_world_gen_wnio)\n",
    "1. [Wykresy: Najpopularniejsze produkty dla mężczyzn i kobiet w Europie](#food_eu_gen)    \n",
    "    1. [Wnioski](#food_eu_gen_wnio)    \n",
    "1. [Podsumowanie](#Podsumowanie)    \n",
    "1. [Możliwe zakłamania](#risk)\n",
    "1. [Źródła](#źr)   \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 102,
   "id": "e350e259-eda0-4c0c-9959-703ecc9f13a8",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# import bibliotek oraz ustawienia\n",
    "import pandas as pd\n",
    "import missingno as msno\n",
    "import matplotlib.pyplot as plt\n",
    "import pycountry_convert as pc\n",
    "import plotly.express as px\n",
    "from plotly.subplots import make_subplots\n",
    "import plotly.graph_objects as go\n",
    "import numpy as np\n",
    "from dash import dcc, html, Input, Output\n",
    "from jupyter_dash import JupyterDash\n",
    "import plotly.io as pio\n",
    "pio.renderers.default = \"notebook_connected\" # bez tego nie wyswietlają mi sie wykresy kiedy eksportuje je do htmla\n",
    "plt.style.use('fivethirtyeight')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "779243ba-75d0-4322-9f2d-cedf89cad028",
   "metadata": {},
   "source": [
    "# Wczytywanie danych <a id=\"hello\"></a>[&uarr;](#top) [[2]](#źr)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 103,
   "id": "eaf16e1b-dd83-4e47-8859-0b7f3539671f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>BW</th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Consumers_P05</th>\n",
       "      <th>Consumers_P90</th>\n",
       "      <th>Consumers_P95</th>\n",
       "      <th>Consumers_P975</th>\n",
       "      <th>Consumers_Standard_deviation</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "      <th>Total_P05</th>\n",
       "      <th>Total_P90</th>\n",
       "      <th>Total_P95</th>\n",
       "      <th>Total_P975</th>\n",
       "      <th>Total_Standard_deviation</th>\n",
       "      <th>ExtBW</th>\n",
       "      <th>ExtBWValue</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>60.62</td>\n",
       "      <td>0.00</td>\n",
       "      <td>8.33</td>\n",
       "      <td>116.67</td>\n",
       "      <td>150.00</td>\n",
       "      <td>166.67</td>\n",
       "      <td>NaN</td>\n",
       "      <td>66172</td>\n",
       "      <td>1.06</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0</td>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>female</td>\n",
       "      <td>608</td>\n",
       "      <td>55.87</td>\n",
       "      <td>0.00</td>\n",
       "      <td>8.33</td>\n",
       "      <td>116.67</td>\n",
       "      <td>133.33</td>\n",
       "      <td>158.33</td>\n",
       "      <td>NaN</td>\n",
       "      <td>33953</td>\n",
       "      <td>1.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0</td>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>male</td>\n",
       "      <td>549</td>\n",
       "      <td>65.89</td>\n",
       "      <td>0.00</td>\n",
       "      <td>10.00</td>\n",
       "      <td>133.33</td>\n",
       "      <td>158.33</td>\n",
       "      <td>166.67</td>\n",
       "      <td>NaN</td>\n",
       "      <td>32219</td>\n",
       "      <td>1.12</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0</td>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>167</td>\n",
       "      <td>55.26</td>\n",
       "      <td>0.00</td>\n",
       "      <td>8.33</td>\n",
       "      <td>100.00</td>\n",
       "      <td>116.67</td>\n",
       "      <td>158.33</td>\n",
       "      <td>NaN</td>\n",
       "      <td>66172</td>\n",
       "      <td>0.14</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>0</td>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>female</td>\n",
       "      <td>82</td>\n",
       "      <td>54.71</td>\n",
       "      <td>0.00</td>\n",
       "      <td>8.33</td>\n",
       "      <td>83.33</td>\n",
       "      <td>116.67</td>\n",
       "      <td>183.33</td>\n",
       "      <td>NaN</td>\n",
       "      <td>33953</td>\n",
       "      <td>0.13</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   BW Country  Year FoodCode   FoodName AgeClass SourceAgeClass  Gender  \\\n",
       "0   0   China  2002    A000G  Oat grain      All            All     All   \n",
       "1   0   China  2002    A000G  Oat grain      All            All  female   \n",
       "2   0   China  2002    A000G  Oat grain      All            All    male   \n",
       "3   0   China  2002    A000N  Buckwheat      All            All     All   \n",
       "4   0   China  2002    A000N  Buckwheat      All            All  female   \n",
       "\n",
       "   Number_of_consumers  Consumers_Mean  Consumers_Median  Consumers_P05  \\\n",
       "0                 1157           60.62              0.00           8.33   \n",
       "1                  608           55.87              0.00           8.33   \n",
       "2                  549           65.89              0.00          10.00   \n",
       "3                  167           55.26              0.00           8.33   \n",
       "4                   82           54.71              0.00           8.33   \n",
       "\n",
       "   Consumers_P90  Consumers_P95  Consumers_P975  Consumers_Standard_deviation  \\\n",
       "0         116.67         150.00          166.67                           NaN   \n",
       "1         116.67         133.33          158.33                           NaN   \n",
       "2         133.33         158.33          166.67                           NaN   \n",
       "3         100.00         116.67          158.33                           NaN   \n",
       "4          83.33         116.67          183.33                           NaN   \n",
       "\n",
       "   Number_of_subjects  Total_Mean  Total_Median  Total_P05  Total_P90  \\\n",
       "0               66172        1.06          0.00       0.00        NaN   \n",
       "1               33953        1.00          0.00       0.00        NaN   \n",
       "2               32219        1.12          0.00       0.00        NaN   \n",
       "3               66172        0.14          0.00       0.00        NaN   \n",
       "4               33953        0.13          0.00       0.00        NaN   \n",
       "\n",
       "   Total_P95  Total_P975  Total_Standard_deviation  ExtBW  ExtBWValue  \n",
       "0       0.00         NaN                       NaN    NaN         NaN  \n",
       "1       0.00         NaN                       NaN    NaN         NaN  \n",
       "2       0.00         NaN                       NaN    NaN         NaN  \n",
       "3       0.00         NaN                       NaN    NaN         NaN  \n",
       "4       0.00         NaN                       NaN    NaN         NaN  "
      ]
     },
     "execution_count": 103,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food = pd.read_csv(\"fullcifocoss.csv\", on_bad_lines='skip', sep=';', skipinitialspace = True)  # wczytanie danych do dataframe pozbywając sie rzędów, które mają za dużo pól oraz spacji\n",
    "pd.set_option('display.max_columns', None) # sprawiam, że można przejrzeć wszystkie kolumny, ponieważ by deafault ilość wyświetlanych kolumn jest ograniczona\n",
    "food.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2584899e-9f3b-442e-97d1-d02c2e462ddb",
   "metadata": {},
   "source": [
    "# Usuwanie niepotrzebnych kolumn <a id=\"del_col\"></a>[&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 104,
   "id": "7f1d2832-8f95-460a-8462-155c193d4f2b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>60.62</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>1.06</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>female</td>\n",
       "      <td>608</td>\n",
       "      <td>55.87</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>1.00</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>male</td>\n",
       "      <td>549</td>\n",
       "      <td>65.89</td>\n",
       "      <td>0.00</td>\n",
       "      <td>32219</td>\n",
       "      <td>1.12</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>167</td>\n",
       "      <td>55.26</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>0.14</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>female</td>\n",
       "      <td>82</td>\n",
       "      <td>54.71</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>0.13</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>male</td>\n",
       "      <td>85</td>\n",
       "      <td>55.80</td>\n",
       "      <td>0.00</td>\n",
       "      <td>32219</td>\n",
       "      <td>0.15</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000P</td>\n",
       "      <td>Barley grains</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>61</td>\n",
       "      <td>38.58</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000P</td>\n",
       "      <td>Barley grains</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>female</td>\n",
       "      <td>28</td>\n",
       "      <td>37.50</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000P</td>\n",
       "      <td>Barley grains</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>male</td>\n",
       "      <td>33</td>\n",
       "      <td>39.49</td>\n",
       "      <td>0.00</td>\n",
       "      <td>32219</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000T</td>\n",
       "      <td>Maize grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>2422</td>\n",
       "      <td>86.97</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>3.18</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Country  Year FoodCode       FoodName AgeClass SourceAgeClass  Gender  \\\n",
       "0   China  2002    A000G      Oat grain      All            All     All   \n",
       "1   China  2002    A000G      Oat grain      All            All  female   \n",
       "2   China  2002    A000G      Oat grain      All            All    male   \n",
       "3   China  2002    A000N      Buckwheat      All            All     All   \n",
       "4   China  2002    A000N      Buckwheat      All            All  female   \n",
       "5   China  2002    A000N      Buckwheat      All            All    male   \n",
       "6   China  2002    A000P  Barley grains      All            All     All   \n",
       "7   China  2002    A000P  Barley grains      All            All  female   \n",
       "8   China  2002    A000P  Barley grains      All            All    male   \n",
       "9   China  2002    A000T    Maize grain      All            All     All   \n",
       "\n",
       "   Number_of_consumers  Consumers_Mean  Consumers_Median  Number_of_subjects  \\\n",
       "0                 1157           60.62              0.00               66172   \n",
       "1                  608           55.87              0.00               33953   \n",
       "2                  549           65.89              0.00               32219   \n",
       "3                  167           55.26              0.00               66172   \n",
       "4                   82           54.71              0.00               33953   \n",
       "5                   85           55.80              0.00               32219   \n",
       "6                   61           38.58              0.00               66172   \n",
       "7                   28           37.50              0.00               33953   \n",
       "8                   33           39.49              0.00               32219   \n",
       "9                 2422           86.97              0.00               66172   \n",
       "\n",
       "   Total_Mean  Total_Median  \n",
       "0        1.06          0.00  \n",
       "1        1.00          0.00  \n",
       "2        1.12          0.00  \n",
       "3        0.14          0.00  \n",
       "4        0.13          0.00  \n",
       "5        0.15          0.00  \n",
       "6         NaN          0.00  \n",
       "7         NaN          0.00  \n",
       "8         NaN          0.00  \n",
       "9        3.18          0.00  "
      ]
     },
     "execution_count": 104,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.drop(columns=food.loc[:, 'Consumers_P05':'Consumers_Standard_deviation'], inplace=True)\n",
    "food.drop(columns=food.loc[:, 'Total_P05':'ExtBWValue'], inplace=True)\n",
    "food = food.drop(['BW'], axis=1)\n",
    "food.head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 105,
   "id": "52f92bb7-2171-4e5a-ad6d-48a87af629a6",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(544686, 13)"
      ]
     },
     "execution_count": 105,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e86b838d-a64f-4378-912a-cb1b58d26a6c",
   "metadata": {},
   "source": [
    "### Sprawdzę czy typy danych w kolumnach się zgadzają"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 106,
   "id": "91dd81b5-5eeb-465a-8299-cf97257c8763",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Country                 object\n",
       "Year                     int64\n",
       "FoodCode                object\n",
       "FoodName                object\n",
       "AgeClass                object\n",
       "SourceAgeClass          object\n",
       "Gender                  object\n",
       "Number_of_consumers      int64\n",
       "Consumers_Mean         float64\n",
       "Consumers_Median       float64\n",
       "Number_of_subjects       int64\n",
       "Total_Mean             float64\n",
       "Total_Median           float64\n",
       "dtype: object"
      ]
     },
     "execution_count": 106,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.dtypes"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6286d279-7906-4b4b-9763-7f31280c5095",
   "metadata": {},
   "source": [
    "### Wszystkie kolumny mają dobre typy danych"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "bca13dda-44b0-4c9a-9ead-0584ac3c5295",
   "metadata": {
    "tags": []
   },
   "source": [
    "### Ze względów estetycznych ustawię by dane miały dwie liczby po przecinku. Jest to moja preferencja, a w razie potrzeby wrócenie do ustawień deafaultych nie będzie problematyczne."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 107,
   "id": "f9bf05cc-912f-403b-ab5e-b82cf73d9f7a",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>60.62</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>1.06</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>female</td>\n",
       "      <td>608</td>\n",
       "      <td>55.87</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>1.00</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>male</td>\n",
       "      <td>549</td>\n",
       "      <td>65.89</td>\n",
       "      <td>0.00</td>\n",
       "      <td>32219</td>\n",
       "      <td>1.12</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>167</td>\n",
       "      <td>55.26</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>0.14</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>female</td>\n",
       "      <td>82</td>\n",
       "      <td>54.71</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>0.13</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Country  Year FoodCode   FoodName AgeClass SourceAgeClass  Gender  \\\n",
       "0   China  2002    A000G  Oat grain      All            All     All   \n",
       "1   China  2002    A000G  Oat grain      All            All  female   \n",
       "2   China  2002    A000G  Oat grain      All            All    male   \n",
       "3   China  2002    A000N  Buckwheat      All            All     All   \n",
       "4   China  2002    A000N  Buckwheat      All            All  female   \n",
       "\n",
       "   Number_of_consumers  Consumers_Mean  Consumers_Median  Number_of_subjects  \\\n",
       "0                 1157           60.62              0.00               66172   \n",
       "1                  608           55.87              0.00               33953   \n",
       "2                  549           65.89              0.00               32219   \n",
       "3                  167           55.26              0.00               66172   \n",
       "4                   82           54.71              0.00               33953   \n",
       "\n",
       "   Total_Mean  Total_Median  \n",
       "0        1.06          0.00  \n",
       "1        1.00          0.00  \n",
       "2        1.12          0.00  \n",
       "3        0.14          0.00  \n",
       "4        0.13          0.00  "
      ]
     },
     "execution_count": 107,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pd.set_option('display.float_format', lambda x: '%.2f' % x)\n",
    "food.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6aa82287-84c6-41e8-a829-a650b3e4d3d6",
   "metadata": {},
   "source": [
    "### <a id=\"stand\"></a>[&uarr;](#top) Również rzuca mi się w oczy to że female i male w kolumnie Gender zaczynają się z małej litery a All z dużej. Przypomina mi to o tym żeby ujednolicić stringi. Zrobię to dla wszystkich kolumn zawierających stringi poza FoodCode bo mogło by w przyszłosci mieć to znaczenie podczas wczytywania kodów."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 108,
   "id": "a7bf9443-e8a9-4468-9621-c44ce6535c57",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>60.62</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>1.06</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>Female</td>\n",
       "      <td>608</td>\n",
       "      <td>55.87</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>1.00</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>Male</td>\n",
       "      <td>549</td>\n",
       "      <td>65.89</td>\n",
       "      <td>0.00</td>\n",
       "      <td>32219</td>\n",
       "      <td>1.12</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>167</td>\n",
       "      <td>55.26</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>0.14</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>Female</td>\n",
       "      <td>82</td>\n",
       "      <td>54.71</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>0.13</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Country  Year FoodCode   FoodName AgeClass SourceAgeClass  Gender  \\\n",
       "0   China  2002    A000G  Oat Grain      All            All     All   \n",
       "1   China  2002    A000G  Oat Grain      All            All  Female   \n",
       "2   China  2002    A000G  Oat Grain      All            All    Male   \n",
       "3   China  2002    A000N  Buckwheat      All            All     All   \n",
       "4   China  2002    A000N  Buckwheat      All            All  Female   \n",
       "\n",
       "   Number_of_consumers  Consumers_Mean  Consumers_Median  Number_of_subjects  \\\n",
       "0                 1157           60.62              0.00               66172   \n",
       "1                  608           55.87              0.00               33953   \n",
       "2                  549           65.89              0.00               32219   \n",
       "3                  167           55.26              0.00               66172   \n",
       "4                   82           54.71              0.00               33953   \n",
       "\n",
       "   Total_Mean  Total_Median  \n",
       "0        1.06          0.00  \n",
       "1        1.00          0.00  \n",
       "2        1.12          0.00  \n",
       "3        0.14          0.00  \n",
       "4        0.13          0.00  "
      ]
     },
     "execution_count": 108,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.loc[:, 'Country'] = food.loc[:, 'Country'].str.title()\n",
    "food.loc[:, 'FoodName'] = food.loc[:, 'FoodName'].str.title()\n",
    "food.loc[:, 'AgeClass'] = food.loc[:, 'AgeClass'].str.title()\n",
    "food.loc[:, 'SourceAgeClass'] = food.loc[:, 'SourceAgeClass'].str.title()\n",
    "food.loc[:, 'Gender'] = food.loc[:, 'Gender'].str.title()\n",
    "food.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1408c8a2-cf91-4c50-afa0-4834c8f12246",
   "metadata": {},
   "source": [
    "### Wszystko bardzo ładnie się udalo i mam ujednolicone stringi."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "beecd998-1ab2-4022-b50a-32fb69631d84",
   "metadata": {},
   "source": [
    "# <a class=\"anchor\" id=\"del_dup\">Usuwanie duplikatów i pustych danych.</a> [&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 109,
   "id": "543a1de1-99db-4a4d-9bd5-b3aa88a0a69b",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(544686, 13)"
      ]
     },
     "execution_count": 109,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 110,
   "id": "b2481ab3-9c68-4615-b6f3-42918c701757",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "food = food.drop_duplicates()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 111,
   "id": "b0fd6c28-37ac-44c6-bbe9-1501a20e3ef2",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(523276, 13)"
      ]
     },
     "execution_count": 111,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 112,
   "id": "27004b87-8790-42f2-a390-09d26072022b",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "24805"
      ]
     },
     "execution_count": 112,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "544686-519881"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "19e21a9d-0ce4-455d-a5a5-2fd053bdedbd",
   "metadata": {},
   "source": [
    "### Tym prostym sposobem pozbyłem się 24805 duplikatów."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ef634d44-54a7-4811-a2a4-315872a050d4",
   "metadata": {},
   "source": [
    "### Przy użyciu biblioteki missingno oraz metody isna sprawdzam, gdzie znajdują sie puste dane.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 113,
   "id": "f8205f60-21d4-4c7b-9312-c6a81a9e0e6d",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<Axes: >"
      ]
     },
     "execution_count": 113,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAACL0AAARXCAYAAAAfhIGCAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8pXeV/AAAACXBIWXMAAA9hAAAPYQGoP6dpAAEAAElEQVR4nOzdd7xXBf0/8Ne9XEBkTwEVcSHuWWY5cmtWmKvUNEtEc+S2LNOvKCEK7p1pabhyh0BmKo5M0EQ0cYt7MGXIuuP3B797AxkCFzh87Pl8PHzI/ZzPOZ9z4PV4Hz58Xp9zyiZNmlQTAAAAAAAAAAAoIeVF7wAAAAAAAAAAACwppRcAAAAAAAAAAEqO0gsAAAAAAAAAACVH6QUAAAAAAAAAgJKj9AIAAAAAAAAAQMlRegEAAAAAAAAAoOQovQAAAAAAAAAAUHKUXgAAAAAAAAAAKDlKLwAAAAAAAAAAlBylFwAAAAAAAAAASo7SCwAAAAAAAAAAJUfpBQAAAAAAAACAkqP0AgAAAAAAAABAyVF64X/K7NmzM3ny5NTU1BS9K/wPkj+KJoPA/zIzkKLJIEWTQYokfwBQHOdhgDnMwa8upRf+Z0yaNCnnnntuTjjhhDz33HOprq4uepf4HyJ/FE0Ggf9lZiBFk0GKJoMUSf4o2rhx4zJ48OCid4P/UfJH0ZyHKZo5yMpg/PjxSZKysrIkyi9fRRVF7wCsCOPHj8+PfvSjPPvss+nYsWNmzZqV6urqlJfrfbH8yR9Fk0GKNnXq1Dz55JN56qmnMmvWrDRv3jwHH3xw1lhjjTRu3Ljo3eMrzgykaDJI0WSQIskfRRs3bly23377fPLJJ/n973+fAw44oOhd4n+I/FE052GKZg5SpM8++yy33npr/vWvf+X111/P+uuvn+9973vZfffd07Jly9TU1NSVYCh9Si985U2aNCk9evTIf/7znxx44IG57LLL0qRJk3meY7CxvMgfRZNBijZhwoQcffTReeqppzJ9+vS6x4cNG5bDDjssBxxwQFZdddUC95CvMjOQoskgRZNBiiR/rAx+/etf55NPPkmSHHXUUSkrK8v+++9f8F7xv0L+KJLzMCsDc5CijB8/PoceemieeeaZusdGjx6dESNG5L333ssxxxwz30yktKlz8pVWWVmZPn365D//+U9+/OMf54orrkiTJk3mu4Rf7V/sXNqPZUn+KJoMUrTx48dn7733zsMPP5yNNtoov/jFL3L66aenQ4cOefbZZ3PddddlxIgRSVxSkmXPDKRoMkjRZJAiyR8ri1122SXNmzfPhhtumCTp2bNn7rnnnoL3iv8V8kdRnIdZWZiDFGHChAn53ve+l2eeeSa77rpr7r///txzzz35yU9+kqlTp+bOO+/MhAkTit5NlrGySZMm+YSBr6yZM2dm5513TnV1dR5//PE0atQoSVJVVZUPP/wwzzzzTKZMmZKOHTtmm222Sfv27QveY75K5I+iySBFmjp1ao444oj84x//yE9+8pNcdNFFadiwYZLkxRdfzLHHHpuXXnopBxxwQH7/+98XvLd8FZmBFE0GKZoMUiT5Y2UxbNiwHHjggfn973+fl156Kf3790+S/OEPf8h+++1X8N7xVSd/FMV5mJWFOciKNmXKlPzsZz/Lww8/nJ/85CcZMGBAGjRokCT5+OOPc+qpp2bw4MG54YYbXHXoK8btjfhK+89//pPRo0fniCOOqPuL3axZs3LxxRfnr3/9a15++eUkcxrNnTt3Tp8+fbLDDjukTZs2Re42XxHyR9FkkKJUV1fntttuyz/+8Y/suOOOdYWXysrKNGjQIJtuumn69u2b733ve3n44YczZsyYrLXWWi6pyzJlBlI0GaRoMkiR5I+VxTe/+c20bt069913X2666aZ89tln+f3vf58jjzwySbLffvuluro65eUuiM6yJ38UxXmYlYU5yIo0e/bsXH/99Xn44Yezyy67pH///mnQoEFmz56dhg0bpmPHjvn617+eZ555Jt27d08y723eZLG0+ZPjK62qqipJ0rhx4yTJ559/nj59+qRfv36ZMGFCvvOd72SHHXbI+uuvnw8++CAnnnhibrnllnz66adF7jZfEfJH0WSQosyePTuDBw9Os2bN0rdv3zRs2DBVVVWpqKhIWVlZqqqqstFGG2XdddfNpEmTMm7cOIUXljkzkKLJIEWTQYokf6wsGjZsmE022SQvvvhikuTCCy9Mr169kiRHHnlk7rrrrroPN5599tm89NJLhe0rXz3yR1Gch1lZmIOsSJMnT86gQYPSvHnzXH311amoqEhVVVXdv00nyfjx49O6detcfvnlOeKII/KjH/0ovXv3zgcffJDy8nK3eythrvTCV1qnTp3SpEmTvP7660mS119/PX/84x+z7rrr5t57782aa66ZWbNmZcKECXWXtLr44ovTtm3b/PjHP9bqo17kj6LJIEV5//338+GHH2arrbZKx44dk6TuMpK1v27Tpk023HDDvPnmm5k0aVJBe8pXmRlI0WSQoskgRZI/VgZVVVVp0KBBdtppp5xzzjl54oknssMOO6Rfv35Jkuuvvz5HHXVUWrZsmcmTJ+fYY4/Nd77znQwYMMDVDqg3+aNIzsOsDMxBVqSampq0bds2v/rVr/LGG2+kTZs2qa6uToMGDeqy+MILL2TgwIGZMGFCJk2alOnTp2fWrFl56KGH8te//jV33XVX1lprLTOwRPkT4yujtqU3t+bNm6dTp0555JFHcu+99+axxx7LtGnTcvnll2fNNddMZWVl3SWtBg4cmB/84AeZPHly/u///i/vvfeeocZikz9WBjU1NfP8LIOsaLUZXHfddXPWWWfllFNOWeCb1NqZ2bx58yRReqHenIcpmgxSNBmkSPLHyqq2eL/lllsmST788MO6Zf369cvRRx+dJDnooIPSq1evzJo1K9tvv70P2lgm5I8VxXmYoi0og4k5yIrxxfztueeeOfLII9OwYcO6WdagQYO8/vrr+cEPfpAJEybkwAMPzL333pu//e1v+ctf/pLtttsub7zxRo488shMmDDBDCxR/tT4Shg3blyOPPLIukukJXPuvdayZcuceOKJadCgQe6+++78+9//TkVFRVq0aJEkdbdZqKysTJJce+212XrrrTN+/Pjcd999dduBRZE/ijZz5swkmef2MDU1NTLICjN3BmvfaHzve9/LTjvttMDn12a1c+fO86yfzPtGZfbs2ctlf/lqcR6maDJI0WSQIskfK4uF5aWmpiZrr712WrZsmcGDB6empibTpk1LklxwwQXZZZddUlZWlpqamhx66KE58sgj69aDxSV/FMV5mKItKINzMwdZnubO39yfjayyyip1v66pqcmMGTNy3HHHZeLEiTn11FNz/fXXZ5NNNsnGG2+cnXbaKVdddVU23njj/Oc//8nIkSPr1qO0KL1Q8saNG5fdd989999/f5588skkmefSU1//+tez9dZb58EHH8yjjz6aRo0a1f2FrfYvdbX3dWvUqFG23nrrJMkHH3yQJBp9LJL8UbSxY8emZ8+eufXWW+d5vPYveTLI8vbFDM59G6OFqc1V7RuQWbNm1f2/dv0bbrghf/jDHzJ16tTlsdt8RTgPUzQZpGgySJHkj6KNHTs2d9xxR5I5eVnQB7RlZWVZY401svnmm+fll19OTU1NmjZtmiS5//7788gjj6SmpiY1NTUZOHBg7rnnnrr1YFHkj6I5D1O0hWVwbuYgy8uC8regqw6VlZVllVVWyf/93//loosuyllnnZXkv3Owtpi11VZbZcaMGXn77bfr1qO0OGtR0saOHZvdd989Y8aMSZLceeedmT59+jxvNLp3756jjz467dq1y9SpUzNlypRcffXVSf77l7rkv629jTbaKImBxpeTP4o2bty47Lbbbhk0aFAmTpy4wPaxDLI8LU4GF6Vhw4ZJUldsadSoUZLkwgsvzOmnn54777yz7g0IfJHzMEWTQYomgxRJ/ija2LFjs+uuu+aYY47JH/7whyQLLh7U/rzBBhvkjTfeyL///e8kyR133JEjjjgiSXL55Zfn5JNPTpIcffTR832pBL5I/iia8zBFW1QG5/73QXOQ5WFh+WvQoMFC/336m9/8Znr27JlkTjmmoqKi7tfJf2efwl/p8idHyRo3blz22GOPjBkzJoceemhWX331jBw5Mtdcc02SzHNy3W+//fLLX/4yTZs2TVlZWe65557069cvyZxvpM894B577LEkyVZbbZXEJaxYMPmjaLVN5nfffTe9evXK0UcfPd+bUhlkeVqcDC5Mba5qL6s7Y8aMumUXXnhh+vbtm5YtW+bKK69Mq1atlvm+U/qchymaDFI0GaRI8sfK4Pzzz897772XJDnttNNy4403Jpm/eFD7wUXt7RMmTZqUv//97znmmGOSJH379s1hhx2Ws88+O8ccc0wqKyvz61//OlOmTFnBR0QpkT+K5DxM0b4sg3P/+6A5yLK2JPlbmNorjdfOwJqamowaNSodO3bMDjvssFz3n+VH6YWSVPtB25gxY9KrV69ceeWVOeWUU9KgQYOMGDEis2fPrntu7RuNnj175rzzzkunTp1SWVmZyy+/PL/85S8zadKkzJw5M8mcNyz33XdfNtlkk+y4445JNJuZn/xRtLmbzMccc0z69OmTioqKuuzV5q6srKzuMRlkWVrcDH7x17Vqc1V7pZfGjRsnmfNGt7bwMnTo0LpvGcHcnIcpmgxSNBmkSPLHymK77bZL8+bN8/Wvfz1Jcuqpp+amm25KsuArbnTo0CHl5eU57bTT8qMf/SjJnML9McccU/fcvn375qSTTsoDDzyQ5s2br8CjodTIH0VxHqZoi5vBL5amzEGWhaXN34JUVVXVlV9OO+20jBw5Mtttt11WW2215XoMLD9lkyZNUtekpMw91I455picd955qaioyJNPPpkDDjggM2fOzLXXXpsf/vCHdevMfS/LBx54IH/+85/z5JNPZvr06VlvvfWy6qqrZvbs2Rk9enQ6duyY+++/P926dSvqEFmJyR9Fq20yv/322+nVq1dd2WBuEydOzCqrrJImTZrMt74MUl/1zeDcbrnllvziF7/Iz3/+87Rt2zbnn39+XeGle/fuy/MwKFHOwxRNBimaDFIk+WNlMnz48Oy1117p27dvKioqctpppyVJLr744vz0pz9NMm/+ampqctRRR+Xuu+9OMueDtqOOOqruedXV1fO9r4GFkT+K4DxM0ZYmg7VqamrSq1ev3HXXXUnMQZZcffK3KOeff34GDBiQLl265IEHHshaa621nI6A5c2VXigp48aNy7e//e35hlp1dXW23377/OIXv0iS3H777fnoo4/q1pu7Yf/9738/559/fi699NJ069Ytn3/+eUaNGpXZs2enR48eGTx4sL/YsUDyR9EmTpyYr33ta3n77bdz5JFHpl+/fnVvBmbPnp2///3v+eUvf5ndd989u+22W/bff//ceeedeeedd+q2IYPUx7LI4Nxqb280ZMiQXHzxxQovLJLzMEWTQYomgxRJ/liZ1NTUpFu3buncuXMeeeSRHHLIITnjjDOSJKeccso8V9yo/aZvWVlZjjvuuHzrW99K79695/mgrby83AdtLDb5owjOwxRtaTNYq6ysLMccc0x23HFHc5AlVt/8fdHnn3+e999/Pz179syAAQPSsWPH3HnnnQovJc4UoWRUVVWlX79++eCDD+ouyVdRUZGqqqq6tvLOO++cP//5zxk5cmTefffddOrUqe6kWftGo6ysLN26dUu3bt2y2267Zfr06RkzZkw23HDDNGrUKM2aNSv4SFkZyR8rgwkTJtRdcu/dd9+tuwTftGnT0r9//wwcODBjx45NMue+lC+//HKee+65bLfddvnNb36TTTbZJElkkKW2rDJYq3nz5mnYsGHGjBmT1q1b58EHH1R4YYGchymaDFI0GaRI8sfKpqysLK1atcqmm26a119/PQ0aNMiZZ56ZBg0apG/fvjnllFNSXV2dI488MmVlZRkxYkRatWqVLbfcMjfffHPatGmTZN4rIMDikj9WNOdhilbfDNbaaqutcuONN6Zt27ZJzEEWz7LKX61p06blD3/4Q2688ca88847+eY3v5krrrgi66yzzoo+NJYxtzeipIwaNSovvfRSDjrooLqhVvvhW60jjjgi999/f7bffvvceuutC733X+1f9GBxyR8rg9GjR+dnP/tZXnnlleyxxx659tpr86c//Snnnntu1lxzzRx33HFZe+2107Rp09x44415+umn89FHH2WXXXZJv379st566yWRQZbesspgkjzzzDP5wQ9+kFVWWSVDhgzJBhtsUOCRsbJzHqZoMkjRZJAiyR8rk9r89e/fP3369MngwYOz3XbbpaqqKgMGDEjfvn2TJNdff32aNWuWQw45JPvvv3/69++fVq1aJZFDFt8XsyJ/FMF5mKItywwmcsiSWdb5Gzp0aAYPHpwNN9ww+++/fzp06LC8D4EVQOmFkvXFll7tzy+99FIOOeSQzJo1K9dff3123HHHBQ5AqA/5o0hzlw4233zzvPPOO2nVqlUGDx6cTp061T1v+vTpufXWW3PllVfm448/zkknnZRTTz217lsesLTqm8GysrK6uXj//fdns802y9prr13U4VCCnIcpmgxSNBmkSPLHyuLf//53dt1111x88cX56U9/miSprKzMpZdemj59+iT57609+vXrl169ehW5u5SY2bNnp2HDhgtdLn8UxXmYoskgRVpW+ZsyZUqaNGni1lpfIT7xoiTU3v90bl/8wLb2586dO2fjjTfOJ598knvuuSdJnFSpF/mjaF/M4IYbbpgbb7wx3bt3zwsvvJBmzZrlpptuSqdOnVJZWZlkzjePmjRpkoMPPjj77LNPZsyYkQceeCCVlZUKLyy2WbNmZcqUKUlSdw/opP4ZbNCgQd32evToofDCIjkPUzQZpGgySJHkj6ItKIPJnPcn7dq1S7NmzfLkk08mSWbOnJmKioqcdtpp6dGjR903yPfff/+6wkHt+xVYlHHjxuWEE07IiBEjFrhc/lhRnIdZGckgK8rymIG122zevLnCy1eMT70oCbVvEub+wG1h2rRpk2OOOSZJcsstt+Thhx9ervvGV5/8UbQvZrCmpqaudLDRRhtlxx13zCabbJIkdX9Rqy0VrLrqqjn22GPTpk2bvPzyy3nllVeKOQhKzqRJk3LOOefke9/7Xl555ZX53lDUN4PKVywu52GKJoMUTQYpkvxRtIVlsLy8PF26dMk3v/nNjBgxIp9//nkaN26cJPnLX/6S+++/PzU1Namurs7dd9+dm266Kcmc9yuLk2f+d40bNy677rpr7rjjjowaNSqJ/FEc52GKsjSzSgZZ1pbHDHRbra8uFSZWSlOnTs3DDz+cESNGZOLEiWnVqlV+9rOfZb311vvSdWtqarLddtvlgAMOyD333JPnnnsuu+22m3sEstjkj6J9WQZrs7ThhhvmT3/6U6ZOnbrAVnJ5eXlqamrSsGHDuoLBrFmzVtyBULLGjRuXgw8+OM8++2zat2+f1157Ld26dVtg8UUGWdachymaDFI0GaRI8kfRFjeDtd/SXXvttfPQQw/lzTffzKabbpo77rij7gOPCy64INXV1fn1r3+dU045JdOnT8+xxx6rgM9CjR07NrvvvnvefffdJMkll1yS7373u1lttdXmeZ78sbw4D1O0KVOmpHnz5ikvL1/iWxPJIPVlBlIfZZMmTVrwNSKhIBMmTMhRRx2Vxx9/fJ5LPrZp0yYDBgzId7/73TRo0OBLh9Qf//jHnHzyyWnatGkeeuihbLTRRst71/kKkD+KtqwymKTujclHH32UHXbYIWuuuWYefPDBrLrqqsvzEChxkyZNyne/+9385z//yf77759rrrlmkfcxXxQZZEk5D1M0GaRoMkiR5I+iLU0GH3300ey333656aab0qhRoxx66KFJkn79+tXdUqZ///7p06dPkuTtt99Oy5YtffjBfMaOHZs99tgjY8aMyWGHHZZRo0blhRdeSO/evXPcccelrKxsvtzIH8uS8zBFGzduXHbbbbdsttlmufnmm5NkiYsviQyydMxA6kutmJXK+PHjs9dee+WRRx7JlltumbPOOisnnnhivv71r2fChAk544wzMnLkyJSVlS30nr61jx9xxBHZY489Mm3atNx2222ZPXv2QteBRP4o3rLIYK2535BccMEFGT9+fLbZZhvfKGKRqqqq0q9fv/znP//JoYcemquvvjoNGzZc5CUkF7ZMBllSzsMUTQYpmgxSJPmjaEubwfbt26dx48bp3bt3Dj/88CTJhRdeWFc4qK6uzqmnnprevXvnySefTKtWrRQOmM+4cePqCi9HH310+vXrlwMPPDBJMmzYsJSXly9w/skfy4rzMEWbNGlS9t1337zzzjsZNGhQTjzxxCRzbl9eVVW1WNuQQZaWGciy4EovrDSmTp2an/3sZ/n73/+en/70p7nwwgvrbpUwefLkHHbYYXn88cfzta99LXfffXeaN2++0G1VV1envLw8N910U371q19lzTXXzKOPPrrIdfjfJn8UbVlmcG6/+93vctFFF2XttdfOfffdly5duizPw6DETZ06NXvttVcqKyvz6KOPpkmTJknmFFg+/vjj/POf/8zUqVPTtWvXdOrUKd27d0+SRV4mUgZZHM7DFE0GKZoMUiT5o2j1yeCsWbNyyimnZODAgUnmFA6OOuqoJEv37XT+99QWXt5+++0cffTROe+889KwYcOMGjUqe+21V6ZPn54LLrggRx999Hzryh/LgvMwRZs5c2Z69+6dq6++OmuuuWY+++yzTJ48OYcffnguu+yyJIs/02SQJWUGsqz4qi0rhZqamtx+++35+9//nh133LFuqFVWVqa6ujotWrTIb3/726y22moZP358pk2btsjt1X6LfN99982qq66aN998M5MnT14Rh0IJkj+KtqwzOGXKlHz00Ufp2bNnLrroonTs2DG33XabsgFfavTo0fnPf/6TzTbbLKusskqSOf+Id9FFF+Wggw5Kr169csopp2S//fbLAQcckN///vdJMl/hRQZZEs7DFE0GKZoMUiT5o2j1zWCjRo3yox/9KLvsskv69OlTVziorq5WOOBLjRs3LrvuumvefvvtHHPMMTn//PPTsGHDzJ49O5tttllOP/30lJeX5/HHH8+kSZPmW1/+qC/nYVYGTzzxRAYPHpyOHTumT58+ueiii9KqVavcfPPNS3zFFxlkSZiBLEtKL6wUqqqqMmjQoLRp0ybnnXdeKioqUlVVlYqKirohteaaa6aioiJvvfVWnn/++cXaZuvWrXPppZfmmWeeyeqrr768D4MSJX8UbVlm8PPPP8///d//Zffdd8/dd9+dr33taxk0aFA22GCDFXU4lLDaFn27du1SVlaWmTNnpk+fPunXr18mTJiQPfbYI3vssUe6dOmSDz74IGeccUb69u1bt35lZaUMssSchymaDFI0GaRI8kfRlkUGt99++1x11VU59thjk/z3W76wKDU1Nendu3fefffd9OrVa578NWzYMEmy1VZbpVmzZhk8eHD+/e9/L3A722+/fa6++mr5Y6k4D1O0mpqaPPPMMxkzZkz22Wef7LDDDtl3333zu9/9rq74ctJJJyVZ/OKLDLK4zECWpYqidwCSOfcLfP7557P22mvXfQt87jZ8TU1NVltttWy99db54IMPFuvEWrv+97//ffdKZZHkj6Itywyuuuqq2WefffLuu+/mkEMOyU9/+tN06tRpuR8DXw2NGzdOWVlZnnjiiYwbNy7jxo3LLbfcknXWWSeDBg2qy9ILL7yQe++9N5dddlkuvPDCNG/ePMcff3wqKipSUVEhgywR52GKJoMUTQYpkvxRtPpmsPZWqx07dqz7WeGAxVFWVpZTTjkl22yzTQ455JC6D9rmzt9OO+2U/fffPzfddFMGDBiQTTfdNO3bt69bXpu/1VZbre5n+WNJOA9TtLKyshx44IH54IMP8qMf/SitWrVKkvTo0SNlZWU588wz86c//SlJcumll9YVXxZ1NSsZZHGZgSxLSi8UrqamJu3atcuQIUPy7rvv1p1U51Y7mFq3bp0kmT59+mJv31BjUeSPoi2PDO6yyy7ZYostsuqqq9bdogYWx0YbbZRvfvObGTVqVIYPH5533303EydOzJ///Od06tQpM2fOTOPGjbP55ptnvfXWS6NGjXLRRRfl/PPPz9Zbb53tttsuiQyy+JyHKZoMUjQZpEjyR9GWRQa/mDO5Y3FVV1ena9eu6dq1a5LM9yFu7RVbDjvssDz88MMZM2ZM3n///bRv375umfxRH87DrCy6deuWAQMGpEmTJnVlvlVXXTU9evRIkkUWX2qfX2vun2WQRTEDWdbUjilUTU1Nkjm3Q9hoo42y1157LfB5lZWVSVJ3acm576E6d7Ov9nmwOOSPoi3PDLZp00bZgEWqqampy2Ay5x/0kmTvvffOlClTctVVV+X9999P06ZN06ZNmyRzrgRTq2nTpvnxj3+c7bffPjNnzszrr78+z3ZkkC/jPEzRZJCiySBFkj+KJoMUrfaKLLVZ/OJVC2qXr7feetlggw3y4Ycf5tJLL51nGSwtM5CVTZMmTZLMWxRo0qRJevTokb59+6ZVq1b505/+NM+tjmbMmFH3/A8//HC+9WFhzECWB387ozDTpk3L9OnTU1ZWloqKRV90qPaNRNu2bZP8dyDO3cC//PLLc+eddy5R04//XfJH0WSQopWVldW9EZ37Wxj77rtvNtxww/zzn//Mn/70p0ybNi3Tpk2re97cunTpko033jhJ6u5v7h//WBxmIEWTQYomgxRJ/iiaDFKE2bNnZ/z48Rk5cmTeeOONusfLysrme69bq6amJs2bN8+ZZ56Z5s2b54knnsgjjzxStwyWhhlIURY2B5OFz7SFFV+qqqrqvux28skn54wzzsgrr7yy3I+B0mcGsry4vREr1OTJk/P73/8+w4cPz2uvvZZmzZrl5JNPzne/+900atRooevVDramTZvO83jtUOvfv3/69OmTNddcM/vss09dKxXmJn8UTQYp2tSpU/OPf/wjzz33XD788MN06dIl++yzT7beeuskc94wrL766rn22muzzz77ZOrUqUmSq666KhdccEE6dOhQV5CpvdXRJptskiRp3rx5YcdFaTADKZoMUjQZpEjyR9FkkCJNmjQp5557bp555pmMHj06FRUVOeqoo7Lffvtlm222WeiVCWofX2eddbLDDjtk8ODB+ec//5lddtnF1QxYImYgRVvaOZj8t/iS/PdWRw0bNsxFF12UU045JX/84x/TuXPnulvQwBeZgawISi+sMOPHj88hhxyS4cOHp2HDhmnYsGHGjBmTI488MhdddFF69uy50HVr75NaO8jGjx9ft+zCCy9M375907Zt29x2221p2bLlcj8WSo/8UTQZpGjjx4/PUUcdlSeeeGKeSz5eeumlueGGG7LffvulrKwslZWV2WyzzfKnP/0pP/nJTzJ16tSMGDEit9xyS4444oi0bds2s2bNqrvVUe233Lbccssk8141BmqZgRRNBimaDFIk+aNoMkiRxo0blx49euTll19Ox44d071797zyyiu5/vrrM378+HTt2jXt2rVb5DZatWqVH/zgBxk8eHAuueSS7Lrrrtluu+1W0BFQ6sxAirYs5mBt8aWysjJnn312brjhhjzxxBN59dVX065du9x9991ZbbXVVtARUUrMQFYU159nhZgwYUK++93vZvjw4dl9990zaNCgPPjgg3X3/zv99NPz8ssvf+l2mjVrliR1l03r169f+vbtm5YtW2bQoEF1t1iAuckfRZNBijZhwoTsvffeefTRR7PVVlvl3HPPzXHHHZddd901NTU1OfLII/Poo4+mvLy87rKSu+yyS2677bY0b94877//fv74xz/mggsuyJgxY+oa+Oeff37uvffebLTRRvnmN7+ZxL17mZ8ZSNFkkKLJIEWSP4omgxRp0qRJ2X///fPyyy/noIMOyrBhw/Lwww/n2muvzdprr50777wzw4cPX+Q2am+lsP/++2ffffdNdXV1hg0blmTO1VJhUcxAirYs5mCtVVZZJT/+8Y9zwQUXpFmzZnn11VfTunXrPPjgg+nevftyPhJKkRnIiuRKLyx3U6ZMyc9//vO88sor+elPf5p+/fqlYcOGSZItttgi06dPz3XXXZc333wzG220USorK+e7j1vtJaxqL001ffr0DBgwIBdccEFatmyZoUOHOqmyQPJH0WSQok2dOjU///nP8/rrr+dnP/tZ+vfvX1dM+eijj3L22WfnrrvuyoUXXpgtttgirVq1qrun+fbbb5+hQ4fmxBNPzEsvvZQbbrght99+e7p165apU6fmtddey2qrrZabbropHTt2LPhIWRmZgRRNBimaDFIk+aNoMkiRKisrc/HFF2fUqFH5wQ9+kCuuuKLuCxw//OEPM3Xq1Jx22mn597//ne985zt13yZP5r2C6dz//8Y3vpH77rsvN954Y3r16pU2bdoUc3CUBDOQoi2rOVi7rdp8PvLII5k6dWpatWqVIUOGpFu3biv+4FjpmYGsaEovLFeVlZW54YYb8tBDD2WXXXbJBRdckIYNG9a14Bs0aJD11lsvq6yySjp37pxkTkN+7sE298m1diDefPPN+fTTTw01Fkn+KJoMsjK444478tBDD2WHHXbIBRdckLKyssyaNSuNGjVKp06dcuihh+bRRx/NBx98kOnTp9fdf7esrCzV1dXZaKONcvPNN2fw4MEZMmRInnrqqfz73//O+uuvn3333Tdnn3121l577YKPkpWRGUjRZJCiySBFkj+KJoMUrUGDBnn++efTokWLnHfeeWnUqFEqKytTXl6e8vLydOvWLW3bts1WW22VZM7tPzp06JBkzvvhqqqqutsp1OrVq1euuuqqvPfee5k6darSCwtlBrIyWJZzsDabxx9/fO644460adMmgwcPzgYbbFDMwbFSMwMpgtILy9WECRPy/PPPp127dnUt0toTZXV1dZI592BbffXVc8UVV2T27Nl54403csABB2THHXfMtttuW/ehW3l5ed23zz/55JO0bNkyQ4YMMdRYKPmjaDJI0WbNmpW77ror7dq1S58+fereXNR+qyOZ06xv06ZNXn/99Tz33HN1bzSSOW36mpqadOrUKUceeWSOPPLIjBkzJtOmTasruqy66qor/LgoDWYgRZNBiiaDFEn+KJoMUqTq6uq88cYbefrpp1NeXp6JEydm9dVXT0VFRd0Hvu+8805mz56dvn375vzzz8/bb7+d3XbbLd/+9rdz5JFH1mW19lvmtd9A/+1vf5utttoqXbp0KfgoWZmZgRRteczBu+++OwMHDkybNm1c4YVFMgMpQtmkSZNqit4Jvrqqqqpy++23p7y8PAcccEAqKipSVlZW9ybhhRdeSI8ePfLZZ5+lZcuWadKkST7++OMkybbbbptf/OIX+c53vlO3vTFjxmTLLbdMkvzrX//SImWR5I+iySBFmzFjRjbeeOM0adIkTz75ZFq1ajXP8to3Dj/+8Y/z4IMP5tprr80Pf/jDBW6r9rlfvLwpLIwZSNFkkKLJIEWSP4omgxRt5syZ2XfffTNy5Mj0798/P/jBD+q+tPHSSy+lR48emTBhQrp27ZpmzZrljTfeSGVlZcrKynLaaafljDPOWOB25/4AGBbGDGRlsDzm4HnnnZeDDjpIBlkkM5AiKL2w3NR+KFZdXZ3PP/88zZo1m2f5K6+8kn322ScTJkzIQQcdlFNPPTXt2rXL008/nYEDB2bo0KHZc889c8kll6Rjx451LcDRo0enYcOGWW+99Qo6MkqB/FE0GaRotRmcMGFCnnvuuey+++4Lfe4vf/nLXH/99bnmmmvyox/9aAXuJV9VZiBFk0GKJoMUSf4omgyyMqiqqso555yTq666Kp07d84RRxyRzp07Z+rUqenXr18mTpyYXr165ayzzkqjRo3yr3/9K3fddVduvfXWNG/ePJdddll69OhR9GFQgsxAVhbLcg4u6JZvsCBmIEVxeyOWuerq6pSVlaWsrCw1NTUpLy+fb6hVVlamX79+mTBhQs4444yceeaZdcv22WeftGrVKi+//HKGDh2aI444Ih07dqy77NWGG264og+JEiJ/FE0GKdrcGZw9e3batGmz0MLLF7+hNm7cuLpfezPL0jADKZoMUjQZpEjyR9FkkJVFTU1NGjRokF//+tcZO3ZsBg0alN/97ndp0KBB2rRpk4kTJ+bwww9Pv3796tbZaaed0qpVq7z99tt56qmn8uyzzyq9sETMQFYmy3oO+jdCvowZSNFch49lrry8vO62B7Vtvi+qqKjIOeeck2uvvbZuqFVVVaWmZs6Fh771rW9lzz33TJK89dZb82wbFkX+KJoMUrS5M9iwYcO6XC1K8+bNk8x541H7/9o3s/369cstt9yynPaWrxozkKLJIEWTQYokfxRNBllZlJWVpaqqKquuumouu+yyDBw4MOedd17+8Ic/ZMcdd8w666yT3/zmN0n++z44STbffPN8+9vfTpI89dRTmTZt2mK9p4bEDGTlYg6yopmBFM2VXlgmpk6dmkceeSTPPfdc3nnnnWy44Yb52te+ll122SXl5eULvNdp165d07Vr1yTzfpt81qxZadSoUaZPn54kCxyMMDf5o2gySNEWlcHaNxkLenNQ+1jr1q2TzHnjMff/+/fvnwsuuCDNmzfP97///bRs2XIFHRGlxAykaDJI0WSQIskfRZNBijR16tRMnjw5nTt3nm9Z7TfDV1lllXz729+u+xD373//e8aOHZvJkyenQ4cOde9/Z86cmcaNG6ddu3ZJki5duqRp06Yr7FgoTWYgRTMHKZIZyMpE6YV6Gz9+fHr27Jknn3yyrhF6//33p7y8PBdeeGGOPPLIlJeX193HbUFqh1pVVVUaNWqUmpqavPjii+ncuXN23XXXFXYslB75o2gySNHqk8Hax2ofnzRpUt2yCy+8MH379k27du1y//33K7ywQGYgRZNBiiaDFEn+KJoMUqSxY8fmoIMOyjrrrJNzzjknXbp0mS9rX/ygrbKyMp9++mlmzpyZ8ePHZ7311qv7hnnjxo2TzPkwOEm+/vWvJ8ki88v/NjOQopmDFMkMZGWj9EK9TJgwIXvvvXdef/31fP3rX88+++yTTz/9NK+88kr+8Y9/5LTTTkuLFi1y4IEHfulJce5G3xlnnJGRI0dm3333TceOHVfEoVCC5I+iySBFq28Ga9901H6jo/aNcL9+/XLBBRekZcuW+etf/5ru3buv0OOiNJiBFE0GKZoMUiT5o2gySJE+++yz7LfffnnppZfy3nvv5ZJLLskpp5ySNddc80s/XFtttdUya9asnHzyybnjjjuy5ppr1i0/99xzM3jw4Gy44YbZd999k8QHvSyQGUjRzEGKZAayMlJ6YalNnTo1P//5z/P666/nZz/7WQYMGFC37LXXXstVV12Vm2++OXfccUf23HPPNG/efJHDrXaonX/++bnhhhuy+uqr55xzzkmrVq2W96FQguSPoskgRVsWGfzi7Y2qqqpyySWX1BVehg4dqvDCApmBFE0GKZoMUiT5o2gySJFmzpyZ/v3756WXXsrqq6+eJLn11ltTU1OTU045JV26dFnoumVlZTn99NMzYsSIjB49Ovvtt1/22WeftGjRIk8//XQefvjhtGvXLn/6058WeKsQSMxAimcOUiQzkJVV+Zc/BRbsL3/5Sx566KFsv/326du3b5I5J9skWX/99bPXXntl1VVXzYgRIzJu3LhFDrWJEyfmww8/zBFHHJEBAwZk9dVXz9133113Xzf4IvmjaDJI0ZZlBhs2bJgkueWWW9K7d2+FF76UGUjRZJCiySBFkj+KJoMU6Z///Gfuv//+dO7cOeedd15OOumkrLbaarn99ttz8cUX57333lvoujU1NenSpUsuuOCCrL/++nnjjTdy2WWX5bzzzsvDDz+cLbfcMkOGDMn666+/Ao+IUmMGUjRzkCKZgayslF5YKjNmzMhdd92VVq1apW/fvmnUqFGqqqrq7vlXVlaW3XffPRtvvHEmT56cV199daHbqqmpyZVXXpmNN944999/f7bffvs88MAD2WCDDVbU4VBi5I+iySBFW1YZrKmpSZI0adIkyZx7Abdq1SpDhgxReGGhzECKJoMUTQYpkvxRNBmkSFVVVXnxxRfz3nvvZccdd8yee+6ZH//4xznhhBPqPvAdMGDAQj/wrf3g7dvf/nYGDRqUo446Kvvtt1/222+/XHrppbn11luz3nrrrchDosSYgRTNHKRIZiArM7c3YqlUVVVl6tSpadKkSd191WovQZUk1dXVKS8vT/v27ZMkH3744UK3VVZWlpNOOilvv/12ttlmmxx44IF168GCyB9Fk0GKtqwyWPtGd9NNN03Tpk0zbdq0DB061JsLFskMpGgySNFkkCLJH0WTQYrUoEGDbLHFFunVq1cOPvjgrLrqqkmSgw8+OEly5ZVX5vbbb0+SnHrqqVlzzTUXuJ3q6up06NAhF1544YrZcb4yzECKZg5SJDOQlZnSC0ussrIyTZs2ze23356333477dq1m+855eVzLiLUrVu3DBkyJBUVC4/arFmz0rx589xwww2prq5e5HNB/iiaDFK0ZZ3BqqqqdO7cOf/4xz/SuHFjl49kkcxAiiaDFE0GKZL8UTQZpEiVlZWp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WVmZr3/96wtc/o9//CM//elPM3ny5DRr1izrrbdeZs+enffffz9/+MMfsvvuuy/f0kvbtm2z5557Zuutt85WW22Vm2++OQ888MCSbqbOO++8kxNOOCFVVVXp3bt3TjjhhJSVleXdd9/N/vvvn3//+98555xzctFFFy31awAAAAAAAAAArEinnHJKDj300C99Xk1NTTp27Jif//zn+eEPf5iOHTsmSaqrq3PDDTfkl7/8ZW677bZsueWW6dWr1zzrfutb38rmm2+enXbaKS1atKh7/N13383xxx+fxx9/PMccc0yefvrpedZr3Lhxjj766Bx++OHZeOON6x4fNmxYevbsmRdffDEnnXRSbr755nnWO/XUU3Pqqacu8DjeeuutbLXVVkmSH/7wh/Mtf/HFF3PooYemuro6/fv3z+GHH55GjRrVHeuzzz6b1VZb7Ut/v+a2xLc3+qLaS9cs7e2NTjvttNxwww3ZZZddcs8998yz7Jlnnsmee+6Zhg0b5j//+c8CL7kDAAAAAAAAALCyqO1RXHXVVYtVepkxY0aqq6sXegecU045JTfeeGM23njjPPXUU4u9H2PHjk23bt1SU1OT5557Luuuu27dsokTJ6Z169YLXO+ee+7Jz372s5SXl+eNN96Y72ovC/O73/0uF154YbbYYos89thj8y3fbbfd8uyzzy7278viKP/ypyw/NTU1dfdwOuyww+Zbvu2226Zbt26ZPXt2Bg8evKJ3DwAAAAAAAABguVpllVUWWnhJkp133jlJ8uabby7Rdtu3b59WrVolST7//PN5li2s8JIku+yyS5I5V1956623Fvv17rzzziQLvsrLiBEj8uyzz2bdddfNIYccstjb/DJLfHujZem9997Lxx9/nGROwWVBtt1227z22mt59tlnc8QRR6zAvQMAAAAAAAAAWDoPPPBAHnzwwUyZMiXt27fPtttumx/96Edp2bLlEm1n5syZSeaUY5bEG2+8kYkTJ6Z58+bzXOXly8yYMaPu14v7ms8880zGjBmTioqKHHDAAfMtHzp0aJJkjz32yGeffZY//vGPefrppzNr1qysu+662X///bPddtst9j7WKrT0UtsIaty4cTp16rTA53Tt2jXJkjeWAAAAAAAAAACK8re//W2en++555707ds3N9xwQ3bbbbfF3s69996bZOEXE/mi8ePH55lnnsk555yTJDn77LMXeSWZhb1eq1at0r1798Va54477kgy5yox7du3n2/5yJEjk8zph2y//fZ5//3365Y9+uijueGGG9KzZ89cdNFFKSsrW+x9LbT0MmnSpCRJy5YtF7rTtZfa+eyzzxa5rffee2+ethEAAAAAAAAAwLK2/vrrL3L52muvnbPPPjt77LFH1lprrZSVlWXEiBHp06dPnn322Rx66KEZOnRottxyyy99rUceeSQPPvhgkuQXv/jFQp83atSo7LjjjvM8tummm+b222/PXnvttRhHNcfHH3+ciy66KEly7LHHpqLiy2sls2bNqivKLOjWRrXbTZKrrroqq6yySq677rrss88+mTVrVm655Zace+65ueGGG7LeeuvlmGOOWez9LbT0UltSadSo0UKfU7ts+vTpi9xW+/btM2vWrGW3c8vY9ddfX/QulLxevXoVvQslTQbrR/7qR/7qTwbrRwbrR/7qTwbrRwbrR/7qTwbrRwbrR/7qTwbrRwbrR/7qR/6+2mbPnp0JEyakTZs2adiwYdG7w3JgBtafOfjVZQb+bzAH66fUZ+AZZ5wx32M777xzvvWtb2XvvffOc889l3POOScPPPDAIrfz3nvv5aijjkqS9OzZM9/61rcW+txmzZrlG9/4RmpqavLRRx/lgw8+yOjRo3P77bdn2223TevWrb90v2fNmpWf/vSnmTBhQjbddNOcdNJJX7pOkjz00EOZOHFiWrRoke985zsLfM7nn3+eZM4MvPjii+cpx5x44on55JNPcvXVV+fiiy9Oz549F6tskxRceqm999Oiyiq1y5o0afKl21rS+1etSOPHjy96F0peixYtit6FkiaD9SN/9SN/9SeD9SOD9SN/9SeD9SOD9SN/9SeD9SOD9SN/9SeD9SOD9SN/9SN/X20zZszIhAkT0rRp05X63/ZZemZg/ZmDX11m4P8Gc7B+vqozsFGjRvnNb36T/fbbL08++WQmTZpUd/ebL5o4cWIOPPDAjB8/Pttvv3369OmzyG2vs846GTp0aN3P77//fs4666zcd999ee211/L4448vskhSU1OTY489Nk8//XQ6duyYP//5z4u8gMncam9t9P3vf3+h3Y7aedeqVascfPDB8y0/9thjc/XVV+fTTz/NqFGjstVWWy3Wa5cv1rOWk7lvXVRTU7PA58x9CyQAAAAAAAAAgFL1ta99LUlSXV2dMWPGLPA5U6dOzYEHHphXXnklW2yxRW677bY0btx4iV5njTXWyI033phNNtkkL7/8cu6+++5FPv+MM87IXXfdldatW+eee+7JWmuttVivM2nSpDz00ENJFn5ro+S//ZC11157geWbNdZYI82aNUuSvPvuu4v12knBpZd11lknSTJz5sx89NFHC3xO7R/yuuuuu6J2CwAAAAAAAABgmZv7tmaVlZXzLZ85c2YOOeSQPPvss+nevXvuvvvuNG/efKleq7y8PLvttluS5IUXXljo884777z8/ve/T7NmzXLXXXdlo402WuzXuO+++zJz5sysscYa2X777Rf6vPXWWy9JFlneqf29qaqqWuzXL7T0suaaa2a11VZLkjzzzDMLfE7t49tss80K2y8AAAAAAAAAgGXtlVdeqft1586d51lWWVmZI444Io8//ni6du2ae++9N23btq3X69UWaxZUsEmSyy+/PAMGDMgqq6yS2267LVtvvfUSbb/21kYHHXRQysrKFvq82ivcvPPOOwtc/tlnn2XixIlJkk6dOi326xdaeikrK8t3v/vdJMktt9wy3/Jnnnkmr732Who2bJi99957Re8eAAAAAAAAAMAyc+WVVyZJunXrNk/ppaamJscee2yGDBmSTp065b777lui8seCVFZW1t16aNNNN51v+R//+MecffbZadiwYf74xz9mhx12WKLtv/POO/nXv/6VZNG3NkqSffbZJ40bN85HH32URx99dL7lAwcOTJI0b948W2211WLvw/w3SloOrr766lxzzTX52te+lhtvvHGeZSeccEJuueWWPPLII7n88stzwgknpKysLO+++26OP/74JMnhhx9ed0UYAAAAAADgy5155plF70JJ69u3b9G7AACUoEcffTSPP/54fvKTn6Rr1651j3/22Wfp06dP7rrrriTJGWecMc96v/zlL3PnnXembdu2ue++++ZZd1F+/vOfp2fPntlqq63mudLK6NGjc8455+S1117Laqutlh49esyz3n333ZdTTjkl5eXlufbaa7PXXnst8bHeeeedqampyRZbbJENNthgkc9t27ZtjjrqqFx55ZU5/fTT85e//CVrr712kjkXRLnwwguTJEcffXRWWWWVxd6HJS69/Otf/8ohhxxS9/O0adOSJJdcckmuueaauscff/zxrLHG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Pufuu+/Or3/96yXe9ueff5599903w4cPT5J06dIla6+9dsaMGZMHH3wwDz74YM4999yceOKJC1y/f//++d3vfpfq6up06NAhm2yySSZNmpRRo0ZlxIgROfnkk9OsWbO65//4xz/O008/nSRp1apVNtxww0ycODEvvvhiRo0alT//+c/561//mq5du873WtOmTcs+++yTkSNHplGjRunevXvGjRuXIUOG5KGHHsr111+f/ffff4l/D5bqSi/Dhw9P7969U15enhtuuCEjR47MU089lWHDhqVDhw4ZMmRIrrrqqsXeXu/evfPGG29k/fXXz7/+9a88//zzefLJJ/Pqq6/miCOOSFVVVU455ZRMnjx5aXYXAAAAAAAAAGCFqqmpyUknnZSGDRtmxx13XOjzmjdvnp133jmnnXZabr311vTq1Wuxtn/VVVdl+PDhadeuXR5++OGMGjUqw4YNyxtvvJFf/epXSeb0Md5666351v3jH/+Y888/P506dcq9996b1157LY888kj+/e9/Z8yYMbntttvSuHHjedYpLy/PwQcfnIcffjhvv/12hg0bllGjRuWxxx7Luuuum/feey8//elPF7ivZ511VkaOHJlu3brl2WefzeOPP56XXnop5557bqqqqnL88cfn/fffX6zjnmeflniNzGn71NTU5PDDD5/n6iubbrpp+vTpk2TOlWBmz569WNt76KGHksz5ze7WrVvd402bNk3//v3Ttm3bTJ48Oc8888zS7C4AAAAAAAAAwAp1yy235Omnn84ZZ5yR1VdffaHPO+yww3LvvffmrLPOyne+8520bt16sbZf27U4/fTTs80229Q93rBhw/zqV7/Kpptumqqqqjz66KPzrDd27Nj89re/zSqrrJJ77rknO++88zzLmzRpkr333jsNGzac5/E///nPueaaa7LNNtukrKys7vHNN9881113XZLk+eefzwsvvDDPeh9//HFuueWWJMmVV16ZLl26JJlTojnxxBOz8847Z/r06bniiisW67jntsSll8mTJ+exxx5LMuc3/ov23XfftGjRIhMmTMgTTzyxWNucPn16kizwEjcVFRVZc801k2S++0UBAAAAAAAAAKxsxo0bl3POOSfdu3fPscceu1xeY1FdiyRZe+21k8zftfjzn/+cKVOm5KCDDsoGG2yw2K+3qDLONttskxYtWiRJ3nzzzXmWDRkyJJWVldlggw3y9a9/fb51a7snDzzwwGLvS60lLr2MGjUqs2bNyiqrrJLNN998vuUNGzbMlltumSR59tlnF2ubG2+8cZLU3WdqbhMnTszrr7+eioqKbLrppku6uwAAAAAAAAAAK9Svf/3rTJw4Mf3795/viinLyqK6FjNnzszIkSOTJFtttdU8y4YOHZok2XPPPfPmm2/mrLPOyn777Zcf/vCHOf/88zNmzJgl3peqqqq6cs0qq6wyz7IRI0YkSbbddtsFrlv7+EcffbTEtziqWNIdrb3X0xprrJGKigWv3rVr1wwbNmy+9s7C/OpXv8oBBxyQ3/72t2nQoEH22GOPNG3aNC+++GLOPvvsTJs2LaeddlrWWGONhW5jxowZmTVr1pIezgrTtm3boneh5E2ePLnoXShpMlg/8lc/8ld/Mlg/Mlg/8ld/Mlg/Mlg/8ld/Mlg/Mlg/8ld/Mlg/Mlg/8lc/8ld/Mlg/Mlg/8ld/Mlg/Mlg/8ld/Mlg/K3sGa69osjDDhg3LnXfemYMOOijbb7/9ctuPk08+OQ8++GAuv/zytG7dOvvtt19at26d119/PX369Mm7776bgw46KF/72tfq1qmurs6oUaOSzOl/9OzZs+6KMUnyt7/9LZdffnmuuOKK/PCHP1zsfRk6dGg+//zzNGjQYJ7Xq32dZOFXpOncuXMaNWqUWbNm5c0331xkN+SLlrj0MmnSpCRJq1atFvqc2mW1z/0yO+20U+6999706dMnxx9//DzLunTpkuuvvz4HHXTQIrcxduzYzJgxY7Ferwg9evQoehdK3ieffFL0LpQ0Gawf+asf+as/GawfGawf+as/GawfGawf+as/GawfGawf+as/GawfGawf+asf+as/GawfGawf+as/GawfGawf+as/GayflT2Diyq9zJgxIyeffHJatGiR888/f7nuR/fu3TN06ND07t07v/3tb3PWWWfVLWvTpk0uvPDC9OzZc551Jk+eXFdy6d27d9Zee+1ccskl2WabbfLRRx/ld7/7Xe68884cd9xx2WCDDbLFFlt86X5MmzYtZ599dpLk4IMPTvv27edZ/mU9k7KysrRs2TJjx45d7J5JrSUuvdQWSxZ1+Z1GjRrN89zF8c4772TcuHEpKyvLGmuskebNm+ftt9/Ou+++m5tvvjnbbrtt1lprrYWu3759+5X6Si/XX3990btQ8nr16lX0LpQ0Gawf+asf+as/GawfGawf+as/GawfGawf+as/GawfGawf+as/GawfGawf+asf+as/GawfGawf+as/GawfGawf+as/GayfUs5g//7989Zbb+Wiiy5Khw4dlvvrvf/++/n0009TU1OTTp06pV27dnn77bczYcKEDBw4MN/4xjey2Wab1T1/2rRpdb+urq7OrbfemvXWWy/JnCuxXHfddXnttdcycuTIDBgwILfccsuX7sMJJ5yQN998M6uvvnrOO++8+ZYvTs+kcePG8zx3cS1x6aX23kuzZ89e6HNqyydfvE/Twlx88cXp3bt3unXrlieeeCKbbLJJkmTq1Kk588wzc8stt2SvvfbKv/71r7Rs2XKh+7W4r1eE8ePHF70LJe/LLhHFoslg/chf/chf/clg/chg/chf/clg/chg/chf/clg/chg/chf/clg/chg/chf/chf/clg/chg/chf/clg/chg/chf/clg/ZRqBl999dVcfvnl2XzzzXPkkUcu99e78847c/TRR6dDhw4ZNGhQ3a2UZs2alQsvvDD9+/fPPvvskyeeeKLu1kJz9yp22223usJLrbKyshxzzDE55phj8thjj6W6ujrl5eUL3Yf/+7//yz333JNmzZpl4MCBad269XzPWZyeycyZM+fbv8Wx8D1biMW5ddHi3AKp1tixY3PhhRcmSa6++uq6wkuSNGvWLJdcckm6d++ejz76KH/4wx+WdHcBAAAAAAAAAJa7U089NZWVlbn44osXWRRZFmbPnp2zzjorNTU16du3b13hJZlzd56zzjoru+yyS6ZMmZJLL720blmLFi3q9q1bt24L3PYGG2yQJJkyZUomTJiw0H244oorcumll6Zx48YZOHDgQm+F9GU9k5qamnz22WfzPHdxLfHv8jrrrJNkziVyKisrF/icMWPGJEnWXXfdL93e888/nxkzZqRZs2bZeuut51teUVFR94fz/PPPL+nuAgAAAAAAAAAsd6NGjUpZWVkOPvjgdOvWbZ7/7r333iTJZZddlm7dumXnnXeu12u9+eab+fTTT5MkO+200wKf8+1vfzvJvF2Lhg0bZq211kry31sKfVGjRo3qfl1VVbXA5/zpT3/Kb3/721RUVOSmm25a6D4k/+2Z1HZJvujDDz+su6PQ4vRM5rbEpZfNNtssDRs2zIwZM/LCCy/Mt3z27Nl1v2HbbLPNl25v6tSpX/qcmpqaJP+9nA0AAAAAAAAAwMqmqqoqn3766Xz/zZgxI8mcjsSnn36acePG1et16tO1+NrXvpZk4SWU2scbN26ctm3bzrf87rvvzsknn5zy8vJcc801+c53vrPI/ajtjjzzzDMLXF77eKdOnbLGGmsscltftMSllxYtWtS1gW655Zb5lt93332ZPHly2rRpM8/lcxamttEzderUPPfcc/Mtr6yszFNPPZVkyRs9AAAAAAAAAAArwrvvvptJkyYt8L+DDz44SfKb3/wmkyZNyosvvliv11p77bVTVlaWJBk2bNgCn/PYY48lmb9r8YMf/CBJ8re//S0TJ06cb72BAwcmSbbbbrtUVFTMs+yhhx7KMccck+rq6gwYMCAHHnjgl+7r3nvvnYqKirz66qsZPnz4fMtruyff+973vnRbX7RUN5E69dRTU1ZWlptvvjl33XVX3eMvvvhifvOb3yRJTjzxxHkueXP11Vdn0003zc9+9rN5trX55pune/fuSZJjjz02L730Ut2yKVOm5OSTT84rr7ySJPnhD3+4NLsLAAAAAAAAAPCV0bZt2+y6665JkjPPPLPuYiJJMmvWrJx//vl59NFHk8zftdhrr72y5ZZbZsqUKTn++OMzZcqUumU33nhjBg8enCQ56aST5lnv6aefzk9+8pPMnj07vXv3zk9/+tPF2tdOnTrl0EMPTZIcf/zxeffdd5PMuRLN5ZdfnkcffTSrrLJKTjjhhCX4HZij4sufMr9vfOMb+c1vfpPzzz8/PXv2zPnnn5+mTZtm9OjRqa6uzp577pnjjz9+nnU+++yzvPfee+nSpcs8j5eVleXaa6/Nvvvum9deey077LBD1lxzzTRv3jxvvfVWpk+fniQ566yzssUWWyzN7gIAAAAAAAAArJTef//97LjjjnU/1/Yk7rzzzjz44IN1j9966635xje+UffzxRdfnO985zt5//33s88++6Rz585p27ZtxowZU1dk+clPfpLvf//787xeWVlZbrrppuy999558MEHs+GGG6Zbt2755JNP8sEHHySZc0Wa2rsA1TrhhBMyffr0NG7cOIMHD64rx3zRqaeemt13332ex84///w8//zzGTVqVLbZZpt0794948aNy4cffpgGDRrk8ssvz5prrrmEv3NL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AAAAAAAAUHKUXgAAAAAAAAAAKDlKLwAAAAAAAAAAlBylFwAAAAAAAAAASo7SCwAAAAAAAAAAJUfpBQAAAAAAAACAkqP0AgAAAAAAAABAyVF6AQAAAAAAAACg5Ci9AAAAAAAAAABQcpReAAAAAAAAAAAoOUovAAAAAAAAAACUHKUXAAAAAAAAAABKjtILAAAAAAAAAAAlR+kFAAAAAAAAAICSo/QCAAAAAAAAAEDJUXoBAAAAAAAAAKDkKL0AAAAAAAAAAFBylF4AAAAAAAAAACg5Si8AAAAAAAAAAJQcpRcAAAAAAAAAAEqO0gsAAAAAAAAAACVH6QUAAAAAAAAAgJKj9AIAAAAAAAAAQMlRegEAAAAAAAAAoOTUq/Ty0EMPpUePHunatWs6d+6cHXfcMdddd12qq6uXepv33ntv9t9//6y//vrp0KFDNtxww+y///655ZZb6rOrAAAAAAAAAADL3aBBg3LSSSdlp512ygYbbJD27dunS5cu2WOPPXLNNddk1qxZ863zySef5Lbbbsvpp5+eXXbZJR06dEirVq1ywgknLPK1Ro4cmd/+9rfZe++9s8kmm6Rjx47p3Llztttuu/z2t7/Np59+utB1q6urc/PNN2evvfZKly5d0rlz53zzm9/MgAEDMnPmzC89ztdffz0nn3xyNt9886y22mrp2rVrdtxxx/zmN7/JpEmT5nt+q1atFvnfz372sy99zS+qWOI1/r9LLrkk5557bpKka9euadq0aV566aX88pe/zGOPPZaBAwemvHzxOzUzZ87MEUcckSFDhtRtc80118ynn36aRx99NOPHj89hhx22tLsLAAAAAAAAALDcXXnllfnXv/6Vxo0bp2PHjtlkk03yySefZPjw4Rk+fHjuuOOO3HfffWnVqlXdOnfffXd+/etfL/FrDRo0KFdccUUaNGiQ1VZbLd27d89nn32W1157LaNHj87AgQNz7733ZvPNN59nvcrKyvz4xz/O0KFDkyTrrLNOWrRokdGjR+e8887LoEGD8te//jXNmjVb4OsOHDgwp5xySmbOnJlWrVplo402yrRp0/LGG29k1KhROfTQQ+c5vrl94xvfWODj66+//hIf/1KVXoYPH57evXunvLw8119/fQ444IAkyYsvvpj9998/Q4YMyVVXXfWljaO5HXfccRkyZEi++c1v5rLLLpvnYMaNG5dRo0Ytza4CAAAAAAAAAKwwhx12WH7zm9/kG9/4Rho2bFj3+IgRI3LEEUdk5MiROf/889O/f/+6Zc2bN8/OO++crbfeOltttVUee+yxXH/99V/6Wt/61rey+eabZ6eddkqLFi3qHn/33Xdz/PHH5/HHH88xxxyTp59+ep71BgwYkKFDh6Z58+b585//nJ122inJnH7GEUcckSeffDK/+tWvcuWVV873mg8//HBOOOGENGvWLNdee2169OhRd1GUysrKPPXUU+nYseNC97m2aLMsLNXtjfr375+ampocfvjhdYWXJNl0003Tp0+fJHOuBDN79uzF2t7DDz+cu+66K926dcvdd989X3unXbt22WWXXZZmVwEAAAAAAAAAVphDDz00O+ywwzyFlyT52te+VtepePDBB+dZdthhh+Xee+/NWWedle985ztp3br1Yr3WzjvvnO9973vzFF6SpEuXLvnDH/6QsrKyjB49Om+++Wbdsurq6lx33XVJklNPPbWu8JLM6WdcffXVady4cW677ba8884782x31qxZOemkk1JTU5NbbrklP/jBD+a5C1BFRUV22mmntGnTZrH2v76WuPQyefLkPPbYY0mywNsN7bvvvmnRokUmTJiQJ554YrG2ec011yRJTjvttDRp0mRJdwkAAAAAAAAAYKVXexGQzz//fLm/Vvv27etuMTT367322muZMGFCkqRHjx7zrdelS5dsueWWqaqqygMPPDDPsr/+9a95//33s9NOO81TlinKEt/eaNSoUZk1a1ZWWWWV+e75lCQNGzbMlltumWHDhuXZZ5/90iu0TJ8+PcOGDUtZWVn22GOPPPHEE7njjjvy7rvvpmXLltluu+1y2GGHpXnz5ku6qwAAAAAAAAAAK40RI0YkyQL7FsvaG2+8kYkTJ6Z58+ZZd9116x6fNGlS3a87deq0wHVrH3/22Wfnebz21kR77rlnPvroo9x4440ZOXJkampqssEGG+Tggw/OJptsssj9OuOMM/L666+nvLw8Xbt2zZ577pndd989ZWVlS3yMS1x6eeutt5Ika6yxRioqFrx6165dM2zYsHkuj7MwL730UiorK9O5c+dcdtllueSSS+ZZ/te//jVXXHFF7rjjjmy22WYL3c6MGTMya9asJTiSFatt27ZF70LJmzx5ctG7UNJksH7kr37kr/5ksH5ksH7kr/5ksH5ksH7kr/5ksH5ksH7kr/5ksH5ksH7kr37kr/5ksH5ksH7kr/5ksH5ksH7kr/5ksH5W9gx+8VZCX6aqqioff/z/2LvzcC3nxH/g79OukkaFQpJ1jAwmu2GsWcc2GTEZSxpL2fd1kD0aIcYyYzfC2FLGYCrLKNmZ0MgSSqQUOm3n/P7wO+fbUanTg+M2r9d1uTj38nk+9/G+znOe57yfzz0hQ4YMydlnn51mzZrlrLPO+o5ml0yaNCkjRoyofowzzzwzTZs2rd4/9/zHjx+flVdeeZ4xxo8fnyQZM2ZMje0vvvhikuTzzz/PJptsUqNA8+ijj+bqq6/OGWeckWOOOWaB87v22mtrfH3DDTdk0003zc0335zWrVsv2kX+f2VTpkyprM0J/fv3z5lnnpnOnTvn0Ucfne8xZ511Vi6//PJ06dIld9555zeO9+CDD6Z79+5p2LBhZs2alR122CHnnntuVlpppbz66qs55phj8tJLL2WFFVbIM888k+bNm893nHHjxqW8vLw2lwIAAAAAAAAAUCtVtyhamAEDBuTUU0+tsW3nnXfOaaedlrXWWusbz73gggty0UUXpXv37rniiisW+lgvv/xytthiixrbOnXqlNNOOy077LBDje2zZ8/OyiuvnGnTpuWcc87JkUceWWP/uHHjssEGG6S8vDzLL798Xnvttep97du3z9SpU9OwYcO0atUq/fr1y1ZbbZXJkyfnqquuypVXXpkkuf3227PTTjvVGPc3v/lNfve732XddddN27ZtM2nSpAwaNCh9+vTJ1KlT07lz5zz88MMLXIBlfmq90ktVsaRhw4YLPKZRo0Y1jv0mVfeNmjVrVjp06JBbbrmleuz1118/AwcOzHrrrZf3338/t912W/7whz/Md5w2bdr8oFd6+XpTidrr2bNnXU+h0GSwNPJXGvkrnQyWRgZLI3+lk8HSyGBp5K90MlgaGSyN/JVOBksjg6WRv9LIX+lksDQyWBr5K50MlkYGSyN/pZPB0vxYMtiuXbtsvPHGmTVrVsaNG5eJEyfmiSeeyD333JM11lgj9evX/9Yeq3nz5tl4441TWVmZ8ePH54MPPsjo0aPzt7/9LRtttFF+8pOfVB/boEGD7L///rnqqqvSt2/frLHGGunSpUuSZMKECTnkkEOq+x7Tp0+v8ThffPFFkq86Hn/+85+z5ZZbJvnqdkh9+vTJO++8k0GDBuWiiy6ap/Ry9913z/P96dmzZzp37pwuXbpk1KhRufvuu7PPPvss8nXXuvTSpEmT6gtYkKrySdWxizJekhx88MHzlGmWXXbZ7Lnnnrn11lvz2GOPLbD00qRJk0V6vLoyadKkup5C4dV2iShqksHSyF9p5K90MlgaGSyN/JVOBksjg6WRv9LJYGlksDTyVzoZLI0Mlkb+SiN/pZPB0shgaeSvdDJYGhksjfyVTgZL82PJ4O67757dd9+9+utRo0bl6KOPzqWXXprJkyfnsssu+9Yeq2PHjnn44Yerv37//fdz+umn57777subb76Z4cOH11hB5fTTT8+oUaMyYsSI/Pa3v03btm3TsmXLjBkzJnPmzMnee++dgQMHplmzZjUep0mTJvniiy+y1lprVRde5nb44Ydn0KBBeemll/LJJ58s0u2K1l9//ey22265++678+CDD9aq9FJvkY/8/1q2bJkkNe7L9HVV+6qOXZTxkmT11Vef7zFrrLFGkuS9995blCkCAAAAAAAAAPygdO7cOXfddVcaN26cG2+88TvtQKywwgr5y1/+krXXXjv/+c9/cs8999TYv8QSS+SBBx7Iueeem3XWWSdTpkzJ+++/n8022yz3339/Nt988yRfLVQyt6qOx4Ju8VTV70hq1/HYYIMNkiRvv/32Ip+TLEbppWPHjkm+agXNnj17vse88847SZJVVllloeOtuuqq1f/duHHj+R5TdbukOXPm1GaqAAAAAAAAAAA/GG3btk2nTp1SUVGRV1999Tt9rHr16mXbbbdNkrz00kvz7G/cuHF69+6d4cOHZ/z48Rk3blzuv//+bLHFFnnhhReSJOuuu26Nc6o6HgvrdyS163hU3RVoQT2UBal16WWdddZJw4YNU15ePt9vyqxZs6ovvnPnzgsdb/nll88KK6yQ5P/KMl9Xtb1t27a1nS4AAAAAAAAAwA9GVbGjtgWP7+uxZs+encGDBydJunTpUmNf1YosC+t3JLXreIwePTpJ0q5du0U+J1mM0kuLFi3yq1/9Kklyyy23zLP/vvvuy9SpU7P00ktXL3ezMLvttluS5G9/+9s8+8rLy3PvvfcmSbbYYovaThcAAAAAAAAA4Afh3XffrV7hpVOnTt/pY82ePTuPPPJIrR/r6quvzkcffZRVV10122yzTY19u+++e5Jk1KhRGTNmzDzn3nbbbUm+uotQ1QIoCzNx4sTcddddSVLdR1lUtS69JMlxxx2XsrKy3Hzzzbn77rurt7/yyis57bTTkiRHHXVUjWVrBgwYkE6dOuWggw6aZ7wjjzwyzZs3zzPPPJO+ffumoqIiSTJ9+vQcc8wxmTBhQlq2bJkDDjhgcaYLAAAAAAAAAPCde/HFF3P++efPdyWURx99NF27ds3s2bOz/fbbZ+WVVy758Q477LA899xzqaysrLF99OjR2XffffPmm29m2WWXrV6MpMoHH3yQO++8M9OnT6/eNmPGjAwYMCB//OMfU79+/fTr1y/16tWslay99tr59a9/nYqKivTq1SsTJ06s3jdo0KD89a9/TZIcffTRNc47++yzM3DgwHz55Zc1tr/yyivZfffdM2XKlLRp06bWvZAGtTr6/9t4441z2mmnpU+fPunRo0f69OmTZs2aZfTo0amoqEiXLl3Sq1evGud89tlnGTduXNq3bz/PeMsuu2yuu+66/P73v0+fPn1y7bXXZoUVVsh///vfTJ06NU2bNs1f/vKXtG7denGmCwAAAAAAAADwnZs2bVouvvjiXHzxxVl22WXTrl27zJw5M++//34+++yzJMn666+fq6++usZ577//fo2731SVUQYOHJiHHnqoevvtt9+ejTfeuPrrO+64I3fccUeWXHLJrLTSSmnQoEHGjx+fiRMnprKyMm3atMkdd9yRFi1a1Hi8SZMm5Q9/+EN69+6d9u3bp3nz5nnrrbcybdq0NGnSJFdeeWV++ctfzvcaL7/88owZMyYjRoxIp06d8tOf/jRTpkypLvrsv//+2X///Wuc88Ybb6Rfv35p0KBBOnbsmBYtWuSTTz6pPmeZZZbJHXfckZYtWy76NzuLWXpJkuOPPz5rr712BgwYkBdffDETJ07MWmutlf322y89e/ZM/fr1azXejjvumH/961+57LLL8uSTT+aVV15J69ats9NOO+XYY4/N6quvvrhTBQAAAAAAAAD4znXq1CkXXnhhhg0bltdffz1jxozJzJkzs/TSS2fDDTfM7rvvnt/+9rdp0KBmXWPOnDn59NNP5xlvxowZmTFjRvXXs2bNqrH/mmuuybBhw/LCCy/kgw8+yLRp07Lkkktmo402ynbbbZeDDz54vkWSFVZYIYcddliefPLJvPfeexk3blyWW265dO3aNb169UrHjh0XeI0/+clP8thjj+Xyyy/Pfffdl9dffz2NGjXKpptumoMPPjh77bXXPOccfPDBWWaZZfLcc89lwoQJGTt2bJo2bZr1118/22+/fQ455JC0atVqYd/eeSx26SVJdthhh+ywww6LdOwpp5ySU0455RuP+dnPfpYbbrihlCkBAAAAAAAAANSJli1b5tBDD82hhx5aq/NWWmmlTJkypdaPt88++2Sfffap9XlLL710LrjgglqfV6Vp06aL1AOpss0222SbbbZZ7MdbkHoLPwQAAAAAAAAAAH5YlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCKan08sgjj2S33XZLhw4d0q5du2yxxRb585//nIqKipIndvPNN6dly5Zp2bJlevfuXfJ4AAAAAAAAAADfpcrKyvz73//OGWeckW233Tbt27dPmzZtsuaaa6Z79+4ZPnz4N54/cuTIdOvWLausskqWW265bLTRRrn44otTXl6+wHNmzJiRK664IltuuWWWX375rLDCCtlqq61y/fXXL7C/MXbs2PTp0ye777571llnnbRr1y7LLbdcfvGLX+S4447L22+/Pd/zKioq8sgjj+SCCy5I165ds8oqq6Rly5Zp1arVIn1/ysvLc9FFF2WjjTbKcsstl1VWWSXdunXLs88+u0jnf12DxTorSb9+/XL22WcnSTp06JBmzZrl1VdfzUknnZShQ4fmtttuS716i9ep+eSTT3LWWWct7tQAAAAAAAAAAL53w4cPz2677ZYkqVevXjp27JimTZtm7NixefDBB/Pggw/m+OOPz+mnnz7PuQMHDsxhhx2WOXPmpF27dll++eUzevTonH/++Xn44YczaNCgNG3atMY506ZNyx577JFRo0alrKwsa6yxRho0aJCXX345L7zwQv75z3/mtttuS4MGNeshTz75ZPr27ZuysrK0adMmq666ar788su89957ueGGG3L77bfn1ltvzTbbbFPjvKlTp2bvvfderO/NF198kZ133jkvvvhiGjVqlDXXXDOffPJJhgwZkkceeSTXXntt9tprr1qNuVitlJEjR+acc85JvXr1cv311+fFF1/MU089lWHDhmWZZZbJkCFDctVVVy3O0EmSU089NZ999lm6dOmy2GMAAAAAAAAAAHyfKisr07Fjx1x66aUZO3ZsRo0aleHDh2fs2LE59thjkyR9+/bNww8/XOO8d999N717986cOXNyzjnn5LXXXsvw4cPz3HPPZbXVVsvzzz8/38VDTj755IwaNSpt27bN8OHD88wzz+TJJ5/M888/n5/+9Kf5xz/+kcsuu2ye8372s5/luuuuy5gxY/Lmm29m+PDhGTVqVEaPHp299tor06dPT8+ePTN9+vQa59WrVy/rrLNODjzwwFxxxRUZOHDgIn9vTj/99Lz44otZffXVq78vr776as4+++zMmTMnvXr1yvvvv7/I4yWLWXrp27dvKisrs//+++c3v/lN9fZOnTrlvPPOS/LVSjCzZs2q9dhDhw7NwIEDc+CBB2bdddddnOkBAAAAAAAAAHzv1l9//YwcOTIHH3xwWrZsWb29UaNGOfPMM7PddtslSW666aYa511xxRWZMWNGtt566xx55JEpKytLkrRv3z5XXnllkuTGG2/MxIkTq8/59NNP87e//S1Jct5556VTp07V+1ZaaaX079+/euwvvviixuP94he/SNeuXdO6desa21u1apWrr746LVu2zKRJk/LMM8/U2N+iRYsMHz48/fr1S/fu3bPGGmss0vdlwoQJueWWW5IkV155Zdq3b5/kqxLNUUcdla222irTp0/PFVdcsUjjVal16WXq1KkZOnRokqR79+7z7N99993TokWLfPrpp3niiSdqNXZ5eXmOPfbYtGnTJmeccUZtpwYAAAAAAAAAUGdatGgxz62E5varX/0qSfLWW29Vb6usrMygQYOSzL+HsdFGG2X11VfPrFmzMnjw4Orto0aNypw5c1KvXr3ssssu85y3wQYbpF27dpk2bVoeffTRRb6GRo0aZaWVVkqSfPnll4t83jcZMmRIZs+enTXWWCMbbrjhPPurrvuBBx6o1bi1Lr28/PLLmTlzZpo0aZKf//zn8+xv2LBh1ltvvSRffYNro2/fvhk7dmzOOeecGo0nAAAAAAAAAICimzFjRpKkSZMm1dvGjRuXCRMmJPmq4DI/Vdvn7mFMmTIlSdK6des0atRovue1bdt2nvMWZvLkyfnvf/+b+vXrZ+21117k877Js88+m2Th1zd+/Pha3eJowfWiBRg7dmySZIUVVlhgO6lDhw4ZNmxYjWbSwrzxxhvp379/Ntlkk3Tr1q2200p5eXlmzpxZ6/O+L61atarrKRTe1KlT63oKhSaDpZG/0shf6WSwNDJYGvkrnQyWRgZLI3+lk8HSyGBp5K90MlgaGSyN/JVG/kong6WRwdLIX+lksDQyWBr5K50MluaHnsEWLVos1nmVlZW57777ktQsf1T1MBo3blxdUvm6Dh06JKm5QkzVPCZNmpSZM2fOt/gyfvz4JMmYMWMWOr8pU6bkpZdeyrnnnpsvvvgiRx55ZPWKL6Wqusaq6/i6du3apVGjRpk5c2beeuutrLDCCos0bq1LL1VNoW9aiaVqX9WxC1NZWZmjjz46FRUVufTSS2s7pSTJxx9/nPLy8sU69/uw22671fUUCu+jjz6q6ykUmgyWRv5KI3+lk8HSyGBp5K90MlgaGSyN/JVOBksjg6WRv9LJYGlksDTyVxr5K50MlkYGSyN/pZPB0shgaeSvdDJYmh96Bhe39HLTTTfl5ZdfTqNGjXL44YdXb6/qViy11FIpKyub77lVPYzPPvusett6662XsrKyzJkzJ4MHD87uu+9e45znnnsuH3744TznzW3KlCnzFFE6dOiQAQMGZN99963F1X2zhXVNysrKstRSS+Xjjz9e5K5Jshill6piScOGDRd4TFV7aFFLKLfcckv+/e9/p3fv3llrrbVqO6UkSZs2bX7QK71ce+21dT2FwuvZs2ddT6HQZLA08lca+SudDJZGBksjf6WTwdLIYGnkr3QyWBoZLI38lU4GSyODpZG/0shf6WSwNDJYGvkrnQyWRgZLI3+lk8HS/Bgz+OKLL+bkk09Okpx++ulZeeWVq/dVdSsWdIuiufdNnz69etuyyy6bXXbZJQ8++GBOOeWUrLDCCuncuXOS5L///W+NYs3c582tQYMG2XjjjZMkEydOzLhx4/Luu+/mrrvuyuabb5727dsvzuXOY1G6Jo0bN65x7KKodeml6r5Ss2bNWuAxVeWTue9BtSCffPJJzjrrrCy//PI56aSTajudGvNalMerK5MmTarrKRTe4rbl+IoMlkb+SiN/pZPB0shgaeSvdDJYGhksjfyVTgZLI4Olkb/SyWBpZLA08lca+SudDJZGBksjf6WTwdLIYGnkr3QyWJofWwbfeeed7LPPPikvL0/Xrl3Tu3fvGvurug7ftNBH1b4llliixvbLLrssr7/+esaMGZNtt9027du3T6NGjTJ27Ng0aNAge+yxR+699940a9ZsvuM2b948Dz/8cPXXn376aS644IJcd9112W677TJixIhvvBPQolqUrsmMGTNqHLso6tV2Ioty66JFuQVSlTPPPDOTJ0/O+eefn+bNm9d2OgAAAAAAAAAAP0gfffRR9thjj0yYMCFdunTJgAED5rmF0dy3LqqsrJzvOHPfAmlubdq0yaOPPprjjz8+a6yxRiZOnJiPP/44Xbp0yaOPPppVVlklyVerwiyKpZdeOpdcckm6dOmSjz76KNddd10trnbBFtY1qaysrL4FU21KNrUuvXTs2DFJ8v7772f27NnzPeadd95Jkupv3jd5+eWXkyQnnHBCVl999Rr/XHnllUmSu+++u3obAAAAAAAAAMAP3eTJk7PHHnvk7bffzmabbZYbb7xxvrf3qephzJgxI+PHj5/vWN/Uw1hqqaVy+umnZ8SIEZkwYULefffd3HHHHVlnnXXywgsvJEnWXXfdWs29S5cuSZKXXnqpVuctSNU1Vl3H13344YfVq9ksStekSq1LL+uss04aNmyY8vLy+V7crFmzqr9pVfeKWhQTJ06c558vvvgiyVf3lqraBgAAAAAAAADwQ/b555+na9eu+c9//pP1118/f/vb3+a5NVGVFVdcsXollhEjRsz3mKrttelhTJ48OU8++WSS/yuxLKqqRVAWtBhKbVXNe2HX17Zt26ywwgqLPG6tSy8tWrTIr371qyTJLbfcMs/+++67L1OnTs3SSy+dzTfffKHjPfnkk5kyZcp8/znppJOSJN27d6/eBgAAAAAAAADwQzVjxozsu+++GTVqVH7605/mnnvuyZJLLrnA48vKyrLLLrskmX8PY8SIEXnzzTfTsGHD7Ljjjos8j/PPPz8zZszIlltumTXWWKNW1/DQQw8lSTp16lSr8xZkxx13TIMGDfLGG29k5MiR8+yvuu5dd921VuPWuvSSJMcdd1zKyspy88035+67767e/sorr+S0005Lkhx11FFp1KhR9b4BAwakU6dOOeiggxbnIQEAAAAAAAAAftDmzJmTgw46KMOHD8/KK6+ce++9Nz/5yU8Wel7v3r3TqFGjPP744+nfv38qKyuTJO+991569eqVJNl///2rV4Sp8tprr2XQoEE1VmT5/PPP88c//jHXXXddmjZtmr59+87zeCeeeGKGDx+eOXPm1Nj+3nvv5dBDD82wYcOyxBJLpHv37rX+HsxP27Zts99++yVJevXqlffeey9JUllZmf79++df//pXmjRpkt69e9dq3AaLM5mNN944p512Wvr06ZMePXqkT58+adasWUaPHp2Kiop06dKl+pte5bPPPsu4cePSvn37xXlIAAAAAAAAAIAftHvvvbd6lZR69erlgAMOmO9xyy67bG666abqrzt06JDLL788RxxxRM4888xcc801ad26dUaPHp1Zs2Zl3XXXzTnnnDPPOG+//XZ+97vfZYkllshKK62Uhg0bZsyYMSkvL89SSy2VW265Jauttto85w0ZMiTXXnttllhiiay88spp0qRJJkyYkAkTJqSioiJLLrlkrrvuuvl2PLp161Z9O6KKiookX5V9OnbsWH3MXnvtlUsuuaTGeX369MkLL7yQl19+OZ07d86aa66ZTz75JB9++GHq16+f/v37Z8UVV1zId7imxSq9JMnxxx+ftddeOwMGDMiLL76YiRMnZq211sp+++2Xnj17pn79+os7NAAAAAAAAABA4cyYMaP6v99666289dZb8z1ufuWObt26pWPHjrnssssycuTIvPHGG+nQoUP22muvHH300WnSpMk856y99to58MAD8+9//zsffPBBZs+enRVXXDFdunRJ796951kZpspFF12Uf/7znxk5cmQmTJiQzz77LE2bNs3Pf/7zbL311jn44IPTrl27+Z47derUfPrpp/Nsn3vb559/Ps/+JZdcMv/4xz9y+eWX55577skbb7yRZs2aZYcddsixxx6bDTfccL6P900Wu/SSJDvssEN22GGHRTr2lFNOySmnnFKr8RfnHAAAAAAAAACAurDffvtV38ZncWy00Ua58847F/n4Dh06pF+/frV+nJ122ik77bRTrc9LUr2SzeJYYoklcvLJJ+fkk09e7DHmVu9bGQUAAAAAAAAAAL5HSi8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhKL0AAAAAAAAAAFA4Si8AAAAAAAAAABSO0gsAAAAAAAAAAIWj9AIAAAAAAAAAQOEovQAAAAAAAAAAUDhKLwAAAAAAAAAAFI7SCwAAAAAAAAAAhaP0AgAAAAAAAABA4Si9AAAAAAAAAABQOEovAAAAAAAAAAAUjtILAAAAAAAAAACFo/QCAAAAAAAAAEDhlFR6eeSRR7LbbrulQ4cOadeuXbbYYov8+c9/TkVFRa3Geemll3Leeedlp512SseOHdO6deusuuqq+c1vfpMHH3ywlCkCAAAAAAAAAHwv3nnnndx000058sgjs9lmm6VVq1Zp2bJlLrnkkoWeO3LkyHTr1i2rrLJKlltuuWy00Ua5+OKLU15evsiPP3To0LRs2TItW7bMbrvtttDjn3/++fzhD3/I2muvnWWWWSarrLJKtttuu5x77rmZPXt2jWPffffd6rEX9M8f//jH+T7Ows476KCDFvka59Zgsc5K0q9fv5x99tlJkg4dOqRZs2Z59dVXc9JJJ2Xo0KG57bbbUq/ewjs1b7/9drbccsvqr1daaaW0b98+77zzTh599NE8+uij6datW6666qpFGg8AAAAAAAAAoC5cc801ueaaa2p93sCBA3PYYYdlzpw5adeuXZZffvmMHj06559/fh5++OEMGjQoTZs2/cYxysvLc+yxxy7yY/bt2zfnn39+Kioqsswyy2TttdfOlClT8vLLL+fZZ5/NMccck+bNm89zXuPGjbPeeuvNd8z27dt/42NuvPHG892+2mqrLfK857ZYpZeRI0fmnHPOSb169XLttdfmN7/5TZLklVdeyV577ZUhQ4bkqquuSu/evRc6VmVlZZZbbrkcdthh+e1vf5vlllsuSVJRUZHrr78+J510Uu64446st9566dmz5+JMFwAAAAAAAADgO9eqVat06dIlv/jFL7L++uvn5ptvzgMPPPCN57z77rvp3bt35syZk3POOSe9e/dOWVlZ3nvvvey11155/vnnc9ZZZy10tZi+fftm7Nix2XHHHTNkyJBvPPbGG29Mnz59svzyy+fKK6/MVlttVb1v+vTpGTp0aBo3bjzfc5dZZpk8/PDD3zj+gizueQuyWEun9O3bN5WVldl///2rCy9J0qlTp5x33nlJvloJZtasWQsdq127dnn++edz1FFHVRdekqRevXrp2bNnDjzwwCTJTTfdtDhTBQAAAAAAAAD4Xpxwwgm58847c+KJJ2bbbbdNs2bNFnrOFVdckRkzZmTrrbfOkUcembKysiRfrZpy5ZVXJvmqpDJx4sQFjvHGG2+kf//+2W677bLLLrt84+N9/PHHOeOMM9KkSZP8/e9/r1F4SZIlllgiO+64Yxo2bLjQude1Wpdepk6dmqFDhyZJunfvPs/+3XffPS1atMinn36aJ554YqHjNWnS5BuX4Kn65r711lu1nSoAAAAAAAAAwA9WZWVlBg0alGT+HYyNNtooq6++embNmpXBgwcvcIyjjz469erVW+hqMEly6623Ztq0adl7772zxhprlHYBdazWtzd6+eWXM3PmzDRp0iQ///nP59nfsGHDrLfeehk2bFhGjRqVrbfeuqQJzpgxI8lX5RgAAAAAAAAAgB+LcePGZcKECUm+KrjMz0YbbZQ333wzo0aNygEHHDDP/ltuuSX//ve/c8opp6RDhw556qmnvvExq24x1KVLl7z11lv561//mv/85z9p2LBhOnXqlN/97nfp0KHDAs+fNm1ajj766Lz99ttp1KhRVl111ey6667ZdNNNF3q9J554YsaMGZN69eqlQ4cO6dKlS7bbbrvq1W1qq9all7FjxyZJVlhhhTRoMP/TO3TokGHDhn0rq7Pce++9SRb8P7dKeXl5Zs6cWfLjfVdatWpV11MovKlTp9b1FApNBksjf6WRv9LJYGlksDTyVzoZLI0Mlkb+SieDpZHB0shf6WSwNDJYGvkrjfyVTgZLI4Olkb/SyWBpZLA08lc6GSzNDz2DLVq0+NbGqupgNG7cOG3btp3vMVUFlPl1MD755JOcddZZ6dixY44++uiFPl5FRUVefvnl6sfu0aNHpk+fXr3/H//4R/r3758rrrgiv/3tb+c7xpQpU3LjjTdWf/3Pf/4zV199dXbbbbcMGDDgG2/pdO2119b4+oYbbsimm26am2++Oa1bt17o/L+u1qWXKVOmJElatmy5wGOq9lUdu7gef/zxPPTQQ0mSI4888huP/fjjj1NeXl7S432Xdtttt7qeQuF99NFHdT2FQpPB0shfaeSvdDJYGhksjfyVTgZLI4Olkb/SyWBpZLA08lc6GSyNDJZG/kojf6WTwdLIYGnkr3QyWBoZLI38lU4GS/NDz+C3WXqp6lUstdRSC1ztpKqD8dlnn82z79RTT83kyZNz/fXXp3Hjxgt9vKlTp1aXXM4555ysvPLK6devXzp37pzx48fn/PPPz8CBA3PEEUdkjTXWyLrrrlt9boMGDbL77runW7duWWuttbLsssvmww8/zF133ZVLLrkk999/fyorK3PzzTfP87jbbrttfve732XddddN27ZtM2nSpAwaNCh9+vTJ008/nX322ScPP/zwAhdfWZBal16qiiUNGzZc4DGNGjWqceziGDduXA455JAkSY8ePbLZZpt94/Ft2rT5Qa/08vW2ErXXs2fPup5CoclgaeSvNPJXOhksjQyWRv5KJ4OlkcHSyF/pZLA0Mlga+SudDJZGBksjf6WRv9LJYGlksDTyVzoZLI0Mlkb+SieDpflfymBVr6KqZzE/VfvmXpElSYYNG5aBAwdmt912yzbbbLNIj/fFF19U/3dFRUVuv/32rLrqqkm+WlHmz3/+c9588828+OKLufTSS3PLLbdUH7/88svXWOGl6pwTTjgha621Vvbbb7888MADefrpp+e51dHdd99d4+t27dqlZ8+e6dy5c7p06ZJRo0bl7rvvzj777LNI11Gl1qWXJk2aJElmzZq1wGOqyidVx9bW5MmT07Vr10yaNCmbb755zjvvvEWa1+I+3vdh0qRJdT2Fwvs223L/i2SwNPJXGvkrnQyWRgZLI3+lk8HSyGBp5K90MlgaGSyN/JVOBksjg6WRv9LIX+lksDQyWBr5K50MlkYGSyN/pZPB0vwvZbCq5/BNi3xU7VtiiSWqt5WXl+eYY45J8+bNc/7559f68ZKvVl+pKrxUKSsry6GHHppDDz00Q4cOTUVFRerVq7fQ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AAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAoHKUXAAAAAAAAAAAKR+kFAAAAAAAAAIDCUXoBAAAAAAAAAKBwlF4AAAAAAAAAACgcpRcAAAAAAAAAAApH6QUAAAAAAAAAgMJRegEAAAAAAAAAoHCUXgAAAAAAAAAAKBylFwAAAAAAAAAACkfpBQAAAAAAAACAwlF6AQAAAAAAAACgcJReAAAAAAAAAAAo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o0enoqIiXbp0ye2335769etXH3/BBRfkoosuymabbZaHHnponvHuuOOOHHHEEamoqEi7du3SunXrjB49OrNmzcq6666bhx56KM2aNVvMywQAAAAAAAAA+O7Vtk/B4luslV6S5Pjjj8/f/va3bLHFFvn000/z9ttvZ6211soFF1ywWP+DunXrliFDhqRLly6ZPn163njjjXTo0CEnn3xyHn74YYUX+AGrWp0p+eo+dAAAAAAAAAD/q77tPgULttgrvQB83b333psBAwbkjjvuSOvWret6OgAAwP+AysrKlJWVLfBrAAAAAH68FnulF344Kioqqv/bKhvUlaFDh+YPf/hDRo0alUcffbSupwMAP3pzr7Q2Y8aM+W4H+LGbu+DyzjvvJInCCwAA8L2orKysfh/G+zF8X2QN5qX08iNQr95X/xvvueee3HPPPUmSOXPm1OWU+B8w9y9yc+bMyQ033JAGDRrkmmuuyT777FPHswOAH7e5/8j73HPPpV+/frnzzjuT+GMv35+532SZPHlyjfIVfF+qfuY98MAD2XrrrXPJJZfU8Yz4X+LNZuB/lZ9//BDML4dzf0AYvitzZ2/u92C8H8P3oaKiojpr48aNy3/+85+8/fbb+fjjj+t4ZlC3lF5+JJ555pn06NGj+o8d7gHGd63qSfW1117LF198kbFjx2bffffNb3/72yReYPD9mvuFhjdeqAtfz50c8l2au/By7733pnv37rnoooty9913Z8yYMXU8O/5XzP0my7Bhw9KrV68cddRRmTBhQh3PjP9FI0eOTK9evTJz5sz85Cc/qevp8D9i7ufjDz74IGPGjEl5eXkdz4r/FXO/3qh6/6XqA3Dej+G79vU/tr333nt5/fXXaxzjNTHftbmfh0ePHp1BgwYl+b8PCMN3Ze7sPfLIIzniiCOy66675phjjsljjz2WadOm1fEM+TGrrKyssRDCbrvtli233DJbbrllunbtmocffriOZwh1p0FdT4Bvx3LLLZdWrVpl6NChuf/++7PbbrvV9ZT4H/Dwww+nW7du2X333TNhwoRssMEGSb568esFBt+1uV9gVP3769mTRb5LX8/g3HnzyQ6+K3Pn7tZbb03v3r1Tv379nH322fn973+fFi1a1PEM+V8w95ssAwcOzAknnJCpU6dm8803z/jx47PccsvV8Qz5sZv7Z2Hy1a1Wp02blv79+6d79+51ODP+V8z9e98jjzySfv365csvv8yxxx6bnXfeOQ0aeLuN787cPwP/+c9/ZujQoRk/fnxat26dHj16ZPXVV6/jGfJjNvfvgX//+9/Tt2/ffPrpp5k8eXK6du2aLl26ZNddd01ZWdk8z9fwbZn7efihhx5Knz598vrrr+e4447L6aefXsez48eu6ufa7bffniOOOKJ6+1NPPZWHH344u+66a0466aS0atWqrqbIj1hV/u6666707NkzSfLTn/40X375ZV566aV069Ytl112WQ488MC6nCbUCa/CfwQqKirSoUOHnHjiiTnllFPy9NNPK73wnausrMyMGTPSvHnz/OMf/0h5eXmmTp2a5KtPFyka8F36+m09Hn/88bzwwguZM2dONt5442ywwQbZfPPN5ZDvzNwZHDVqVB599NEMHTo0Sy21VNq3b5+DDjoo7du3T7NmzbzRx7eqKktDhgxJ796906pVq1xyySXZY489ktT81CV8V77+Jt+SSy6Zfv365YADDqjbifE/oyqD//rXvzJz5sy8+OKL2WGHHaoLL4rPfJfm/oPvHXfckWOPPTbl5eXp2rVrVlppJYUXvnML+mNb8tUqgKeddlp23nnntGnTpi6mx49cVf7uvPPOHHrooUmSNddcM59++mluu+22DB06NO+++2569eql+MJ3Yu7n4VtvvTVHHnlkKisrc9xxx2W77baTOb4XTz31VE444YQsueSSOeGEE7LaaqvlX//6VwYPHpzrrrsukydPzgUXXJDWrVvX9VT5kaj62VZZWZmPPvoo/fr1S5s2bXLhhRdmzz33zEcffZSbbropF1xwQY499tjMmDGj+nka/leUTZkyxVqDPxIjRoxI165dM23atDzyyCPVq27Ad2XmzJn55z//mZNOOikffPBB1l9//QwZMiSNGjXyRjPfi0GDBuXwww/PtGnTUq9evRrLOPft2zcHH3xwHc6O/wUPPPBAevXqlWnTpqVx48Zp2LBhPv/886y00kr53e9+l+7du2fZZZet62nyI1JZWZnPP/88v//97/Ovf/0r11xzTY1bC9arVy+zZs3KuHHjMmnSpPziF79IWVmZN5z51j355JPp2rVrGjRokCuvvLK6dD9r1qw0bNhwnuP9bsi37YUXXsjWW2+dDTfcMBMnTswGG2yQa6+9NrNnz1Y64HsxcODA/OEPf8jSSy+dc845J/vtt1/1vqqfeZ57+a4MGzas+nfAY445Jssvv3wee+yx3HfffWnevHmOPPLIdO/e3eprfGvm/mPbu+++mz333DPTpk3Lueeem7333jvPPPNMhgwZkuuuuy716tXLiSeemKOPPrrGufBtuu+++3LggQemTZs2Offcc6t/JsJ34euvZ6+55pqccsopueGGG7LnnnsmSaZNm5annnoq55xzTkaPHp299torF154oeILJZv7eXTOnDmZPHlyVltttVxyySXp0aNHjWOvu+66nHjiiUmSCy64QPGF/ynedSyQhd0LdaONNqr+dOX999+f2bNnu48v36lGjRpl2223zYUXXpgVV1wxzz//fI4//viUl5enXr161feThu/C448/nu7du2f69Ok544wzMnLkyDz66KO56KKLkiTHH398zjjjjDqeJT9mjz/+eH7/+99n5syZ+eMf/5ihQ4dm8ODBOfnkkzNz5sxcffXVOeOMM/LZZ5/V9VT5ESkrK8vnn3+eUaNG5Wc/+1n23nvv6n1Tp07Ns88+m9133z077rhjtt9++3Tv3j2DBg3KnDlzvNHMt6Lq9UXVSn9nnHFGjVUmGzZsmPLy8tx555257rrrMnjw4EydOnWeciqUqnHjxtljjz3y/PPP55133sn06dOTJA0aNFjoa2co1YsvvphTTz01ZWVlueyyy6oLLzNnzkySGm9KJ/Hzj5J9PUPPP/98Zs+enauvvjonnXRSfve73+Wvf/1rzjnnnLRo0SJ/+tOfcsstt2TChAl1NGN+TOb+Y9v06dNTWVmZt99+O6ecckr22Wef1KtXL5tuummOPvro9OnTJ0ly0UUXpV+/fklSXZaBb8uYMWNy/vnnJ/nqj7pVhZfZs2dXHzNt2rTMnDmz+uen52JKUVV4ueeee3Lrrbdm1KhR2WmnnaoLL3PmzMmSSy6Z7bbbLhdffHF++tOf5p577snJJ5+cTz75pC6nzo9A1XNwv379suaaa+app57KBhtsUL3q85w5c6pfdxxyyCHp27dvkuSUU07J1VdfXTeThjrg408FMfeLiy+//DJNmzatsa+ioiL169fPnnvumbvuuiuDBw/OUUcdlTZt2mjT852oajc3btw42223XZLkpJNOyi233JIlllgi55xzTho3bpw5c+akfv36dTxbimpBnwr/8MMPc9555yVJLr300uy///7V+9q1a5frr78+Y8aMUTbgOzN+/PjqgtUFF1xQ4z6pn3/+ee66666MHz8+7dq1y1JLLVVX0+RHqnHjxmnevHlmzpxZnbPXXnstN910U+655558+umnWW211TJjxowMHjw4kyZNytprr52VV165rqfOj0DV8/LLL7+cevXqZYsttqjeN378+IwYMSIXX3xxRo8enSRZYoklssUWW+Tqq6/OT37ykzqZMz9Oa621Vk488cQstdRSufHGGzNo0KDceuut+d3vfmd1K74zVbl6+eWXM2nSpBx//PE1in+NGjXK5MmTc9VVV+Wzzz7LrFmzcvTRR6dDhw4ySUmqnn8HDx6cpZdeOk899VS22mqr6j92zJgxI40bN07v3r3TtGnT9OvXL3/6059SWVmZ/fff34ovlKTqZ9dNN92Uv/3tb+ncuXPat2+fbt26JUn1KmutWrVKt27dUlZWljPOOCMXX3xxkq9WI/LczLfpk08+yQcffJB99tkne+21V/X2ioqKjB07NhdccEHGjBmTJZZYIttuu20OOOCAtGrVSgYpyfPPP58ePXpkrbXWSkVFRVZfffUkqbHSZP369bPJJpvk4osvzoknnph77rknSaz4wrdi8ODB+eSTT3LkkUfmiy++yFtvvZVWrVpV//2t6m8pVavfH3/88Tn11FOTJIcddlidzRu+L1Z6KYC5fxnr169f1l133fTv3z+jRo1K8tULj6ofamuuuWZ+/vOf5+23307//v39IkdJ5v4UxqRJkzJmzJg8+eSTGT9+fI0iQuPGjbP99tvnwgsvTNu2bXPttdfmzDPPzIwZM1K/fn0rvlBr48aNS5LqJcG/bvLkyRk9enS6du1ao/Dy0ksv5YADDsiYMWNyyCGHpH///vOc69NFfBs++uijvPrqq+natWuNwssrr7ySs88+O2+99VYOPvjg/PGPf6y7SVJ4C/p51bBhw2y66aYZM2ZMevTokR49emTHHXfMddddl7XWWiv9+/fPyJEjM2TIkHTu3DkjRozIE0888T3Pnh+7ZZddNhUVFbn//vszderUjBgxIieeeGIOP/zwvP/++9l+++1zwAEHpF27dvnHP/6RAQMG1PWUKbi5P51b9SneNddcMz169Khe8XTAgAF55JFHkvhUOd+e+X0yfOzYsUmSNdZYo3rbO++8kxtuuCFbb711Lr300lx//fW56aabsu222+all16SSUr2r3/9K/vtt19OOeWUTJ8+PR07dkzy1a0FGzduXJ3Vgw8+OMccc0x+8pOf5PLLL8/NN99sxRdK9sknn+Tuu+/OM888k8ceeywzZ87M1KlTk6TGe4TNmjXLPvvskz59+qSsrCwXX3yxFV9YZF/PR9WHfb9u9OjR+fLLLzNjxoxMmzYtSfL666/nT3/6U3bdddfcfffd+e9//5tnnnkmF198cS644IJ88cUX/k5CSZZeeukceuiheeedd/L6669Xr+DSoEGDGjmdu/hSteLLqaeemokTJ9bV1Cm4qp+N//jHP7LFFltk6tSpadKkScaMGZPk/16vzL3C7sEHH1y94supp56ayy67rA5mDt8vpZcfuLlLKzNmzMiTTz6Zjz/+OGeddVZ+/etfp0+fPnnqqaeqj2/SpElOPvnktGzZMiNGjKhe5cALCmpr7uxV3UZmyy23zK677ppNNtkkZ5xxRp577rnq4xs1apQuXbrkoosuUnyhJDfffHN22223PPDAA0nm/6bIa6+9lunTp9d4k/nVV1/NCSeckJEjR+bggw+u/kRRkkycODEvvvhi9XiwuKqyOHLkyHz55Zc1Vs549dVXc9xxx2XEiBE1XlgkX71BOH78+O99vhTX3M/Dr732Wu6///7qN1SWXHLJHH/88dlxxx3zyiuv5J577kmTJk1y4okn5rbbbsu+++6bJPnpT3+arbbaKslXv0dCbc39/FteXl5jufAePXqkY8eOufDCC7PJJptkhx12yKBBg7LtttvmL3/5S+68885cdtll1Z8mev3117/3+VN8c2dwQbfI+tnPfpYePXpkv/32y+jRo3PRRRcpvvCtqaysrP5j7pAhQ3LzzTdnzpw5WWmllZIk1113XV588cUMHjw4hx12WE488cRUVFRk//33z1//+tdst912mTRpUo477riUl5d7LUJJVl555Wy11VZ57bXX8vTTT+fZZ5/N559/noYNGyaZ9w8dcxdfbrvttnz44Yd1OX0KrnXr1jnjjDOy8847Z/To0ZkwYUKGDRuWZN4PLDVr1iy//e1vq4sv/fr1q16t189BvklZWVm+/PLL/Oc//6n+usq9996bu+66K0my3XbbZY011sgzzzyTfv36ZcCAAdlnn31ywQUXpFWrVjnxxBMzaNCg9OnTJ0suuWSeeOKJfP7553VyTfx4dOjQIYcddlgOPfTQNGnSJE8//XSuuOKKJPO+Vpm7+NKpU6fcddddueSSS7w2YbGUlZVl9uzZqVevXu69995sttlm+eKLL3LBBRdk7NixqVevXvX7NV//fbCq7HLllVf6OciPntsb/YDN/ceOa6+9NkOHDs0999yTp59+OoMHD87VV1+dSy+9NNdcc0222Wab9OrVKyuttFLWWWed/OIXv8hjjz2Wu+66K4cccogXFNRaVWbuv//+6k9O7rDDDlluueUyZsyYXH311Xn22WdzwgknZJtttknyf8WX5KtbHV177bWpX79+zjrrrDRu3LhOroNimTp1ap5++um8/fbb6devX+rXr5+dd955nmVwq/49adKkJF+t8HLCCSfk2WefrVE2qFri+aGHHsrAgQPzpz/9qUZRBmqrKnvLL798je2vvPJKjjvuuHkyWF5eniZNmuSGG27I8OHDc8stt2TppZf+3udNscx9a7dBgwbl7LPPzn//+98cf/zxOfLII9O8efOsueaaueKKK/Lxxx9n0qRJWXbZZbPqqqsmSY2i6VNPPZUWLVpk4403rpNrobjmzuGIESPyz3/+My1btswBBxyQ5s2bZ5111knfvn1zxRVXZPTo0fnlL3+ZXXfdNYccckj1GGVlZdW5XGKJJerkOiiuuX/3GzFiRP7+97/n3//+d5o0aZJWrVqlV69e6dSpU1q0aJGf/exnOfzww1NZWZnbb789F154YZJk++23dzsFSlKVm7vuuis9e/bMWmutlU033TQHHnhgHnvssTz00EPVBdMk6datWw466KCsv/76qVevXn7+85/n5ZdfzieffFL9eyEsjoqKinTo0CH9+vXLiSeemGHDhuXDDz/MsGHD0qVLl+rbKlT9oWPupe379++fPn36pGnTpvnDH/4w31sIwzepeh7dcMMNc+SRR6Zhw4a57777ctlll2XFFVfMJptsMs/zbVXxpV69ejnmmGNy991358gjj8ySSy5Zx1fDD9msWbMycODA3HXXXdlxxx3Tq1ev1KtXL3/5y19y3HHHZZNNNskvf/nLtGrVKj169MhVV12Vfv36VeevZ8+e6dmzZ9q3b5+GDRumXbt2ue222zJ69Oi8+eabWXbZZev6EimoqufW9u3bp3v37km+KhH8+c9/TuvWrdOtW7caz8HJ/xVfzj777PzpT39K7969vSZhkc2dpcrKyjRo0CAzZ85Mo0aN8sADD2T33XfPE088kT333DNDhgxJ27ZtM2fOnNSvX79GFg888MA0adIkm2++eZo3b+61MT9qSi8/YFU/eAYNGpSTTz45lZWVeeyxx7LNNttk0003zc4775xnn302f/7zn/PAAw/kiSeeyM9+9rOcccYZ2WmnnfLYY4/l73//e7p06ZL27dvX8dVQRMOGDUuvXr3SokWLnHnmmdVvmFx44YV56qmnMmrUqJx22mkpKyvL1ltvnaRm8eW0007L1VdfnUaNGrnFB4ukRYsWOfbYY9O8efPccMMNueiii5KkuvhS9cta586d07p167zyyit55plncvbZZy+w8JIk119/fSorK907lW9NVXHlvvvuy6qrrpq//OUvefbZZ3PQQQfVyGDVHzb++c9/5v3338/MmTPrbM4Uw9yfKL/lllty1FFHpbKyMscdd1x23nnnGm8St2rVKq1atapxftUL4IqKipx22ml5+umns9NOO9VYlQgWZu4c/v3vf8+JJ56YSZMmZe+9987bb7+dTp06pUmTJtlqq62y1VZb5eOPP07Tpk3TrFmzJF+9Wd2wYcNUVlbmhhtuSJL86le/qh7bGywsiqqcPPDAA/nDH/6Q8vLytGzZMo0aNcqzzz6bxx9/PIceemj23nvv/OxnP8taa62V3r17J4niCyWbOy8ffvhh+vbtmzZt2uToo4/OaqutliS59dZbc+655+b1119PmzZtstlmm6Vr1641xikrK8v06dOz6qqrpmXLlt/3ZfAjUvXHi5VWWikXXXRRTjrppDzyyCO59NJLs+yyy+YXv/hFdWa/Xnz58ssvc++992bXXXdVeGGxlJWVVf8hbcMNN0xZWVlmzpyZwYMH55JLLsmpp56azp07z7f48pvf/Kb6j21LLrmk52O+0ezZs1NZWZl///vfefvtt7PMMsvkyy+/zHHHHZdll102RxxxRJZbbrkkXxVNN9hgg9xzzz1ZccUVs9JKK2X77bdP8n+rBbZp0ybl5eX5+c9/nvXWW6/OroviWNDPqLmfWzt06JDf//73mTNnTgYMGFD9PuCCii9bbrllNttsszRq1CizZ8+uLqrC1339zh9z5szJrFmzstRSS6WsrCyNGjWqLtLfd9992WOPPTJ8+PDsuOOOGTx4cNq1azff4ku3bt2SRP740SubMmWK9bR+YKp+EFVUVGTmzJnZd99988ILL+Tyyy/Pr3/963mOnzBhQu68887861//ql5WcrPNNsszzzyTJZZYIjfffHO22mqrGk+2sDAffPBBevbsmaeffjqXXHJJevTokSS55pprcuaZZ6aysjJbb711Hnnkkay++uo577zzsu2221afP3PmzAwaNCgXX3xxbrzxxqy55pp1dSkU0JgxYzJgwIDceOONWXvttXPyySdn5513TvLVL3+TJ0/OAQcckCeeeCJt27bN+PHj07Nnz+qSzNyfojzuuOPyl7/8Jcccc0xOPvnkNGrUqM6ui+Kb+7n0iCOOyO23357WrVvnk08+ySGHHFJ9W63p06dXr2pw7LHH5q9//WuOPvronHLKKTLIIqlaaa1NmzY599xz89vf/naBx379TZmZM2fmmGOOye23356OHTvmoYceynLLLecNZmrtlltuqf407x//+Md07969RvGq6s2U5P9+Ps697fTTT89VV12VTTfdNLfeemt+8pOf1Ml1UFxDhw7NXnvtlUaNGuXMM8/MXnvtlYYNG+bBBx/M5Zdfnvfffz/bb799zj///Ky44opJvrqV1hVXXJHbb789G264YXr37p1ddtmljq+EIpn7+XLKlCl55513stVWW+VPf/pTfv/73yf5v3Jfknnea6kq31dUVOTwww/PnXfemZNPPjknnXSS52IW6psyUllZmYqKitSvXz/vvfdeTjjhhDzyyCPZYIMNcuGFF2a99darce7c2fz888/TvHnzGs/T8HVz56+ioiJffvllZs+ePd/S3qhRo3LJJZfkkUceydZbb51TTjklnTt3nmecuckfi+KDDz7I3/72t1x++eWpV69ePvvss7Rt2zb9+/evfu/5m7JU9Txc9eGRv/71rznwwANzwQUXWImcbzT38+ZLL72U119/PW+88UaaN2+evffeO0svvXSaNv1/7N1lWFVZ///x96FbRAQDxVYsLOzuxtYZY8RuwUDERgQBATtRMVFMlLDFDgxsTCzEFkUazvk/4H/2nCM44ty/GceZ9XriPZ7w7Ota91p7rfXZ32Ugvf/p06esXbuW5cuXU7x4cSZNmiSFC8RenPC9VMfOo0ePEhQUxLVr10hNTaVRo0a0b99emtcq9z7kcrkUfLG2ts4RfBGE/xoRevkHu3XrFuXKlaNWrVp06dKFOXPmADknIKqJvY0bN3L8+HH27dsnndtmZ2fHjh07yJcv3w+7FuHnc+TIEXr27MmYMWOYO3cukF0tY8aMGWRmZhISEkLFihUZNmwYhw8fxsbGhtmzZ0uJesheCExLS8PIyOhHXYbwE7t79y4rVqxgw4YNVKpUiSlTptCpUyfp9ejoaNq2bUtaWhoVKlTg3LlzOb7D09MTb29vatSowcaNG3McSSMIuVEdZ9+9e0dSUhKGhoaYmpqiqakppeKPHDmCm5sbN27coEKFCuzatYsiRYqofZeyDVavXp1NmzaJNijkSWxsLP369eP27dsEBATQvXt34PcnMhQKBQkJCWhqamJgYCA9pREbG8uePXvYuXMnd+7coXr16mzcuBErKysx4RW+28GDB+nTpw+mpqb4+vrSrVs3IPfFuy831T59+sSUKVMIDQ2lRIkShIWFUaRIEbHwJ6hRjrdf2xh78+YNQ4cO5cSJE2ohfMg+VnDo0KHcvXuXESNG4OnpqfbZmJgYli9fzqZNm2jUqBFBQUFSJSJByKuNGzeya9cuGjZsyJIlS4iKisLS0lLqy3Jbm1Hl6urKihUrqFGjBtu3bxdVJ4VvUm1H169fJzY2losXL1KtWjWpohX83n9+b/BFhK6EP6LaPo4dO8a+ffukdZYmTZrQu3dvqlatKgX+4M8FXwQhr/r160dYWBhaWlr8+uuvLFq0CFAPnn6NQqHA2dmZgIAAKleuzK5du7CwsBDtUvgq1baxY8cOpk2bxps3b6TXixQpQv/+/fnll1+wtraW/v7L4MvkyZPp06dPju8UhD+i2la2bNnCuHHjkMvllCpVCgMDA27evImGhgbTpk1jwoQJwNeDL18edSQI/yUi9PIPtXnzZsaOHUuXLl24fPky3t7etG3b9qsdleokNi0tjUuXLrFp0yYuXrzIu3fv2Lp1Kw0aNBALzUKe7d27l7CwMDw8PChYsCDh4eE4Ozvz8uVLdu3aRZMmTcjMzGTv3r2MGTMGuVxOmTJlmDt3Li1atPjRP1/4SSkUCrUjFW7cuMHGjRsJCAigdu3ajBo1Cnt7e+n9ERERODg4kJaWRseOHWnfvj02NjYkJSWxdu1a9uzZQ8GCBQkLC5PKkAtCXh04cABPT09iY2OxtLSkXLlyeHt7S8EVhULB6tWrCQgI4OnTpzRs2JBff/2VypUr8+HDB9asWcPu3bsxNzcnPDxctEEhzy5dukTnzp3p2LEjq1evlv4+NTWVZ8+e4eHhwd27dzEwMKBOnTpMmTIFExMTbty4waBBg8jIyKB169ZMnjyZggULiomu8N1SU1MZPnw4+/btY8mSJfTr1w/4fSEmLS2Na9eukZSURMWKFbG0tATg7du3rFy5ktWrV5OYmEjDhg1ZtWqVeNJIyNXz58+xsrKSys9/uSD86NEjWrduTa1atdi2bZv099evX8fZ2ZkLFy4wZMgQfHx8cv3+mzdvsmHDBgYNGoSNjc1fdyHCv9Lbt2/p378/58+fp2TJkrx//57Lly9ToECBP9zAiI+P59WrV8ydO5djx45RqlQpQkJCsLKyEusxwh9SbVc7d+5k9uzZxMfHSw+0GRoa4uvri729PXp6et8VfBGEb/lys83R0ZHMzEyKFy+OQqEgLi4OGxsb+vbty6BBg9SqZXwZfHF1daVmzZo/6lKEf4nTp0/TqVMnTExMSE9Px8zMDEdHRwYNGoSmpuZXx9QXL15w8eJFli9fTlRUFOXLl2fnzp3iQRAhz7Zv386IESOQyWRMmjSJFi1acOPGDSlk365dOyZOnKh2hLQy+LJixQpKlizJyJEjGThw4A+6AuFnpqz6bGpqysyZM3FwcABg6NCh7Ny5E4CpU6fi7OwM5B58MTY2lsL6gvBfIw7v+of4ctFEmVbet28fCoWC58+fS+/LjepTRjo6OjRo0IBKlSqxbt065s6dS1BQEA0aNBALLEKedenShSpVqmBmZgZkl1R7+fIl/v7+UuBFS0uLHj164OPjw71797hz5w4jRowgICCAJk2a/OArEH42yj5MJpMRGRnJnj17uHDhgtQ3RkVFsXTpUjQ1NaVSfu3atWPXrl0MGzaM0NBQQkND0dfXJyUlBYCaNWuyYsUKETYQvtuhQ4ekkqRFihQhISGB8PBw7ty5g7e3Nw0bNkRPT49hw4aRL18+goKCOHbsGMeOHVP7HtEGhT/j4cOHpKSk8OnTJz59+oSJiQl37txh7969bNq0ifj4eIyMjMjMzOTy5cvEx8ezZMkSqlSpwrZt20hOTqZMmTLo6+uLhT3hT/n8+TNnz56ldOnS9OrVSxqj379/z61bt5g3bx7Xr18nNTUVKysrfH19ad26NTKZjPz589OgQQPs7OwYOHAgZmZmoh0KOSxdupQZM2awefNmtSMsVefEN27c4N27d2pV1G7evMmkSZOIiopi8ODBaoGXuLg40tPTpQXoypUrM2/ePHGsoPCnmJubM2fOHPz8/Dh58iQpKSkEBgbi6OiIpqZmrsGXtLQ0NmzYIB252rp1axYuXCietBTyRNmetm3bxsiRIwEYO3YsjRs35sqVK3h6ejJixAhevnzJb7/9hqmpKQqFguLFi0t94aFDh5g2bRqzZ8+mdu3aIvgi5JmyrSgfbDM2NmbmzJkMGTKEZ8+eMWHCBI4cOcLq1atJSUlh9OjRUvClVq1aTJ48GciuGp2QkICfnx+2trY/7HqEn8+X42q9evUYPHgwtra2fPr0CU9PT/z8/FAoFAwbNkyt8r3y81lZWYSHh7N48WJevXpF9+7dmTdvHpaWlmIcFvLkxIkTTJkyBTMzM7y9vaWqu2fPniUhIQG5XM727dvJzMxkypQp0ryjePHiDB48GE1NTfz9/dm+fTu9evVSOwpJEL7l+vXrzJ07FwMDAxYsWCC1Pz8/P3bu3ImhoSFJSUlSAMvZ2Rk9PT0p+LJnzx6aNWvG9evXpdC0IPzXiNDLD5KVlYWGhgYymUztBi0uLo6CBQvSu3dvdHV1GTZsGBkZGRw/fpwhQ4agpaX11Zs05Y2h8k9TU1O6du3KwoULCQ0NZdy4cZQrV+7vu0jhp6VsY6VLlway08qbNm2iUKFCNG7cGLlcjpaWlnRGqoWFBRUrVkRXV5c9e/ZQvHjxH3wFws9I2XeFhoYyaNAg5HI59vb2FClShHLlyhEZGcmlS5dYsGABgBR8adCgAaGhoRw9epTIyEhSU1MxMzOjZcuWNGnSRKSahe+WkJCAv78/pqamzJkzhw4dOpCQkICrqyuHDh3C0dERLy8vWrRogZ6eHn369KFZs2ZERERw5swZEhISKFy4ME2bNqVhw4ZYWFj86EsSfjItW7bExsaG8+fPM2fOHEqUKMGaNWt49uwZtra2DB48mFatWnHv3j1mzpzJhQsXePnyJaVLl5bGbshe+BMLe8KfVaBAAV69esXDhw+xsbHh6tWrBAYGsn//fj58+ICNjQ3a2tpcv36dUaNGERERQdmyZXFwcKBv374YGRmhpaWFXC4X7VDI4dWrV0B22fqgoCDatm2b46gjZfg+ISEBgDt37jBhwgQp8KK8J1Qu8u3btw93d3fOnDlDiRIlAETgRfhuqpWHateujZOTEwqFgmPHjhEREUHt2rVp1KhRrkdz6erq0r17dz59+kT58uWxt7fH1NRUbLQJeRYZGYmzszPm5ua4u7vTu3dvIHtNRktLi8zMTGbPnk1mZiaDBw/OEXzR0tIiPDychQsXsnHjxm8e/yH8N32tQkZ0dDQzZsyQqgr17NkTyH7q/OjRo+jo6PDu3TuWLl2KQqFgzJgxasEXZ2dnPn36RGxsrDjWV/guquPp8+fPefPmDdWrV5fu9d68eUNKSgoLFy5k4cKFAGrBF8h+IFhLS4tevXphYmJCvnz5qF+/PsbGxmIcFvIkISGBDRs28PHjRxYtWiQFDnx8fPDw8MDIyIjp06cTFBTE7t27gezQQalSpYDs4MuAAQMwNDSkd+/eIvAi5LBz506KFSuWazBZLpdz5MgRHj58iJeXl9T+/P39mTt3LkZGRpw/f57r16/z66+/4unpiVwux8XFRS34cvz4cd69eyeqPgv/WeJ4ox/g8+fP7Nu3j6JFi1K7dm309fUBWLNmDZs2bcLd3V1aRAkJCWHo0KFkZGQwZswY5s6dC5CnDis9PR0dHR3GjBnDli1b2LNnD02bNv2rL0/4SahOKNLT00lJSeHz589qE1NlO3v69Cl16tTB0tKSI0eOYG5uLgVeAKpUqYKdnR0eHh4AFCpU6O+/IOFf4dq1a3Tq1InExESWLVvGr7/+Kr0WERHBxo0bOXDgAFWqVMHZ2VkKvgjC/6UXL15ga2vLtGnTcHR0lP4+OTmZmTNnsnbtWooWLYq3tzfNmzdHT0/vx/1Y4V8nKysLmUzGvn378PDw4P79+9JrI0aMYPjw4VhZWaGlpUVCQgI9e/bk0qVL4j5P+D83efJkAgICsLCwoHbt2kRGRvL582eaNm1Knz596NSpEwYGBvTu3ZtDhw4xa9Ysxo8fL54qF/LMw8NDqk6gDL7A7/OU58+f06xZM7S1tZkwYQI7duzg4sWLDBo0CF9fXwC1OUnHjh2JiYnh6NGjWFtb/5iLEn46f3RUkVJUVBReXl4cPXpUOj6wVq1aX/28ciz/8il0Qfgj79+/Z9y4cYSFhbFo0SIGDBgAgLe3N56enhgZGTF8+HCWLVtGamoqs2bN4rfffiN//vxSO3z8+DFeXl5MnTpVPIwk5BAUFES1atWwsbHJ0TfJ5XIWLFiAp6cn3t7eDB06FMh+uly52bZlyxZiYmKYM2cO+fLlw8HBgbFjx6rNh69du0bRokUxNzcX/Z+QJ6rjaEREBL6+vly+fBl/f3/69euHllb2M9uvXr1i8+bN+Pv7Y2JigqOjI0OHDpU+q1AoWLp0KaVKlZKqCH75/YLwR+7cuYO9vT1dunTB29sbgJUrVzJz5kx0dHQ4fPgwNjY2LFu2DG9vb2QyGW3btmXy5MlqDx8p+z4ROBBUhYWF0a9fP2xtbfHz86NGjRpqr2dkZODh4cGdO3eko323bNnC1KlTkcvl7Nu3jxo1apCWloaHhweLFy8GstdtXF1dAfW5sRiDhf8qUenlB7h+/Tp+fn68e/eOJUuW0LFjRzZt2oSzszPGxsZoaWlJN2P29vZA9pltS5cuRVdXl+nTp6OpqfnNgVP5VNv79++Brx+NJPw3fFnyUdnGTp48SVBQEBcvXiQxMZGKFSvSqFEjBgwYQMGCBaWnhmxtbblw4QKrVq1i9OjRmJqaAjBnzhyeP3/O+PHjRdhF+NOUbfLq1askJiYydOhQKfCiDPC1a9eOYsWKYWJiQnBwMH5+fsjlcjp37gwgHbn15XcKwh/JrZ1kZGRgaWlJy5Ytgez+U6FQYGBggLu7OzKZjICAAJydnfH29qZly5bSmKtayU20QeFrvmwbqv2X8t6uXbt2VKtWjS1btlC8eHGKFi1K8+bNAaSn2UxNTfn48SM2NjZUr179b74K4d9K2R59fHxIS0sjJCSEsLAwrKysGDduHGPHjkVXV1dqw40aNeLQoUNoa2uLPk/IE+U81tXVFblcjq+vL7/88ota8CUzMxMrKysGDhyIv78/7u7ufPz4MdcKL5D9lOWZM2cYMWKEqPIn5JnqHDk2Npb4+Hhu3rxJ5cqVsbCwoEyZMgDY2dkxZcoUFAoFhw4dApCCL7nd86mu04jFZiGv4uLiCAsLY+TIkVLgZfny5Xh7e2NoaMjBgwepWLEiMpmMBQsWMGfOHBQKBQ4ODlLFlxIlSkhHAn85Pxb+2/bv38+oUaMoU6YMW7duzXH8bmpqKtHR0XTt2lUKvGzcuBE/Pz8MDQ3Zv38/1apVo3Dhwhw5coTDhw9Lm3Ljxo2TNtmURxqJzTYhL1THz82bN+Po6EhWVhYODg4UK1ZMrQ+ztLSkX79+yGQy/Pz8WLhwIXK5nBEjRgAwd+5c/P39qVOnDs2aNZOqbIj5iZBXJUuWZOjQodIDlmfPnmXt2rVoaWmxY8cObGxsAOjbty/79u3j4sWLhIeHo6GhgZOTk9SvKvs+EXgRVFWqVImWLVty5MgRjh49miP0oq2tzYABA8jIyACyK1zt3r2b9PR0Nm3aRI0aNcjKykJXV1ftsz4+PqSnpzN79mxpLAYxBxH+u8Ts5weoVasWDRo0YOPGjbi6unL8+HHWrVtH0aJF8fLyon79+mrvt7e3l86rVD7Rltfgi6enJxEREZQuXVoamIX/ntevX7NhwwYcHR3VQlUhISEMGTKEzMxMypYti6GhIdeuXePEiRNERESwfv16ihUrBmQHr54+fcq6deu4f/8+zZs358SJE+zevZvSpUtLC9SC8L+4e/cugPRUWlZWFjo6OtJEuHLlyvTv35/79+8THR3NihUrAOjcuTNaWlpqE2YxsRW+RbW9REdHc+vWLT5//kxKSgpGRkZq5e2VT+rq6elJVddUgy+tWrVCW1tbbUwWbVDIjeoC8OnTpzl58iSRkZFYW1tja2vLqFGj0NDQQFdXlxIlSjBt2jS1zyuf3JDL5Tg7O3P//n369++vNrkVhG9R7f8+f/5MUlISnz59omzZsmqLy4sXL2bw4MFoaGhgZGQknVmuupF26NAhjIyMqFu37t9/IcJPSXUzdvr06WhpaeHl5cUvv/zC5s2b6dChgzSetm7dmsjISK5evUqJEiWkjThACrx4eHiwZs0aqlSpwujRo0UFNiFPFAqFNB7v3r2b+fPn8/jxYzIyMtDS0sLU1BRXV1f69euHtrY2dnZ2TJ06FSBPwRdB+F6VK1fGzc2NRo0aAXDq1CnWrFmDjo4OO3fupGLFigBMmzaNq1evcvToUdzc3MjKymLw4MHkz58f+H2TTQReBFXKIMDx48fZvn0706dPV5uXGBgYMGfOHD59+gRkryMGBweTlZXFli1bqFatmrR2+Ntvv3H48GEePXrE2rVrSUtLw9nZWe1IQbHZJuSFctwMDw9n7NixFCxYEDc3N/r06ZPr+y0tLenbty8ACxcuZM6cOVy+fJnPnz9z4MABChUqxOrVq8WxMsJ3y8rKQk9Pj4kTJ0rt8ty5czx48IBZs2ZRr1496YE4U1NTOnXqxK1btyhVqhRBQUEYGxvj4eEhgi5CruRyOSVKlMDPz4+wsDAprPf27VvMzMykMVO53gJw5coVjh07RvPmzWnYsKHa3KVevXoUK1aMOnXqsHPnThYtWsSECRMwMTH5+y9OEP5hxAzobyaXy9HR0cHb25uCBQvi6+vLunXryJ8/P/PmzZPK732ZiO/SpQsymYyhQ4fi6+uLQqFgxowZ3wy+KMvqbtq0SVTh+I9KSUmhfv36fPjwgYEDB1KwYEEgu8LLkCFD0NHRwd3dnUGDBvHu3TvS0tIYNGgQly9fpkaNGty7d4/8+fPTokUL4uPjWb9+PSEhIYSEhABgZWXF1q1bsbKy+pGXKfzklBMKCwsLAG7fvk1WVpba68qF5IYNG9KxY0euXr3KhQsXyMjIICsri65du4qFZuG7KNtLaGgow4cPJzk5GUAKuKxbtw53d3cMDQ2lv1dOhFWDL66urqSnp9OhQwe0tbV/zMUIPwXVSWpQUBCTJ08mKSkJQ0ND7ty5w86dOzl37hzjxo2jVq1aaGpq5rgnVAZeJk+ezLp167CxsWHatGno6emJDTchT1TbyYEDB9i4caO0WGxnZ0fPnj3p0KGDVNVP+cSukrICm1wuZ8aMGZw6dYq2bdtKFREE4VsUCoW0Gas8hzw+Pp6NGzfSr18/KfgC2RU2xo0bh4eHBzExMTg6OtKwYUPatm1LfHw8wcHB7N+/H3NzcwICAsScRMgzZT8YFBTEqFGjABg4cCCmpqa8e/eOTZs2MWHCBB4/fszQoUOxsrKiVq1aOYIvzs7O1KxZU4y/wv9MJpMxevRoqS2dPn2ax48f4+PjQ926daXNNk1NTamiVfHixZk3bx6GhoaMGDFCtEMhV5mZmVhYWLB69WqCg4OlPi8xMZF8+fJJ1UpVq79cvnyZM2fO0KNHDxo1aqS29lyuXDny5ctHly5d2Lx5M+Hh4YwbN04t9CIIefX27VtWrlwJgLu7O7169QK+Xi3I0tKS/v37Y2pqipeXFzt37kQmk1GtWjU2bdqElZWVOFZG+KqvrZko24tMJkMmk5GcnMyJEyeA3+fDyrVp5fdoaGgwfPhwdu/ezZgxY0SbE3KIiYmhQoUK0jpzsWLFpMDLqlWr2LBhA4sWLZJC9Ko+f/4MZAdh9PX1USgUZGZmoq2tTXJyMs+fP2fNmjX069ePEiVKYGJiItYEBQEQseu/mXLDTFdXV9rcVQ6IJiYmZGZmSu/7kr29PWvWrEFbWxs/Pz/c3d3VPp8bV1dX7t69K6q8/Ifp6+tTvHhxzMzMSEpKAiA5OZlVq1aRmZnJ3LlzGT58ONra2hQqVIi0tDSp/fXs2VN6WsjU1BQHBwc2btzIyJEjGTJkCK6uroSHh1OuXLkfdn3Cv4Ny0lC1alX09PSIiori3bt3UrAPsicXyiM9OnXqRP78+WnevDmXL19m9erV0s2gIHyPc+fOSYGXX3/9lREjRmBubg5klzI9cuSIVFoSkNqkMvgybNgwnjx5gpeXF2lpaT/qMoSfhHLyuXPnTkaNGkVWVhZubm5cu3aN/fv3U6ZMGcLDw5k3bx6nTp0iMzMTDQ0NqY988eIFW7dupW3btqxbt44KFSoQHByMpaWlFHQWhD/yZQnxX375hYiICKytralRowZ37txh+vTpzJgxg9evXwOohVAh+wjVlJQURowYwfLly6UnlvLlyyeN04LwNapt8NixY/Tv359atWoRExMjvadfv35ERERI/92pUyfpAZHLly+zYMECWrVqRf/+/QkLC6Nu3bpiTiL8KWfPnsXZ2RkjIyMCAgLw9/dn1qxZLF68GBcXFyC74tWdO3ekzyiDLy1atODIkSNMmzaNa9eu/ahLEH4yf3TsuHKDVy6Xk5CQwL59+wDUjktQjsmlS5emYsWK9O7dm3LlytGxY0dxHyjkcOPGDSC76k9WVhbm5uZS4GXJkiU0atSIu3fvoqmpmaNtvnjxAgAzMzOpoqlyXqytrc3Hjx+pUqUKCxcuZMeOHdJmmyB8r9evX3PlyhWaNWsmBV5UHxbJTcGCBRk4cCBhYWHMnj2bNWvWsGPHDhF4Ef6QXC6XxsqnT59y+fJlQkNDiYyM5PPnz9I8RS6Xo6urK1XTjYmJkV5T9peHDh3C2tqanj17snnzZooVK5Zj3iz8t/n7+1OvXj02b94M/L7fK5fL+fz5M+Hh4dy5c4eZM2dy5cqVHGOosv3t2bOHmzdvIpPJpActlUURNDU1adKkCdbW1mRmZop7QUFAVHr5ITQ1NUlOTiY2NpYCBQpQvXp1jhw5wujRo/H09KRdu3ZfTcfb29sDMGrUKHx9fTEyMsLR0fGr/5aGhoZU2UP471HekBUpUoSrV68SGRnJwIED+fjxI2fPnqVhw4YMGjRIev+NGzdwcnLi8uXLDBkyBB8fH+m1rKwsDA0NqVSpEh4eHj/icoR/kS+Tx8r/XadOHSpVqsTly5cZNGgQu3btQldXVyqBr1wI1NDQ4MOHD7Rq1Ypy5coxYMAAjIyMftTlCD+RL9veqVOnSE1NZdmyZfz6668ADBgwAA8PD8LDw/H398fAwICmTZtKkwtl9Q09PT1mz56Njo4Ov/76q2iDgpqvPWFx4cIFpk2bhqmpKT4+PvTo0QPIPlrh4cOHaGpqcurUKdLT05kyZQqNGjVCS0uL9PR0zpw5g6+vL8+fP6dnz57MnTtXCryIhT0hL5Rtcv/+/YwdOxYzMzNmzZrFgAEDSElJYcqUKWzatIndu3eTlJSEl5cXBQsWlMbfZ8+e4ePjQ1RUFDExMdSoUYONGzdSuHBh0Q6FPFG2wbCwMAYMGIC2tjb29vbUq1eP0qVL8/TpU86cOcOvv/5KUFCQdIRq8+bNqVSpEjExMezatYvMzEyMjIxo1qwZdnZ2UmBVEPJCOUYfO3aMz58/4+XlRffu3aXXL126RHh4OADjx4+nVatWAFI/V6tWLVxdXUlISODx48cULVr0h1yH8HNRrVrw9OlTEhMTefz4MRYWFtja2krrgJqampiamlKyZEnp3hAgNTVVOr5t//79mJiY4OrqipOTE/r6+mIcFtQsXbqUGTNm4OXlxbBhw9QqSKampnLw4EGePXvGkCFDWLt2LeXKlVNro8ojp6Ojo7lx4wZVqlSR2qinpyfa2tq0aNGCEiVKAIj2J3w35Vh8/fp1kpKS0NPTk0IJf7RxqzrPLlOmDOPHj5dek8vloh0KuVINUu3ZswdPT0/u378vvW5nZ0fbtm0ZP3681IZ69erF+fPn2blzJ6VKlaJp06Zoamoyffp0Tp8+Tb9+/ZDJZFI4QbQ9QZWymrijoyMaGhrSmrPy6OjFixczbdo0wsLCcHFxYf78+dSoUUPq3zp27EjXrl3Zs2cPw4YNk9YRN2/ezLZt26hXr55ahTZxrKUgZBP/T/hBDAwMmDhxIiNGjMDa2hoXFxdWrVrF1KlT0dDQoE2bNmrBF9WJh729PSkpKXh6etK1a9cfdQnCT0A5EWjdujVhYWE8efIEgHfv3pGQkEC+fPmk99y4cYOJEyfmGnh59+4dkZGRtGrVSu1sQFEyTfgequ0lKyuLjIwMEhMTpapXAEZGRixbtoxevXpx5swZBgwYQGBgIPr6+sDvN3ArV65ET0+P9u3bU7RoUXFetJBnyjZ48uRJMjIyOHfuHO3atZMmHxkZGdjY2ODm5oaRkRHbtm2Tgn6qwRflk5b6+vrSUUeCAHD8+HFKly5N8eLFc4yTaWlp7Ny5k9evX7NgwQIp8LJgwQLmzZuHkZERy5cvZ8eOHezfvx9/f38UCgWNGzdGR0eHJk2aYGhoiL6+PnZ2dhgZGYkFZuGrlE8KfXmvdufOHdzd3dHT08PT01N6onL16tVs2rQJfX19LC0t2bNnDwDz58/HwsIChUKBhYUFcXFxvH37ljFjxjB+/HjMzc1FOxS+y+3bt3F0dEQul+Pr60vfvn2B7KNl4uLiWLhwIQEBAfzyyy9qwZeCBQtiaWlJkyZNfuTPF/4FZDIZmZmZHDhwADMzM9q3by+N2VFRUTg5OXHr1i2cnJyYOXOm9Lnk5GSMjY0BqFGjBr6+vhQtWhRzc/OvHsMgCKC+2RYSEsKCBQt48uQJiYmJaGhoUL16dSZOnEjdunXJnz8/WVlZlClThoiICKZMmcKuXbukefPUqVOJjo5m2LBhUiVpEJttwu/S09OlSrheXl5oaGgwZMgQteN6169fz7hx4zhw4AADBw4kMDCQcuXKSUcdVa1alVatWnHkyBFWrFhBmzZtsLW1ZcGCBQQHB9OoUSPMzMykf1O0P+F7KecoyjU91XH0a+vNCQkJ3Lhxg0aNGuU65opxWPia3I61HDBgAAUKFCA2NpaTJ08yd+5cYmJiWLZsGdra2lIQZvfu3YwePVqqJHTz5k1KlizJtGnTRN8nfNW0adMwNDRkzpw5jB49GkBae5bL5VhbW+Ph4UFmZiYHDx7MNfgybdo0kpKSOHToEP369ZOqj1tbW7NmzRqp2q7o+wThd7KEhARRe/Av9kfBAGX1guTkZObMmcPq1aspXLgwXl5eUvBFdRH5wYMHFC9eXCorrq+vL32HIHzNyZMnsbe3x87OjoMHD3Lv3j3q169P48aN2bNnD9HR0UyePJlLly6pBV6UTxLt27cPDw8PZs2aRbt27X7w1Qg/I9V+8Ny5c+zZs4eLFy+SkJBA1apVqVSpEpMmTZL6uvDwcJydnYmLi6NatWqMGjWK0qVLY2FhwbJly1i5ciV2dnYEBwdjamr6A69M+BlFRUXRunVrmjdvztu3b6lduzY+Pj6kp6erBU4fP37M/PnzCQ4OxtbWFldXV7XgiyB8SbmA8uuvvzJ16lSsrKzU+r+EhARq165N7dq1pRKnAQEBzJgxA01NTUJDQ6lWrRpRUVH07t2bDx8+0LhxY8aPH0+jRo3Q1tbO02Kg8N+2ZMkSypcvT+vWrXMNvqxdu5ZJkybh7u4uLb4sXLiQOXPmYGRkxL59+8jIyGDIkCE8e/aMLl26MH/+fCwtLYHs+cvDhw+xtraWnsgUiyzC9zhw4AD9+vWjW7durF69GsgOnaqOrzNnzmTJkiUAbNmyRQolKNu06AeF/wuNGzfmzZs3HD9+nEKFCnHx4kUmTJiQI/CSlZVFYmIi8+bNo2XLlrRp00bte0Q/KOSV6mZbly5dyJcvH7dv3yYqKooiRYowYMAA+vTpg7W1NUlJSXTp0oVLly5RvHhxihUrRlJSEtHR0ZQpU4b9+/dTqFChH3xFwj/Vx48f2bhxI7Nnz8bIyIgZM2YwZMgQ4PeqLG/fvmXUqFEcPnwYGxsbKfiiHFsjIiLw9vYmOjoaAGNjYxITE7G2tiYsLIyiRYuK/k/4n928eZNmzZqRmZnJhg0b6Ny5M5DzwTlNTU3u379P48aNWbJkifQAiSDk1ZkzZ+jduzcymYwlS5bQpUsX6bVly5Yxa9YssrKyWL16NT179gSyjzYKDAwkNDSUuLg48uXLh42NDQEBARQtWlQ8/CHkSrVd+Pn5SQ9LqlYZV46fT58+xdnZmYMHD1KrVi3mz59P9erVpbE1ISEBX19fLl68iKamJhUqVGDy5Mmi2q4gfIVISvzFVG/+b9++zcuXL1EoFBQsWJCqVatK56oaGBjg5uYGZD9lOWXKFABatmwpVTiYMWMG586dY8aMGTRp0iRH5QNBgN8nBaqTg/Lly1O0aFHu37/Py5cvKV68ODVr1iQyMpLly5cTGhrKpUuXGDx4sBR4SUtLk0rnrlq1ipcvX1KyZMkfdl3Cz03ZFvft28fIkSOlpyQTExN59uwZ+/fv5+TJk3h5eVG5cmXatm1Lvnz5GD9+PNHR0YwYMUIq/5eQkICFhQVLly4VgRfhT9HU1KRNmzZERkaSlpYmLRbr6Oio9Z0lSpTAxcUFgODgYDw8PJDJZDRp0kQEX4Qc5HI5+vr6lCtXjl27dqGlpcXkyZOl4AuAqakpu3btIiEhAYD79++zefNmZDIZW7ZsoVq1amRkZGBnZ8fEiROZPn06J0+eJD09nYyMDFq2bKk2oRUbvcKXzpw5I23S7t27lyZNmkhBAWVlg/j4eLp3786IESOA7A04f39/DA0N2bdvH9WrV+f9+/f06NEDf39/jh49ypQpU/Dx8aFgwYJoaWlRvnx5QP3JdUHIq4cPH5KVlSXdx6mGTpXzZxcXF16+fMmOHTvo27cvmzZtomPHjjm+S/SDwv+iYMGC3Lx5k/v37/P48WMmTZqUI/CSlpaGrq4uL1++ZNeuXQA5Qi+iHxTy4tSpU0yYMAEDAwMWL16sdqSWs7Mza9aswcvLi9q1a1O8eHEMDQ3ZvXs3Dg4OXL58mTNnzmBkZET16tXZtGkThQoVEpsdwlfly5ePAQMGIJfLcXNzkzbchgwZIj0pbm5uzvLly6Xgi2rFF4B27dphbGzM0aNH2bp1K6VKlaJYsWLMmTNHbLYJefatgHLlypUZP348vr6+LFmyBAsLC+rWrYtMJkMul5OVlYW2tjYKhQI3NzdSU1P/xl8v/Bso2+CJEydISkpi/vz5aoGXixcvsn37drKyspg4caIUeAGoUKECLi4ujBw5kitXrmBtbU2pUqUwNTUVfaDwVZqamtJDHRMmTEBbW5uZM2cyevRo5HI5/fr1kypcFS9eHG9vbwC1ii/K4IupqSlz587l48eP6OvrI5PJ0NbWFu1PEL5CzMz/QqqLwNu3b6djx450796dHj160KZNG/z8/EhJSUFTUxOFQoGuri5ubm4MGzaM+Ph4nJ2d2bFjB/fu3WPatGksXbqUe/fuYWNj84OvTPgnSk1NJSEhQZpIKP9UKBRYWlpSunRpEhISePToEfr6+nTq1An4PUw1ZswYFixYAGSXbVaWyHV1deXs2bN07tyZYsWK/YArE/4tTpw4wcCBA5HJZMydO5fTp0+zb98+fH19KVy4MGfPnmX06NFcvHgRDQ0NGjRowKFDh3BycqJly5bkz5+fMmXK0KdPHyIiIqSFGEH4XjVq1MDFxQV7e3t0dHQ4ceIEO3bsAJBCg0rK4EuvXr24ffs2zs7OnD59+kf9dOEfTENDg3bt2jF79mxKly7Nli1b8PHx4fnz51K7ksvlVKlShUaNGgHZiyvXrl1j2LBhNGnSRG3Sqixh36pVK86fP8+GDRvIzMz8Ydcn/BwaNGgghVm6dOlCZGSk2j2hlpYWI0eOxMnJCU1NTVJSUggJCSE1NZW1a9dSvXp1MjMzMTMzkxb7EhMTpdDqu3fv1P49ETgQ/gzl8TBXr15FLperVVlTzp/19fVp0aIFBgYGAPTv35+QkBBkMplod8Kfonp/l5WVBUCnTp1QKBR4eHjkWuFFGXiB7Hnxp0+faNWq1d//44WfmlwuByAsLIzU1FTc3NzUAi/Xrl3jzJkzAIwZM4ZmzZohk8nIyMjA2NiYzZs3s3v3bgICAti1axe7d+8WT5cLeZIvXz5+++03Zs+ezefPn5k7dy6rVq0CyBF8adWqFXfu3GHgwIHcu3dP+o6GDRsya9Yszp49S0REBEuWLBGBFyHP5HK5dN8WFxfHtWvXCAkJ4datW7x69Up6X+fOnWnevDmXLl3C09OTY8eOAdn3hcoHjqZPn05oaCjNmzenZcuWf//FCP9Yyvu6jIwMtfs9JZlMRlpaGsePHydfvnxSNSHIrgQ9YcIEbty4gZOTE9OnT5de+/jxIwqFAlNTU6ytrenatSs1atTA1NQUuVwu+kDhq+RyudR3JScnM3z4cKnCy9ixY9m6dStAjuBLmzZtuHTpEi4uLly9elWtPefLlw8dHR3pe0X7E4TciRIhfyHlTd3evXulxWdlub5Tp04xd+5cnj59yqRJk6SngJXBFy0tLQIDA3F2dkZXV5dPnz5RsmRJ9u7di4WFhSgfKah5/fo1v/32G4mJiTRv3pyiRYtSs2ZNSpcujaGhITo6OpQvX56TJ09y8uRJGjRowNixY4mJiWHr1q3o6elJIRhAWlx2d3dnxYoV2NjYMHnyZAwNDX/UJQo/MYVCQWJiIkuWLJEWlQcMGABA8eLFadSoES1atGDAgAFER0czffp0duzYQb58+TAzM2P69OlSuT9LS0sUCoVUhUgQvpfyCY9q1aoxbNgwFAoFu3btIiAgAHNzc2mRObeKL58/f+bMmTOi6pWgRnlPpryPa9asGXK5HA8PD7Zs2QKQo+KL8jNRUVEAFChQAMietCorHhQpUoT8+fPToUMHihUrxvjx46WNN0HIjfLIU09PT7S0tFi6dCldu3Zlz549NG3aFLlcjlwup0CBAlKbu3btGgcPHqRevXrUr19f+o7MzEyKFSuGtbU1bdq0ISIigitXroiwgfB/olmzZhQvXpx79+4RFhZGhw4dcsxtZTIZdevWxcDAgAoVKnDlyhWGDx9OixYtMDQ0FG1R+KYvnyxX/d/KReImTZpgY2PD+fPnARg5cqQUeElOTsbAwACFQoGrqyvHjx+nc+fO1KtX72+8CuFnogwBfBkG0NDQID09nZMnT2JpaakWeImKisLJyYnbt28zYcIEZsyYIb2mrOqsp6dH9erVqV69uvSa2GwT/ohq/2doaEiHDh34+PEjfn5+0rrMiBEj8lTxJSsrCw0NDfLnzw/8Xh1VtD/hW1QfBg4JCcHX15e7d++Snp6Ovr4+FSpUYOzYsXTt2pWqVasybNgwUlNTOXnyJOfPn2fs2LEUL14cDQ0Ndu3aRWRkJNbW1ixZskQKHYi9EUE55sbGxuLu7s7YsWOxtbXNMVdIS0sjJSUFLS0tKYz6tWMt5XI5Hz9+ZNOmTdjY2OQaeBZtT/ga1b5v7969rFq1isePH6s96DF69Gg0NDTo06fPH1Z88fLyolq1aqK9CcJ3EKGXv4Dq5kdKSgpr167FzMwMPz8/7O3tAdi/fz9Tp05lw4YNpKenM3XqVIoVKyZtmMyaNYuSJUsSERHB06dPadOmjSgfKeRKLpfj4uJCdHQ0qamp3Lp1CwBtbW0sLCwoUaIEbdq04ePHjwC8fftW+uzkyZNJT09n586dtGnThjFjxlCiRAlkMhn79+8nMjISS0tLAgMDRZUX4bspF1pkMhkpKSlcvXqV8uXLS4EX5cZaVlYWxYoVY8uWLbRr146oqCgmTZrEmjVrgN8XqIsVKyY2OIQ8+1oJXeVTk9ra2tSsWZORI0eSmZnJ3r178ff3RyaT0bRp01yDL/PmzUNHR4fChQv/3Zcj/AMp7/eUk8+PHz+SL18+9PT0aNGiBTKZDA8PDzZv3oxCoWDy5MnSWKp6/CDAixcvyMjIQENDQ5oIL1u2DICePXvy22+/AYh7QCFXyr5K9chTZQn7L4MvqkcdAVJ5cFNTU6n6hrKygVwu5+nTpxQpUoT169dTtGhRzMzMxAKz8E25jcHKv8vKyiJfvnw0a9aMDRs2sH79ekqXLo2NjY1aVSxNTU10dHTQ1NRk7ty5XL58mcaNG2NkZPSDrkr4mai2wcOHD3Pu3Dnu3LlD+/btqVSpEjVq1ACgZMmS0jpNeno6Hz584MaNG9jY2GBgYEBKSgouLi5s3LiRcuXK4e3tjbGxsegHhRweP37M5MmTWbBgAdbW1rnes2VkZGBkZCQd7XbhwgUmTpwobbYpAy9yuZyXL1+yYsUKJk+ejImJSY5/T7Q/4WtU+7+QkBC2bNnCxYsXsbCwQKFQEBcXh7+/P5qamgwdOvQPgy8bNmygbNmyan2eWJMR8krZVrZu3cro0aOB7Lmtnp4e7969Izw8nEGDBvHkyRMcHR1p06YNJiYmBAcHExgYiK+vr/Rdmpqa1K9fn9WrV1OkSBExLxYkysBL+/btefnyJZ8+fWLWrFlUqlRJrb8yMTGhbNmy3L17l6SkJB4+fJhr4CU1NRU9PT2eP3/OvHnzcHJyElX+hO+ibHfBwcEMHz4cExMTHBwcqF27NtHR0dy4cYMDBw4wcuRIFAoFv/zyy1eDL8OGDWPdunVUrVr1R16SIPxUZAkJCTlrfgn/J+Li4qTksrOzM5MmTQJ+3yQ5ceIELi4uxMTE8Msvv0jBF1VpaWl8/vwZIyMjdHV1xU2dkKuEhASMjIyIjIwkPj6ekydP8ujRIx4/fsz79+/V3mtsbMzOnTupXbs2CoWChIQEFi1axKJFi3K8z87ODh8fH0qVKvV3Xo7wE1H2Z3K5nMzMTM6cOUOBAgVy3Izdu3eP+vXrU6VKFY4fP57je5R9W1RUFL1798bQ0JA9e/ZQpkyZv+tShH8R1YW+R48e8ezZMx48eICpqSnt27dHX19f7f3R0dEsWrSIkJAQGjZsyIQJE2jatGmO7xIEJWXfl5CQwIkTJ9i/fz+xsbHMnDmTWrVqYWhoSHp6OkeOHMHDw4M7d+7Qt29fKfiibFcnT57EwcGB9+/fM3/+fBo2bEjx4sWZPXs269ato3379qxZs0aqwCYIqlSD9nK5nKioKEqUKEGhQoWk98yYMYOlS5cCqAVfIHsx5t69ezRo0ABDQ0MWL16sVurZycmJwMBAQkNDadCgASCCV8K3qY6b8fHxpKWlAWBmZqa2cRsdHc3QoUN58OAB7dq1Y+TIkdSuXVutopWrqysrVqzg6NGjUkhBEL5HUFAQo0aNkv5bU1OTsmXLMnLkSCmID3DmzBkcHBx48+YNBQsWpGTJkujo6BAbG0tcXBwVKlQgODiYYsWKiX5QyOHJkye0bNmSt2/fUrt2bdauXYuVlZXUVuRyOZ8/f6Z9+/bcunVLOrZj3Lhx3Lx5M9fNtuvXr9OkSRPGjx/P7Nmzf+DVCT+rbdu2MXLkSIyNfzLDQgAA6FdJREFUjenfvz/ly5cnJiaGU6dOcevWLfLly8e0adMYMmQI8Ps93tu3bxk9ejSHDh3C0tKSiIgIUelU+NNOnjxJ79690dbWxs/Pjx49ekj3irNmzWLx4sVAdkCrcePG0ucOHDhAdHQ0T548wdLSkjp16lCvXj1MTU3FOCzk4OjoyIYNGzAyMuLz5880adIEd3f3HMGXBQsWMG/ePEqUKIGenh4xMTE4Ojoya9YsQP1Yyx49ehAZGcnWrVtp3br1D7ku4ed17do1unXrxvv37wkMDJQKISiprtOsWLGCPn36AL+v8Tx79oxhw4Zx584dKbgqCELeiNDLX2TNmjU4Ozvj7e3N1q1b8ff3p1q1amRmZqKpqSkNuHkJviiJjTfha3JrG+np6Tx//pxbt27x5MkTTp06xbNnz7hz5w7FihVjzZo11KlTR3r/2bNnefbsGY8fP0ZfX5/GjRtjbW0tlTAVhC8pb8Q+ffrE6tWrOXz4MBcvXsTOzo6ZM2fSsGFD6b0PHz6kVq1aQHZpvyZNmuT4PoVCwfv37+nZsydXr14lODhYpOmF76baHx48eJBp06bx8OFD6XUbGxucnJxo3ry5dLwHiOCLkHfKvu/58+dMnDiRo0ePoqWlhba2Ni4uLnTu3Fm6l0tLS+Po0aO5Bl+Uli9fzrRp04DswKmxsTEvXrzA2tqa8PBwihQpItqgkIOyHb57946NGzdy8OBBLly4QOfOnZkzZw4lSpSQ3jtz5kyWLFkCwO7du2nWrJkUlJHJZLi5ubF06VKqVKlCx44dqVOnDoGBgezatQs7OzuCg4Olp9IFIa8OHjzI7NmzefnyJampqTRo0IBffvlF7ViP06dPM2LECOLi4qhatSq1a9fml19+AbKfCl67di1Vq1Zl165dmJub/6hLEX5S58+fp0ePHshkMpycnJDJZNy4cYM9e/YAMG/ePLVAzM2bN1m7di1nz57l3r17AFSvXp169erh6OhIwYIFxUabkENaWhrjxo0jODgYQ0NDkpKSqFmzJhs2bKBo0aJqbWbJkiXMnDmTli1b8vz5c2JiYtSONFLdbOvcuTPR0dFs2bKFRo0a/bDrE35O0dHRdO7cmcTExBybbdHR0QQHB7Nq1SqMjY2ZNm0aQ4cOBdSDL3379iUqKorbt2+rBaoFITdfzleV/+3i4sKqVavw9fVl0KBB0uuXLl1i0qRJXLt2TS3c9615r6i0JuTm0KFDjBkzBg0NDQwMDIiNjaVZs2a4ubmpBV/S0tLo0aMHp0+fBmDQoEFSRSHlMdNyuRxXV1dWrVpF165dWbRokVQRVRDy6vDhw/Tr1w97e3tWr14NZFe8V60W7e7uLrW/5cuXS/NgZT/34sULdHR0MDc3F32fIHwHcbzRX0S5SDJz5kxSU1OJiYmhWrVqUtlx5U1ckyZNmD9/Pi4uLgQFBQHZT7RZWVnl+E6x2SF8zZdtQy6Xo6OjQ6lSpaQqLUOGDOHUqVP4+flx/vx5Bg8ezPr167GzswOgfv36f/vvFn5eqpttAwYM4OzZs1hZWdGuXTs6d+6co5JG6dKl6du3L1u2bCEiIoLy5cvnWDhRKBQUKFCAMmXKcPXqVZKSkv7OSxL+JZT9YVhYGP369QNg4MCBNGzYkKtXr7Jq1Src3Nx48uQJ/fv3x9LSEoBq1aoxfvx4IPspIy0tLdLT02ndurUYfwWJsu978uQJnTp14tmzZzRr1oxJkyZJFTZUJ6K6urq0aNECAA8PD7Zs2QKgFnwZNWoUhoaGhISEcPz4cQoWLEjLli1ZtGiRKN0s5ErZDp8+fcrQoUO5ePEiVlZWNGzYkBYtWvDhwwdKlCghtR03Nzcge7OtW7duUvBFQ0MDmUxGr169eP36NcHBwURHR0v/TsmSJVm3bh2mpqZikUX4LhEREfz6668AlC1blvfv33P06FGOHj3Ky5cvpRL3DRs2ZN26dcyfP58rV65w/fp1tm3bRlpaGhkZGRQuXJjVq1eLwIvwp1y+fFk6brpLly4AvHv3jho1ajBjxgwpcKoMvlSuXBlPT0/kcjmxsbFkZWVRsWJFFAoF2traYjwWcqWrq0u1atUIDg6WgsqXL19m4MCBBAYGUrRoUelY36ZNm2Jra8uRI0cAGDx4sBR4SUlJkebQLi4unDp1ih49elC9evUfdm3Cz+vBgwckJibi4OAgBV6UR/xWq1YNKysrDA0N8fX1xcvLC7lczvDhw9WOOgoKCkIul2Nubi76PyFXERERmJmZUadOnRxrJspjzg8dOkTx4sXp1q2b9FpUVBROTk45jpUBSE5OxtDQEMgOYSnnK8p9FDEfEXJTu3ZtihQpwuvXr+nbty9BQUEcP36c2bNnM3v2bCn4oqury8SJE/n48SM3btzg6dOnxMbGUqJECbS0tEhOTsbFxYVNmzZRvnx5PD09xbGWwp/y4MED0tPT0dPTA34PVcHvAdPp06cTHx/P1q1bGTVqFHK5nL59+0oV9YsUKQKIsJ8gfC8Revk/oJpCVv5vHx8f9PT0WLp0KRoaGly5coVOnTpJN26qN2xfBl8SExPx8vKSOjZB+F5fDoRyuRw9PT2aNGmCXC5n4cKFnD9/HgcHByn4olrqXhD+iEKhQENDg/fv39OhQwfu3r1Lu3bt8PPzI3/+/Gpl6VU1adKE0NBQNm3aRLly5ejWrZv05Ljqzd+zZ88wNTWlfPnyf9clCf8y58+fZ9y4cRgbG+Pm5sbAgQMBePPmDZqamjx//pzly5eTkZHBoEGDcgRftLS02LlzJ7q6ujRs2FAcLSMAv/d9L1++5JdffuHZs2eMGjWKefPm/eHn8hJ8+e233+jZsyevXr0if/786OjoYGBgIBaYhRxUy922b9+euLg47O3tmT9/PsbGxtJcA5A2Lv4o+AJQsWJFpk6dSosWLVi3bh3m5uYUKVIER0dHLC0tRTsUvkk5r1UoFLx9+xZvb2+1MfjOnTscOnSI2bNnM336dLKyshg3bhyQvUjt7+/P9evX2bRpE+/evUNLS4uqVasyevRotapFgvA1uT0ZfvfuXZo3b06XLl2k1wsUKMCYMWMwMDBg4sSJOYIvGhoa6OnpUalSpRzfKfpB4UvKNjJy5EjCwsK4f/8+Hh4eBAYGcvr0abXgC0CVKlXo27cvb9++JT4+nnz58hEdHU21atXQ19cnLS0NFxcXAgMDsbGxwd3dHSMjI1HxT/huz549A5DWW+RyOdra2tLr5ubm9O7dm/v37xMSEsKSJUuQy+WMHDlSun80MzOTPiv6P+FLISEhDBw4kHbt2jFp0qRcj6HMysoiPT1dCo7C1wMvcrmchIQEli9fTtOmTWnYsKFauxN9oPA1crkcU1NTXF1d6dOnD3K5nJ07d9KjRw+OHj2KQqFgzpw5UvCldu3aTJkyBT8/P44cOULTpk2pW7euFHp++PAhFSpUYMeOHWIuLPxpyoc2rl69SkZGBjo6OtL9nOo6Tffu3YmIiODDhw+MHz+elJQUhgwZora3JwIvgvB9xP9j/keqk8+MjAxkMhmZmZkAzJ07l5EjRyKXy9m4cSMHDhxQ+6xyYRCyN4O9vLywsLDg9OnTOaokCML/Qjk46ujo0Lx5c5ycnKhbty5xcXE4ODhw6dIlMYEQ8kwmk/H582dGjhzJ3bt3cXBwIDAwkEKFCqktpHypZ8+eDBgwgOTkZGbNmsWqVau4ffs2gBR4mTdvHufPn8fW1pbChQv/Ldcj/FzkcrnafyvHUaWEhAQCAgJ4//49rq6uUuBl6dKlzJw5k6ysLEaOHImBgQFr165l3bp1vHz5Uvp8tWrVGD58OL/++iuzZs0SgRdBIpPJSE1NxcvLSzqqyN3dHUBaxPsaZfDF1dUVGxsbtmzZgo+Pj7QgDaCvr0/JkiUxNTXFwMAAhUIhFleEHDQ0NHj79i1DhgwhLi6OsWPHSmNwbv2VckEFwM3NjbFjxwLQrVs3jh8/Lr2vWLFidO/end27d7Nhwwbc3d3FIp+QZ6rzYR0dHaKjoxk3bpw0BtvY2DB+/HhWrlwJwKxZs6QjtwCsra3p1KkTwcHBHDhwgPDwcLy8vETgRcgT5VFtAG/fvuX58+ckJyeTnp4uzYO/nOsOGjQIPz8/AKZNm8ayZcuA7DmJss8U82PhW5RrenK5nHbt2vH69WtOnjzJjBkzqFGjBpcuXWLgwIHExcVJnxk6dCgjRoygcOHCLFy4kM6dOzNkyBB69+5Nw4YNCQwMpGzZsmzfvl0ah0VbFL6X8hjfy5cv8/Hjx1w3zMqUKSMF8+Pi4li0aBGLFy8G1EN+YrNNyI2xsTENGzbk6NGjXL58We015RqNoaEhhQsX5uPHjyQlJXHp0iUcHR1zBF7S0tLQ0NAgNjaWwMBAzp0797dfj/Bz+HL9D37voypWrEi1atXw8PAgPT2dzZs3U7p0aY4dO8asWbO4desWcrkcAwMDWrduzbp16+jTpw9GRkYcOnSII0eOoKenx7BhwwgJCcHKykrMhYU/rUmTJpQsWZKbN2+yadMmMjMz1faCle2qbNmyaGpqUqtWLbKysvD19SU5OflH/nRB+OnJEhISco4WwndbuXIlx44dY/Xq1ZiamkrlSwFmzJjB0qVL0dPTIyAggA4dOqh9VjU4c/78eak8vihdJfxVMjIyOH78OP7+/pw/fx5DQ0P2798vSucK36TsrzZs2ICjoyMNGzZk165d0gLx1yYDqv3ZlClTWL16NTo6OhQtWpSOHTtibGzM1atXiYiIoGDBgoSHh1OmTJm/89KEn4Cy/X348IHbt2/ToEEDtb8HuH79Oq1ataJfv37S2aiBgYFMmzaNtLQ0Dhw4QK1atZg6dSorV66kSJEi9OvXDwcHB7Ujt1JTU6UylIKg9OzZM7p06YKenh5Hjx5FT0/vuxZC0tLSOHr0KB4eHlJwxtnZGSsrK/EUr/BNCoUChUKBr68vHh4e2NvbExgYCPDNdqj6+syZM6XAgbLii1wuVysbLtqj8L22bt2Kp6cnY8eOZevWrezYsYOCBQuSmZmJpqam1J527NjBsGHDAPUglvLYBUH4Hqp91Z49e/Dz8+PJkydYWlqiq6uLiYkJGzdupECBArn2aevXr2fChAlAdjW2kSNH/q2/X/j3ePPmDc2aNUNbW5ugoCA+fvzIpEmTuHnzJrVq1VKr+ALZR7EePnyYLVu2oKWlRWpqKhUrVqR+/fpMmjRJBE+F/8mdO3fo2bMnWVlZbNiwgdq1a6u1J2XfqWy3NWvWZN++fZQtW5Zjx45hZGT0g69A+BmcOnWK6Oho6V7u7du3UnUD5b6Iu7s7vr6+tGjRgrdv33Lt2jXGjx/P7Nmzgez5sa6uLgqFAnt7ey5cuMCOHTto3Ljxj7os4R9Iuaas/FO1yqTq/Z1yrXrs2LG4ublx5coVhg0bxsOHD2nevDlz5syhYsWKavttcXFxvH//nszMTCpUqIC2tjZaWlpiDBb+0B+tl8jlctLT0/Hz82PhwoVUqVKFGTNm0KhRIzQ1NaW1F01NTV69ekWzZs3w9fXl7du3NG7cGGtr67/5agTh30WEXv5HCoWChIQE6tSpw5s3b+jatSt+fn45gi/KxeW8BF/g2wvXgvC/ysjI4MSJE8ycOZM7d+5w6dIlSpcu/aN/lvCTGDRoEAcOHCAkJAQ7O7s89Vmq71m2bBmhoaGcP39eel1XV5eKFSuycuVKypUr95f+fuHn9enTJ+rXr09ycjJr1qyRnk5TjqNJSUm4uroydOhQKleuzJkzZ3BycuLhw4cEBwdL73/79i2dOnUiJiaGQoUK4eDgwIABA9SCL4LwpdWrVzNlyhQGDBjAwoUL/1S5b9Xgy4MHD2jXrh0eHh6iupWQZx06dOD+/fscOXKE4sWL53ne8LXgy549e2jatKkIugh/WkZGBv369ePQoUMUKlSIt2/fEhISQv369aX3qLavrwVfxEMfwp+1c+dOhg4dCoCVlRWfP38mISEBgDVr1tCjR4+vHuerGnxZuHAhv/3229/3w4WfimofpdqnKf9+zZo1ODs7S/3ahQsXcHZ25vr167kGXwBu3LhBeno6Hz58oGbNmhgYGKCrqyvWBIU/9K17trS0NIYOHcr+/fuxsbEhLCyM/PnzS59TBk2fP39OlSpVWLJkCZmZmbRo0YJixYqJe0LhD+XWPtatW0dERATOzs7Y2dlJfx8TE0P79u358OEDAM7OzkydOhWA5ORkqcKpi4sLq1evpkePHvj7+4vglSBRjrFPnz7Fzc2NESNGUKFCBamNKCuuaWpqkpiYSLdu3YiNjeXo0aNYW1tz9epVhg4dqhZ8UR51JAh/hur94NOnT3nz5g3x8fEYGRlRs2ZNjIyMkMlkXL9+nWnTpnH69Gnq1auHg4MDnTt3RldXV/quCRMmsH79eiIiIqhbty6A2p6yIAjfT6wo/Y9kMhn58+cnODiYsmXLsmfPHsaPH09CQgJaWlrSUUfKSW9qaipDhgwhLCwsx/eoEpNb4a+mra1N48aNmTdvHtHR0SLwIuTZs2fPOHbsGCYmJlJAIC99lqamprTYPHr0aFasWMHatWtxdXXF0dGRTZs2ERQUJAIvwh96/vw5pUuX5sOHD0ydOpXDhw8DSIt3hoaG+Pr6UqFCBQAuXrzI/fv3mTlzJi1atEChUJCRkYG5uTmtW7dGR0cHfX19PD09CQoK+uYxNcJ/W2JiIgDVq1eXKmJ8D+WTbM2bN2fatGkUKFCAqKgoUVVIyLPo6GjOnj1L0aJFMTMzA/I+b9DU1MwxNwHo2rUrZ86cEQt/wp+mra3NypUr6dixIy9fvkShUEjHtymPJVQt59yzZ09Wr14NZAewvLy8AHGEgpB3quXt37x5g7+/P+bm5gQEBBAVFcWuXbvo168fkH2czPHjx6U+7svS+A4ODsybNw9zc3OaNWv2912E8FN5+vQp/v7+REZGAr+v4WVlZUl9V+3atSlQoABLly4lJiaGOnXq4O3tja2tbY6jjpRzjipVqlCzZk1atmxJ/vz5pYoHYk1Q+BrVI92ePn3KrVu3CAsLIyoqivT0dCD7gaJFixZhY2PDnTt3pIc9lO1OWVnNx8cHbW1tatasycCBAylWrJg4Ukv4pi/bR3x8PNu3b+fIkSMsX75c7bijChUqsGrVKqmf/PDhAwkJCdIxM5mZmUycOJHVq1djY2ODu7s7RkZGuR5jI/w3aWho8PjxY5o3b86uXbvo0qULjo6O7Ny5E8huj8ojfY2NjWnevDnv3r1j2bJlpKamUr16dQICAnIcdaRsY6KtCd9DoVBI/dmePXvo0aMHLVu2pH///nTt2pXu3bvj5+dHZmYmVatWxcXFBTs7O86dO8ecOXMYMWIEhw4d4vDhwwwZMoT169dTq1YtaQ0bEIEXQfgfiUov/weU6b7r168zcOBAYmNj6dy5M4sWLfpqxRd9fX0CAgJo3779D/71giAI3+fx48c0bNiQEiVKcOjQIfT19b9rUSQuLi7HE26C8D2io6Px9/dn3759lClTBg8PD1q1agWoVzL4+PEj3bp148qVK4SFhVG/fn21p0A8PT0JCAhg9OjR7Ny5k8DAQBG6EnKlvNebPHkyAQEBDBs2jPnz56tNeL8lPj6e+/fvU7duXXR0dEhNTeXs2bNUqlQJS0tLUeFAyJPz58/Trl072rVrx9atW7/7KaCPHz+SL18+6b+VTxZdu3aN4sWL/xU/WfgP+fDhA+PGjSM0NBRDQ0PCwsKwtbX9anWEXbt2MWTIEAAePnxI/vz5xUab8E2qbSgxMZG3b99So0YNfHx8pPakNH36dJYtWwb8fpzb1yq+JCUlYWhoKJ6uFHKIjY2lVatWvHv3DkNDQ3r16kWXLl1o0KBBjnCKl5cX8+fPZ/HixfTv35/09HSuXr3KlClTuHbtmlrFF1HNRfheqv1fSEgICxYs4MmTJyQmJqKhoUH16tWZOHEiNWvWxMLCgpiYGBwcHIiJiaFkyZLY29tjZ2eHmZkZ69atY8eOHdSpU4fg4GBMTEx+8NUJP7MTJ06wdOlSjh49SseOHRk/fjw1a9aUXt+/fz+DBg2SjpApWbIkurq63Lx5kwcPHlCuXDl27dqFlZWV6BsFNSkpKVK1cQMDA4yNjXn16hUArVu3pkOHDvTu3VuqnvHp0yeaNm2Knp4eoaGh0oMi0dHRDBkyhIcPH9KiRQvpqCMx9xD+jKCgIEaNGgXAgAEDKFCgALGxsZw8eZL379/TvXt3li9fjo6ODtHR0axdu5aDBw/y5s0btUIJZcqUYc+ePVhZWYk1QUH4PyJCL9/hj84N/DPBF8guw6s8akEQBOGfSrW/e/ToEY0bN0ZDQ4Pw8HAqV678Xd/h7u5OgwYNxJOUwndTbYfR0dH4+fmxf//+HMEX1bLNXbp04ezZswQGBmJvb6/2ffb29qSmphIaGkpSUhKmpqZ/9yUJPxnlxLZTp05s3LgR+HZ5caWtW7eyYsUKVqxYkaPfFAt7Ql6dOXOGjh07YmNjw4EDB/K8QaFQKEhLS8PHx4e+fftSqlQp6bWEhIQc8xVB+F7K+fCHDx9wcnIiJCSEUqVKsWHDBipXrvzV4EtISAilS5fO8/2kICitWLGCJUuWMGPGDJYvX8727dspUqQImZmZaGhoSO1NNfiiepwb5Ay+iCM9hC+lpaVRs2ZN4uLiMDExoUCBAsTHx5OZmUmTJk2YPHkypUqVomDBgkD2UR6dO3fG2NiYo0ePYmpqSlZWFpcuXZKCL3Z2dgQGBlKkSBGxwSH8KaqbbV26dCFfvnzcvn2bqKgoihQpwoABA+jTpw/W1tbEx8czbNgwTp8+LX1euaZdunRp9u7dKzbbhD9Nddw8efIkCxcuJDIykg4dOjB+/Hhq1aolvffKlSvMmzePmJgYXrx4AYCNjQ1169bFxcUFCwsLMS8WcrV7924CAgI4f/48bdu2pXz58sTFxXHs2DHevXtHlSpVGDVqFNWqVaNChQpSANXFxYUpU6ZI36MafKlZsybLli2jfPnyP/DKhJ/RmTNn6N27NzKZjCVLltClSxfptWXLljFr1iyysrJYtWoVvXr1AuDdu3fExsYSEBBAQkICmpqaVK5cmcGDB4u+TxD+j4m72e+gvPl/8uQJoF6iWUNDA7lcTtWqVQkMDKRUqVLs27cPJyenXI86cnBwwNDQUAysgiD8Y504cUIqS6ra35UqVQo7OzuSk5M5d+4cQJ6OhJHJZLx8+ZKgoCDWrFnD+/fv/7ofL/z0VEuMqh6NoFStWjUmTJhAp06dePDgAa6urmpHHWVmZqKtrU2rVq3Q0NBg+/bt3LlzR/q8u7s7J0+exMbGBi0tLbXKB4LwNcqSo/v375dCL6r9Y26U/eONGze4efMm9+7dy/EeMbkV8qpChQoUL16c58+fc/78eeD3PvKPyGQyHj9+zPr161m3bh2pqanS3MTU1BSFQiECL8IfUu3nnj17xvXr19m3bx+HDx8mLS1Nak/58+fH39+fDh068OjRIwYOHMitW7ek+TJkt0fl/7a3txeBF+G7ZWVlcejQIeLj45k6dSo3b97k8ePHQHZJcA0NDWn8dXd3Z8yYMUD2cW6RkZFfDbaIwIvwJV1dXVasWIGBgQGfPn3CzMyMZcuWUatWLY4ePUr37t0ZNGgQ+/fvJy0tjQoVKtCpUycePXrE9u3bpQqTdnZ2eHl5YWtrS1RUFPb29rx8+VKEDITvdurUKSZMmICBgQEBAQGsX7+ehQsXcujQIYYOHcqLFy/w8vLi0aNHABQuXJjg4GBWrFiBg4MDdnZ2tGnThgkTJhAWFiZV1hBtUfiW3Oa8MplMGm8bN26Mk5MTTZs2JSwsjEWLFnHp0iXpvTVq1GDdunUcP36c8PBwIiIiOHz4MJ6enmLTV8iVss1169aN0aNHY2trS0REBHFxcXTt2pUDBw7QrVs34uPjGTlyJL169WLr1q1UqFABU1NTwsPDpfUXuVxOtWrVWLt2Lfnz5+fmzZsUKFDgR16e8JNRtscTJ06QlJTE9OnT1QIvFy9eZPv27WRlZTFx4kQp8AJQoEABatWqxcqVK9m2bRtbtmxh6tSpou8ThL+AuKP9TsuXL6d69ers2LED+HrwZd26dRQoUIC9e/cyYcKEHMEXPz8/bt68KU0uBEEQ/kkOHTpEly5d8Pb2Jjo6Gvh9g0LZz2VlZbFx40YpofxHfZnytdjYWF68eIGpqalUYlIQvqQ8R1x5JrlyAU65Qab884+CL8rN2+bNm1OjRg0iIiIYNmwYv/76K126dMHX15fChQszfvx4ZDKZ2OQQ8qR69eqMGzcOgI0bN0pPTH4t+KKcvH7+/JkjR45QqVIlqSKRIPwZenp6VK5cmcTERGk+orq5mxvla7du3eLDhw8YGBigp6enFnIRfaDwR1Sf4j18+DC9e/emdevW/Pbbb/Tq1Ys2bdqwbNkyXr9+DWQHX5YsWUKHDh14+PBhrsEXsbkm/FkKhQJNTU02b95M+/bt+fjxIzo6Oly8eJGMjAzpfarzk7lz50rBl27dunHw4EHR7wl5IpfLadSoEbt370ZbW5vLly9z5swZAgMD2bJlC+3ateP06dMMGDCAXr16sXnzZkaPHo25uTnHjh2T+joNDQ3s7Ozw9vamePHiPH78WPSDwndRjp9hYWGkpqbi5uZG9+7dpdevXbvGmTNnABgzZoxUWTczMxN9fX369OmDn58fu3btIigoiGnTpmFpaSk224Q8kcvl0riZkJDAixcvuH//PhkZGWrjaaNGjXB0dFQLvigfpgMwNjbGwsKCevXqUbduXQwNDdHV1ZXGdkFQpbrO0qFDB5ydnbG1tWXHjh0EBgaSkZFBQEAA+/btY/To0bx//57Ro0fj7+9PZmam2kNHytMbbG1tCQ0NJTo6GnNz8zw9QCL8NyjnDRkZGV8N+aWlpXH8+HHy5ctH586dpdeioqKYMGECN27cwMnJienTp0uvffr0Sfrfqu1N+W+Ivk8Q/m+JGdZ3UnZSw4YNY/fu3UDuwRdbW1vWrVuHhoYGe/bsYdy4cTmCL8qnKkXHJgjCP42+vj516tThyJEj+Pr6SsEXZalwR0dHSpYsyc2bNxk8eDDp6eloampK/Zsq1UUUf39/dHR06Nq1K5D7kyLCf5vyaci3b9/Sr18/xo0bx8mTJ4mPj1dbNFa2nWrVquHk5ETnzp1zBF8Aqlatyrx582jdujVxcXFERERw7tw5ypcvz549eyhZsuQPuU7h59W8eXMqV67M1atXWbNmDVFRUYD6U26QvcCs7PsmT57MgwcPaNmypXTWtCD8GYaGhlLwaufOncyePRvgq+FT5Rgsl8tZuXIlBQoUoFOnToAYg4W8U25mhIWF0atXL+7cuUPnzp2ZOHEiHTp04O3bt3h7ezNlyhSp2kb+/PlZunQpHTt25MGDB/z2229S8EW0PeF7fLkZoazoZ2hoyOrVq2nTpg3p6emsX79emrMofRl8GTduHAqFgnHjxpGWlibaovBNyjW+OnXqEBoaira2NuvWrWPOnDk0atSINWvWsGnTJgYNGsSlS5cYO3Ysv/76K6mpqRw6dIjt27erfVetWrUIDAzk5s2bWFhYiM02QaJsC8o+68v7Og0NDdLT0zl58iSWlpZqgZeoqChGjx7N7du3mTBhAm5ubtJryvmIMhRoZGQkfZ/q64KgpFx/UVI9+iokJIT+/fvTuHFjmjZtSseOHZk1axZPnz6V3t+4cWO14MvChQul4MvX7gNFEFX4GtV9t3bt2jFlyhSqV6/OoUOHmDVrFhcvXsTGxgZ3d3d27drF3Llzef78Oenp6SgUCrVKu8rvqlixIoUKFRJVrgSJct0kNjaWESNGcO3atVz7qrS0NFJSUtDS0pLG7YsXL+Lk5MStW7dwcnJi5syZQHbf+eHDBwIDA6V1atX2Jvo9QfhryBISEsQs/zstWrRIWmBeu3Yt3bp1A9SfgJPL5SQnJ9OtWzeio6PJyMigcePGbNq0CRMTkx/10wVBEPLs/PnzeHh4cOrUKTp27MjEiROpVq2a9Hp4eDgTJ07k5cuXdOjQgXXr1qGjoyP1hQqFgqysLOlJ8rlz5+Ln50fLli2ljTdByE1CQgL169eXFlpMTEwwNjamR48eVK5cmXbt2mFgYKA2Qbhy5QoLFy5k//79lClTBg8PD7WKGs+ePePly5ecP3+e8uXLU7lyZYoUKfK3X5vwc1C9p8vNunXr8PT05MOHDzRv3hwHBwfatWuX63tdXV1ZsWIFVapUYffu3Zibm/9VP1v4F1MuNiv/XLp0KTNmzACyQ1Wurq453puZmYmWlhYKhYLJkyezdu1aevXqha+vr7ThIQh5FR0dTc+ePXn//j2LFi2iX79+0mtr1qxh5syZpKam4ufnh4ODg/RaQkICY8eOJTQ0FDMzM0JDQ7GxsfkRlyD85NasWcPjx4+ZO3euWh+XnJzMkCFDiIiIoHTp0qxfv54qVaqofVY1hO/t7U3Pnj1F8Fn4LsqxNSoqig4dOpCRkUGXLl1YtmwZBgYGZGVlERMTw9KlS4mOjiYmJgYLCwtmzJih1l/m9p2CoGwLjx8/ZvLkySxYsABra+scVVjS09Np0KABCoVCOjbmwoULTJw4MdfNtpcvX7JixQomT54s1qKFPNm4cSPjx49nyJAhTJ48GQsLC+m1oKAgRo0aBWQfe/7x40cSEhLIysqiaNGibNiwgZo1a0rvP3nyJAsXLiQyMpIOHTrg6Ogovf6t+bYgfEm1zURERODj48PVq1dp06YNo0aNonHjxtJ7Hz9+TFhYGMbGxgwYMOBH/WThJxMbG0v79u15+fIlLVu2ZNasWVSqVClHX+Xg4EBoaChnzpxBU1NTerhDdQxOTU1FT0+PGzdu0LJlS5ycnHBxcfkRlyUI/zni4PbvoJxsjB8/HrlcjpubG4MHDwayS+QqN3mVxyQYGRlRsGBBmjVrRlRUFCdPnlQrtysIgvBPpOzH6taty9SpUwEIDQ1FoVAwadIkKfhSv359nJycWLBgAWFhYdjb2+Pv70+RIkUwMTFBJpNJgZdp06axfPlyLC0t8fLyEoEX4Q9FRkZKC8AymQxDQ0PevXvHokWLgOzqLqVKlWLgwIEUKlSIsmXLUqNGDVxdXcnKyiI8PJypU6eiUCho3bo1AFZWVhQrVgw7O7sfdl3Cz0F1A0K5kJeUlISZmRkWFhZoaGgwaNAgkpOTWbNmDYcPHyYqKoohQ4bQqVMnSpYsSUJCAnFxcXh7e3P8+HFKlCjB1q1bpfK5YoND+JYvF4JVK10BdO7cmfj4eJYvX46Pjw/v379n6tSpmJqaSpsjWlpaZGVlMWXKFNauXUuZMmVwc3PDyMhILDQLeaZsK6dPn+bt27e4uLiobeDevn2bHTt2kJqayuDBg9UCL5Bd3XTJkiUkJiZy4sQJUe1K+G4KhYKnT5/i7OwMgIGBAVOnTpWq6BoYGBAQECAFXxwcHHIEX5QVKbW0tKTvUf63IOSFMnhqZ2dHWFgYHTp0YO/evchkMhYtWoSxsTGVKlXCx8eHxMRE1q5di5GR0VcDL8rvFATIbgtPnjyhVatWvH37lmHDhrF27VqsrKzUqvalpqaiq6vLrVu3uHr1KgCTJk366mbb27dvWbp0KZqamtLDm4LwR4yMjChcuDABAQFoamri5OSEpaUlMTExzJgxAwsLC9zc3Gjfvj1v3rwhKiqKzZs3c/r0aXr06MHmzZtp0KABgFoIISwsDEAKvoh5iPC9VPfdlA8c+fj4cPDgQSD7Xk/Z9kqUKMHw4cOl+zxxjJuQF4sWLeLly5cYGRlx5MgRMjIycHd3zxF8qVSpEnv37qV3797o6ekRExODo6OjNAanpaWhp6cHwJw5c8jKyqJGjRo/5JoE4b9IVHrJxR8tAmdkZKCtrQ1kH9OhLBm5bt066bgO5WZGRkYG1atXx8nJiVatWqGtrU3hwoXFZocgCP94qhOC6OhoZs6cyenTp3M8nfHmzRsOHjzI/PnziYuLw9ramkqVKtG6dWv09PR4+PAhx44d4/LlyxQvXpzt27dToUKFH3lpwk8gNTWVnTt3smrVKu7evUvXrl2pWbMmRkZGLFu2jDdv3vDmzRt0dXUxNDSkd+/eVK5cmY4dO3L79m22b99OYGAg5cqVY86cObRt2xYQTxMJ36baRvbv38/KlSu5cuUKqampGBsb061bN9q3by+FqbZt28bevXulhRZjY2MMDAxISkoiKSkJhUJB48aNWbFiBUWKFBGLLUKeqM4VYmJiiI2N5fLly1SuXJlChQpRt25dIPtJpK1bt+Lr64tCoaBu3brSGJyZmcmjR4/YtWsX0dHRlClTht27d1OsWDHRDoU8+XLM7NWrF8ePH+fChQuUKlUKgJs3bzJhwgSioqIYPHgwCxYskN6vLPusnDsrA4RFixb9ey9E+NfYs2cP48ePJzExkQkTJjBt2rQcFV+GDh1KeHj4Vyu+CML/SjlGX7p0iQ4dOpCenk63bt3w9/fHxMQk1/mGWAMUviUtLY1x48YRHByMoaEhSUlJ1KxZkw0bNlC0aFG1e7clS5Ywc+ZMWrZsyfPnz4mJiWHChAlSBcC0tDQpYNq5c2eio6PZsmULjRo1+mHXJ/xcwsLCmDp1Ks+ePWPYsGFMmTKFixcv8ssvv7BixQr69Omj9v6EhATGjBlDWFgYZmZmHDp0iNKlS0uvq1Z86dy5MxMmTKBq1ap/92UJ/xKq4+yBAwfw9vbm6tWrtG7dmnHjxknBF7H+J3yvQ4cOMWbMGDQ0NDAwMCA2NpZmzZrh5uamFnxJS0ujR48enD59GoBBgwbh6+sLZFdk09HRQS6X4+rqyqpVq+jatasUkBYE4a8nQi9fUJ2M3rt3j1evXnHnzh309PRo3rw5xsbG5MuXT3q/avDF39+fX375RZpcuLi4sGrVKlavXk3Pnj0BkSwVBOGfT3Vi8OzZM+RyOWvXruXw4cPExMTQo0cPRowYIQVfUlJSuHv3LhMnTuT+/fskJiaqfZ+lpSX169dn5syZlChR4u++HOEncOLECYyMjNRK4aalpREcHMzChQuJj4+nY8eOeHp6YmhoSHx8PIGBgTx69IjQ0FDpM5UrV8ba2poKFSoQERFBTEwMFStWZNKkSdjb2/+ISxN+Ups3b2bs2LEAtGzZEg0NDZ49e8adO3coUqQIkyZNkqoZxMXFcfr0aQIDA3n79i2vXr3CwMCABg0a0KpVK9q2bYupqam4BxTyRHUM3rlzJ3PmzOH58+fS6zKZjJEjRzJ16lSMjIz4/PkzBw8exNnZmaSkJNLS0tS+z8zMjKZNmzJv3jzp3HLRDgUlZXuTy+WkpKSwf/9+ChcuTJMmTdTel5WVhb29PdHR0Vy4cIGiRYty/fp1Jk2alCPwkpWVxefPn9mwYQO2trbSU75i0Vn4s1TXaEJCQhg5ciQpKSl5Cr4EBgZSuXLlH3wFwr/Nt4IvIuQi/BkrVqzA1dWVsmXLolAoePDgAbVq1SIwMJCiRYtK/dyNGzcYO3Ys165dA1Abg1NSUtDX1wd+X5Pu0aMH/v7+4mhL4ZtU+67Q0FBcXV159uwZo0ePxtzcnMWLF3Pz5k0MDAyk9yrvJTMzM+nTpw9Hjx6ldevWrFmzRu1IrZMnT+Ln58epU6cYMmQIM2bMwNDQUNwfCn+KCL4If4WEhAS6dOnC69evGTx4MEFBQTx8+JAWLVowe/ZsteBLZGQkM2fOlI4v8vb2pkSJEigUClJTU3FxcWHTpk2UL1+ekJAQLC0txf2hIPxNROhFhepAuHv3btzd3YmPjyc1NRUAa2trmjRpwqBBg7C1tZU+t2jRIqlMZNu2bbGysuL+/fucOHGCihUrsm/fPnGUhyAIP53w8HBmzZrFw4cPMTExIT09nZSUFAC6du3KmDFj1Mrzff78mStXrnDu3Dni4+PR0dHBwsKCTp06UahQIbXAoCAoHTp0iN69e9O6dWumTp0qHZ8F2cGXHTt2sHjxYh48eECPHj2YOHEi5cuXlyYLp06dIjY2lnXr1vHy5UtevXolfV5bW5uMjAzs7OzYvXu3WOgT8uTo0aP06tULExMTfHx86NGjB5A9AZ42bRpbt24Fstuu6nFZnz59QktLiw8fPqChoUHhwoWl18TkVvhe27dvZ8SIEchkMsaMGUPhwoVJSkpi6dKlfPz4kc6dO+Pq6kr58uUBuH//Pjdv3uTw4cN8+vQJfX19rK2tad++PWXLlsXY2FgEXgQ1yn4pMTGRdevWERERwYULF4DsYIEyrKJQZC8XjBo1im3btrFnzx5Kly7N4MGDcwRelMcpPH78mNq1a/Pbb7/h4+PzYy5Q+Ckp12S+3KRQ/e/vCb7kz5+f8PBwUWlS+D/3teDLwoULxZO8wndR7d86duzI/fv38fDwIDAwkNOnT6sFX5TWrFnDokWLiI+Px9HRkU6dOknz6LS0NFxcXAgMDMTGxoY9e/ZgaWkpNn+FPFFtJ6rBl3LlypGQkEB0dDT6+vpq71P2h9HR0fTv3x/IrppaokQJtXnw8ePHcXFx4dGjR+zcuTNHyFoQvsfXgi9t2rRh/Pjx1KtX7wf/QuFnouyrDh06RJ8+fZg6dSo9e/akR48ePHz4kObNmzNnzhwp+JKcnMzx48fx8/PjypUrmJiYULduXeRyObGxsTx8+JAKFSqwY8cOtaMKBUH464nQSy62bdvGyJEjAejRowcmJiZcunSJx48f8+nTJ8qVK4e/vz/169eXPrN+/Xr8/f159eoV6enpAFSsWJHt27djZWUlNjsEQfipHD58WNr0dXJyolevXjx58oSoqCh8fHz4/PkzHTt2ZMKECVSvXv1H/1zhJ3bq1CnmzZtHVFQU7du3Z+LEiTmCL8HBwSxdupSHDx/SrVs3Kfii6tOnT7x//54dO3Zw8+ZNIiIiyMjIQENDgzNnzojNDuGbFAoFWVlZjB07lm3btrFo0SIGDBggvX7hwgUmTZokHeehLCGuXGxRncR++eSbIHyPqKgoevXqRWpqKkuXLqV79+7Sa4GBgTg7O5ORkcGaNWvo0aNHjnYml8uRyWRf3TAWBGUf9e7dO4YMGUJkZCRFihShfv36NGrUiJIlS+Y4BkFZAatkyZIYGhpy8+ZNtcCL6nEKDg4OhISEsHbtWukIYEH4FtV+6sOHD+TPn19tbP1a8GXixIm4urrmCL706tWL8+fPc/PmTQoVKvTDrkv49xLBF+H/ikKhQKFQsGLFCqZPn86AAQPo27cvU6dO5cqVK7kGX5YuXcrKlSuJj4/H0NCQ1q1bk5iYyKNHj3jw4AFly5Zl165d4mhL4bup7mHs37+f2bNn8+TJE7KysliwYAGDBw/O9XOfP3+mZ8+enD9/npUrV9K7d29AffyeN28eCxYsYPz48dIDxMJ/z927d3Os6f0ZuQVfbt68Sc2aNZk7dy61atX6n/8N4d/nj9ZGnj9/zoABA7h69SoXLlxALpfTr18/teBLxYoV0dDQICMjgxcvXjB//nxOnjzJixcvAKhUqRINGjRg4sSJWFhYiDFYEP5mIvTyhYsXL9KjRw+ysrJYvny5dBxCRkYG4eHhrFu3jpMnT1K8eHHWrl2rNnhevXqVp0+fcu3aNcqXL0+LFi0wNzcXHZsgCD8NhULB69ev6du3L5cvX8bf35+BAweqvefAgQP4+/tz8eJF7O3tGTdunFTxRWz0Cn/G+fPn8fDw4NSpU3Ts2DHX4MuOHTtYsmQJjx49omvXrkyePJmyZcsCuR8deOPGDS5fvkzjxo0pVarU33k5wk/s/fv3NGzYEHNzc44fPy61q4sXLzJhwgRu3bqFk5MTM2fOlD6jutErCP8L5di5dOlSZsyYgZubm3TMFmQHr6ZMmcK1a9fU2mFuwasvv1MQlFQDL+3ateP+/fu0bNkSf39/ChQoIB2LAOrja3p6OoMHD5aOFbS3tycwMBBQ7wfd3d3x9fWlVatWrFixQlQ8Fb7b4sWLmTVrFpGRkdja2n41+LJ3717pqMFJkyYxdepUteBLSkoKycnJFChQQKzJCH+Z3IIvLVu2ZP369aLKpPDd3rx5Q7NmzdDW1iYoKIiPHz9Kofvcgi9hYWEcPnyYLVu2oKWlRWpqKhUrVqR+/fpMmjQJS0tL0f8JeaIadPly/hASEsK8efO4f/8+rVu3ZsaMGTmODkxPT0dHR4fJkycTEBDA8uXL+eWXX3L8OyNHjmTbtm3Mnz+f4cOH/7UXJfwj+fv74+bm9tU28r1U2+vBgwdxcXEhPT2dEydOYG5u/j9/v/Dvoeznvty7+LLP27BhA46OjowdOxY3NzeuXLnCsGHDcg2+KMXFxfH+/XsyMzOpUKEC2traaGlpiTFYEH4AUXrk/5PL5UD2pkZiYiITJkxQC7xoa2vTsWNHPDw8aN26NU+fPsXHx4fnz59L31G9enXs7e2ZOXMmvXv3xtzcHLlcLjo2QRB+GspNs/j4eGxsbKTAS1ZWltRPtm3bFldXV6ytrQkJCWHFihVcuXIFQLrhExtsQl4oj0yoW7cuU6dOpVGjRoSGhrJgwQKio6Ol9+nq6tKzZ0/Gjh1LqVKl2LNnDz4+Pty/fx9AbSNE+WeVKlX47bffROBF+C7v37/n48eP6OvrS8dbRkVFfTXw8vr1a7Zv3y61RUH4XygXXCIiItDR0aFZs2bSa1FRUUycODFH4AWyj96C7L5Q2Q+qfqcgqNLQ0ODjx48MGDCA+/fvM3jwYLZs2YKVlZUUXFEoFGRmZkrj6/Pnz9HR0WHw4MHUqVMHgOTkZM6dOwdkt7P09HRcXFzw9fXFysoKLy8vEXgR/pSoqCgAunTpwo0bN9DU1CQrKwv4vZ9Uvq6sNLRgwQLc3d2Ry+XSArO+vj4FChQQazLCX0q5eVKrVi3Cw8MBOHLkiFQBWhCUlOspyj8Btfs2uVxOwYIFGT9+PI8fP+bw4cPUqVOHBQsWULVqVS5dusTAgQOJi4uTPtOhQwcWLlzIsWPHCA0NZceOHYSGhuLu7i4CL8J3Ua7l7dmzh4MHD5KZmSm9Zm9vz/Tp0ylRogSHDh1i3bp1xMbGSq+npqaio6MDwM2bN9HW1qZYsWI5/o1z586xbds2ihQpQrt27f7iKxL+qT59+gTA+PHjCQ4O/p+/T/XesE2bNvj7+3Ps2DFpX04Q4PfAy9OnTxk2bBiXLl0iKSkJ+L0NKecb3bp1o1atWmzdupUnT55Qo0YN1qxZQ+nSpTl27BizZs3i9u3bamN40aJFqVKlCtWrV0dfXx8tLS0AMQYLwg/wnwu9pKSkEBcXx+rVqzl+/LjUuSlv7pQLLLa2tgBkZmaira0NZHdSFStWZPjw4VSoUIFLly4RExMD8NVBVBxpJAjCz+bVq1e8ePGCxMREXr16JS0UK1PQAE2aNMHFxQWAnTt3snTpUrWQgiDkhTJkBVCvXj3c3Nxo1KgR4eHh+Pr6SmEq+HbwRfl9uf0pCN+i7NvMzc0pVKgQHz9+xNDQkBs3buDk5JQj8KIMxFy9epWZM2eK/k/4PyOTydDV1UVLS0tqlxcvXsy1HWZmZpKUlMS8efNYtWqV9HlB+CPKiqZnz56lTZs2eHh4oKOjQ1ZWljR3VQYHAEaNGsWUKVO4d+8eTZs2ZezYsdSrV4/Dhw/Tvn17fv31V3r37k2TJk1YtWoVxYsXZ8eOHZQsWfJHXqbwE1L2eZs2baJPnz4kJCTQoUOHXIMvyvWXjh07Ur58eWQyGf7+/ri4uKBQKNQWmMWajPBXUwZfatasSWRkJDdu3MDMzExstgkS5Rj79OlT/P39iYyMBH6/b1Mdg2vXrk2BAgVYunQpMTEx1KlTB29vb2xtbXMEX5T9YpUqVahZsyYtW7Ykf/786Orq5ugLBeFbzp07x6BBg5gwYQInTpxQC7507twZNzc3ihcvzvr165k7dy4HDx4EQE9PDwBXV1fOnz9P1apVc1SCgew1n1mzZrF9+3aKFy/+91yU8I8za9Yspk2bRkZGBiNGjPg/C74ox9ymTZtiaWmpVr1IEDQ0NHj8+DHNmzdn165ddOnSBUdHR3bu3AlktyHlfMPY2JjmzZvz7t07li1bRmpqKtWrVycgIEAt+HLr1i21hy8FQfhn+E/1/C9fvmTmzJl06tSJKVOmMGbMGE6fPk1ycrL0HuWE4NatW0DOBRKZTEb9+vWxtbXl/fv3bNmyJdf3CYIg/KwsLS0pUaIEHz584OXLl9IiHqhPJHr16kX9+vUBCA0NZcaMGVy/fv2H/W7h56O6EPfs2TPy589PtWrVKF++PKGhoWpVhCBvwRdB+BbVyaiyQoayb9PX16dMmTLcvXsXBwcHRo4cya1btxg/frwUNEhLS0NPTw+FQsHixYvJzMykdOnSP+JShJ/Ylxthyk0LgBIlSpCcnMzdu3c5d+5crpWG0tLS0NLS4u3bt+zfv58rV66IhRYhT1JTU4mMjKRo0aIsXLhQCrwox2PVCi9jx44lKCiI8PBw/P39efDggfRU+dixY8mXLx+RkZHS5t2QIUPYt28fFSpU+FGXJ/xEvqxwoBraW7FiBT179iQxMTHX4Ity/cXMzAxDQ0OaNm0KwObNm6UniAXhj+Q2Zv4vIRXlnNnW1hYrKyu1EIMgaGpqEhsbS/PmzXF3d6dfv35MmDCBkydP5qjGYmtry9ChQ3n9+rX0YGb16tXx8vLKEXxR7Re/JILQwveqVKkSvXv3Jj4+nkmTJhEZGakWfOnUqRPu7u5YW1uzZ88ehg0bRtu2bRk2bBi1a9dmxYoVlC1blg0bNmBqaqrWpyrbqaOjY66BGOG/QdkOlMdSKhSK/7Pgi+rxXKr/LQiQXQhh6tSpvHv3DgMDA4yMjNi1axdDhw6ld+/ebNy4kbS0NGk8Hj16NCVLllTbO65WrZpa8GX27NlSxRcx5grCP8d/pvd/8uQJXbt2JSAgAD09PVxcXJg/fz41atTAwMBAGhBr1qwJIG3cqm72QvbAqaenR+/evdHR0ZEqxQiCIPxbFClShOrVq5OUlMT06dN5/fq1WpUX1fMv9fX1qVixInZ2dly7dk2UsRe+i3JSEB4eTrdu3ahevTobN27kyZMnwO9VhK5evSp9Jrfgi5+fn1R5TRC+RdnuNm7cyMSJE7lz5w6Q3bfp6uri7OyMoaEhe/fulYIGs2fPBrInyrq6usjlciZPnszZs2fp2rWr2OAVvptyEe7GjRtA9mZIRkYGAM2bN0dXVxdPT08cHR1zDbwon+B1dnbm9evXtGvXTiy0CHly9OhRLl68SPny5cmXL1+Oo1+UFV7GjBnD5s2bsbGxoUiRImzbtg0fHx9iYmIoV64cbm5uHD16lKNHjxIREcHBgweZN28e1tbWP+rShJ+I6uJwdHQ0a9eu5cKFC2RmZkpzjtWrV6sFX27evCkd46bcNMnIyODly5cMHDiQffv2cfHiRfLlyydCgMIfUm1/d+7cISwsDPjfN8hUPy8qbAhKCoWCtLQ0OnXqxLt37zAxMcHCwoKgoCC6d+9O7969uXDhAm/evJE+Y29vT8GCBVm4cCEJCQno6OhQq1YtteCLg4MDL168QFNTU1QVEv5nWVlZmJiY4OPjQ//+/Xn8+DGTJ0/ONfgyd+5cSpcuTXJyMhcuXODjx4+ULFmSmTNnsn//fooWLZoj+Cf6RAFQC+o5Ozv/nwdfsrKypPFd2W7FPaEAoK+vT8+ePalXrx4pKSnUqFEDR0dHevbsyeXLlxk/fjytWrVi27ZtxMTEYGJiQu/evblz5w5r1qyRvkc1+HL06FHGjx/PvXv3fuCVCYLwpf9E6CUuLo4uXboQExND//79OXbsGFOmTKFTp04ULFgQ+H0DpG7dumhqarJ79268vb2B7ImrckBWTiSysrJIT0/HyMjoB1yRIAjCX0PZx02aNIkKFSpw+vRpfH19efv2rXQUjerk9fXr19SuXZv58+dz6tQpihYt+iN/vvATOnz4MH379uX169fMnDmTs2fPsmvXLubMmYORkZEUavla8KVs2bJs27aNlStXShvGgpAb1bKj7969Y/ny5ezevZuVK1dy+/Zt6X3VqlVj6tSpGBgYAGBsbCy9pq+vD8CUKVNYu3YtVapUYcaMGWoBakHIq61bt9K4cWPmz58PIB2p2qhRIxo2bMijR4+4f/8+Dg4OakdrKQMv06dP59ChQ7Rr145mzZr9sOsQfi5paWnIZDLpvPHcNnnnzp3Lli1baNSoETt27MDPzw8rKyuCg4NZvHixdKRb6dKlsbGxoW7dupiYmKCjo/M3X43wM1INHISEhNCvXz+cnZ0JDg7mzZs3yGQyaaNCNfjSrl07Tp06Bfy+eTZr1ixevHiBkZERjRo1kipsiBCg8DWqVYXCwsIYNGgQ/fr1w93d/X/+7q9V3BD+25RHV65YsQIDAwM+ffqEmZkZy5Yto1atWhw9epTu3bszaNAg9u/fT1paGhUqVKBTp048evSI7du3SwFVOzs7KfgSFRWFvb29VJ1XEP4XyvCUsbEx8+bN+2bwZcaMGZQsWRKZTIaFhQXLli3DyckJS0vLHNWLBEHVXxV8UW1369evZ8OGDaSkpIh7QkFaq+vWrRujR4/G1taWiIgI4uLi6Nq1KwcOHKBbt27Ex8czcuRIevXqxdatW6lQoQKmpqaEh4dLwRa5XE61atVYu3Yt+fPn5+bNm+IBYEH4h9H60T/gr5aQkMD48eN5/PgxI0eOxMPDA+CrN2A1a9bE39+fcePG4enpiZ6eHuPGjZPeq/wzKCgIADs7OwBRxkoQhJ+Cal8VFxfH+/fvefToEdra2tStWxcDAwP09PSwsrLCwcEBPz8/Nm7cyJs3b5g7d65aqGXevHncuHGDnj17UqVKlR91ScJPSqFQ8Pr1a7y8vACYM2cOAwcOBLKrDdWrV49y5crh7+9PaGgompqajBs3jho1agC/B1/S0tLYunUrI0aMkDaMBeFLquc5x8XFkZWVRdOmTcnMzGTjxo1oamoyZMgQKlasiKamJvb29qSkpODv74+bmxvHjx+nWrVqZGZmcu7cOaKjoylVqhRbt27FwsJCLOwJefLlfCE5ORkNDQ0CAgKQyWRMmTIFgHz58rF48WLatWvH06dPuX37NpGRkVSqVIkCBQqQkJCAq6srQUFBlC5dGj8/P6lih9j0EL7l9evXKBQK7t27R0ZGBhoaGmr9V3p6OuXKlaNPnz6MHTuWokWLUrRoUT59+sS8efMICgpCJpPh7u5O/vz5f+CVCD8j1X5w06ZNjBs3DplMxuzZs7G3t6dw4cJAdsWhzMxMtLS0WL16NQA7duygT58+9O7dmxIlSnDu3DkOHDiAra2tdH8I4mly4esUCoU0Tm7evJlx48ahUCiYOHEirVq1+p/W9VTvBZcvX06NGjWoW7fu/9lvF35ucrmcRo0asXv3bjp16sTly5c5c+YMgYGBXL58mT179rBz505Onz5N48aN6dmzJ6NHj2bfvn0cO3aM4cOHA9kPZdrZ2eHt7c3QoUN5/PixuPcTvotqP/flHFZZ1VkZfIHssXry5Mn4+PjQpEkTac3F3t4eDQ0NRo4cSXh4OHPnzpW+R4zDwrcogy+ampo4OzsD4OnpyYgRIwDo1avXd32falv28fHBw8ODWrVq0b17d+nBJeG/SyaTSX1fhw4d0NDQwMvLix07dvDx40dmz55NQEAAMTExbNmyhcDAQCkck5mZyc2bN7l37x7lypWTKuHb2toSGhqKmZkZ5ubmYi1GEP5BZAkJCf/Kx1KVHVloaCiDBg2iXr16hISEAF8PvCg/k5yczOLFi6WNuGHDhtGhQwfKli2LpqYm8+fPZ/369VSpUoXdu3djbm7+t16bIAjCn6E6uT1y5Ahubm7cv3+f1NRUAKpUqULt2rVxcXHB3NycV69esX37dtauXcvTp08pVqwYnTt3pkCBAly5coXQ0FCKFStGaGgoxYsX/5GXJvykXrx4QatWrciXLx9nz54Ffi9HqpwsnDhxgvHjx/PkyRN69OjByJEj1TY20tPTSU5OxtTU9EdcgvATUO37goOD8fb25smTJxgYGCCXy/n8+TMAAwYMYPjw4VSsWBHIDk6fPXsWV1dX6cgtgKJFi1K/fn3c3NwoVKiQCLwIeaLaDi9fvsz9+/e5du0aUVFRXL58mYIFCzJ06FAmT54sfSYuLo5+/foRHR2NgYEBlpaWGBsbEx8fz5s3b6hUqRLbtm2TKhuIdijkRWRkJL169cLW1pbw8HC0tbVzLNKlpaWRkZGBkZGRFDyA7E3iiRMnki9fPkJDQylXrtyPugzhJxcaGkr//v0xNzfH09OTHj165Po+1bY5depUtmzZQmJiovR6+fLl2blzJ1ZWVmKxWcizvXv34uDgQMGCBZk7dy69e/f+n75PdQz29fXF3d2dMmXKcPLkSbHZJkiUfdTFixfp2LEjGRkZ/PLLL3h5eWFsbExoaCjHjx9n27ZtJCcnU758eeLi4vj8+TMrV65Ua6dyuZxr165RpEgRLC0tRf8nfLdVq1Zx+fJlFi1alKOfUranxMREXFxc2Lp1K2XLlsXT05PGjRurPWx05MgRKlWqROHChcUDwUKeqPZXqvMMb29vPD09kclkrFy5Ms/Bl9wCLyYmJoSHh1OpUqW/5iKEn5JqHxUREYGPjw9Xr16lVatWTJw4kTp16gBw4cIFoqKiWLhwIYmJiWRkZDB9+nQmTJiQ63eJtRhB+Gf514ZelEaNGkVQUBDBwcG0atVKbTD9IwkJCWzdupVp06YB2eXs8+fPT1ZWFq9evaJ06dLs3btXLK4IgvDTUS4yA7Ro0QIzMzPOnTvHx48fSUxMpGrVqmzbto3ChQvz7t07Lly4wNKlSzl37pza95QpU4bNmzdTvnz5H3EZwr/A1atXad68OVZWVhw5coSCBQtK46nqBGLbtm2MHDkSgK5duzJu3DiqVav2o3628JPatWsXQ4YMwcLCggkTJtChQwc+fPhAaGgoK1asIDExkV9//ZXRo0dLwReAd+/e8fDhQ+Li4tDS0qJWrVqYmpqir68vJrfCdwsKCmLKlCkkJiZSsmRJChQowI0bN8jMzERXVxcnJycmTZokvf/du3esWbOGc+fOSeHA2rVrU79+fYYPH465ubloh8J3efHiBc2bN+fVq1dMnDiR6dOnA39cuTQtLQ1dXV0uX75Mu3btaNeuHRs2bPg7f7bwL/L69WsGDhzIuXPn1DZylesqWVlZPH36FIACBQpgYmIiffbgwYPExMTw4MEDypcvT69evUTFNeG73L9/n759+3L//n0CAgLo3r07oL7x9vnzZ3R0dNDS0pIqH3xtzS+3zbYCBQqwZ88eUQ1VyEHZlqKioujQoQMZGRl06dKFZcuWYWBgQFZWFjExMSxdupTo6GhiYmKwsLBgxowZ9OvX7w+/UxDyQllxt3r16qSkpODg4MC8efP+MPjSq1cvzp8/T9myZfHw8KBp06Y59lbEOCx8zbfCUOnp6dIRqd8bfPla4OXAgQPY2Nj8312E8K/xteBLmzZtGDVqFI0bN5be+/jxY8LCwjA2NmbAgAE/6icLgvCd/rWhF7lcTkpKCi1btuTRo0ecO3eOUqVKfff3nDhxgvXr13Pjxg1ev35N2bJlqVmzJpMmTRLnVAqC8NO5evUqPXr0IDExEX9/f/r27QvAq1evOHfuHD4+Pty+fZty5cqxb98+LC0tgew+dfv27bx69YrXr19TuXJlmjZtSpEiRX7k5Qg/uRcvXtChQwfevHlDWFgYtra2aot2yv8tl8vp1KkTZ8+eRVtbmzp16jBv3jyqVq36g69A+FnExsbSq1cvHjx4wNq1a+nWrZva6yEhIfj5+XH9+nX69evHyJEj1YIvuRFPsgnfKywsjH79+lGgQAG8vLykjTblER1r1qwhKyuLyZMnqwVflH3hs2fPAChWrJg0BxEbHcKfsXr1ambOnEnRokWZMWMGXbp0AXLv11Tnu7/88gvHjx8nMDCQtm3bin5Q+FNiY2Np3rw5tra27N27V/r7T58+8fDhQ+bOncutW7fQ1NSkXLlyLFy4kBIlSnz1+8SajPA9zpw5Q69evbC3t2f58uXS36enp/P8+XM8PT25f/8+BgYGtGzZkoEDB2JmZvbN/lFstgl5pbx3u3TpEh06dCA9PZ0uXbqwePFijI2NAUhKSiIxMZGAgACMjIxwdHT8sT9a+Nc5ceIEo0aN4sWLFwwYMID58+fnCL4o+7grV67QpUsXEhMTKVWqFG5ubrRp0yZPDxUL/22qc9Xo6GiuXbvGxYsXqVKlCpUrV6Zhw4YApKamoqenB+Q9+CLGYOHP+qPgy9ixY2nQoIH0XtVQtJhzCMLP4V99d5KRkcG7d++AP3ee5OPHj2nUqBH169cnKSmJV69eYWVlhY6ODtra2qKjEwTh/7F3n1FVXGsYx/+HXqQoAiIoKiZiRdFYSbwm9h57NIlGBStRRDpWLBF7x94LVmxoYkk0ikaN3diSSOwVQaTDOfcD60zOETVqEhHz/r54w8yZO7PWXntm9n7m3QWG9oHuyJEjJCQkMHToUCXwkp2djaOjI61bt8bd3Z1+/fpx6tQp/Pz8iIqKwtraGgMDAz777LN8vgrxrilevDjVqlVj8+bNhIeHs2jRIhwcHJT2qvtlpbm5ORUqVMDW1pbTp09jZ2eX36cvCpCUlBTu37+Pl5eXEnhRq9VoNBoMDQ1p06YNxsbGBAcHs3LlSoyNjendu7cSfHlWsEAmesXL0mg0pKamEh0dDcCwYcOUwAtAnTp1KFeuHCVKlGDEiBFMnjwZjUajLHWUk5ODgYEBLi4uym+07VECL+J1tG3bltjYWPbv38/ChQsxMzOjadOmqFQqvXdc3UG+8PBwdu3aRbNmzahZsyYg/aB4Pffu3SMxMZF79+5x7do1SpYsyZkzZ1i3bh3r1q3j/v37ODk5YWBgwP79++nUqRPbtm1TwvhPkzEZ8TzPCtNfvnyZ1NRUMjIySE5OxsrKiosXL7J161aWLVvGrVu3sLS0JCUlhZ9//pnbt28zcuRILC0t9Y4tk23idWnfcWvUqMGOHTto0aIFMTExGBgYMHXqVKytrbGwsMDS0lKpxgZS0UW8nucFlOvXr8+8efPo1asXy5cvB8gTfNH2cRYWFqhUKurUqcPhw4eZOXMmn3zyiYRexAtpNBqlz1q/fj1hYWHcv39f2W5lZUW3bt0YP348ZmZmSvAlMDAQgPHjx9O3b1+APMEXtVot92Dx2lQqldI3NmvWDJVKRWRkJN9++y0aTW59CG3wRfc9Q945hCgY3tmnZQMDA2xtbXFzcwPgjz/+AHIH7l5WTEwMGzduRKVSYWtrS7ly5bC0tFTWrpSOTghRUGgf6LRLI2jXqczKylJeVA0MDHB3d2fkyJG4urry008/KUsaqdVqveNpHwKFeF3aNjV06FDc3d05ePAgkydP5sGDB8qkm3aiF3InSGrWrMk333zDjz/+iLOzc36evihgbty4QVJSEqmpqaSnpytty9DQUOnPmjdvTv/+/QFYsmQJ8+bN49KlS4AEC8Tfo+3TLl68iK2tLQ0aNAByJ8y0ihQpQseOHfH390etVjNnzhy++eYbAIyNjVGr1ahUKmXQWsIG4u9wcHBg0qRJlC1blkOHDjF58mRlwkP3HVf7jDhy5Ehmz56Ns7Mz48aNo0iRIvly3uLdUKtWLRo3bsyFCxfo27cvYWFhfPrpp8yePRs3NzciIyPZvXs3GzdupFq1avz222/88ssv+X3aooDRnWxbvHgx/v7+QO7yvu+//z5Hjhxh2rRpzJ07l88++4zx48djZ2dHQEAA27dvJyIiAisrKw4cOMCTJ0/0ji2BF/F3PR18MTExYdOmTfj5+fH48WNUKlWeMRh5HxGvSjfwcvnyZfbt28fvv/+ubPfy8lI+PFq+fDnBwcGkp6cr2zMzM4Hc95TChQvTu3dvBg0axLx585SqHEI8j+5y5T4+PiQkJBAUFERsbCzLly8nOzubqKgovvrqKwAl+AIQGBhISEgIGo0GX19f5T0F9AOAcg8Wr0s7TwLQtGlTAgMDqVatGt999x0zZszg0KFDefYTQhQM7+wTs0ajISMjAwcHBzIzM1mxYgWQO3D3Mh3Vo0ePiIqKYtSoUTx48ODfPl0hhPjXZWdnKxNs2olcbYhPV9WqValRowYJCQns3bsXyDvAIpNt4q/o3mtv3rzJ2bNn2bJlC7GxsSQkJCgDKC4uLnz11Vc4OjqyfPlyAgMDuXnzJoaGhspg8tixYzl79ixlypShcuXKuLq65ss1ibfL0wPB8PxAXokSJShcuDB37twhKSlJWRYG0BtU7tu3L56engAsX76c2bNnc/PmzX/pCsR/SUpKCqmpqSQmJnLjxg0gb4DexsaGZs2aUbZsWRITE1m0aBETJ04E/pwcEeKfUrZsWVasWEHlypX5+eefCQwMpG/fvhw9epSbN29y/fp19u7dS4cOHZg+fTrFixdn48aNL1xmRgit592Ps7KyABg9ejQNGjTg8OHDzJs3j7S0NPz8/Fi+fDk9e/bE2dmZcuXK8d5776FWq7l3796bPH3xDtC+r27btg1/f3+WLl1KXFwcdnZ29O7dGxMTE6ZMmUJYWBjx8fH4+PiwZMkSAgICqFq1Kp06dcLe3p7Lly9z5coV5bi6X5dPmjRJJtvEa3tR8CU5OVlCLuJv0QbmAbZv386XX35J165d2bp1KwkJCcp+TwdfAgICuH37NhqNBhMTEwBGjRrFrVu3qFOnjvKR3Kt8VCz+u/bv309oaCh2dnbMmzeP4OBg6tSpw927d8nIyMDQ0JCYmBh69eoF5A2+hIWFkZmZyYQJE0hNTQX+HJ8eOXIk33zzDTY2NnIPFq/lRcGXmTNnKh8CyxyIEAXLO1uHTqVSYWpqSt++fdmzZw8xMTF4eXnRvXt3vRJWT9N+sXH9+nVSU1P5+OOPKVasWD5cgRBC/LOMjY2pV68eO3fu5MyZM3prpuqysbGhVatWbNy4kRs3bkgZXfHKdO+xe/bsYfTo0Vy5ckV5ea1cuTI1a9YkODiYokWL0qZNG9LT01m0aBGbN2/m+PHjtG7dGjs7O06cOMH27dspUaIEbdq0yc/LEm8Rbb/0xx9/EB8fT40aNbC0tHzuM97777+Pu7s7hw8fZvjw4UyZMgVLS0vlOAYGBkoo0MDAgA8++ABTU1NWrFhBqVKlGDJkSH5cpnjLPe994lmcnJzw8vJi3bp1nDx5krp16z7z/lq+fHn+97//8csvv5CcnMy0adOwsbHBx8dH7sXiH+fu7s7y5cuZMGECW7duJTo6mm3btgG579MpKSkYGRnx0UcfMW3aNEqXLp3PZywKAt2+7cqVK6SlpfHo0SO8vLyUwH25cuXYsGEDGzZsoGjRolhbW1OjRg1AvwrWlStXcHFxoXbt2m/+QkSBpG1/OTk5pKamsmDBAuzs7IiMjKRu3boAfPbZZ9SsWZMNGzZQsmRJXF1dady4MfBnYMve3p6MjAw8PDyoWrWqcnxt2x4zZgyTJ0+mcOHC7NixQybbxGt51lJHmzZtAmDatGlYWVnl8xmKgki30tXKlSsZPHgwOTk59O3bl8aNG+ep2KcNvnh7e7Ny5Uru3r1LgwYNqF69OgsXLmT9+vV89NFHFCpUSPmNLG0k/kpiYiJLlizh0aNHTJ06VVned9KkSYwdOxYrKyumT5+On58fmzZtQq1Ws2TJEr2ljoYOHYqFhQUtWrTAwsJCOXZqaioxMTGo1Wp27dqFu7t7fl2myEeXLl2iXLlyf+sYumOITZs2BSAyMpJ9+/aRlJRERESE8o4ihCgY3vknFA8PD9q2bcvatWtZsWIFjo6OynrlTw8065YojYiIIDk5mRYtWgCydqoQomB51vrlkDuZZmJiwrp162jQoAFdunTR+11WVhbGxsaYmpoCuUEZ6fvEq9L9ouiLL74AckuJFylShMOHDxMfH8/Zs2c5duwYa9euxcnJiW7dulG2bFlmzZrF4cOHmT17tnK8smXLsnLlSkqWLJkv1yPePgYGBly7do0PP/yQ5ORkWrVqRb169ejTp4+yj+6kh7GxMWFhYfTp04fY2Fjc3NwYMGAAlpaWyuSaoaEhOTk5PHz4kHbt2lGrVi1OnjxJREQENWvWxMvLK78uV7yFtO8NKSkpZGVlYWtr+5e/8fT0JDo6mlmzZtG4cWPee+89vfePjIwMTE1NsbKywtPTk86dOzNy5EgWL15M+fLl+fDDD//lqxL/RaVKlWLSpEl07dqV2bNn8/DhQ65cuYK9vT0eHh60bt2aunXrUrRo0fw+VVEA6E60rV+/nnHjxvHw4UOSk5Px8vKia9euNGvWDFtbWwwMDOjUqZPe77X9oEajITg4mJMnT9K+fXtpf+Kladvf9evXKVWqFKdOnaJ37960a9cOyK1+WqhQITw8PPDw8ND7rW778/f35+rVq/Ts2TNPddT4+HgOHz6MoaGhBF7E3/a84Mvjx49ZsmSJXtBAiJehHY/ZvHkzvr6+2NvbM3r0aL3xP+0kr/ZdxMvLi8WLFxMaGsr333/P7t27lffjMmXKMHv2bKysrF4p9C/+2xITEzl8+DCff/45PXr0ACAqKorIyEgsLS3ZsmUL1apVw9DQkP79+xMTE0NOTg7Lly/HzMyMtLQ0zM3NlSWos7OzlRUcLCws2LNnD0lJSbi5ueXjVYr8MnXqVEaPHs2cOXP47LPP/taxng6+qFQqgoODuXbtmlQ5FaIAUiUmJr7zi5LFx8fz5ZdfcvbsWerVq0fv3r1p27YtkDtgbWBgoAzOqNVqwsPDmTt3Lh9//DGLFy/GxsYmfy9ACCFewsu+fGq/SoPc5TtatWqVZ58BAwawevVqJkyYgI+Pzz9+ruLdd/LkSTp06EBycjJTp06lW7duANy9e5fDhw8zceJEfvnlF95//322bt2Ko6MjkBtUiI6O5u7du9y7d49KlSrxv//9j+LFi+fn5Yi3iPYL3D59+rB+/Xql39NoNDRo0IBPPvmEjh074uDgoPebpKQkFi5cyMyZMzE0NKRLly6EhITofUEZGhrK3LlzlRfniIgIpkyZwldffcWUKVMkBC2AP++3v/32G97e3pQuXZpu3brx8ccfK/vohll0de7cme+++w4XFxe2b9+uLNem27aaN29OZmYmq1evZubMmcyaNQtfX19Gjx79Zi5Q/Gdpv6q8d+8eZmZmWFtb5/cpiQJqw4YNeHt7A1C7dm3i4+O5c+cO9vb2dO3aFV9fX+zs7J55X83OzsbPz4+VK1fy3nvvsXXrVooVKyYTbeKlRUVFERISQv/+/Tl48CBjxozhww8/VCbMXkSj0RAYGMjChQupVKkSGzduxMHBQa/9ZWdnExcXh6urqyy7Kv4x2v7w559/pmHDhgD89ttveapyCPEyrl69SqdOnfj1119ZsmSJMg+i/dAtJyeHnJwcnjx5otfGLl++zPfff8/WrVuxtLSkZMmSBAQE4Ojo+Nz3G/Hf8vTzmEaj0Qs9a925c4c9e/bg6elJhQoViIuLY9CgQdy6dYv169dTt25dsrOzefz4Mf369WP37t1oNBratWvHokWLXngO0hbFqFGjmDZtGsbGxsyaNStPkP516LbtH374gfLly+Po6CjjgEIUMP+J0AvAxYsX+fzzz/ntt98oU6YMn376KUFBQUBuJYPMzEzS0tIICAhg/fr1uLq6snPnTpycnKRjE0K89XQfzE6fPs3Bgwc5evQoxsbGuLm50aJFC6pUqaLs7+/vz+LFiwEYMWIEtWrVwtPTk5ycHCIjI5k+fTrvv/8+GzduxMXFJV+uSRRM2rY4d+5cQkNDGTp0KGFhYcCfX2ao1WouX75Mv379OHXqFM2aNSMqKkom18QrOXXqFJ9++ikpKSl069aNb7/9ltu3bwPg6urK4MGDqVq1ql5J+mvXrrFixQqWLl3KgwcPqFKlCq1bt8bS0pLvv/+e7777jvLly7Np0yaKFSvG/v37adu2LXXq1CE2NjafrlS8jR4/fkzTpk25cOGC8reuXbtSp04dPv/8c+Vv2j5R2/8lJCTw+eefc/jwYYoXL86kSZOoUqUKzs7OqNVqwsLCiIqKok+fPnzzzTccPHiQ1q1bY25uztGjR3F2ds6PyxX/Edr2qlarUalUL1wWWAhd2nai0Wh48OABbdq04eHDh4wdO5YOHToQHx9PdHQ0K1eu5P79+3z11Vf4+/tTtGhR5bc3b95k3bp1bN68mbNnz1KpUiXWrFmDi4uLTG6IVzJnzhzl/QNyl1Lo1avXC39z69Ytjh07xuzZszl27JiyBJe0P/EmacefT58+jZ2dHS4uLjImLV7LgQMHaNOmDZ9//jkzZ85U7rUZGRncvn2b8ePHc+PGDVJTU+nYsaNSTeNp2v5P+kGh68mTJxw+fBgPDw8cHByUfmrp0qUcPnyYefPmAbnLEGmXJZo8eTJjxoxh9OjR+Pr66vVto0aNYtasWZibm5OcnEyvXr2YNGlSvl2fKBi0S2WpVCqioqL+keDL0/dcuQcLUfC888sbabm7u7N27Vr8/f356aefmDx5Mvv378fJyYny5ctz9uxZLl26xO+//06VKlVYvXo1Tk5O8lAnhCgQtJMRO3bsYPDgwTx48EBv+9SpUxk7dizNmzfH2dmZSZMmYWpqyty5cxk1ahQWFha4ubmRkpLC77//TrFixVi+fLkEXsQr0054xMXFAVCrVi3gzy+KILeEs7u7OyNHjmTQoEH89NNPHD58mCZNmuR5oZDJNvEsGo2GMmXK0LBhQzZs2ECVKlUYNWoUa9euZePGjRw9epTAwECsrKzo06cPzZo1w93dnZIlS9K7d2/ef/99Jk+ezJkzZzhz5oxy3IoVK7J27VqKFSum9/9XuHDhN32J4i2XkpJC4cKFUalU2NjYYGlpybp161i9ejXbtm2jY8eOeHl5KW3JyMiIrKwsihQpwuLFi+nTpw8HDhygT58+uLi4UKpUKW7evMmZM2coU6YMX3/9NQDVq1enbNmyXL16laysrPy8ZPEfoL3f6t6H5R4sXoa2ndy/f5+0tDSuXr3K6NGj6dChA5C7jFbfvn0pU6YM48ePZ8mSJQBK8CUnJ4cbN26wc+dO4uPj6dGjB6Ghodjb28uYjHhl/fv3x8jISPnQ7cyZM3qhvmdVF9qxYwezZ8/m1q1btGvXjnHjxkllA/GXnvWu+ncmyLQVyLVLb0n7E68rISEBQGk/KpWKy5cvs2XLFpYtW8bNmzcxMTEhMzOTU6dOkZiYSGhoKKDfhrX/SjsUWhqNhj179jB8+HDef/99pk+fjrOzM0uXLsXPzw9HR0fOnDlDlSpVlMBLVlYWO3bsAHLHXAAlhGVqakrhwoWpWbMm/v7+hIaGPjeEJQT8eW8cOnQoarWa8ePH07dvX4C/HXzR9nna+7sEXoQoeP4zlV607t69y+bNm5kyZQoJCQnk5OQo2ypWrEj9+vXx8/NTBl7koU4I8bZ4VglJ3f/evXs3nTp1wsTEBF9fX2rXrs3ly5c5fvw4mzdvRqVS0a9fP7y9vZU1KZcuXcrevXvZs2cP6enplCpViho1ahAaGkrp0qXf9CWKd0RWVhbdu3dn586djBkzhgEDBjxzv6SkJPz9/dm4cSPe3t5ERka+4TMVBd2WLVvo0aMHZmZm7Nmzh4oVK6LRaJg1axaHDx9m586dAJQtW5aqVasSGhqKo6MjFhYWPH78mPXr13Pz5k3S09MpV64cLVu2xM7OTjm+j48P69evZ/jw4fj5+UkIS+hZv349Pj4+eHh40LVrV9LT05k8eTKPHz/G1NQUZ2dnwsLCqFixIuXKldP7rUajITw8nCNHjnDixAkArK2tqVy5MvPmzVMquiQkJFCvXj2sra3Zu3cvhQoVeuPXKYQQL2PFihXMnz+f5s2bs2DBAvbv30+JEiX0xlVSU1OJjY1l3Lhx3Lp1S6/iS1paGr///jvp6emUL18eCwsLGZMRr0y3zcybN4/g4GAAIiMjlSW3nhVKuHfvHnv27MHe3p7atWtjZWUl7U+8kO57wYULF/j9999p0aJFPp+VELnOnz/Phx9+iJGREYGBgRQpUoSoqCiuXLlCxYoVadmyJS1atODMmTMMHDgQY2Nj4uLiKFu2bH6fuigAzp49S58+fbhw4QIdOnSgUqVKjBw5kuLFixMZGfnMvvCzzz5j165dylLSuksONmvWjHv37vHzzz8r9+iXWZJQ/HfpPqNFRkYyfvz4f6zii+6xte1QxgKFKDj+c6EXrZs3b/LLL79w7tw5ihQpgqmpKY0aNcLKygoTExN5uRVCvFW0fVJycjLXrl1TkvFaf/zxB59//jnnzp1j1qxZdOvWTW/7xIkTmTFjBqmpqQQFBfH1119jZmYGQGZmJrdu3eLJkycUL14cCwsLZZsQr2v27NmEh4fTqVMnpk+f/tw2pQ0tNGvWjJUrV0qKXrwyHx8fNmzYwOjRoxk4cKDy96SkJH744QfWrl3L/v37SUtLw9nZmbp169K5c2c++eSTFx537NixTJo0iXLlyrFx40ZZVkYotAMeaWlpdO/enUOHDjF16lQ6derElStXiI6OZv/+/Rw/fhxjY2PKli1Lx44d6dq1K0WKFFGqXkFuqOWXX34hNTWVYsWKUapUKb2l3gIDA1mwYAFdunRh2rRpmJqa5sclCyHECyUmJjJ48GC2bNlC6dKlefjwIT/++CMlS5bMEzB4VvBlyJAh2Nvb6w0oy+CyeJEXtQ/dNrdgwQICAwMBmD59Ol9++WWefXSX55L2J16GbvvZsWMHY8aM4eLFi/j7+xMeHv63ji3j0eKfEh0drVQ/0PL29qZv376UKlVKacPNmjXjyJEj7N+/X29ZdCGeJysri1OnTjF8+HCOHDkCgKOjI/PmzaN+/fpA3vvokiVLGDJkCI6OjkyfPp0mTZqQk5NDWFgY8+bNo0ePHkycOBEDAwMZFxQv5d8Ivugec8mSJajVarp27Yq5ufk/dt5CiH/Xfzb08iLyciuEeJtoH7ju379P48aNqVq1KhEREXpLD506dYq2bdtSu3Zt1q5dC+SmkQElGa8NIahUKtavX/+XE75CvAzdAT/d/71v3z4+++wzMjMzmTt3Ll26dNH7nXa5o127dvHZZ5/RunVrli1b9sbPXxR82jK6pUqVYvfu3RQtWlTvq6Dw8HBmz56NsbExlpaWJCYmAtC7d29KliyJr6+vcqyEhAQeP37MuHHjWL9+Pfb29mzbti1PlQ4htKZNm8aoUaMoVaoUu3btwtHRkYyMDLKyspgyZQqHDx9WBgKrV69O1apV8fPzw8HBQS/88iwjR45UykVv375dqdImhBBvo7NnzzJ//nw2btxIWlqa3uTv02MsusGX+/fv07ZtW0aPHi3LCYqXovvOcerUKS5dusTZs2eVj9lcXFz03pUXLlxIQEAA8PzgixAvS7c/W7lyJV9//TUajQZ/f38aNWpEzZo1X3tMWXeybc6cOXh6elK7du1/7NxFwfW6cxVHjx5V3pHLli2rjANqj5eZmUnt2rUxMTFh3759ynI0QryMUaNGMW3aNCD3XXfz5s1YWVnpLW+uu7xgUFAQCxcuBMDLy4uHDx9y4cIFypQpw/bt23FycsqvSxEF1D8ZfNE91sSJExk3bhw1atRg/fr12Nra/tOnLoT4l8jb3TNI4EUI8bbQDbw0b96c+Ph4HBwc8rwInDlzhqSkJOUFNTMzEyMjI4yMjFCr1QAMGDAAHx8fNBoNkZGRysSvEK9Ko/kzL6s7UKz7vz/++GMlTNCvXz+2bdumdwztC7D27/Xq1fvXzle82z7//HNq1KhBfHw8c+fOJT09XQm8TJ8+XQm8zJ49m6VLl9KjRw8gdwJk+vTpen3hmTNnlJfa6tWrExsbK4EX8UzafnDgwIF88MEHxMfHs23bNtRqNYaGhhQqVIjhw4ezbds2mjVrBsDPP//MokWLaNKkCSNHjuTw4cN5jpuYmMj+/ftp06aNEnjZsGGDBF6EEG8tbX9YuXJlfHx86NChA6ampsTExLBlyxYApYqGloWFBc2bNyc8PBwDAwN+/PFHGYcRL0Wj0SjvHNHR0bRr146+ffsye/ZspkyZQocOHfD19eXQoUPKb3r37s3EiRMBGDRoEMuXLwdy312078pCvCxtXxUTE4Ovry9FixYlKiqK8PBwatWq9Y8EXiZPnkxYWBi+vr6kpaX9Y+cuCi6VSkVOTs4r/Uaj0VCzZk3CwsLo06ePEnjJyMhQjhccHMzVq1epW7euLCUjXppGo+G3335j+fLlFC1alNKlS/Pzzz/Tr18/rl+/jrGxsXJ/1faJBgYGBAQE4O/vD8DBgwe5du0aH3zwAVu3bsXJyemV27j479K2L0NDQ+Wj38DAQEJCQtBoNPTt25d169a99PGeFXixtrZm2rRpEngRooCRSi9CCPGW0g28NGnShKtXr9K3b19Gjx6NsbGx3pce2iViKlWqxP79+zEwMNDbrj3WpUuXaNu2LWZmZnz33XfY29vn5yWKAki3XZ0+fZqDBw9y9OhRjI2NcXNzo0WLFnolcf39/Vm8eDEAI0aMoFatWnh6epKTk0NkZCTTp0/n/fffZ+PGjXpfZArxMrR925o1a/D398fDw4NNmzZhbm7O1KlTGT16NEZGRixatIjWrVsrv9u1axcnTpzgyy+/xMXFRa9dL1++nISEBLp06UKxYsXy69JEAaBtf7NmzWLYsGE0atRIGVjRtqnp06czcuRITExMCAgIYN++fRw+fFiZAB4+fDiDBg1SJvAuX77MmDFj+OGHH6hZsyaRkZGUKVMmPy9TCCEUz/vSXPfv586dY86cOaxbtw5PT0/8/f1p0qTJM3+fkpLCDz/8gKenJ05OTlJ1V7y0DRs24O3tjaGhIQEBAXh4ePDHH38QFxfH1q1bcXBwIDIykjZt2ii/WbRoEUOHDgX0K74I8aquXLlCt27duHLlCgsXLqR9+/YAetUmnzx5gomJCUZGRkrA6nmVhZ412WZnZ8fmzZupXLnym7ko8VYaN24c33//Pbt3737tYzxrCTeAgIAAFi5cSPny5YmJicHBwUHuw+KVbNq0CRsbG5ydnRkwYAAnTpygefPmTJgwARcXl+f2eydPnuTx48dYWVnh5uaGjY2NLO0mXuiv+qbMzExMTEyAV6/48rzAy65duyhfvvw/dxFCiDdCQi9CCPEW0j5wPXjwgMaNG3P16lX69OlDREQExsbGeV4G7ty5Q6NGjbhx4wZTpkyhe/fueYIvAPfv36dhw4Zcu3aN3bt3U6NGjfy4PPEO2LFjB4MHD+bBgwd6fzc2Nmbs2LE0b94cZ2dnNBoNYWFhzJ07F8j9stfNzY2UlBR+//13ihUrRkxMjFTTEH/Lr7/+Srt27bh+/TozZswgJSWFkJAQjI2NWbx4MS1btgTQK7Or7Ue1/+oOyMiAi3gVV65coXHjxiQmJjJmzBgGDBgA/Ln0kZGREYsXL6ZVq1ZkZmYSHR3NDz/8QGxsLEeOHMHV1VXveL/88gv379+ncuXKFClSJD8uSQgh8tB9r3j48CGPHj3i5s2buLq6Ym1trddfnTt3jtmzZ7Nu3Tpq1KjBkCFDnht80ZJ7r3hZ586do1OnTty+fZslS5bQtm1bZdt3331Hv379SEhIICwsjKFDh+o94+kGX+bNm/fKpe+FADh06BCdOnWiTZs2zJkzR/l7ZmYmN27cYPz48Vy5cgULCwsaNmxIjx49KFKkyDP7P5lsE88TFRVFSEgIVlZWbN26lapVq/7tY/7xxx8cO3aMJUuWEBcXR7ly5diwYQMuLi5yHxZ/SXs/fVaY5aeffiIkJISTJ0/mCb5oNJo8Yy7POq4Qz/L0spanT5/m6NGjVK5cmUqVKuHl5QVAeno6ZmZmwMsHX+QeLMS7R+rWCSHEW0Y38KJb4WXkyJF6gRftv6mpqRQrVozOnTszffp0Vq9ejZubG15eXsrLiPYFw9LSEpVKRfny5XFzc8vvSxVvqacH457+7927d/P5559jYmKCv78/tWvX5vLlyxw/fpzNmzcTFBREfHw83t7elCpVinHjxvH++++zd+9e9uzZw9mzZylVqhQdOnQgNDSU0qVL58dlindI2bJlCQgI4OuvvyYsLIzk5GQlaKANvGg0GiXwAigvttp/dQdZZLBPvCyNRsN7771HYGAgYWFhHDlyhAEDBjB9+vQ8gZecnBxMTEz44osv+OKLL0hOTsbKykr5Kljb11aoUCG/L0sIIfToPgtu27aNefPmcfr0aZ48eYKdnR1ly5Zl8ODBNG3aFIBKlSopAcB169YxZcoUAJo0afLMr81B7r3i5V26dInbt28TFBSkF3g5duwYERERJCQk4O/vr4RbdJ/xevXqRVpaGqNGjaJmzZpv+tRFAaQ72ab935cvXyY1NZWMjAzlee7ixYts3bqVZcuWcevWLSwtLUlJSeHnn3/m9u3bjBw5EktLS71jy2SbeJ4ffviB0NBQihUrRlRUVJ7Ay+tUZFGr1Zw6dQofHx+MjIzo0KEDY8aMwdHRUQIv4rl021p2djZZWVmkpaVhaWmJubm5sl+NGjWYMGECQUFBxMbGAijBF+1xxowZw927d5k9e7be/4cEXsTz6C5ruX79esLCwrh//76y3crKim7dujF+/HjMzMyU4EtgYCAA48ePp2/fvgB5gi/apalB7sFCvEsk9CKEEG8ZQ0NDHj58qFR46dixI2PGjMHQ0FCpUqB9If31118JDw8nIiKCLl26EBcXx+HDh5k8eTIPHz6kVatWeuvyRkZG8scff9ClSxdMTU3z8SrF20rbtpKTk7l27RoVK1bUG0z5448/GD16NABTpkyhW7duADRs2BCA8uXLM2PGDKKiorCxseHrr7/GzMyMHj160LVrV27dusWTJ08oXrw4FhYWSgpfiL/rgw8+oHz58ly4cAFzc3NWr17N//73P+D1BgWF0PWsNqT7t2rVqmFvb8/27dvx9vZmw4YNeoEXyDuYZ2VlhUajUe7T0kaFEG8rbf+0cuVKfH19AahduzZpaWk8ePCAn376ic8++4zRo0fz+eefU7hwYSpVqsTAgQOBP4MvKpWKxo0bS38n/pbDhw8D6IVWjh07hp+fH+fPn8fPz4/w8HBl28OHD8nOzsbR0RGAgQMH0qNHDwoVKqS3HI0QT9OdbFu8eDFnz55l6tSpfPLJJ7z//vscOXKEadOmUbRoUebPn098fDyVK1emW7duNG/enIMHDzJt2jQOHDjAkydP9EIvEngRL3L69Gk0Gg29e/emfv36yt+vXbtGyZIlX+s+amBgQKNGjVi6dClGRkZ8+OGHWFlZSeBFAH+G+jIyMpTxYt3Q3759+4iJieH48eMkJydTvnx5atWqha+vLyYmJhgaGuLp6akXfFGr1UyZMgUnJydGjx7NtGnTsLe359GjRxQuXDg/L1cUENq+bu3atfTr1w9DQ0OCgoKoX78+Dx48oE+fPkRFRXHnzh2WLFny3OCLr68v6enpytKWum1b7sFCvFvkzU4IId5Ct27d4urVq6hUKlQqFfHx8ZQpUwZjY2Ml+HLlyhUaNWpEUlISrVq1olu3boSGhjJs2DAOHDhAfHw8u3btokuXLqhUKjZu3MjKlStxcnIiKCgICwuL/L5M8ZbRDnbcv3+fxo0bU7VqVSIiIpQvMwAePXrE9evXadKkiRJ4yc7OBsDIyIiAgAAsLCwIDw/nm2++oXr16nzyyScAmJiYUKpUqTd+XeK/wd3dnf/9739cuHCB4sWL88EHHwBSKle8Pt1Qy5MnT8jKyiIxMRF7e3usrKxQqVRKv1m7dm3atWtHVFQUGzZswNjYmEWLFimBl+cFr2TiVwhRUOzbt49BgwZhZ2dHZGQk7dq148mTJ1y/fp3Vq1cza9Yshg8fTkZGBoMHD8bIyIiKFSsqwZfNmzczbNgwTE1N9SbwhHhV2uc6bVglLi6OwMBAJfAyfPhwIHepGbVazfz58zEwMGDAgAGYm5srFVB1g6dCPItuhSt/f38AOnbsiIeHB71792bOnDlKoE+j0eDj44OPjw8lS5bE2NiY4sWLs2rVKi5evMiVK1eU4JXu1+WTJk2SyTbxXFlZWcr/XrJkCStXriQ0NFQZY3lVFhYWtG7dWvlvbVVo8d+mHTOJj48nICBAqeisvd+uWrWKQYMGkZOTg62tLY8fP+bGjRvs3r2bkydPMnDgQKpXr46xsTGenp5ERkYSEhLCrl27OH36NMWKFePkyZM4OzsTGxtL4cKFZZxGvLT9+/cTGhqKnZ0dEyZMoH379gAsXLiQjIwMDA0NiYmJwcDAgEWLFuUJvhgYGDB27FgmTJhAhw4dsLCwUNreyJEjmTlzJjY2NuzcuVPuwUK8A+TOIoQQb6HKlSuzd+9eIPfLyIkTJ3LmzBnUajXGxsZcunSJpk2bkpSUREBAgBI+8PLyIjIyko4dO5KcnMy6devo3Lkzn376KStXruT9998nJiZGggciD93AS/PmzYmPj8fBwQEnJye9/c6cOUNSUpISmsrMzMTIyAgjIyPUajUAAwYMwMfHB41GQ2RkJImJiW/6csR/jEajAXLbXoUKFbhz5w47d+7U2ybEq9ANqezatYu+ffvSoEED/ve//9GuXTvCw8NJT0/XGyT+8ssvKVu2LCqVihEjRihLGkmlISFEQaa9j27ZsgW1Ws2IESNo164dAIUKFaJ8+fJEREQolQDHjh3Lli1blN9XrFgRX19fPvnkE1JSUmQwWbw2bVt0d3cH4MCBA1y+fJmgoKA8gZeMjAxMTEx48uQJUVFRnD59GjMzM+W+rf24RIhn0b7X5uTkkJyczIIFC7Czs2PRokXUrVsXS0tLPvvsM5YuXcrAgQOZMGEC0dHRTJgwATc3NyVMZW9vT0ZGBh4eHnrL02gn28aMGcPYsWMpXLiwBF6EnkqVKmFlZcX06dM5cuQIK1euZMiQIVy7di3PMll/h/SDQjfw0qhRI/bs2cMvv/yibN+xYwcDBw7ExsaGqVOn8tNPP7F9+3ZmzZqFlZUVO3bsYOTIkcTFxSnjitWrVycqKorGjRtz+/Zt/vjjD7y8vPj2228pWbIkOTk5EngRLyUxMZElS5bw6NEjwsPDlcDLpEmTCAgIwNLSkgULFmBjY8OmTZv46quvAJTgC8DQoUMZO3YssbGxeh8Ap6amEhMTg1qtlnuwEO8QVWJioswECCHEW+rEiRPKFxydO3dm+PDhpKam0qRJExISEggKCiI4OBhAqQADcPfuXa5cucKiRYtISUnBxMSEWrVq0a5dO5ydnfPtesTbSTfw0qRJE65evUrfvn0ZPXo0xsbGehO2W7ZsoUePHlSqVIn9+/djYGCgt117rEuXLtG2bVvMzMz47rvvsLe3z89LFP8RqampBAQEsHr1aj755BM2bNiQ36ckCrhVq1YpVQoqVaoEwNWrV0lJSaF+/fqMGjWKSpUqYWhoSEpKCt7e3uzcuZOmTZuyZs2a/Dx1IYT4xzx58oTatWuTmJjIoUOHcHV1VSZJdJdFGDNmDJMnT8bOzo4dO3ZQrlw55RiXL1/G3t5evu4VL+15odGzZ8/SsGFDMjMzKVGiBNevX8ff319Z0kh3aYbPP/+cHTt2MHXqVLp37y4TvOKVxMfHU6pUKUqWLEnv3r2VUNWLlsXStj+NRoO/vz9LliyhZ8+ejBs3Tm+J6fj4eAYMGMBPP/3Ejz/+KJNtIg/tPdXExITMzExcXFwYN26cUknydT1rOSMJ6f836QZemjZtyt27d/UCpA8ePKB79+7ExcWxcOFCJXCgdeLECUJCQjh69Cgff/wxs2bNwsnJSe85b//+/dja2uLq6oqtra0spyVeSXx8PE2aNKFx48bMnDkTgKioKIYPH46JiQnbtm2jWrVqbN26lf79+5OSkkKrVq1Yvnw5AGlpaZibmyvH096/tX3egwcPSEpKws3NLV+uTwjxz5PQixBCvOV0gy/Nmzfn0KFDJCUlERwcTFBQEPDsl1YhXoa27Tx48IDGjRtz9epV+vTpQ0REBMbGxnna1p07d2jUqBE3btxgypQpdO/ePU/wBeD+/fs0bNiQa9eusXv3bmrUqJEflyf+gy5fvkyLFi148OAB8+fPp2PHjvl9SqKA+u677+jcuTM2NjaMGzeOrl27kpmZyaNHj+jQoQPnzp3Dzc2NmJgYnJ2dUalUnDlzhtatW5OZmUlUVBStW7eWQWQhRIGXmprKRx99REJCAvv27aNUqVLPDD1nZGTQqVMnDh06xLJly2jRokWeZ0kJvIgX0W0fjx8/xsLCgvT0dAoVKqTX5ubPn6+8Czdu3Jjo6GhAf+J22LBhzJo1i0aNGjF//nxsbW3f/AWJAisqKoqQkBD69+/PwYMHGTNmDB9++OELAy9aGo2GwMBAFi5cSKVKldi4cSMODg567TM7O5u4uDhcXV1xdXV9E5ckCgjd+2a7du04cOAAarUaPz8/hg0bBrz+vVT32DNnzqR06dK0bNnynzt5UWDoBl6aNGnCvXv3GDJkiNLGAK5du0b9+vUpWbIk+/fvB9Cr0qJSqTh9+jTdunXj5s2beHt7ExkZqez39Di1PAMKrafHSDQaDRqNJk/7uHPnDnv27MHT05MKFSoQFxfHoEGDuHXrFuvXr6du3bpkZ2fz+PFj+vXrx+7du9FoNLRr145Fixa98BxkLkWId5PcZYQQ4i3n6enJ3r17UalUxMbGkpSURI8ePZRBvqysrGc+pGkfGHX/WwhduoEX3Qovo0aN0gu85OTkALkTHsWKFaNz584YGRmxevVqDh48iFqtRqVSoVarlX0tLS1RqVSUL19eEvPijXr//ffx8vLC2dmZ+vXr5/fpiAJIrVaTnJysDJKMHz+erl27AmBiYkJSUhLZ2dlA7kSbi4uL0geWKlWKRo0akZaWxo8//ghI2XAhRMGm0WiwsLCgaNGiPHr0iJUrV5KRkaHXt2nfRUxNTSlTpgw5OTmcOnVKb5uWTHaI59Gd7Ni6dSve3t60bNmSLl268O2335KQkKDs26xZM/r27QtAXFwcEydO5MaNG9y8eZOrV6/y1VdfMWvWLMqUKcP06dOxtbVVlqwR4mVo28ucOXM4c+YMly9fBnhh4OXWrVts2bKFJk2asHDhQsqVK8eaNWtwcHAgJydHr980MjLio48+ksCLyEN739y2bRvff/+9UjkoKipKWcL37wZeJk6cyPDhwwkLCyM5OVnGC/9jnq7wcu/ePUJCQggJCQFQxvUSEhJISkrCxMRE+Z2hoaGyRKBGo8HDw4NZs2ZhYGDA5s2buXDhApD3+Q/kGVD8SaVS8eTJE3bv3s29e/f07o9Lly6lT58+ABQrVox27dpRoUIFAA4fPsyvv/5KcHAwdevWRa1WY2RkRJEiRahQoQKGhoZYWVmxadMmhg4d+sJzkMCLEO8mudMIIUQB4Onpye7du5VyuBkZGVy5cgWNRqMsafS0p9cpl0k38TRDQ0MePnxI48aN+f333+nYsSNjxozB1NRUCVNpB0Z+/fVXevbsyZUrV+jSpQsffPABx48fZ/LkyWzZsoXs7GwMDAyUl4bIyEj++OMPPDw89Mo4C/EmjBgxgr179yoDzEK8CgMDA1JTUzl69Cj16tXjs88+U7YdPXqUnj17cvHiRYYMGcK4ceP0fmdtba18Lblu3TpSU1NlEFkIUSDo9lUPHz7kxo0bepO0n332GRYWFvzwww+cOHEiz+8zMzMBeO+99wAoVKjQGzhr8S7RtrW1a9fSvXt3vvvuO06fPs2hQ4f48ssv+eabbzhz5gwAJUqUoHfv3gwdOpQnT54wbtw4GjVqRMOGDalfvz4xMTFUq1aNLVu24OTkpPdluhAvo3///kyYMEH57zNnzij95LMCVNnZ2ezYsYMRI0Zw6tQp2rVrx5YtW3BxcZGvycVrSUxMpFatWixduhR/f39SU1Pp1asXsbGxr3yspwMv48aNw9bWljVr1mBlZSXjhf8huoGXZs2acffuXcqUKUNAQABGRkakp6djaGiIRqNR/j1+/DgnTpzIcx/VfvhRtWpVqlatSkJCAo8ePcqnKxMFiUajYc+ePfj7+9O/f39u3ryJgYEBS5cuxc/Pj/379yvPfBYWFkDuR787duwAoGLFikBuG8zIyACgcOHC1KxZk6VLl1KuXDn69++fD1cmhMhvL67HKIQQ4q1RvXp1duzYQcOGDVmzZg1qtZr+/ftTpUqV/D41UYDdunWLq1evKiGp+Ph4ypQpg7GxMVlZWRgbG3PlyhUaNWpEUlISrVq1olu3boSGhjJs2DAOHDhAfHw8u3btokuXLqhUKjZu3MjKlStxcnIiKChIeUER4k0pVaoU8OeXSEK8qkePHpGYmIidnZ3yt2PHjjFkyBDOnz+vV14c4Pr16+zevZuePXvSpk0b+vfvj4+PDxYWFhJ6EUK89XTLze/Zs4cFCxbw+PFjvL29adu2LQYGBnh5eVGlShWOHDnCrFmzsLS0pEKFCsoEiZmZGQD79u3D0NCQSpUqAXnLlwvxIhcuXGDMmDHY2toSFhZGnTp12L59O9HR0SxevJiEhAQGDhxItWrVcHNzIzg4mDp16rB48WLi4+N58uQJHh4e1K9fn86dO2NnZyeBA/HKtG3Gx8cHjUZDcHAwy5cvp1KlSnh7e2NgYJBnmQ4jIyPatGmDpaUl9vb21K5dGysrK2l/4pVp28wXX3yhVAPSVpKcM2cOvXv3ZuHChTRv3vyVjgd/Bl5sbGyIjY2lfPny/+aliLfM0xVe7t69i7W1tfIR3Nq1azEzM1OWcatcuTIdOnRgw4YNrFy5kmLFilG8eHG9Y6pUKmxtbbG3t0etVnP//v18ujpRkKhUKtzc3ChUqBB79+5l5MiRVKpUiZEjR1K8eHEiIyPzzHcYGxvj6OgIwN27d4Hc/k37oeXOnTu5d+8eH3/8MXFxcRgYGLzUkoRCiHeLKjExUUZhhRCiADlx4gSffPIJAF26dKFfv34SfBF/y4kTJ2jYsCEajYbOnTvTr18/KleujIGBAZcuXaJ58+YkJCQQEBBAaGio8rtjx46xYMEC9uzZw6NHj5SgDOQuMbNixQref//9/LosIYR4LRqNhosXL1K3bl08PDzYt28fx48f1wu8DB8+HECZ6N2+fTv9+/dnxowZtG3bVgkNyiCLEOJtpxtKWb16NYMHDyYrK4t27drh4+NDzZo1le1Hjhyhd+/e3Lx5Ey8vL7p27UqHDh2UypOhoaHMnTuX2rVrs2bNGmxtbfPrskQBtXfvXjp06MDs2bOVpQUBYmNjmTt3LocOHaJt27b4+vpSrVo1ZXtGRgY5OTmkpKRgb2+v/P3pYIIQul4UytNtOwsWLCAwMBCA6dOn8+WXX+bZR3ss3WNK6E+8jL9qJ5mZmcryMsOGDWPWrFmYm5u/VPDlWYEXa2trdu3aJYGX/5hnBV58fX2pXLky4eHh3Lt3j//9739s3rwZyL2vmpqaEhMTQ0hICBkZGQQGBtK+fXvlPqt9583KyuKTTz7hwYMHbNmyRan6J8SLZGVlcerUKYYPH86RI0cAcHR0ZN68ecpS5U/3j0uWLGHIkCE4Ojoyffp0mjRpQk5ODmFhYcybN48ePXowceJEDAwM5PlPiP8oCb0IIUQBJMEX8U/TbVOdO3dm+PDhpKam0qRJExISEggKCiI4OBj488UWctP1V65cYdGiRaSkpGBiYkKtWrVo164dzs7O+XY9QgjxV3QHULKzs1GpVHpf4nbu3Jm4uDj8/PyIiYnh7NmzeoEX7UCgRqPh448/5t69e2zevFnCfkKIAmnr1q10796dokWLEhERQZcuXZRtuv1lXFwcQ4cO5cKFCwCULVsWFxcX7t69y4ULFyhZsiSxsbE4OztL4EC80LMmehctWsTUqVM5d+4coD/Z+8MPPzB58mQl+PL1119TtWpVgDzVNCRsIP6Kbv906tQpLl26xNmzZzE1NaVRo0a4uLjg4uKi7L9w4UICAgKA5wdfhHhVuu3nzJkzXLx4kR9//JH33nsPBwcHvXux1ssGXyTwIp4WHx9PixYtuHXrFkOGDFEql0ZHRzNs2DDu37+vF3wBSEtLY8yYMcydO5eiRYvSrVs3unTpQrly5ZR9tKHnli1bEhUVhaWl5Ru/NlFwjRo1imnTpgG5Ve43b96MlZWV3tiz9rlOrVYTFBTEwoULAfDy8uLhw4dcuHCBMmXKsH37dpycnPLrUoQQbwEJvQghRAGlG1L4/PPP6dmzp97XbkK8Kt021bx5cw4dOkRSUhLBwcEEBQUBeQeUhRCiINIdYD527Bh79+7FwcGBli1b4uDgAMDs2bMJDw/H1NSUjIwM/P39CQ8PByA1NVVZumjIkCEsXbqU3r17ExERoSzxIYQQBcXVq1f5/PPP+eWXX1i0aBHt2rUDnl3FAODcuXOsW7eOnTt38uuvvwJQokQJqlSpwsSJE3FycpJnRvFCuu3p/PnzJCYmkpqaSlJSEvPnz2fTpk1YWFhgYGCgt+/333/PlClTnhl8EeJl6bap6OhoQkJCePTokbLd0tKSGjVqMHToULy8vJS/L1q0iKFDhwIwdepUevToAUjwRbwe3Xa4fv16hg8fzp07d/T2ady4Md7e3tSrVw9zc3Pl738VfNFtk5MmTWLs2LESePmPS09Px8XFhZycHL33WsgNtmzfvp2wsLBnBl+ePHnCqFGjiI6OJj09HXt7ezp37oyBgQHHjx9n//79uLq6EhsbS/HixSV4Kl6KRqPh999/p3HjxhgYGGBlZcXVq1dp0aIF48ePp0SJEs+8v967d4/58+czefJkAGXJ1SVLluDs7CzvIEL8x0noRQghCrATJ07QrFkzMjMz6dWrF2PHjlXWshTidegudQTQo0cPpk6dCuhXeNGl3VfKOAshCgLdPmrDhg0EBwfz8OFDmjVrRmhoKBUrVlTK03ft2pVdu3ZhZWXFtm3bcHd317vPhoSEEBUVRbVq1YiOjsbe3l76QCFEgXPkyBE+/fRTmjdvzqJFi4BnP8/p/i0zM5P09HTOnTtHWloa5cuXx8bGBktLSxlsFi9N+3V5UlISmZmZmJubk56ezo4dO6hTp46y3/OCL+3bt6dPnz7UqFEjvy5BFGAbNmzA29sbQ0NDAgIC8PDw4I8//iAuLo6tW7fi4OBAZGQkbdq0UX6jG3zRrfgixOtat24dffr0wczMDB8fH2xtbXn06BGrV6/m4cOHuLu74+PjQ6dOnfQqaGiDL1ZWVsoSq0/TVnixtbUlNjZWAi//cfv37yc2NpYJEyYA6C3F+1fBl9TUVJYvX05sbCw//vij8nczMzOqV6/OvHnzJHAgXsumTZuwsbHB2dmZAQMGcOLECZo3b86ECRNwcXF5brD05MmTPH78GCsrK9zc3LCxsZH2J4RAFpgXQogCzNPTk23bttG5c2d69eolgRfxt3l6erJ7925atGhBRkYGGRkZXLlyhbJlyz4z8ALkmRCRyV4hxNtM98vevn37YmFhwaRJk+jYsSPW1tbAn1WtVq1aRceOHdm3bx/t2rWjbt261KpViydPnrBnzx5+/vlnSpUqxfLly7G3t5dBFiFEgXTs2DHS09OVpSl1J0F06T7jmZiYYGJiQt26dfX20Wg00g+Kl7Jt2zb69u0L5FaZjI+P5+HDh6SlpTFhwgQmT56Mm5sbgBJGValUNGjQAAAjIyM2bNiAtbU1Hh4ez31XEeJZzp07pyxZuXDhQr3AQOnSpTl48CD37t3jypUrwJ+VM3r16gXA0KFDGTRoEGZmZnTq1OmNn794N5w6dYphw4ZhZmbGvHnzaN26tbKta9eujBgxgn379jF79mxsbGxo06YNGo0GIyMjIiIiMDQ0ZPr06YwePZqmTZvqVZy8dOkSO3fuxNramh07dkjgRVC/fn3q168P5L7v6j7rmZub07JlSwDCwsL44Ycf+PTTT5Xgi4WFBd7e3nTu3JkdO3aQkJBAcnIytWvXpnr16tja2sq7sHgp2vup9l9thUmAcePGERISQmxsLIBe8EX7jqH93dPV7tVqtbQ/IYSEXoQQoqCrWbMmFy5ckOUUxD+mevXq7Nixg4YNG7JmzRrUajX9+/enSpUq+X1qQgjxjzhy5AjBwcGYm5sze/bsPF9GGhoaKpO+GzZsICQkhD179rB9+3a2b98OgL29PW3btmXcuHGylIcQokDThllu374N8MzAi9bjx485d+4cNWvW/MtgjBC6tJMUGo0GtVrNsmXLKFy4MFOmTKFt27Y8evSIDRs2sGLFCvbv38/EiRMJDg6mVKlSQN7gS2ZmJjY2NgwePFgCL+KVXbp0idu3bxMUFKT3HHjs2DEiIiJISEjA399fqeqi+5V5r169SEtLY9SoUdSsWfNNn7p4h1y4cIF79+4xePBgJfCindx1d3dnwoQJjBkzho0bN7J48WIaNGhA4cKFyczMxMTEhJEjR2JpaUmnTp3yjAmWK1eOIUOGUKlSJaUfFQKeH1D+q+CLRqOhcOHCfP7553l+K4ED8SK6Ffuys7PJysoiLS0NS0tLvaXbatSowYQJEwgKCsoTfNEeZ8yYMdy9e5fZs2fr/X/IMoNCCJDQixBCvBMk8CL+adWrV2fv3r188sknREdHo1Kp6NevnwRfhBAFmnaw5ciRIyQmJjJs2DBlouPpsrlGRkZK8OWbb77h0qVLnDhxgsePH6PRaPjwww9xdXWlUKFCEngRQhRotWrVwsbGht9++4379+8/s3KVtj88e/Ys33zzDUOHDlW+FhbiZWjvsSdOnKB06dLcuHGDnj17KvfhwoUL88UXX+Dq6sr48eNZt24dKpWKoKCgZwZfmjRpwv/+9z9MTU3lPixe2eHDhwH0QivHjh3Dz8+P8+fP4+fnR3h4uLLt4cOHZGdn4+joCMDAgQPp0aMHhQoVem51LCGeR9uPff/99wAUKVIEQK8v02g0lCpViqCgIE6ePMmhQ4eYPXs24eHhmJiYKPsGBAQA+lXatO812gCDELpeFFB+UfDFyMjoucueS+BAwJ99T0ZGhlKNXnecZd++fcTExHD8+HGSk5MpX748tWrVwtfXFxMTEwwNDfH09NQLvqjVaqZMmYKTkxOjR49m2rRp2Nvb8+jRIwoXLpyflyuEeAvJE7kQQgghnsnT01MJvqxduxZAgi9CiAJH96silUpFZmYmu3btAlCW5XjeZJnuBEa5cuUoV67cM48vE21CiILM0dGR4sWLc/LkSSZOnEhkZKRe+XDdEviRkZEcPnxY+j3xWjZu3Ejv3r359NNPSUxMpGrVqsCfEyJmZmbK8kXjxo0jOjoa4LnBF+2EirRH8aq0E3Davi0uLo7AwEAl8KJd+igzMxO1Ws38+fMxMDBgwIABmJubY2hoiKWlpbLUjBCvQvtuUrp0aQCSk5MB/b5MpVKhVqt57733CA0NpXfv3pw9e1bp/57u93TboQQQxN/xouCLsbGxBE3FM2mf5eLj4wkICMDf35/atWsr/dGqVasYNGgQOTk52Nra8vjxY27cuMHu3bs5efIkAwcOpHr16hgbG+Pp6UlkZCQhISHs2rWL06dPU6xYMU6ePImzszOxsbEULlw4z4dLQgghPYIQQgghnksbfAFYu3YtCxYs4OTJk/l8VkII8XJ0Ay9aqampZGRkACj/vmjQLjk5mUePHj13uyzlIYR4m2g0mlf+TcmSJRk/fjwACxYsIDQ0VK//1PaRwcHBHDhwgCZNmuDh4fHPnbT4T9CGA2xsbIiNjeXBgwckJCQAueFTLWNjYxo0aEBoaChVqlQhOjqaCRMmEB8fr+wj917xurR9pLu7OwAHDhzg8uXLBAUF5Qm8ZGRkYGJiwpMnT4iKiuL06dOYmZkpfaJKpZK2KP4WbZhv6dKlnDhxIs927WRu8eLFgdzlkJKSklCr1W/sHMV/kzb4MnbsWOzt7fnhhx+UUKoEXsTTdAMvjRo1Ys+ePfzyyy/K9h07djBw4EBsbGyYOnUqP/30E9u3b2fWrFlYWVmxY8cORo4cSVxcnBKqql69OlFRUTRu3Jjbt2/zxx9/4OXlxbfffkvJkiXJycmRwIsQIg/pFYQQQgjxQtrgi4mJCStXrmTVqlXKRLEQQrytdCdsly9frqw9bmtri7u7OyqVit9//x3Qn2zTys7OBnIHaNasWaN8gSmEEG8zlUr1zD7tRTQaDfXr12fBggUAzJ07ly+++IKoqCiOHTvG3r176dq1K/PmzcPNzY1JkyZhZWUlk27ihZ4OYKlUKpo1a8acOXOUJbRWrFihLJWg256eDr5s2rSJ8PBwrl+//qYvQxRwz2qHAB988AEmJiZMnjyZDh06cO7cOfz9/fUCL9pKQoMHD+bx48c0btxYJnvFP6pdu3Y0a9aM+/fvM3fuXK5evaps02g0ZGVlAeDk5ISJiQkVK1bE1tZWJnrFG6ENvowfPx6VSsWpU6d48OBBfp+WeMvoBl6aNm3KgwcP8PPzo2fPngA8ePCAOXPmALkVI3v06IGDgwN16tShW7duxMTEULNmTX766SdmzJjBvXv3gNw+0M3NjejoaGJiYti0aRMrVqzA2dlZqg0JIZ5LnpCEEEII8Zc8PT3Ztm0btra29OrVSxkAFEKIt5V2UmPr1q0MGjSIHTt2sHv3bgDKly+PRqNh8uTJ3LhxA0NDQ71JYrVarZQInzBhAhs3bpSwnxDirTZu3DgaNWoEvPoXuNr+skOHDqxevZoiRYqwY8cOQkNDad26NR06dGDnzp14enoSExODk5OTfF0p/pK2Xd28eVP5m4mJCQ0bNmTChAmULFmS48eP4+/vT1pamrKUlpY2+BIeHk6xYsU4deoUhQoVeuPXIQoe3QBVcnIy2dnZPHnyBPgzBFO5cmUiIiIAuH79Oo0bNyY8PFzZR/u+O2zYMHbs2EGjRo1o27atVHYR/ygTExPat29PqVKliI2NZebMmZw7dw7I7UONjY0BmDRpEpmZmVSpUgW1Wv1aVd2EeB3m5uY0a9aM5cuX88svv1C0aFEJPQuFbuClSZMm3L17lyFDhigBUsittPvLL79QpUoV2rdvD+R+dKTRaNBoNMpSRs7Ozuzbt4+pU6cC6D0X1q9fHw8PD2xtbVGr1RJ4EUI8lyoxMVGekoQQQgjxUtLT0zEzM8vv0xBCiOfSDryo1WpSU1Pp1KkTFy5cYPr06bRu3RrIncxo3bo1Bw8e5IMPPmDp0qUUL15cGUDWVkrw8/NjxYoV+Pj4MHr0aAn8CSHeSlFRUYSEhGBlZcXWrVupWrXq3zre+fPnOXDgALt37yYjIwNHR0fq1atH27ZtsbOzk68rxUtbsmQJkZGRTJs2jSZNmih/z8zMZPfu3QQFBXHz5k169+5NREQEZmZmedpXZmYmhw8fxt3dHUdHR+U+L8Sz6Fb627p1K6tWrSIpKQkjIyN8fX2pUaMGdnZ2QG7YZc6cOURFRVGoUCG+/vprPvvsMwCysrIYPXo0MTExlClThu3bt+Pk5CTtT/zjsrKyiIqKYt68edy5c4fKlSszYMAA3N3dsba2ZuLEiaxcuRJ3d3e2bt2Kvb19fp+y+A+TZ0Ch9XSFl7t37xISEsKQIUMwMjJS2sqpU6f4+OOPqV69Ort3785zH9Xet3/44Qfat29PkSJF2Lp1K+XLl8/HqxNCFFQSehFCCCGEEEK8cy5fvoyjoyO1atWiR48eBAcHA7mTZyYmJpw/f54BAwZw+vRpypYty/Tp0ylbtixFihQhNTWV4cOHs2zZMipXrsyGDRtwcHDQm0gRQoi3wQ8//EC7du1wdHQkKiqK+vXr623/O/2WRqMhJydHqXwFyISveGmpqan4+fmxbt063N3diYiIoGHDhsp2bfAlMDCQW7duvTD4oiXtT7ystWvX0q9fPwDMzMxIT0/HxMSEL7/8ki+++IIqVaoA8Ntvv7F27VomTZoEQLFixdBoNKSmppKcnEy1atVYvnw5Li4uMtkr/nHaPi0zM5PVq1cTHR3NkSNHgNxqV4aGhqSnp1OuXDk2bNgg7VAI8VbQDbw0a9aMO3fuUKZMGY4fP45KpVI+mNRoNJw7d46PPvoIgL179+Lp6fnM4z1+/Jj27dtz6tQptm3bRt26dd/0ZQkh3gHypiiEEEIIIYR4p6xatYpatWoRHBxMZmYmXl5eQO5giomJCQAVKlRg0qRJ1KxZk19//ZUuXbrQsmVLmjVrhpeXF8uWLcPNzY3Vq1fj4OBATk6OBF6EEG+d06dPo9Fo6N27t17g5dq1awB/K/CiUqmUwIu2EpYEDsTLsrCwYPjw4fTs2ZOLFy8SHBzMnj17lO0mJiY0btyYyMhIihcvzsKFCxk2bBjp6el5lh3UkvYnXsaFCxcYM2YMtra2TJw4kT179hAcHIyzszOLFy9m+vTpnDx5EgA3NzeCg4PZuHEjLVq0wM7ODjMzM+rUqcPYsWNZv369BA3Ev0ZbndLExIQvvviCuXPnEhoaSs2aNXFwcMDLy4shQ4awbds2aYdCiLfC0xVe7ty5g7W1Nb///jsdO3YkOzsbMzMzsrOzUalUVK5cmQ4dOgCwcuVKbt26leeYKpUKW1tb7O3tUavV3L9//01flhDiHWH017sIIYQQQgghRMGQnZ1NUlISALGxsaSmpvLo0SNA/wtxlUpFjRo12LRpE2FhYZw8eZIzZ84AUL58ebp3705ISAiOjo4ywCyEeOtlZWUp/3vJkiWsXLmS0NBQPvnkk9c63tNhGQn9idfh7OyMv78/OTk5LFu2jODgYL755hul4ouxsTGNGzcGIDAwkIULF2JoaMiIESMwNzfPz1MXBditW7e4efMms2fPpmvXrgBUrFiRypUrM3fuXDZv3oxGo8HX15dq1aphaGjIxx9/TL169cjJySElJUVvCRm1Wi3PgeIvacOir1phzcDAAI1Gg6GhIaVKlSIgIICvv/6ajIwMrK2tlfcXeR8RQuS3Zy1p5OvrS+XKlQkPD2fv3r107NiRzZs3Y2RkREZGBqamprRo0YKDBw8SExPD+++/T/v27ZX7bFZWFsbGxmRlZXHr1i2cnJyoUKFCPl+pEKKgktCLEEIIIYQQosB6emDZyMiIL7/8EjMzM4YNG0Z2djYbN26kVatWGBkZ6QVf1Go1lpaWTJs2jcTERG7cuIFarcbNzQ1jY2NMTExkgFkI8VarVKkSVlZWTJ8+nf/973/8+uuvDBkyhKJFi2JpaZnfpyf+A55ecujp+3Lx4sUJDAxEpVKxdOlSgoODGT9+PI0aNQL+DL6oVCpCQkKYN28ehQoVIjw8/I1fiyh4nhUwiI+Px9nZWQm8aJe2bN68ORYWFgDExMQA8PXXX1O1alUg9xnS1NRU2Ud7bKkwJP6KbjtMTEykcOHCr/QOof2t9jja9xDdbfI+IoTIb9rAS4sWLbh79y5Dhgxh2LBhQO7z4LBhw/jhhx/49NNP2bx5M6ampgA0adKEY8eOMXfuXKZMmcLdu3fp0qUL5cqVw9jYGIARI0Zw9uxZWrZsSfHixfPtGoUQBZsqMTFRk98nIYQQQgghhBCv6ukBZltbW2VbcnIyGzZsYNiwYaSkpBAcHExQUBCgP0H3ql9jCiHE22bMmDFMnjwZExMTMjMzcXFxYdy4cbRq1epvHfdZE3bSZ4rnOXr0KK6urjg6Oj6zndy6dYuJEyeydOlS3NzcGDdunFLlBXK/9N2+fTszZ85k6dKllCxZ8k1fgihgdNvZ+fPnSUxMJDU1laSkJObPn8+mTZuwsLBQKmlo9/3++++ZMmUKhw4dom3btnrBFyH+jsWLF+Pv78/evXvx9PTM79MRQoh/VHp6urLUmr+/v15AOS0tje3btxMWFsb9+/f53//+x+bNm5XtT548YdSoUURHR5Oeno69vT2dO3fGwMCA48ePs3//flxdXYmNjaV48eLyziGEeC0SehFCCCGEEEIUaIsXL2bp0qXMmjWLKlWqKH9/8uQJ69evJywsDI1GQ1BQEIMHDwbyfpkuhBAFjW4opV27dhw4cAC1Wo2fn5/eV5ev09fpHnvmzJmULl2ali1b/nMnL94pW7ZsoUePHnz11VeEhIRgb2//zMmK69evM3bsWKKjoylXrhwjR46kadOmyvasrCxycnIwMzMjOzsbIyMpUC3+WnR0NMOGDSMpKYnMzEzMzc1JT09nx44d1KlTR9nvecGX9u3b06dPH2rUqJFflyDeAXv37qV79+6kpKQwadIkevXqld+nJIQQ/7j9+/cTGxvLhAkTAPSe1/4q+JKamsry5cuJjY3lxx9/VP5uZmZG9erVmTdvHs7OzlJtVwjx2uTtUQghhBBCCFFgJSYmsnHjRs6ePUtYWBjjx4+nUqVKABQqVIhOnTqhVqsJDw9XBmYGDx6MgYGBBF+EEAWadjB427ZtfP/991hYWJCamkpUVBQ1atSgWbNmfzvwMnHiRMaNG0fJkiWpX78+hQoVkq8uhZ6cnBwyMjJwcXEhOjoaIyMjhg4dioODQ57gS4kSJfjyyy85dOgQv/32G6NHj8bQ0FBvqSNtmXsJvIiXsW3bNvr27QtA8+bNiY+P5+HDh6SlpTFhwgQmT56Mm5sbkLtMjLZNNmjQAMhtZxs2bMDa2hoPDw+l/QnxV55+j9iyZQuZmZmsWLHib4dEde/DMvkrhHib1K9fn/r16wO5/ZPu85q5ubnS/4WFhektdQRgYWGBt7c3nTt3ZseOHSQkJJCcnEzt2rWpXr06tra20ucJIf4WqfQihBBCCCGEKNAuXLjAqFGj+Pbbb6lduzYTJ05Ugi8AKSkprF27Vim/q1vxRQZVhBAF3YoVK1i1ahX+/v789NNPTJ48GXNzcxYuXEjz5s1f6VjPCrzY2tqyY8cOKlSo8G+cvngHpKamsnv3biIiIrh+/Trdu3d/bvAF4NNPP+WHH34AwNbWlmXLlvHRRx/lw5mLgkYbNNBoNKjVajp37syJEyeYMmUKbdu25dGjR2zYsIEVK1Zw9uxZOnfuTHBwMKVKlVKOodsmv/32W9asWUNERAQlSpTIp6sSBdnOnTupUKECQUFB2NraEhUVBbz+coC69+Hly5dja2tL48aNMTMz+0fPWwgh/o4X9XEvqvjyokp+8lGSEOLvktCLEEIIIYQQosC7ePEiw4cPZ/fu3S8VfAkNDcXX1ze/TlcIIf423YmxP/74A1dXVyD3y8o5c+a8cvDlWYEXGxsbdu7cSfny5f+dixAFiu4Ex5MnTyhUqJCyLS0tjV27djF27NjnBl/S09MxMzPD39+fpKQkjI2N+fbbb4mLi6NYsWL5dVmiAPr5558pXbo0zZs3p2XLlsrzHUB6ejoHDhxg/PjxnD59ms6dOxMUFPTc4EtGRgampqYShBav7Ntvv6VLly64u7uTnJxMly5dCA8P/0eWFtTeh+vUqUN0dDRWVlb/9OkLIcS/5kXBl6ysLKmsJoT4V0hsTgghhBBCCPHW02j0s/pqtVrvv93d3Rk9ejSNGjXiyJEjBAQEcO7cOWW7paUlXbp0YcyYMRgbGzN8+HAWLlz4Rs5dCCH+CU/3g7qTs66urmRmZgIwduxYBg4cSFpaGr179yY2NvYvj/2siTZra2sJvAiFWq1WQgJxcXEEBwczatQoZbu5uTlNmzYlLCyMEiVKsGzZMiZPnszdu3f1Ai8AP/74IwCjR4/mxIkTFCtWjJycnDd/UaJA2rhxIw0bNmTo0KEkJiZStWpV4M9nQzMzMxo0aEBISAhVqlQhOjqaCRMmEB8frxxDu9QRgKmpKYAEXsQrK1++PB4eHly8eJHbt2+TlJQE5H1PeRnPC55GRkZK4EUIUeBolzoaO3Ys9vb2ylJHkLucpTz3CSH+DRJ6EUIIIYQQQrz1tBNtZ8+eJSMjAwMDg5cKvpw9e1bZrg2+BAQEUKpUKZo2bfpGr0EIIV6XbuDgzJkzrFu3Dl9fX2bMmMHatWsBMDExUfaPiIh46eDL8wIvu3btksCLAHIDV9qqBRs3buTLL79k1apVHDx4kFOnTin7PR18WbJkCcOGDeP27dtK4CUkJIQrV65Qp04d7O3tsbW1RaPRSOBAvBSNRoORkRE2NjbExsby4MEDEhISAPQm0IyNjWnQoAGhoaEvDL4I8XeULFmSlStXUrt2bdRqNZs2beLXX3/FyMjolSZ0X1RpTbdypRBCFCTPCr40aNAAkKCpEOLfIcsbCSGEEEIIIQqE6OhoBg4cSEBAAIMGDcLU1PSZ5cPPnz9PaGgoBw4coHbt2kyYMIEqVaoo21NTU1Gr1RQqVEhK2Qsh3nq6y3CsX7+e4cOHc+fOHb19GjdujLe3N/Xq1cPc3Fz5+7Bhw5g1a9ZzlzrS7UMnTZrE2LFjJfAinmvlypX4+vpiZmbGqFGj8PHx0WufWmlpaXz33XdMmDCBCxcu4OzsTM2aNbl+/TrHjx+nXLlybN26FQcHh3y6ElFQPKt9ZWZmsmfPHoKCgrhx4wY1atQgNjYWY2PjPM+FWVlZfP/994wbN44LFy7QqFEjxo8fT4kSJd70pYh3kPY94saNG/Tt25dDhw5RoUIF1q1bh7Oz80u9Z0jwVAjxrktLSyM2NhZvb280Gg1XrlyhaNGi+X1aQoh3kIRehBBCCCGEEG+9zMxM5s2bxzfffEOhQoXo06cPAwYMeGbwJScnh507dzJo0CBSUlLw9PQkMjIyz5eSz5pIEUKIt9W6devo06cPZmZm+Pj4YGtry6NHj1i9ejUPHz7E3d0dHx8fOnXqhKWlpfI7bfDFysqKGTNm0LZt2zzH1k602draEhsbKxNtIo+9e/fSsWNHrK2tmT59Om3atAEgOzsbIyOjPPunpaVx5swZJk6cyN69e4Hcr3orVqzI6tWrX3pCWAiAmzdv4uzsrPy3NvgSEhLCtWvX+OKLL5gwYQLm5uZ52lVWVhb79+/H39+fnJwcfvzxRwoXLpwflyEKoKffFzIzMzEyMsoTur9x4wY+Pj4cPnyYDz74gCVLlvxlPyeBFyHEf0Vqair79u2jevXqODk5PfPjJSGE+Lsk9CKEEEIIIYQoEBISEti4cSPffPMNGo2GgQMHPjf4kp2djZeXF5cuXQJylz5aunQp5cqVy6/TF0KI13bq1Ck6d+7M48ePmTdvHq1bt1a2Xbx4kREjRrBv3z5cXV0JDQ2lTZs2yjIgACNHjmT69OmULl2auLg4ZakZgEuXLtGvXz9+++03du7cSYUKFd749Ym3l0ajQa1W069fP9avX8+MGTP44osv9PbJyMjgxIkT3L9/H09PT4oUKYKFhYWyfffu3SQlJVG4cGE8PT0pXLiwBF7ES1uyZAmRkZFMmzaNJk2aKH/PzMxk9+7dBAUFcfPmTXr37k1ERARmZmZ52ldmZiaHDx/G3d0dR0dHmWwTL0U38LJ//36+//579u/fj5mZGVWqVKF169Z4enoqFdZu3LiBt7c3R44coUaNGixduvS5wRfdNiiBFyHEf4k8Awoh/i0SehFCCCGEEEK8tZ7+uvLRo0esW7eOyMjI5wZfMjIyMDU15auvvqJQoUJcvXqVs2fPcuzYMVlKQQhRIK1Zs4b+/fszePBgRowYAeROmGk0GgwNDYmPj2fMmDFs3LiRevXqsWLFCgoXLkxmZiYmJiZA7qRap06dcHV1zXP87du3U6lSJUqVKvUmL0sUECkpKdSuXZvMzEzi4uKws7MD4MGDB5w5c4YxY8Zw7tw5srKyKF++PG3btqVv375YW1s/83gSOBAvKzU1FT8/P9atW4e7uzsRERE0bNhQ2a4NvgQGBnLr1q0XBl+0pP2Jl6H7DrJq1Sr8/PzIysrC2tqa7OxsUlNTKV68OJ06dWLw4MHY2NgArxZ8ARg1ahTTp0/H2tqanTt3SuBFCCGEEOI1yRO+EEIIIYQQ4q2h0ehn8p9efqhw4cJ07NiRoKAgVCoVM2fOZPbs2aSnp2NgYEBaWhqmpqYAHD16FDMzM2bOnMnPP/+Mg4MDarX6jV2LEEL8Xdo+8fvvvwegSJEiQO4XkgYGBhgaGqLRaChVqhRBQUGUKVOGQ4cOMXv2bABMTEzIyckBICAgAFdXV7Kzs5Xja/vEli1bSuBFPJelpSUuLi6kpqZy5swZILf60PDhw+nRowcnT56katWqVK1alRs3brB06VIOHz4M8Mz7rgQOxMuysLBg+PDh9OzZk4sXLxIcHMyePXuU7SYmJjRu3JjIyEiKFy/OwoULGTZsGOnp6RgaGir9ny5pf+JlaN9BtmzZwsCBAzE3N2fy5MkcOHCA2NhYJkyYgFqtZt68efTv35/09HQ0Gg0uLi4sWLCA2rVrc/z4cXr37s21a9eeGXhJSEggNjYWjUYjgRchhBBCiL9JnvKFEEIIIYQQbwW1Wq0MMF+6dIndu3cTERFBdHQ0+/fvV/YrUqQI7du3JygoCAMDA2bMmMG4cePIyclRyosHBwdz69Yt6tatS+nSpSlatKh82SuEKHC0fWLp0qUBSE5OBtCbPFOpVKjVat577z1CQ0MBOHv2rBKYeXqiTbvkEcjkr/hrarUatVpN06ZNycrKwtfXlyZNmtCoUSPWrFlD7dq1WbJkCd999x2bN2+mdevW3L59m4MHDwLSxsTf5+zsjL+/Pz169OC3334jODiY3bt3K9uNjY1p3LgxEydOxNnZmYULFzJixAjS0tJk+QTxt9y4cYPJkycDMHnyZHr27ImrqyseHh6UK1cOExMT0tLSqFKlCmZmZso9Wxt88fLy4siRIwQGBj4zAFikSBFWrlzJzz//LIEXIYQQQoi/yeivdxFCCCGEEEKIf5dGo1EmxjZu3MiYMWO4fv263he6Pj4+dO7cmWrVqmFnZ0e7du1QqVRMnjyZmTNnEhcXR7Vq1bhw4QKHDh2iQoUKfPjhh8rvZeJNCFFQaauwLF26lKZNm+Lp6am3Xdu/FS9eHIALFy6QlJSEtbW19H3ipTy9nKCWtv1069aNlJQUtm7dytGjR3F3d6dz584MHDhQCRbY2tpSr149Vq1apReuEuKvPB1Mfro9Fi9enICAACC3HwwJCQGgUaNGQG7wpVGjRkRGRhISEsL8+fOxsrIiPDz8DV6FeNfcunWL8+fP06NHDzp06KD8/dixY4SHh3Pt2jX8/PwICgrK81sXFxdmzZpFeHg4ERERz70Xv/fee//a+QshhBBC/JfIG6gQQgghhBAi32knNtauXUu/fv0wNDTkiy++wNDQkKSkJDZs2MD8+fO5cOEC3t7etGzZkqJFi9KxY0eKFy9OREQEP//8Mz///DMA5cuXJzo6Wiq8CCHeCe3atWPbtm3s3LmTuXPnEhoaqlR/0Wg0ZGdnY2xsjJOTEyYmJlSsWBFbW9v8PWlRYOgGDE6cOEF8fDwpKSm4uLjQoEEDAIoWLYq/vz+DBg3ixo0bFClSBHt7ewCys7OVkMumTZswNDTEy8srz7GFeB7tc9rRo0dxdXXF0dHxpYIvGo2Gxo0bA38GXzIyMpg5cyZffvnlm78Q8U7Qtr2TJ0+iVqspUaKEsu3YsWP4+flx/vx5/Pz8GD58uLLtzp07PHr0iHLlymFgYICrqyvLli3DwMBAr58UQgghhBD/PHnSEkIIIYQQQrwVjh49SlBQEFZWVsycOZM2bdoo29q3b8/48eP58ccfyczMxNramvr162Nra0uLFi346KOP2L59O0lJSTg6OvLRRx9hZ2dHTk6OlLYXQhR4JiYmtG/fngsXLhAbG4uVlRU9e/akUqVKqFQqjI2NAZg0aRKZmZlUqVJFWTJOAgfir+gGT4cMGUJaWpqyrUuXLowcORIHBwdMTU0xNTWlXLlyyvJZWVlZGBsbo9FoCA8PZ8+ePXz88cfUqFFD79hC/JUtW7bQo0cPvvrqK0JCQrC3t39m8EXbRqOjoxk+fLiy/BbkBl9atmxJs2bNMDMzk6CBeC3aNufk5AT8uUzgkSNHGDp0aJ7AS0ZGBqampixdupTjx48zY8YMpfKaNtAl7VAIIYQQ4t8lT1tCCCGEEEKIf93Tkxa61Ve0244dO8bjx48JDw9XAi/a/Zo2bYqdnR2jR4/m4MGDrF69mnr16mFkZERWVhZWVlZ89tlnev+farVaAi9CiHeCSqWidevW3Lp1i3nz5rF8+XJOnjzJgAEDcHd3x9ramokTJ7Jq1Src3d3p3bu3VLgSr2Tbtm3069cPgE8//RSAb7/9lrVr13Lv3j1GjRpFxYoVlXu59l8DAwMeP37MkCFD2LhxI6VKlWLWrFnY2NhIpTXx0nJycsjIyMDFxYXo6GiMjIwYOnQoDg4OeZ4hS5QowZdffsmhQ4f47bffGD16NIaGhnpLHWmDgBI0EH9H0aJFAVixYgXFihVjzpw5zw28ZGRksHnzZrKzszE1Nc3P0xZCCCGE+E+SJ38hhBBCCCHEv0o76ZWens5vv/2Gvb09Dg4OeSbD9u7dC0CpUqX0fqed7Pjggw8YMmQIJ0+eZN26ddSvX5+uXbsqExtPk4k2IcS7Qq1WY2xsTJ8+fbCysiI6OpojR47g7e2NsbExhoaGpKenU65cOdavX4+9vb1UuhIvpHsPzsnJITo6Gmtra2bMmKEET8+dO8fgwYPZt28fmZmZjBs3TqkuBHD9+nWWL19OdHQ0169fp2bNmixevBgnJydpf+KVGBoa0rJlS0xNTYmIiGDZsmUAzw2+1K1bl7Jly3Ljxg0uXLiAj48Py5Yt46OPPsqvSxAF0POWX9P2j3Xr1qVDhw5s2LCBoKAgkpKSCAwMJCQkBIC0tDTMzc3RaDT4+vpy+fJlgoKCsLGxedOXIoQQQgjxnyejwEIIIYQQQoh/jXbQ+P79+0RGRtK1a1caNGjAzZs3lck27WBzyZIlAUhNTdU7hkqlUpZRaNCgAUOGDAHg0KFDAMo2IYR4VxkYGKBWqzExMeGLL75g7ty5hIaGUrNmTRwcHPDy8mLIkCFs27YNFxcXCRyIv6S9B1+8eJEnT55w+PBhunfvrgResrKyqFSpEnPnzqV+/focPHiQ0NBQzp07pxzDyMiIS5cuYW9vj5+fH6tXr8bZ2Vnan3gh3ee2J0+eKP/bwsKCxo0bExYWRokSJVi2bBmTJk3i3r17es+C6enpAJQpU4b27dvTpUsXVCoV77///pu9EFGgaZcABEhJSeHevXvcvn0bjUajF5zv2bMnnp6eJCUlUb58eby9vZVt5ubmAAwfPpz169dTp04dvL29pcKQEEIIIUQ+kCcwIYQQQgghxL9CG3i5fv06Pj4+HDlyhHLlylG3bt08wRYAR0dHABYuXMgnn3xC8eLFlS8wVSqVcryyZcsCcOXKFXJycqSiixCiQNH2a8/7wvx5tJWvDA0NKVWqFAEBAXz99ddkZGRgbW2t9JESOBAva/ny5QwaNIghQ4ZQpkwZPvzwQyA38GJsbIxGo+G9995j4sSJBAQEsH//fkJDQxk3bhwVKlTAycmJqVOn8uTJE5ycnDAxMZGlBcUL6VYYiouLY/Xq1djb2zNixAggN0TQtGlTAMaOHcuyZctQqVQMGTIER0dH0tPTMTMzA+DHH3+kSpUqjB49mvHjx2Nrayv9n3imw4cPU7NmTaVt6LbDrVu3snz5ck6cOIGhoSFubm40bdqUVq1a4ebmhoeHBz169CA9PZ1ffvmFDh068PXXX+Pk5ERaWhpz585lz549lCxZkgULFmBnZydLuwkhhBBC5AN5+hJCCCGEEEL847SDvdeuXaN58+YcOXKE9u3b8+233zJp0iTee+895Ytd7b+9evWiSpUqnD9/nrlz5/Lo0SO9L3tzcnIAKFGiBJC7DJKhoeErTRoLIUR+0g26JCYmAn/2bS9D+1ttv2hsbIyVlZXeNpnwFS9LWzFj6tSpHD9+nDNnzgAoywZq78Ha4Iu24ktYWBi//PILOTk52NnZ4erqiomJSZ4KCULo0m0fGzdu5Msvv2TVqlUcPHiQU6dOKftpgy/aii9Llixh2LBh3L59Wwm8hISEcOXKFerUqYO9vT22trZKKFAIXVFRUTRv3pxRo0ahVquBPytdrVmzhu7du7N3716lbf3000+MHj2azz//nOPHj2NhYUG7du0IDg7mk08+4fTp0/Tq1YvmzZvTvn179u3bx0cffURsbKxS6Ur6QSGEEEKIN08qvQghhBBCCCH+cdoljb788ktu3LjBwIEDiYiIAFAGnLUTtNp/bW1t6dy5MxMnTmTdunUUKlSIHj164OjoiFqtVibh5s6dC0CVKlWU48ngshCiIND2d4sXL8bf35+9e/fi6en52sfR7fskAChelY+PD8bGxoSGhpKens7Zs2dJSEigSJEiyj5PB1+0FV/69+/PggULcHd319tXiOfRto+VK1fi6+uLmZkZEyZMwMfHJ89Sldrgi4GBARMmTGD9+vXExcVRs2ZNrl+/zvHjxylXrhytWrXKc3whdNnb22NkZMTMmTMxNDRk2LBhGBgYcPbsWcLCwrC3t2f06NE0bNiQlJQUtm3bxs6dO4mLi6N169Zs3ryZWrVq0axZMxo2bMiaNWu4dOkSd+/exdnZmfr161OzZk2pNCSEEEIIkc9UiYmJmr/eTQghhBBCCCFejraSwaRJkxg7dizNmzdn1apVAH85GPzw4UOmTJnC0qVLUalUfPjhh/j7++Po6IiVlRUREREsXryYihUrsmXLFuzs7N7UZQkhxD9i7969dO/enZSUFCZNmkSvXr3y+5TEf5Du/XjRokUEBgaiVqsZNmwYQ4YMybO/9t7+66+/0rt3b+Lj4zl27Bj29vZv+tRFAbZ37146duyItbU106dPp02bNgBkZ2djZJT328y0tDTOnDnDxIkT2bt3L5BbzapixYqsXr1aqawhQQPxItu3b6dPnz6kpqYyaNAgRo4cSUxMDF999RXz58+nY8eOyr6ZmZnEx8czbtw4tmzZgpOTE+vXr6dixYp6x3x6iUIJ4QshhBBC5C8JvQghhBBCCCH+FW3btuXgwYNs2bKFevXqKZMS2kHi9PR00tPT2bp1K8nJyZQsWZLKlStTvHhxpk2bxpo1a4iPj0elUmFtbY2BgQGPHj2ibNmybN68GRcXFxlgFkK89Z7up77++mvWrl3L4sWLadmy5d86tu5kr0z8imd5emJWl27QYMmSJUrYZcyYMQwYMOC5x7p69SqFChXC3t5e7sPipWg0GtRqNf369WP9+vXMmDGDL774Qm+fjIwMTpw4wf379/H09KRIkSJYWFgo23fv3k1SUhKFCxfG09OTwoULS78nXki3/9u2bRt9+/YlNTUVf39/HBwcmDlzJidOnMDY2DhPX3b79m18fX3Zu3cvn332GZGRkVhYWCj7aI/9oj5WCCGEEEK8ORJ6EUIIIYQQQvzjHj9+zEcffcSjR4/YtWsX5cuXJycnB5VKhYGBAX/88QcrV65k7969nDx5Esj9crdUqVKMGDGCVq1acerUKebMmcPp06e5du0aVatWpXLlykrlF5noEEIUJDt37qRChQoEBQVha2tLVFQU8OJQwovo9oHLly/H1taWxo0bY2Zm9o+etyi4dCdxL1++zN27d7lw4QJmZmZ8/PHHWFlZYWNjo+y/dOlS/Pz8AIiIiGDgwIF5jqnbXiXwIl5FSkoKtWvXJjMzk7i4OKVa34MHDzhz5gxjxozh3LlzZGVlUb58edq2bUvfvn2xtrZ+5vGk/YmX8bzgS5kyZUhNTeXEiROYm5s/83d79uzB29sbOzs7vv32W4oWLfqmT18IIYQQQrykvHUjhRBCCCGEEOJvMjAwwMDAgMePH7N8+XLGjx+vVHk5duwYgwYN4vLly+Tk5FCoUCFcXFy4c+cOv/32G3369EGtVtOmTRvmz59PYmIiSUlJuLq6kpWVhbGxsQRehBAFyrfffkvXrl1xd3cnOTmZLl26AK8/aavbB06cOJFx48ZRp04dGjRoIKEXAeRO2Grb1qZNmxgzZgy3b98mPT0dAFdXV+rXr0/Pnj3x8PAAoEePHqhUKgYPHsywYcPQaDT4+vrqHVc3oCWBA/EqLC0tcXFx4dy5c5w5c4YGDRpw6tQp5s+fz/bt20lOTuaDDz4gKyuL3377jaVLl+Lh4UGTJk2e2VdK+xMvQ7caS6tWrdBoNAwcOJDff/8dQ0NDtm3bRvv27fO8V2iXWS1RogTnzp3jyJEjf7s6mxBCCCGE+PfI24EQQgghhBDiH1eoUCF8fX0xNzdn4cKF+Pr6smjRIoYOHUrr1q25cOEC77//Pn369GHv3r3s27eP+fPn06ZNG9LS0li1ahX37t0DwNbWlhIlSgAoyzBI4EUIUZCUL18eDw8PLl68yO3bt0lKSgJyQy+v6lmBFxsbGyIjI7GysvpHz1sUXNpwytq1a+nVqxdXr16lZcuW9OzZkypVqvDo0SOWL1+Oj48PcXFxyu+6d+/OtGnTABg+fDhz5szJj9MX7xi1Wo1araZp06ZkZWXh6+tLkyZNaNSoEWvWrKF27dosWbKE7777js2bN9O6dWtu377NwYMHAQm4iL9HG3wBaN26NTNmzMDa2pqcnBx2796tvHPoysjIwMzMjPLlywO5y8EJIYQQQoi3l1R6EUIIIYQQQvwr2rRpw4kTJ9i0aRMrV65k5cqVyrZmzZoxaNAgKlSooEzSNmrUCLVazb59+/jpp59ISUlR9tdOdrzOEiBCCJHfSpYsycqVK/H29ubIkSNs2rSJPn36ULZs2VeqXPW8wMvOnTuViTkhtI4ePUpgYCAWFhbMmTOHNm3aAJCVlUVsbCyLFy/mwIED9OvXj0WLFlGjRg0gN/gCMHToUMLCwrCwsKBHjx75dRmiAHnecm3a57hu3bqRkpLC1q1bOXr0KO7u7nTu3JmBAwcqfZutrS316tVj1apVSthZiFfxrHaoUqnIzs7GyMiItm3bolKpGDBgABs2bMDBwYGgoCBlKa309HSlatrVq1extLTE1dX1jV+HEEIIIYR4efLmIIQQQgghhPhXFClShOHDh1OxYkUWLlxIZmYmtWvXpmrVqvTv319vX+3gdNWqVbGxseHGjRs8fPiQ0qVL59PZCyHEPycnJwcXFxcWLFhA3759OXToEN27d2fdunU4Ozu/VPDlWYEXa2trCbyIPLRLwRw9epTk5GTCw8P1Ai/Gxsa0bNmSsmXLMnr0aL777jsmTpzI5MmTcXFxAXKDL2lpacyYMYOPP/44Py9HFBC6QYMTJ04QHx9PSkoKLi4uNGjQAICiRYvi7+/PoEGDuHHjBkWKFMHe3h5ACSRA7pJchoaGeHl55Tm2EC+iuxTW7du3efLkCZaWltjZ2WFqaqq0szZt2qBSqejXrx9z5szh8ePHfPHFF9SsWVMJvISGhnL8+HE++OADypQpk5+XJYQQQggh/oIqMTFRk98nIYQQQgghhHi3JSYmkpWVRdGiRZVJC90JXO3/vnz5Mk2bNsXNzY2YmBgsLS3z87SFEOKlPT0pm5mZiZGRUZ5lOW7cuIGPjw+HDx/mgw8+YMmSJX8ZfHle4GXXrl0SePkPS0tLIyEhgR07dvDee+9Rs2ZNvftm9+7d2bp1K+vXr6dhw4Z6oQLIbbPff/89YWFh3Lt3j3nz5uXZLyUlBUtLyzy/FeJ51q5dy5AhQ0hLS1P+1qVLF0aOHImDg4NeP6ntN7VhLI1GQ3h4OHPmzOHjjz9m8eLF2NjY5MdliAJI9z68bt06IiMj+eOPP3B0dKRs2bJMnjwZNzc3vd9s3bqV/v37k5KSQqlSpShevDgVKlTgxx9/5NKlS5QtW5aYmBicnZ31AjVCCCGEEOLtIk9pQgghhBBCiH+dra0t9vb2ykC0RqPJE3hRq9WMGjWKR48e4eXlhampaX6eshBCvDTdibb9+/czcuRImjRpQosWLQgKCuLQoUPKBLCLiwvz58+ndu3aHDt2jB49enDz5k0MDQ3JycnJc2y1Wi2BF5HHnTt3GD58OK1atSIoKIiBAwdy8OBBUlNTlX207eb8+fMAeSZrVSoVdevWxcPDg4SEBFatWgWAkZERarUaQAnRSOBFvIxt27bRr18/0tLS+PTTT/n000+xsLBg7dq19O/fn/Pnz6PR/Pn9pbbfNDAw4PHjx3h7ezNnzhxKlSrFrFmzsLGxUdqiEH9F2542b95Mnz59+O233yhZsiQajYb9+/fTpk0bYmNjyczMVH7TunVr5syZg5WVFfHx8cTFxXHnzh2cnZ0JDAxk+/btSjBVAi9CCCGEEG8veVITQgghhBBCvHHaQWntZK72y97Y2FiqVavGgAEDZIJNCFEg6AZeVq1aRceOHZk+fTq///47Z86cYf78+fj4+BAZGUlSUhKAstRR7dq1OX78+AuDL9pJtlGjRjF+/HhsbGwk8PIf98cff/Dpp5+ycOFCzMzMCA4O5ptvvsHT0xMLCwslVFC9enUAzpw5A+S2Jd0AgUajwczMjM6dO2NiYkJKSoqyTSZ3xcvQbU85OTlER0djbW3N0qVLWbx4MYsXL+bbb7+levXq7Nu3j5CQEM6dO6cXfLl+/TrffPMNXl5ebNy4kZo1a7J9+3acnJwkaCBe2aNHj5g1axYODg4sWbKEAwcOsHv3btq0acPNmzfx8/N7ZvBlxowZSlWhokWLsm7dOkJCQnB0dHypJQiFEEIIIUT+krcGIYQQQgghxBunnezQaDQkJCTQvXt35s6dS8mSJVmxYgVFixZ9ZsUDIYR422gDL1u2bGHgwIGYm5szefJkDhw4QGxsLBMmTECtVjNv3jz69+9Peno6Go0mT/Cld+/eXLt27ZkTawkJCcTGxqLRaNi5c6cEXv7Dbt68Sdu2bbl48SJffPEF+/btIygoiFatWmFvbw/82SZr166NoaEhmzZtIjIyEsgNs2jvr9rAQk5ODpmZmRQqVCgfrkgUZNpAysWLF3ny5AmHDx+me/futGnTBoCsrCwqVarE3LlzqV+/PgcPHiQ0NJRz584pxzAyMuLSpUvY29vj5+fH6tWr/3LJNyGeJykpiRMnTjB06FDatm2LpaUlxYsXZ/78+fTv35979+4RFBTEzp079YIvbdu2ZcaMGUDuEl26IUBph0IIIYQQbz8JvQghhBBCCCHeOJVKxfHjxxk8eDCNGzdm27ZteHl5sXPnTpnoEEIUODdu3GDy5MkATJ48mZ49e+Lq6oqHhwflypXDxMSEtLQ0qlSpgpmZmRJK0AZfvLy8OHLkCIGBgc9cyqNIkSKsXLmSn3/+WQIv/2GJiYkMGjSI+Ph4+vXrx4wZMzAzM3tuSLR69epMnToVgPHjxysTutr7q/bfNWvWAPDBBx8A6FXhEOKvLF++nDp16jBjxgzKlCnDhx9+COQGXoyNjdFoNLz33ntMnDhRL/hy9uxZcnJycHJyYurUqSxevJjg4GDs7Oz0lnUT4nme1VepVCpcXV2pV68ekBvuy8nJwcTEhFGjRinBl8DAwDzBl9atW7Nu3TqOHTuGtbW19IVCCCGEEAWI1AsXQgghhBBCvHEpKSls3LiRlStXUrZsWYYMGcKAAQMoUqSIBF6EEAXOrVu3OH/+PD169KBDhw7K348dO0Z4eDjXrl3Dz8+PoKCgPL91cXFh1qxZhIeHExER8dylPN57771/7fzF2027hNbBgwc5cOAAH330EePGjQN47j1T+5v27dtz8+ZNJkyYwIgRI7h58yYtWrTgvffew9DQkG+++YZNmzZRuXJlOnbsCPxZKUaIl5Geng7A1KlT0Wg0nDlzhkaNGmFsbAzktifd4EtAQAD79+8nLCyMsWPHUqFCBezs7LCzswNy264saST+iu7SgnFxcZw9e5YnT56QlpaGoaEh2dnZQG7701a4MjIyYtSoUQDMmTOHwMBAAJo1a4aJiQkAjRo1Ap7ftwohhBBCiLeThF6EEEIIIYQQb5ylpSWDBw+mRo0aeHh4ULJkSUxMTOTLXiFEgaKddDt58iRqtZoSJUoo244dO4afnx/nz5/Hz8+P4cOHK9vu3LnDo0ePKFeuHAYGBri6urJs2TIMDAzIzs7GyEiGa8SftBO7sbGxZGVlMXDgQIAXthXtbywsLOjbty/W1taEhYUxf/58VqxYQeHChcnJyeHu3bu4ubmxevVqihYtilqtlsCBeCU+Pj4YGxsTGhpKeno6Z8+eJSEhgSJFiij7PC/40r9/fxYsWIC7u7vevkL8FW07WbNmDQMGDMhTlWXx4sVERERgZWUF5Fa2elbwRdtuP/30UyX4ot1fCCGEEEIUHPIWK4QQQgghhMgXjo6OtG/fnrJly2JiYiJf9gohChztpJuTkxPw5yTZkSNHnhl4ycjIAGDp0qUMGzaMO3fuKMfS9n8SeBFPU6vVpKSkcPLkSUxMTHBzcwNevq3Y2trSv39/YmJiaNOmDU5OTjx+/JjixYvTu3dvduzYgYuLCzk5OXIfFq9Eu7TWV199xZgxYzAwMGDLli0sXbo0z766wZdJkybh4eHB9evXlQovQryqffv2MWjQIAwMDOjTpw/+/v64uLgAcPDgQXbv3q3cdyFv8MXX15dbt24xa9as5y4TJ4QQQgghCgYZSRFCCCGEEEK8FeTLXiFEQVW0aFEAVqxYQbFixZgzZ84zAy+mpqZkZGSwefNmsrOzMTU1zc/TFgVIVlYWDx8+BF6vAkF8fDwffvghdevWJSUlhbt37+Li4oKJiQnGxsaylId4Id2lZHRpl5ExMjKiV69eGBgYMGTIECIiIjA1NWXAgAF6+2uDL2XLlmXJkiUUKlQIe3t7qTAkXsrT7eTw4cMALFq0iDZt2gDQtWtXxo0bR0xMDJMnT8bMzIxPPvlEud/qBl+GDRuGpaUlXbt2xdzc/M1fkBBCCCGE+MeoEhMTNX+9mxBCCCGEEEIIIcR/0/MmfHUn4Ly9vdmwYQM2NjYkJSURGBhISEgIAGlpaZibm6PRaOjTpw/r168nKCiIoUOHSmUX8dKaNWvGiRMnWL9+PR999NErLYU1bdo0nJ2d+fTTT6XNiVei289dvnyZu3fv8ssvv2Bubk6DBg2wtrbGxsZG2X/ZsmUMHjwYgNGjR+Pr65vnmLp9qgRexKuKjY1Fo9Ewe/ZsnJ2dWbBgAZAbDjQ2Nub69etMnDiRVatWUb58eUJDQ/WCL0CeoJ8E/4QQQgghCjZ5yxVCCCGEEEIIIYR4Dt0J2ZSUFFJSUsjJyaFYsWJ6E7U9e/bk999/58SJE5QvXx5vb29lm/YL8uHDh7N+/Xrq1KmDt7e3hA/ES9FoNGRmZuLg4EBmZiYrVqzgo48+wsjI6LmBLF2PHj0iKioKIyMjPvzwQ4oVK/aGzlwUdLpLT27atIkxY8Zw+/Zt0tPTAXB1daV+/fr07NkTDw8PALp37w7A4MGDlUpXTwdfdNusBF7Eqzh48CDdunWjfv36PH78mMqVKwN/Bl40Gg0lSpQgICAAgFWrVjFu3DiAPBVfdEngRQghhBCiYJPRFSGEEEIIIYQQQghyl0qoWbOmMvmlG3jZunUry5cv58SJExgaGuLm5kbTpk1p1aoVbm5ueHh40KNHD9LT0/nll1/o0KEDX3/9NU5OTqSlpTF37lz27NlDyZIlWbBgAXZ2dlLhQLwUlUqFqakpffv2Zc+ePcTExODl5UX37t2V5WKeFXzRVi64fv06qampfPzxxxJ4Ea9E267Wrl1Lv379AOjQoQPW1tYcP36c+Ph4li9fzpEjR5g6dSp169YF8gZfDA0N6d+/f/5chHinFCpUiDZt2vDdd9+Rlpam9GnawIu2T3xW8MXAwIAGDRrI0oJCCCGEEO8gWd5ICCGEEEIIIYQQ/3lRUVGEhITg6+vLyJEj9cIoa9asUSZsnZycyMrK4sGDB6hUKsqVK8fMmTOpUaMGKSkp7Nu3j2XLlrF371694xsYGODl5cWcOXNwdnaWpRTEK0tNTSUgIIC1a9dSrVo1hg4dStOmTYG8S8Totq+OHTuyZ88e5s+fT8eOHSVsJV7J0aNH6dChAzk5OcyZM4c2bdoAuZU1YmNjWbx4MQcOHKBkyZIsWrSIGjVqKL9dtmwZQ4cOJTs7m6lTp9KjR498ugpRED0v0HfmzBnmzZvHpk2b0Gg0TJ06lc8++0zvN9p/tUsdrVu3Djs7O2bOnMnHH3/8pi9FCCGEEEL8y6TSixBCCCGEEEIIIf7f3r1HRV3nfxx/zQWGQAxERC4ePWQXFK1MiULTTbBtNaW8lJzMzdzwjtiCGbj+zOONDpiabkltu1Za3mDLxTS0KDcxu63DathGQ+aWVoqCcpH5zu8Pz0wQ2rq1icDz8Y/K9zvD93vO93xRv895f9q84OBgWa1WrVy5UhaLRXPnzpXZbJbdbldGRoaCg4P1+OOPKz4+XqdPn9Zrr72mbdu26d1339Xw4cOVl5enm2++WXfeeafi4+O1fv16lZaW6ujRowoPD9fAgQMVExOjgIAAghf8JL6+vkpLS5PdbtcHH3ygp556SjU1NUpMTJTZbJbT6ZTZbJbL5ZLFYpFhGMrMzFRhYaFuv/12DRkyRBLLyeB7P7Y8ljuOeu+991RZWanMzMxGwYuXl5eGDRum7t276/HHH9eOHTv0xBNPKDs7WxEREZLOTXyprq7WihUrCA3wX3Nfmx999JE6deqk8PBwSVLv3r318MMPyzAMbdy4Uc8++6yCgoI0ZMiQRsGLe+JLenq6KisrtW/fPvXs2bM5TwkAAAC/ECa9AAAAAAAASNq6dauSk5N15swZpaSk6P/+7/+Un5+vBx980DMlw62urk4Oh0OLFi3SX//6V4WGhmrjxo1NHqj98KEyUzbwc33yySe6//779dlnnykyMlJ33323Zs+eLencEh91dXWqrq5WWlqaNm7cqK5du2rbtm0KDQ3l+oOH+1qorq7W8ePH9be//U1XX321YmJi5Ofn59lv/PjxevXVV7Vx40bFx8ervr5eVuv3n6N0uVx68803lZGRoWPHjumZZ55pst/p06fl5+fX5LXAf5KXl6cJEyZo+vTpmjx5skJDQz3b7Ha7Vq5cqc2bNysmJkazZs1SQkKCpKYTX7766iv5+PgoMDCQ8BQAAKAV4l8ZAAAAAACgTXM/FBs2bJiefvppTZo0ScuXL5fValWnTp0UERGhxMRESd8/KPb29tY111yjxYsXq6qqSjt37tSqVauUlZUlX1/fJmGB+3sQHODnuu666/Tyyy/rkUce0d69e5Wdna2ioiKFhoYqKipKdrtdpaWlKisrU+/evbVu3TqFhobyoBce7vvY119/rezsbO3cuVOff/65wsLClJOTowEDBsjX11eSPNfMP//5T8XHxze5h5lMJt166626/vrr9corr+ill15SfHy8rFar5/u4IxqCF/w3DMPQiRMnFBYWprVr18pqtWrixIkKCwuTJPXq1UszZsyQyWTSpk2blJOTI0lKSEhoFLxI8sQyhmFwHwQAAGiF+JcGAAAAAABo0xo+HLvrrrskSZMmTVJ2drYiIyNVX1+v+vp6eXl5NXng27lzZyUnJ+v999/X3r17VVNTo3bt2jV674a/Av8L3bt315o1a5SXl6ecnBx99NFHev/99/Xaa69Jknr27KkpU6YoNTVVHTt2JHiBhztEKS8v13333adPPvlEUVFRevTRR9WjRw/16dNHvr6+nnviTTfdpLy8PO3fv1/SueWxGk4Mcrlc8vHx0b333qu8vDydPn3a872I/PBzmM1mJSUlyWazKTs7W7m5uZLUKHyJjo7W9OnTJek/hi/u9wQAAEDrQ/QCAAAAAADavB+GLy6XS9OmTVNZWZksFotee+01jRw5skk4YDKZNGDAAHXp0kUlJSUqLi7WsGHDmuks0JaEhIRo0qRJuuuuu3TgwAGVlJSoQ4cOstlsSkhIkL+/v7y9vQle4OGOVY4cOaLExEQ5HA6NGzdOWVlZ8vHxabSvOxSIjY2VxWLRli1bdO211yo9PV1ms9lzXbknZzidTtXV1TWK/oCfwx1U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",
      "text/plain": [
       "<Figure size 2400x1000 with 3 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "msno.bar(food)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 114,
   "id": "c9bd90ee-4421-416a-8d17-f0293208ca69",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Country                   0\n",
       "Year                      0\n",
       "FoodCode                 20\n",
       "FoodName                624\n",
       "AgeClass                  0\n",
       "SourceAgeClass            0\n",
       "Gender                    0\n",
       "Number_of_consumers       0\n",
       "Consumers_Mean           32\n",
       "Consumers_Median       4532\n",
       "Number_of_subjects        0\n",
       "Total_Mean             5102\n",
       "Total_Median              3\n",
       "dtype: int64"
      ]
     },
     "execution_count": 114,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.isna().sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4ce0e5b0-e3bf-44b9-b6ed-c1159715e13a",
   "metadata": {
    "tags": []
   },
   "source": [
    "### Zarówno na wykresie jak i w tabeli widać, że FoodName i FoodCode mają puste wartości, wiec zajmuję sie usunięciem tych rzędów. (na razie nie zajmuję sie innymi kolumnami z pustymi watościami, bo nie wiem czy będą użyteczne)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 115,
   "id": "453634dd-dd94-47b2-abed-3005614a27bc",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>540608</th>\n",
       "      <td>Republic Of Korea</td>\n",
       "      <td>2015</td>\n",
       "      <td>fa6adbfab52e8a77f23df411f59c2150</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>3-5 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>692</td>\n",
       "      <td>2.26</td>\n",
       "      <td>0.84</td>\n",
       "      <td>804</td>\n",
       "      <td>1.95</td>\n",
       "      <td>0.59</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>540609</th>\n",
       "      <td>Republic Of Korea</td>\n",
       "      <td>2015</td>\n",
       "      <td>fa6adbfab52e8a77f23df411f59c2150</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>6-14 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>1937</td>\n",
       "      <td>1.89</td>\n",
       "      <td>0.81</td>\n",
       "      <td>2376</td>\n",
       "      <td>1.54</td>\n",
       "      <td>0.48</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>540610</th>\n",
       "      <td>Republic Of Korea</td>\n",
       "      <td>2015</td>\n",
       "      <td>fa6adbfab52e8a77f23df411f59c2150</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>6798</td>\n",
       "      <td>1.80</td>\n",
       "      <td>0.76</td>\n",
       "      <td>8253</td>\n",
       "      <td>1.48</td>\n",
       "      <td>0.48</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>540611</th>\n",
       "      <td>Republic Of Korea</td>\n",
       "      <td>2015</td>\n",
       "      <td>fa6adbfab52e8a77f23df411f59c2150</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>50-74 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>6054</td>\n",
       "      <td>2.04</td>\n",
       "      <td>0.76</td>\n",
       "      <td>7069</td>\n",
       "      <td>1.74</td>\n",
       "      <td>0.49</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>540612</th>\n",
       "      <td>Republic Of Korea</td>\n",
       "      <td>2015</td>\n",
       "      <td>fa6adbfab52e8a77f23df411f59c2150</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>&gt;75 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>1204</td>\n",
       "      <td>1.97</td>\n",
       "      <td>0.40</td>\n",
       "      <td>1650</td>\n",
       "      <td>1.44</td>\n",
       "      <td>0.11</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                  Country  Year                          FoodCode FoodName  \\\n",
       "540608  Republic Of Korea  2015  fa6adbfab52e8a77f23df411f59c2150      NaN   \n",
       "540609  Republic Of Korea  2015  fa6adbfab52e8a77f23df411f59c2150      NaN   \n",
       "540610  Republic Of Korea  2015  fa6adbfab52e8a77f23df411f59c2150      NaN   \n",
       "540611  Republic Of Korea  2015  fa6adbfab52e8a77f23df411f59c2150      NaN   \n",
       "540612  Republic Of Korea  2015  fa6adbfab52e8a77f23df411f59c2150      NaN   \n",
       "\n",
       "                        AgeClass SourceAgeClass Gender  Number_of_consumers  \\\n",
       "540608  Children And Adolescents      3-5 Years    All                  692   \n",
       "540609  Children And Adolescents     6-14 Years    All                 1937   \n",
       "540610        Adults And Elderly    15-49 Years    All                 6798   \n",
       "540611        Adults And Elderly    50-74 Years    All                 6054   \n",
       "540612        Adults And Elderly      >75 Years    All                 1204   \n",
       "\n",
       "        Consumers_Mean  Consumers_Median  Number_of_subjects  Total_Mean  \\\n",
       "540608            2.26              0.84                 804        1.95   \n",
       "540609            1.89              0.81                2376        1.54   \n",
       "540610            1.80              0.76                8253        1.48   \n",
       "540611            2.04              0.76                7069        1.74   \n",
       "540612            1.97              0.40                1650        1.44   \n",
       "\n",
       "        Total_Median  \n",
       "540608          0.59  \n",
       "540609          0.48  \n",
       "540610          0.48  \n",
       "540611          0.49  \n",
       "540612          0.11  "
      ]
     },
     "execution_count": 115,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "null_data = food[food.isnull().any(axis=1)]\n",
    "null_data.tail(5) # NaN w FoodCode widać dopiero na 50 ale dla wygody pozostaje default"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 116,
   "id": "b3c09bc4-4b1f-46b1-be0b-0ada86c77600",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Country                Democratic Republic Of The Congo\n",
       "Year                                               2016\n",
       "FoodCode                                            NaN\n",
       "FoodName                                            NaN\n",
       "AgeClass                                            All\n",
       "SourceAgeClass                                      All\n",
       "Gender                                              All\n",
       "Number_of_consumers                                   1\n",
       "Consumers_Mean                                     3.36\n",
       "Consumers_Median                                   3.36\n",
       "Number_of_subjects                                  214\n",
       "Total_Mean                                         0.02\n",
       "Total_Median                                       0.00\n",
       "Name: 527540, dtype: object"
      ]
     },
     "execution_count": 116,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.loc[527540]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4e0abdc1-0cc6-4354-b95c-b2f1a53fdf18",
   "metadata": {},
   "source": [
    "### Teraz widać, że zarówno w kolumnie FoodName i FoodCode puste dane są opisane jako NaN. Dodatkowo w kolumnie FoodCode widzę, że jest kod znacząco dłuższy od innych, które na razie widziałem i znajduje się on zawsze tam gdzie jest pusta wartość dla FoodName. Na podstawie tego decyduję, żę dobrym rozwiązaniem jest usunięcie rzędów w których FoodName ma wartości NaN bo nawet jeżeli kody są dobre to bez wiedzy jaki produkt one oznaczją są one bezużyteczne. Następnie zobaczę czy po tym nadal pozostaną długie kody i puste wartości w FoodCode. Prawdopodobnym powodem pustych danych jest błednie podany kod produktu co skutkuje tym, że nie ma również nazwy produktu ale to się okaże dalej."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 117,
   "id": "86f1e0a5-6a4c-4861-9d88-c5d648263370",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "food = food.dropna(subset=['FoodName'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 118,
   "id": "f94b4275-c1a5-4b0c-adf1-f99c8be1354e",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Country                   0\n",
       "Year                      0\n",
       "FoodCode                  0\n",
       "FoodName                  0\n",
       "AgeClass                  0\n",
       "SourceAgeClass            0\n",
       "Gender                    0\n",
       "Number_of_consumers       0\n",
       "Consumers_Mean           32\n",
       "Consumers_Median       4532\n",
       "Number_of_subjects        0\n",
       "Total_Mean             5102\n",
       "Total_Median              3\n",
       "dtype: int64"
      ]
     },
     "execution_count": 118,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.isna().sum()      "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9f0bc27b-9413-4ac1-8f6e-06faf805d191",
   "metadata": {},
   "source": [
    "### Usuwanie pustych danych powiodło się. Poprzez usuwanie pustych danych z FoodName usnąłem też przy okazji puste dane z FoodCode. Teraz chcę sprawdzić czy długość kodu miała znaczenie. Zrobię to najpierw na przykładzie kodu który widziałem czyli fa6adbfab52e8a77f23df411f59c2150 oraz sprawdzając kody o długości większej niż 5 czyli standardowej długości, którą widziałem. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 119,
   "id": "35852177-d0ed-419b-952d-6b2d9e93b40c",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [Country, Year, FoodCode, FoodName, AgeClass, SourceAgeClass, Gender, Number_of_consumers, Consumers_Mean, Consumers_Median, Number_of_subjects, Total_Mean, Total_Median]\n",
       "Index: []"
      ]
     },
     "execution_count": 119,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.loc[food['FoodCode'] == \"fa6adbfab52e8a77f23df411f59c2150\"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 120,
   "id": "e8ead441-256a-495e-9ab1-410ca5c491ce",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "FoodCode\n",
       "False    516640\n",
       "True       6012\n",
       "Name: count, dtype: int64"
      ]
     },
     "execution_count": 120,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "temp = food['FoodCode'].str.len() > 5\n",
    "temp.value_counts()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2c0ff0fc-2cf1-4a83-819f-12323090b0be",
   "metadata": {},
   "source": [
    "### Wychodzi na to, że pozbyłem się kodu fa6adbfab52e8a77f23df411f59c2150, ale kody o długości większej niż 5 nadal istnieją i jest ich znacząco mniej, więc sprawdzę teraz czy one są poprawne, chociaż na razie wszystko wskazuje na to, że nie powinno być z nimi problemu."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 121,
   "id": "423d4c2c-2f49-41c8-8995-6e3ce1e35212",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "      <th>CodeLen</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>60.62</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>1.06</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>348298</th>\n",
       "      <td>Portugal</td>\n",
       "      <td>2015</td>\n",
       "      <td>A00DH</td>\n",
       "      <td>Oat Rolled Grains</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Female</td>\n",
       "      <td>1</td>\n",
       "      <td>0.40</td>\n",
       "      <td>0.40</td>\n",
       "      <td>262</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>348297</th>\n",
       "      <td>Portugal</td>\n",
       "      <td>2015</td>\n",
       "      <td>A006R</td>\n",
       "      <td>Traditional Unleavened Breads</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Female</td>\n",
       "      <td>1</td>\n",
       "      <td>1.94</td>\n",
       "      <td>1.94</td>\n",
       "      <td>262</td>\n",
       "      <td>0.01</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>348296</th>\n",
       "      <td>Portugal</td>\n",
       "      <td>2015</td>\n",
       "      <td>A006P</td>\n",
       "      <td>Rusk, Wholemeal</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Male</td>\n",
       "      <td>1</td>\n",
       "      <td>1.63</td>\n",
       "      <td>1.63</td>\n",
       "      <td>259</td>\n",
       "      <td>0.01</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>348295</th>\n",
       "      <td>Portugal</td>\n",
       "      <td>2015</td>\n",
       "      <td>A006P</td>\n",
       "      <td>Rusk, Wholemeal</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Female</td>\n",
       "      <td>4</td>\n",
       "      <td>0.65</td>\n",
       "      <td>0.59</td>\n",
       "      <td>262</td>\n",
       "      <td>0.01</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>251182</th>\n",
       "      <td>Nigeria</td>\n",
       "      <td>2011</td>\n",
       "      <td>17348df7c5044de2950b5bce2d8bb912</td>\n",
       "      <td>(All Meat And Meat Products)</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>6-14 Years</td>\n",
       "      <td>Female</td>\n",
       "      <td>0</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>1</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>32</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>275702</th>\n",
       "      <td>United States Of America</td>\n",
       "      <td>2010</td>\n",
       "      <td>356d09ef45eb5879c5a334a1b9441094</td>\n",
       "      <td>(All Ingredients)</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>&gt;75 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>1429</td>\n",
       "      <td>0.10</td>\n",
       "      <td>0.08</td>\n",
       "      <td>1595</td>\n",
       "      <td>0.09</td>\n",
       "      <td>0.07</td>\n",
       "      <td>32</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>275701</th>\n",
       "      <td>United States Of America</td>\n",
       "      <td>2010</td>\n",
       "      <td>356d09ef45eb5879c5a334a1b9441094</td>\n",
       "      <td>(All Ingredients)</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>50-74 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>4496</td>\n",
       "      <td>0.11</td>\n",
       "      <td>0.08</td>\n",
       "      <td>5215</td>\n",
       "      <td>0.10</td>\n",
       "      <td>0.06</td>\n",
       "      <td>32</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>275699</th>\n",
       "      <td>United States Of America</td>\n",
       "      <td>2010</td>\n",
       "      <td>356d09ef45eb5879c5a334a1b9441094</td>\n",
       "      <td>(All Ingredients)</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>6-14 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>3215</td>\n",
       "      <td>0.07</td>\n",
       "      <td>0.04</td>\n",
       "      <td>4330</td>\n",
       "      <td>0.05</td>\n",
       "      <td>0.02</td>\n",
       "      <td>32</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>217932</th>\n",
       "      <td>Italy</td>\n",
       "      <td>2006</td>\n",
       "      <td>eb31155c944a8c91ec4a53503cf50264</td>\n",
       "      <td>(All Nuts)</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>Female</td>\n",
       "      <td>56</td>\n",
       "      <td>14.83</td>\n",
       "      <td>11.20</td>\n",
       "      <td>873</td>\n",
       "      <td>0.95</td>\n",
       "      <td>0.00</td>\n",
       "      <td>32</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>522652 rows × 14 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                         Country  Year                          FoodCode  \\\n",
       "0                          China  2002                             A000G   \n",
       "348298                  Portugal  2015                             A00DH   \n",
       "348297                  Portugal  2015                             A006R   \n",
       "348296                  Portugal  2015                             A006P   \n",
       "348295                  Portugal  2015                             A006P   \n",
       "...                          ...   ...                               ...   \n",
       "251182                   Nigeria  2011  17348df7c5044de2950b5bce2d8bb912   \n",
       "275702  United States Of America  2010  356d09ef45eb5879c5a334a1b9441094   \n",
       "275701  United States Of America  2010  356d09ef45eb5879c5a334a1b9441094   \n",
       "275699  United States Of America  2010  356d09ef45eb5879c5a334a1b9441094   \n",
       "217932                     Italy  2006  eb31155c944a8c91ec4a53503cf50264   \n",
       "\n",
       "                             FoodName                  AgeClass  \\\n",
       "0                           Oat Grain                       All   \n",
       "348298              Oat Rolled Grains  Children And Adolescents   \n",
       "348297  Traditional Unleavened Breads  Children And Adolescents   \n",
       "348296                Rusk, Wholemeal  Children And Adolescents   \n",
       "348295                Rusk, Wholemeal  Children And Adolescents   \n",
       "...                               ...                       ...   \n",
       "251182   (All Meat And Meat Products)  Children And Adolescents   \n",
       "275702              (All Ingredients)        Adults And Elderly   \n",
       "275701              (All Ingredients)        Adults And Elderly   \n",
       "275699              (All Ingredients)  Children And Adolescents   \n",
       "217932                     (All Nuts)        Adults And Elderly   \n",
       "\n",
       "        SourceAgeClass  Gender  Number_of_consumers  Consumers_Mean  \\\n",
       "0                  All     All                 1157           60.62   \n",
       "348298  Other Children  Female                    1            0.40   \n",
       "348297  Other Children  Female                    1            1.94   \n",
       "348296  Other Children    Male                    1            1.63   \n",
       "348295  Other Children  Female                    4            0.65   \n",
       "...                ...     ...                  ...             ...   \n",
       "251182      6-14 Years  Female                    0            0.00   \n",
       "275702       >75 Years     All                 1429            0.10   \n",
       "275701     50-74 Years     All                 4496            0.11   \n",
       "275699      6-14 Years     All                 3215            0.07   \n",
       "217932     15-49 Years  Female                   56           14.83   \n",
       "\n",
       "        Consumers_Median  Number_of_subjects  Total_Mean  Total_Median  \\\n",
       "0                   0.00               66172        1.06          0.00   \n",
       "348298              0.40                 262        0.00          0.00   \n",
       "348297              1.94                 262        0.01          0.00   \n",
       "348296              1.63                 259        0.01          0.00   \n",
       "348295              0.59                 262        0.01          0.00   \n",
       "...                  ...                 ...         ...           ...   \n",
       "251182              0.00                   1        0.00          0.00   \n",
       "275702              0.08                1595        0.09          0.07   \n",
       "275701              0.08                5215        0.10          0.06   \n",
       "275699              0.04                4330        0.05          0.02   \n",
       "217932             11.20                 873        0.95          0.00   \n",
       "\n",
       "        CodeLen  \n",
       "0             5  \n",
       "348298        5  \n",
       "348297        5  \n",
       "348296        5  \n",
       "348295        5  \n",
       "...         ...  \n",
       "251182       32  \n",
       "275702       32  \n",
       "275701       32  \n",
       "275699       32  \n",
       "217932       32  \n",
       "\n",
       "[522652 rows x 14 columns]"
      ]
     },
     "execution_count": 121,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "checkpoint = food #tworzę checkpoint żeby móc łatwo wrócić do wersji przed sortowaniem\n",
    "food['CodeLen'] = food['FoodCode'].str.len()\n",
    "food.sort_values(by=['CodeLen'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 122,
   "id": "2497f701-a665-438f-8ee1-8f68dcd52942",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "458"
      ]
     },
     "execution_count": 122,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "temp = food.loc[food['FoodCode'] == \"a93a0316b93a7c2af9305e90012af119\"]\n",
    "len(temp)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "75a265d0-cfe9-423e-8732-f9c3a7d8d0b6",
   "metadata": {},
   "source": [
    "### Moje przypuszczenia zostały potwierdzone, puste dane nie są zależne od długości kodu, więc w tych kwestiach nie ma o co się martwić. "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a3bcbdfc-c53b-4b20-aefd-d573daa5d485",
   "metadata": {},
   "source": [
    "### <a id=\"colinfo\"></a>[&uarr;](#top) Teraz zajmę się kolumnami Consumers_Mean, Consumers_Median, Total_Mean, Total_Median. Jako że nie mam legendy to nie wiem co dokładnie one znaczą i zakładanie co znaczą oraz wiara że posiadają dobre wartości może być zgubna"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 123,
   "id": "14d5dcc1-923c-4847-8feb-42e232b032df",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "      <th>CodeLen</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>60.62</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>1.06</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>Female</td>\n",
       "      <td>608</td>\n",
       "      <td>55.87</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>1.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>Male</td>\n",
       "      <td>549</td>\n",
       "      <td>65.89</td>\n",
       "      <td>0.00</td>\n",
       "      <td>32219</td>\n",
       "      <td>1.12</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>167</td>\n",
       "      <td>55.26</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>0.14</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>Female</td>\n",
       "      <td>82</td>\n",
       "      <td>54.71</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33953</td>\n",
       "      <td>0.13</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Country  Year FoodCode   FoodName AgeClass SourceAgeClass  Gender  \\\n",
       "0   China  2002    A000G  Oat Grain      All            All     All   \n",
       "1   China  2002    A000G  Oat Grain      All            All  Female   \n",
       "2   China  2002    A000G  Oat Grain      All            All    Male   \n",
       "3   China  2002    A000N  Buckwheat      All            All     All   \n",
       "4   China  2002    A000N  Buckwheat      All            All  Female   \n",
       "\n",
       "   Number_of_consumers  Consumers_Mean  Consumers_Median  Number_of_subjects  \\\n",
       "0                 1157           60.62              0.00               66172   \n",
       "1                  608           55.87              0.00               33953   \n",
       "2                  549           65.89              0.00               32219   \n",
       "3                  167           55.26              0.00               66172   \n",
       "4                   82           54.71              0.00               33953   \n",
       "\n",
       "   Total_Mean  Total_Median  CodeLen  \n",
       "0        1.06          0.00        5  \n",
       "1        1.00          0.00        5  \n",
       "2        1.12          0.00        5  \n",
       "3        0.14          0.00        5  \n",
       "4        0.13          0.00        5  "
      ]
     },
     "execution_count": 123,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food = checkpoint # powrót do checkpointa\n",
    "food.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9e4ac840-8424-4405-ac4d-f3c0a3a21090",
   "metadata": {},
   "source": [
    "### martwi mnie kwestia że Total_Median, Consumers_Median mają wartości 0,kiedy mediana nie powinna w takim przypadku mięc zerowych wartości"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 124,
   "id": "e082efc1-9c91-4938-be4c-d7fc21635426",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(25090, 31553, 102099, 493224)"
      ]
     },
     "execution_count": 124,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food['Consumers_Mean'].loc[food['Consumers_Mean'] == 0].count() ,food['Consumers_Median'].loc[food['Consumers_Median'] == 0].count(),food['Total_Mean'].loc[food['Total_Mean'] == 0].count(),food['Total_Median'].loc[food['Total_Median'] == 0].count()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 125,
   "id": "6ba2b59f-a395-4f5d-b0d0-330f364bf8dc",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "522620"
      ]
     },
     "execution_count": 125,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food['Consumers_Mean'].count()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ff32f8b9-e007-46a8-80db-33fd3fe5d841",
   "metadata": {},
   "source": [
    "### Total_median ma prawie 500 000 wartości 0. Totalnie dyskfalifikuje to używalność używalność tej kolumny. podobnie z Total_mean, niezależnie co ona znaczy niemożliwe żeby aż w 1/4 wyników miała tym bardziej że one występują w rzedach które mają dane. Dla mnie wyklucza to totalnie używalność tych kolumn. "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "40ff8eaa-5e10-41f9-b9d2-9c8ea97384e4",
   "metadata": {
    "tags": []
   },
   "source": [
    "### Consumers_Mean i Consumers_Median mają mniej zerowych wartości ale nadal dużo ale spróbuję na przykładzie chin dla oat grain sprawdzić czy te wartości może mają jakiś sens."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 126,
   "id": "8ac36cd0-556b-4050-ae1f-0721797396d8",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Consumers_Mean</th>\n",
       "      <th>Consumers_Median</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Total_Mean</th>\n",
       "      <th>Total_Median</th>\n",
       "      <th>CodeLen</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>60.62</td>\n",
       "      <td>0.00</td>\n",
       "      <td>66172</td>\n",
       "      <td>1.06</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>812</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>All</td>\n",
       "      <td>10</td>\n",
       "      <td>28.58</td>\n",
       "      <td>0.00</td>\n",
       "      <td>838</td>\n",
       "      <td>0.34</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1251</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>3-5 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>20</td>\n",
       "      <td>22.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>2235</td>\n",
       "      <td>0.20</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1782</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>6-14 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>107</td>\n",
       "      <td>39.97</td>\n",
       "      <td>0.00</td>\n",
       "      <td>9844</td>\n",
       "      <td>0.43</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2487</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>545</td>\n",
       "      <td>66.67</td>\n",
       "      <td>0.00</td>\n",
       "      <td>33719</td>\n",
       "      <td>1.08</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3267</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>50-74 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>438</td>\n",
       "      <td>62.06</td>\n",
       "      <td>0.00</td>\n",
       "      <td>18143</td>\n",
       "      <td>1.50</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4020</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>&gt;75 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>37</td>\n",
       "      <td>43.87</td>\n",
       "      <td>0.00</td>\n",
       "      <td>1393</td>\n",
       "      <td>1.17</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>279440</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>1.12</td>\n",
       "      <td>NaN</td>\n",
       "      <td>66172</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>280252</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>All</td>\n",
       "      <td>10</td>\n",
       "      <td>2.00</td>\n",
       "      <td>NaN</td>\n",
       "      <td>838</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>280691</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>3-5 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>20</td>\n",
       "      <td>1.31</td>\n",
       "      <td>NaN</td>\n",
       "      <td>2235</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>281222</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>6-14 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>107</td>\n",
       "      <td>1.35</td>\n",
       "      <td>NaN</td>\n",
       "      <td>9844</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>281927</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>545</td>\n",
       "      <td>1.12</td>\n",
       "      <td>NaN</td>\n",
       "      <td>33719</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>282707</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>50-74 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>438</td>\n",
       "      <td>1.06</td>\n",
       "      <td>NaN</td>\n",
       "      <td>18143</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>283460</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>&gt;75 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>37</td>\n",
       "      <td>0.79</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1393</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.00</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       Country  Year FoodCode   FoodName                  AgeClass  \\\n",
       "0        China  2002    A000G  Oat Grain                       All   \n",
       "812      China  2002    A000G  Oat Grain      Infants And Toddlers   \n",
       "1251     China  2002    A000G  Oat Grain  Children And Adolescents   \n",
       "1782     China  2002    A000G  Oat Grain  Children And Adolescents   \n",
       "2487     China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "3267     China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "4020     China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "279440   China  2002    A000G  Oat Grain                       All   \n",
       "280252   China  2002    A000G  Oat Grain      Infants And Toddlers   \n",
       "280691   China  2002    A000G  Oat Grain  Children And Adolescents   \n",
       "281222   China  2002    A000G  Oat Grain  Children And Adolescents   \n",
       "281927   China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "282707   China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "283460   China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "\n",
       "       SourceAgeClass Gender  Number_of_consumers  Consumers_Mean  \\\n",
       "0                 All    All                 1157           60.62   \n",
       "812       0-35 Months    All                   10           28.58   \n",
       "1251        3-5 Years    All                   20           22.00   \n",
       "1782       6-14 Years    All                  107           39.97   \n",
       "2487      15-49 Years    All                  545           66.67   \n",
       "3267      50-74 Years    All                  438           62.06   \n",
       "4020        >75 Years    All                   37           43.87   \n",
       "279440            All    All                 1157            1.12   \n",
       "280252    0-35 Months    All                   10            2.00   \n",
       "280691      3-5 Years    All                   20            1.31   \n",
       "281222     6-14 Years    All                  107            1.35   \n",
       "281927    15-49 Years    All                  545            1.12   \n",
       "282707    50-74 Years    All                  438            1.06   \n",
       "283460      >75 Years    All                   37            0.79   \n",
       "\n",
       "        Consumers_Median  Number_of_subjects  Total_Mean  Total_Median  \\\n",
       "0                   0.00               66172        1.06          0.00   \n",
       "812                 0.00                 838        0.34          0.00   \n",
       "1251                0.00                2235        0.20          0.00   \n",
       "1782                0.00                9844        0.43          0.00   \n",
       "2487                0.00               33719        1.08          0.00   \n",
       "3267                0.00               18143        1.50          0.00   \n",
       "4020                0.00                1393        1.17          0.00   \n",
       "279440               NaN               66172         NaN          0.00   \n",
       "280252               NaN                 838         NaN          0.00   \n",
       "280691               NaN                2235         NaN          0.00   \n",
       "281222               NaN                9844         NaN          0.00   \n",
       "281927               NaN               33719         NaN          0.00   \n",
       "282707               NaN               18143         NaN          0.00   \n",
       "283460               NaN                1393         NaN          0.00   \n",
       "\n",
       "        CodeLen  \n",
       "0             5  \n",
       "812           5  \n",
       "1251          5  \n",
       "1782          5  \n",
       "2487          5  \n",
       "3267          5  \n",
       "4020          5  \n",
       "279440        5  \n",
       "280252        5  \n",
       "280691        5  \n",
       "281222        5  \n",
       "281927        5  \n",
       "282707        5  \n",
       "283460        5  "
      ]
     },
     "execution_count": 126,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all = food.loc[food['Gender'] == \"All\"]\n",
    "food_all_oat = food_all.loc[food_all['FoodName'] == \"Oat Grain\"]\n",
    "food_all_oat_ch = food_all_oat.loc[food_all_oat['Country'] == \"China\"]\n",
    "food_all_oat_ch"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7d1dfbe2-dde2-4b28-ba4b-3de429e333d4",
   "metadata": {},
   "source": [
    "### Tutaj pojawiło się pare ciekawych rzeczy. Po pierwse to to żę dane są podwojone dla wszystkich kolumn nie licząc Consumers_Mean, Consumers_Median, Total_Mean, Total_Median. Dodatkowo polowa danych z Consumers_median i total_mean ma wartości NaN. Na tym przykładzie widać że Consumers_Median i Total_Median sa dla mnie bezużytecznymi kolumnami bo niektórych przypadkach nie dadzą mi w ogóle informacji wiec już teraz moge ustalić ze ich się pozbywam wiec jedynie consumers mean może być użyteczne i to to sprawdzę czy posiada sensowne wartości. Tylko martwi mnie to żę dane są podowjone, a dane consumers mean dwa razy są różne prawdopodobnie ta kolumna też do wyrzucenia jest. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 127,
   "id": "2dccf507-6e0b-43f7-96c1-1e52e3eee913",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Country                   0\n",
       "Year                      0\n",
       "FoodCode                  0\n",
       "FoodName                  0\n",
       "AgeClass                  0\n",
       "SourceAgeClass            0\n",
       "Gender                    0\n",
       "Number_of_consumers       0\n",
       "Consumers_Mean           32\n",
       "Consumers_Median       4532\n",
       "Number_of_subjects        0\n",
       "Total_Mean             5102\n",
       "Total_Median              3\n",
       "CodeLen                   0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 127,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.isna().sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0ef46616-7339-43c1-aae8-2413bcf0ee0c",
   "metadata": {},
   "source": [
    "### Czyli dochądzą kolejne bezużyteczne dane w tych kolumnach."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 128,
   "id": "2122f87f-b347-4b04-a38f-72a104c4d29a",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "60.623"
      ]
     },
     "execution_count": 128,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_oat_ch['Consumers_Mean'].iloc[0] "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 129,
   "id": "a168d1ea-2979-4cbe-8b64-d9090f391159",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1.748473674666022"
      ]
     },
     "execution_count": 129,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "1157/66172*100 # procent konsumentów z całej puli badanych "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 130,
   "id": "d9d27089-954c-471f-90c0-44328ee869da",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "57.19273984442524"
      ]
     },
     "execution_count": 130,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "66172/1157 #liczba badanych podzielona przez liczbę konsumentów"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 131,
   "id": "dc21887c-b13d-49d8-ac09-80aa05bd4d7b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "57.193707865168534"
      ]
     },
     "execution_count": 131,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "(1.12+66172)/1157 # połączona liczba badanych podzielona przez liczbę konsumentów"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 132,
   "id": "a15de394-f250-44d8-b4c1-ba42930ec2df",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "263.15090000000004"
      ]
     },
     "execution_count": 132,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_oat_ch['Consumers_Mean'].iloc[1:7].sum() # suma średnich dla rzędów 1-6"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 133,
   "id": "801e9123-5b06-49da-9712-e46c60f7ab7a",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "43.85848333333334"
      ]
     },
     "execution_count": 133,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_oat_ch['Consumers_Mean'].iloc[1:7].mean() # średnia ze średnich"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 134,
   "id": "36c05bc7-bab8-4bae-ace7-11b20df908b8",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "330.57142857142856"
      ]
     },
     "execution_count": 134,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_oat_ch['Number_of_consumers'].iloc[:7].mean() # średnia z pierwszyć 7 rzędów"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 135,
   "id": "0aae7615-6752-4308-8819-6a30e90c5713",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.01670516892867456"
      ]
     },
     "execution_count": 135,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_oat_ch['Number_of_consumers'].iloc[0]/food_all['Number_of_consumers'].iloc[1:7].sum() # wartość dla all podzielona przez sume wartości rzędów 1-6"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "222eeea4-e495-468e-8a44-1528dad750b5",
   "metadata": {
    "tags": []
   },
   "source": [
    "### Żadne obliczenia nie daja takiej wartości jaka jest w kolumnie Consumers_Mean, więc albo są to jakieś inne dane, np. średnia ilość gramów spożywanego produktu przez ankietowanych albo coś zupełnie innego, ale bez odpowiedniej wiedzy nie można tego założyć. Znaczy to, że tych kolumn też trzeba sie pozbyć, gdyż nawet gdyby były pomocne, mogą one zawierać fałszywe wartości.\n",
    "### Usuwam więc: Consumers_Mean, Consumers_Median, Total_Mean, Total_Median i dodatkowo CodeLen które i tak już nie będzie użyteczne dla mnie."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 136,
   "id": "65ac9e49-a64b-48fd-aaf4-90769f095e16",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(522652, 14)"
      ]
     },
     "execution_count": 136,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 137,
   "id": "399b5be4-5e41-4f5e-9486-b63990c5a11b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(522652, 9)"
      ]
     },
     "execution_count": 137,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food = food.drop(['Consumers_Mean', 'Consumers_Median', 'Total_Mean', 'Total_Median', 'CodeLen'], axis=1)\n",
    "food.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a2db5119-a22a-4e1b-a32b-320f32277a4e",
   "metadata": {},
   "source": [
    "### Wszystko poszło dobrze, pozbyłem się 5 kolumn, więc teraz czas na usuwanie duplikatów, zrobię to za pomocą drop.duplicates bo tak jak widziałem dane były podwojone i jedyne kolumny które uniemożliwiały usunięcie duplikatów przy wczesniejszym przywołaniu dropduplicates wiec samo to powinno bozbyc się niepotrzebnych danych"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 138,
   "id": "325be1d4-abbf-46d9-9283-b2ea9e6c37e9",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(522652, 9)"
      ]
     },
     "execution_count": 138,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 139,
   "id": "b49eb1fa-6fda-4184-88b0-7437dd46893a",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(272016, 9)"
      ]
     },
     "execution_count": 139,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food = food.drop_duplicates()\n",
    "food.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 140,
   "id": "22f15bf3-a19f-4c0c-9d39-525f5e8842e6",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "272016"
      ]
     },
     "execution_count": 140,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "544032-272016\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b1e1ed38-0766-4ca2-80ce-89173de882a1",
   "metadata": {},
   "source": [
    "### Tak jak wczesniej zauważyłem dane były podwojone w całej bazie danych, więc bardzo dobrze, że to zauważyłem, bo inaczej mogło by to mocno zakłamać wyniki.\n",
    "### <a id=\"kraje\"></a>[&uarr;](#top) Sprawdzam z jakich krajów są dane dla wszystkich płci"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 141,
   "id": "530235c2-b4e7-46e9-9867-cfd240d3d276",
   "metadata": {},
   "outputs": [],
   "source": [
    "food_all = food.loc[food['Gender'] == \"All\"]\n",
    "food_fem = food.loc[food['Gender'] == \"Female\"]\n",
    "food_men = food.loc[food['Gender'] == \"Male\"]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a4b56cf9-4c95-4107-9562-f3c41e786a50",
   "metadata": {
    "tags": []
   },
   "source": [
    "### jeszcze przed tym dla upewnienia się sprawdze czy sumują się dobrze rzędy czy czegoś nie straciłem podczas przypisywania"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 142,
   "id": "96c05cff-0511-4b3d-a720-4baaea93db31",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 142,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all['Country'].count() + food_fem['Country'].count() + food_men['Country'].count() - food['Country'].count()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "87fe4116-b2e2-4340-ac2b-f756570d7be2",
   "metadata": {},
   "source": [
    "### takie same ilości więc super"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 143,
   "id": "9e44cadf-42d7-4456-a83b-984ec358a18e",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "41"
      ]
     },
     "execution_count": 143,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food['Country'].nunique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 144,
   "id": "66649823-c014-4873-b645-783a5e4f7880",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "41"
      ]
     },
     "execution_count": 144,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all['Country'].nunique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 145,
   "id": "9ffe65f6-f024-428b-8dfd-2306a8855360",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "41"
      ]
     },
     "execution_count": 145,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_fem['Country'].nunique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 146,
   "id": "d85954db-8303-4cc2-9d7a-d1c6e01b93ef",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "32"
      ]
     },
     "execution_count": 146,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_men['Country'].nunique()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2205c3dd-0b44-42c6-bf7d-b6e4c847606c",
   "metadata": {},
   "source": [
    "### Niestety dane dla mężczyzn są z mniejszej ilości krajów, więc należy wziąć to pod uwagę przy analizie.\n",
    "### Sprawdzę jakie kraje są zawarte w tych danych, czy all. fem mają takie same kraje oraz jakich krajów nie ma w men."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 147,
   "id": "0c81a809-271c-454d-bcfe-a43eab835d81",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['China', 'Republic Of Korea', 'Sweden', 'United Kingdom',\n",
       "       'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus',\n",
       "       'Czech Republic', 'Denmark', 'Finland', 'France', 'Greece',\n",
       "       'Hungary', 'Ireland', 'Latvia', 'Netherlands', 'Portugal',\n",
       "       'Romania', 'Slovenia', 'Spain', 'United States Of America',\n",
       "       'Brazil', 'Italy', \"Lao People'S Democratic Republic\", 'Mexico',\n",
       "       'Mozambique', 'Malaysia', 'Nigeria', 'Pakistan', 'Philippines',\n",
       "       'Burkina Faso', 'Bangladesh', 'Uganda',\n",
       "       'Bolivia (Plurinational State Of)', 'Zambia',\n",
       "       'Democratic Republic Of The Congo', 'Ethiopia', 'Guatemala',\n",
       "       'India'], dtype=object)"
      ]
     },
     "execution_count": 147,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all['Country'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 148,
   "id": "5224bb76-d650-401a-9c46-83ef467b09b6",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['China', 'Republic Of Korea', 'Cyprus', 'Czech Republic',\n",
       "       'Denmark', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland',\n",
       "       'Latvia', 'Netherlands', 'Portugal', 'Romania', 'Slovenia',\n",
       "       'Spain', 'Sweden', 'United Kingdom', 'Austria', 'Belgium',\n",
       "       'Bulgaria', 'Croatia', 'United States Of America', 'Brazil',\n",
       "       'Italy', \"Lao People'S Democratic Republic\", 'Mexico',\n",
       "       'Mozambique', 'Malaysia', 'Nigeria', 'Pakistan', 'Philippines',\n",
       "       'Burkina Faso', 'Bangladesh', 'Uganda',\n",
       "       'Bolivia (Plurinational State Of)', 'Zambia',\n",
       "       'Democratic Republic Of The Congo', 'Ethiopia', 'Guatemala',\n",
       "       'India'], dtype=object)"
      ]
     },
     "execution_count": 148,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_fem['Country'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 149,
   "id": "eae6ea4e-bd80-46d6-8a21-a2960eff9ca9",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['China', 'Republic Of Korea', 'Cyprus', 'Czech Republic',\n",
       "       'Denmark', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland',\n",
       "       'Latvia', 'Netherlands', 'Portugal', 'Romania', 'Slovenia',\n",
       "       'Spain', 'Sweden', 'United Kingdom', 'Austria', 'Belgium',\n",
       "       'Bulgaria', 'Croatia', 'United States Of America', 'Brazil',\n",
       "       'Italy', \"Lao People'S Democratic Republic\", 'Mexico', 'Malaysia',\n",
       "       'Nigeria', 'Burkina Faso', 'Bolivia (Plurinational State Of)',\n",
       "       'Zambia'], dtype=object)"
      ]
     },
     "execution_count": 149,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_men['Country'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 150,
   "id": "af8cd4d0-eb2c-4fc5-9702-45ae91124248",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([], dtype=object)"
      ]
     },
     "execution_count": 150,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "np.setxor1d(food_fem['Country'].unique(), food_all['Country'].unique()) # używam setxor1d z biblioteki numpy żeby sprawdzić czy te same kraje są dla fem i all"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 151,
   "id": "d7ec137f-3251-4db6-bc03-471a815916a7",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['Bangladesh', 'Democratic Republic Of The Congo', 'Ethiopia',\n",
       "       'Guatemala', 'India', 'Mozambique', 'Pakistan', 'Philippines',\n",
       "       'Uganda'], dtype=object)"
      ]
     },
     "execution_count": 151,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "np.setxor1d(food_fem['Country'].unique(), food_men['Country'].unique()) # sprawdzam jakich krajów nie posiadają mężczyźni"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "525e4bce-7da1-47d4-8fca-0be8872b6632",
   "metadata": {},
   "source": [
    "### Jako że jestem przy temacie krajów to sprawdzę czy jest Polska tutaj"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 152,
   "id": "92d5b22a-4596-4196-a1eb-37906a6f7a41",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [Country, Year, FoodCode, FoodName, AgeClass, SourceAgeClass, Gender, Number_of_consumers, Number_of_subjects]\n",
       "Index: []"
      ]
     },
     "execution_count": 152,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all.loc[food_all['Country'] == \"Poland\"]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7878c4c0-40cb-46a5-878e-0a6eda18678d",
   "metadata": {},
   "source": [
    "### Niestety nie ma jej więc wnioski będę wyciągać dla Europy."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cfe06e35-9637-474e-bcd5-59b747a13de4",
   "metadata": {},
   "source": [
    "### <a id=\"ageclass\"></a>[&uarr;](#top) Będę chciał dane sprawdzać dla wszystkich group wiekowych bez rozdzielania dokładnie na grupy więc sprawdzę czy gdy tak filtruje to wszystko jest dobrze."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 153,
   "id": "b6e37fde-028b-4124-b4ee-549d8d4bff9f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>66172</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000N</td>\n",
       "      <td>Buckwheat</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>167</td>\n",
       "      <td>66172</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000P</td>\n",
       "      <td>Barley Grains</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>61</td>\n",
       "      <td>66172</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000T</td>\n",
       "      <td>Maize Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>2422</td>\n",
       "      <td>66172</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>12</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A001B</td>\n",
       "      <td>Common Millet Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>9069</td>\n",
       "      <td>66172</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Country  Year FoodCode             FoodName AgeClass SourceAgeClass Gender  \\\n",
       "0    China  2002    A000G            Oat Grain      All            All    All   \n",
       "3    China  2002    A000N            Buckwheat      All            All    All   \n",
       "6    China  2002    A000P        Barley Grains      All            All    All   \n",
       "9    China  2002    A000T          Maize Grain      All            All    All   \n",
       "12   China  2002    A001B  Common Millet Grain      All            All    All   \n",
       "\n",
       "    Number_of_consumers  Number_of_subjects  \n",
       "0                  1157               66172  \n",
       "3                   167               66172  \n",
       "6                    61               66172  \n",
       "9                  2422               66172  \n",
       "12                 9069               66172  "
      ]
     },
     "execution_count": 153,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_all = food_all.loc[food_all['AgeClass'] == \"All\"]\n",
    "food_fem_all = food_fem.loc[food_fem['AgeClass'] == \"All\"]\n",
    "food_men_all = food_men.loc[food_men['AgeClass'] == \"All\"]\n",
    "food_all_all.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 154,
   "id": "9346ed23-8f62-4183-8c8c-22e4a00968e3",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "23"
      ]
     },
     "execution_count": 154,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_all['Country'].nunique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 155,
   "id": "87923d8b-0f4c-40fc-bcae-db1671568ce8",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "23"
      ]
     },
     "execution_count": 155,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_fem_all['Country'].nunique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 156,
   "id": "627eaef6-5edf-4048-8b8f-20bbe31bd896",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "14"
      ]
     },
     "execution_count": 156,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_men_all['Country'].nunique()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "38e7500d-fcf0-4565-89c3-0cabc20bf956",
   "metadata": {},
   "source": [
    "### O i tutaj jest duży problem przy takim rozdzieleniu ilości krajów są inne niż wczesniej sprawdzałem czyli muszę znaleźć inne rozwiązanie bo wynika z tego że ageclass all nie jest dla wszystkich krajów, niektóre kraje nie mają tego zgrupowanego"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 157,
   "id": "b0ddad70-9344-49d4-bab9-e9abb5c40151",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['Austria', 'Belgium', 'Croatia', 'Cyprus', 'Czech Republic',\n",
       "       'Denmark', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland',\n",
       "       'Latvia', 'Netherlands', 'Portugal', 'Slovenia', 'Spain', 'Sweden',\n",
       "       'United Kingdom'], dtype=object)"
      ]
     },
     "execution_count": 157,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "np.setxor1d(food_all['Country'].unique(), food_all_all['Country'].unique())"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5f3e72fc-1433-486f-a8f9-2968a8dd1112",
   "metadata": {},
   "source": [
    "### tak wstępnie patrząc to wydzhodi na to że z Europy kraje nie mją ageclass All. Na przykładzie Francji sprawdzę jak to dokładnie wygląda."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 158,
   "id": "11285b87-1e88-4cdc-861a-3578d5fe301a",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>37678</th>\n",
       "      <td>France</td>\n",
       "      <td>2007</td>\n",
       "      <td>A03MQ</td>\n",
       "      <td>Shandy</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Male</td>\n",
       "      <td>1</td>\n",
       "      <td>239</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>37679</th>\n",
       "      <td>France</td>\n",
       "      <td>2007</td>\n",
       "      <td>A03MX</td>\n",
       "      <td>Wine, Red</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Female</td>\n",
       "      <td>17</td>\n",
       "      <td>243</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>37680</th>\n",
       "      <td>France</td>\n",
       "      <td>2007</td>\n",
       "      <td>A03MX</td>\n",
       "      <td>Wine, Red</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Male</td>\n",
       "      <td>14</td>\n",
       "      <td>239</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>37681</th>\n",
       "      <td>France</td>\n",
       "      <td>2007</td>\n",
       "      <td>A03MV</td>\n",
       "      <td>Wine, White</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Female</td>\n",
       "      <td>19</td>\n",
       "      <td>243</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>37682</th>\n",
       "      <td>France</td>\n",
       "      <td>2007</td>\n",
       "      <td>A03MV</td>\n",
       "      <td>Wine, White</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Male</td>\n",
       "      <td>13</td>\n",
       "      <td>239</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>173985</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03EA</td>\n",
       "      <td>Soft Drink, With Fruit Juice (Fruit Content Be...</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Very Elderly</td>\n",
       "      <td>All</td>\n",
       "      <td>4</td>\n",
       "      <td>118</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>173986</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03EL</td>\n",
       "      <td>Fruit Soft Drink, Orange</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Very Elderly</td>\n",
       "      <td>All</td>\n",
       "      <td>2</td>\n",
       "      <td>118</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>173987</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03EX</td>\n",
       "      <td>Soft Drink, Flavoured, No Fruit</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Very Elderly</td>\n",
       "      <td>All</td>\n",
       "      <td>1</td>\n",
       "      <td>118</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>173988</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03EY</td>\n",
       "      <td>Soft Drink With Bitter Principle</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Very Elderly</td>\n",
       "      <td>All</td>\n",
       "      <td>2</td>\n",
       "      <td>118</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>173989</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Very Elderly</td>\n",
       "      <td>All</td>\n",
       "      <td>2</td>\n",
       "      <td>118</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>21343 rows × 9 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "       Country  Year FoodCode  \\\n",
       "37678   France  2007    A03MQ   \n",
       "37679   France  2007    A03MX   \n",
       "37680   France  2007    A03MX   \n",
       "37681   France  2007    A03MV   \n",
       "37682   France  2007    A03MV   \n",
       "...        ...   ...      ...   \n",
       "173985  France  2014    A03EA   \n",
       "173986  France  2014    A03EL   \n",
       "173987  France  2014    A03EX   \n",
       "173988  France  2014    A03EY   \n",
       "173989  France  2014    A03FD   \n",
       "\n",
       "                                                 FoodName  \\\n",
       "37678                                              Shandy   \n",
       "37679                                           Wine, Red   \n",
       "37680                                           Wine, Red   \n",
       "37681                                         Wine, White   \n",
       "37682                                         Wine, White   \n",
       "...                                                   ...   \n",
       "173985  Soft Drink, With Fruit Juice (Fruit Content Be...   \n",
       "173986                           Fruit Soft Drink, Orange   \n",
       "173987                    Soft Drink, Flavoured, No Fruit   \n",
       "173988                   Soft Drink With Bitter Principle   \n",
       "173989                   Soft Drink, Flavoured With Herbs   \n",
       "\n",
       "                        AgeClass  SourceAgeClass  Gender  Number_of_consumers  \\\n",
       "37678   Children And Adolescents  Other Children    Male                    1   \n",
       "37679   Children And Adolescents  Other Children  Female                   17   \n",
       "37680   Children And Adolescents  Other Children    Male                   14   \n",
       "37681   Children And Adolescents  Other Children  Female                   19   \n",
       "37682   Children And Adolescents  Other Children    Male                   13   \n",
       "...                          ...             ...     ...                  ...   \n",
       "173985        Adults And Elderly    Very Elderly     All                    4   \n",
       "173986        Adults And Elderly    Very Elderly     All                    2   \n",
       "173987        Adults And Elderly    Very Elderly     All                    1   \n",
       "173988        Adults And Elderly    Very Elderly     All                    2   \n",
       "173989        Adults And Elderly    Very Elderly     All                    2   \n",
       "\n",
       "        Number_of_subjects  \n",
       "37678                  239  \n",
       "37679                  243  \n",
       "37680                  239  \n",
       "37681                  243  \n",
       "37682                  239  \n",
       "...                    ...  \n",
       "173985                 118  \n",
       "173986                 118  \n",
       "173987                 118  \n",
       "173988                 118  \n",
       "173989                 118  \n",
       "\n",
       "[21343 rows x 9 columns]"
      ]
     },
     "execution_count": 158,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_fr = food.loc[food['Country'] == \"France\"] \n",
    "food_fr['AgeClass'].unique()\n",
    "food_fr"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 159,
   "id": "0e8903a3-458a-4b94-baca-722130235f22",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>46892</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Adolescents</td>\n",
       "      <td>Female</td>\n",
       "      <td>74</td>\n",
       "      <td>543</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>46893</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Adolescents</td>\n",
       "      <td>Male</td>\n",
       "      <td>70</td>\n",
       "      <td>587</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>171412</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Adolescents</td>\n",
       "      <td>All</td>\n",
       "      <td>144</td>\n",
       "      <td>1130</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>48840</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Adults</td>\n",
       "      <td>Female</td>\n",
       "      <td>44</td>\n",
       "      <td>1022</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>48841</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Adults</td>\n",
       "      <td>Male</td>\n",
       "      <td>31</td>\n",
       "      <td>751</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>172492</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Adults</td>\n",
       "      <td>All</td>\n",
       "      <td>75</td>\n",
       "      <td>1773</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50326</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Elderly</td>\n",
       "      <td>Male</td>\n",
       "      <td>4</td>\n",
       "      <td>173</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50325</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Elderly</td>\n",
       "      <td>Female</td>\n",
       "      <td>2</td>\n",
       "      <td>211</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>173363</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Elderly</td>\n",
       "      <td>All</td>\n",
       "      <td>6</td>\n",
       "      <td>384</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>45366</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Female</td>\n",
       "      <td>30</td>\n",
       "      <td>424</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>45367</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>Male</td>\n",
       "      <td>23</td>\n",
       "      <td>428</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>170543</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>Other Children</td>\n",
       "      <td>All</td>\n",
       "      <td>53</td>\n",
       "      <td>852</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>43874</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>Toddlers</td>\n",
       "      <td>Female</td>\n",
       "      <td>3</td>\n",
       "      <td>67</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>169694</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>Toddlers</td>\n",
       "      <td>All</td>\n",
       "      <td>3</td>\n",
       "      <td>139</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>51291</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Very Elderly</td>\n",
       "      <td>Male</td>\n",
       "      <td>1</td>\n",
       "      <td>37</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>51290</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Very Elderly</td>\n",
       "      <td>Female</td>\n",
       "      <td>1</td>\n",
       "      <td>81</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>173989</th>\n",
       "      <td>France</td>\n",
       "      <td>2014</td>\n",
       "      <td>A03FD</td>\n",
       "      <td>Soft Drink, Flavoured With Herbs</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>Very Elderly</td>\n",
       "      <td>All</td>\n",
       "      <td>2</td>\n",
       "      <td>118</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       Country  Year FoodCode                          FoodName  \\\n",
       "46892   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "46893   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "171412  France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "48840   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "48841   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "172492  France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "50326   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "50325   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "173363  France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "45366   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "45367   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "170543  France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "43874   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "169694  France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "51291   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "51290   France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "173989  France  2014    A03FD  Soft Drink, Flavoured With Herbs   \n",
       "\n",
       "                        AgeClass  SourceAgeClass  Gender  Number_of_consumers  \\\n",
       "46892   Children And Adolescents     Adolescents  Female                   74   \n",
       "46893   Children And Adolescents     Adolescents    Male                   70   \n",
       "171412  Children And Adolescents     Adolescents     All                  144   \n",
       "48840         Adults And Elderly          Adults  Female                   44   \n",
       "48841         Adults And Elderly          Adults    Male                   31   \n",
       "172492        Adults And Elderly          Adults     All                   75   \n",
       "50326         Adults And Elderly         Elderly    Male                    4   \n",
       "50325         Adults And Elderly         Elderly  Female                    2   \n",
       "173363        Adults And Elderly         Elderly     All                    6   \n",
       "45366   Children And Adolescents  Other Children  Female                   30   \n",
       "45367   Children And Adolescents  Other Children    Male                   23   \n",
       "170543  Children And Adolescents  Other Children     All                   53   \n",
       "43874       Infants And Toddlers        Toddlers  Female                    3   \n",
       "169694      Infants And Toddlers        Toddlers     All                    3   \n",
       "51291         Adults And Elderly    Very Elderly    Male                    1   \n",
       "51290         Adults And Elderly    Very Elderly  Female                    1   \n",
       "173989        Adults And Elderly    Very Elderly     All                    2   \n",
       "\n",
       "        Number_of_subjects  \n",
       "46892                  543  \n",
       "46893                  587  \n",
       "171412                1130  \n",
       "48840                 1022  \n",
       "48841                  751  \n",
       "172492                1773  \n",
       "50326                  173  \n",
       "50325                  211  \n",
       "173363                 384  \n",
       "45366                  424  \n",
       "45367                  428  \n",
       "170543                 852  \n",
       "43874                   67  \n",
       "169694                 139  \n",
       "51291                   37  \n",
       "51290                   81  \n",
       "173989                 118  "
      ]
     },
     "execution_count": 159,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_fr_wine = food_fr.loc[food_fr['FoodName'] == \"Soft Drink, Flavoured With Herbs\"] \n",
    "food_fr_wine.sort_values(by='SourceAgeClass')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5c187989-7eab-4e60-a90f-93d30fbce19c",
   "metadata": {},
   "source": [
    "### oznacza to że muszę znaleźć inny sposob na przedstawienie danych dla wszystkich grup wiekowych. rozwiązaniem może być nieużywanie ageclass all a za to samemu grupować dane dla danego produktu wykożystując to że każde badanie ma unikalną ilość badanych, jest tu ryzko że madania będą miały taka samą ilośc badanych ale na razie nie widzę innej opcji\n",
    "### jako żenie będę rodzielać danych na konkretne grupy wiekowe to sama ich suma mi wystarczy wiec pozbycie sie all i zsumowanie wszystkich wartości robiąc to na podstawie tego że każde badanie ma inną ilośc badanych to nie powinno być tu problemu ale upewnię się\n",
    "### widać że dane female+male=All więc wszystko się pod tym wzgledem zgadza oznacza to że przy rodzielaniu na płcie wszytko idzie dobrze. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 160,
   "id": "072514f4-abaa-4196-b577-37bacf36983c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "243"
      ]
     },
     "execution_count": 160,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all['Number_of_subjects'].nunique()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7f0e0216-db6b-4b43-abc0-bca4108d5022",
   "metadata": {},
   "source": [
    "### znaczy to ze jest grupując tak dane będą z 243 badań brane czyli jest to dobra próba badanych. może znajdę lepszy sposob ale na razie wydaje sie to być najlepsze. \n",
    "### sprawdzę jeszcze na przykładzie chin dla oat grain czy wszystkie wartości dodane do siebie dają tą samą wartość co dla Ageclass All. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 161,
   "id": "a8772aa0-a20a-4555-a16e-5069a3da7a6e",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>All</td>\n",
       "      <td>1157</td>\n",
       "      <td>66172</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>812</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>All</td>\n",
       "      <td>10</td>\n",
       "      <td>838</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1251</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>3-5 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>20</td>\n",
       "      <td>2235</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1782</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Children And Adolescents</td>\n",
       "      <td>6-14 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>107</td>\n",
       "      <td>9844</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2487</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>545</td>\n",
       "      <td>33719</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3267</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>50-74 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>438</td>\n",
       "      <td>18143</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4020</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>&gt;75 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>37</td>\n",
       "      <td>1393</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "     Country  Year FoodCode   FoodName                  AgeClass  \\\n",
       "0      China  2002    A000G  Oat Grain                       All   \n",
       "812    China  2002    A000G  Oat Grain      Infants And Toddlers   \n",
       "1251   China  2002    A000G  Oat Grain  Children And Adolescents   \n",
       "1782   China  2002    A000G  Oat Grain  Children And Adolescents   \n",
       "2487   China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "3267   China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "4020   China  2002    A000G  Oat Grain        Adults And Elderly   \n",
       "\n",
       "     SourceAgeClass Gender  Number_of_consumers  Number_of_subjects  \n",
       "0               All    All                 1157               66172  \n",
       "812     0-35 Months    All                   10                 838  \n",
       "1251      3-5 Years    All                   20                2235  \n",
       "1782     6-14 Years    All                  107                9844  \n",
       "2487    15-49 Years    All                  545               33719  \n",
       "3267    50-74 Years    All                  438               18143  \n",
       "4020      >75 Years    All                   37                1393  "
      ]
     },
     "execution_count": 161,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_oat = food_all.loc[food_all['FoodName'] == \"Oat Grain\"]\n",
    "food_all_oat_ch = food_all_oat.loc[food_all_oat['Country'] == \"China\"]\n",
    "\n",
    "food_all_oat_ch"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 162,
   "id": "2bcc2bc8-8698-421b-afcb-a6a908bb5352",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 162,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all_oat_ch['Number_of_consumers'].iloc[1:].sum()-food_all_oat_ch['Number_of_consumers'].iloc[0]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "82ca6a84-b5f7-4a41-ae8b-cede01b0e998",
   "metadata": {},
   "source": [
    "### wynik jest 0 więc znaczy to że sumy są dobre. Czyli podsumowując moim pomysłem jest usunięcie rzędów z ageclass all i potem samodzielnei grupować dane wykorzstując zależnośc że badania mają różne ilości badanych. czyli teraz usuwam rzędy z ageclass all i wstępnie sprawdzę czy to dobrze działa"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 163,
   "id": "22a3561f-7c7c-486f-9440-7fe8df1d2459",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "8539"
      ]
     },
     "execution_count": 163,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_fr = food_fr.loc[food_fr['Gender'] == \"All\"] \n",
    "food_fr['Number_of_subjects'].unique().sum() # chyba to będzie rozwiązaniem"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 164,
   "id": "698d9f80-eb7f-4b80-aeff-3ae53e0e2391",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>15</th>\n",
       "      <td>France</td>\n",
       "      <td>8539</td>\n",
       "      <td>15546648</td>\n",
       "      <td>A036PA036VA037DA039CA03LGA03HGA03HHA032BA032CA...</td>\n",
       "      <td>Olive OilsRape Seed Oil, EdibleSunflower Seed ...</td>\n",
       "      <td>Infants And ToddlersInfants And ToddlersInfant...</td>\n",
       "      <td>InfantsInfantsInfantsInfantsInfantsInfantsInfa...</td>\n",
       "      <td>AllAllAllAllAllAllAllAllAllAllAllAllAllAllAllA...</td>\n",
       "      <td>503329</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Country  Number_of_subjects      Year  \\\n",
       "15  France                8539  15546648   \n",
       "\n",
       "                                             FoodCode  \\\n",
       "15  A036PA036VA037DA039CA03LGA03HGA03HHA032BA032CA...   \n",
       "\n",
       "                                             FoodName  \\\n",
       "15  Olive OilsRape Seed Oil, EdibleSunflower Seed ...   \n",
       "\n",
       "                                             AgeClass  \\\n",
       "15  Infants And ToddlersInfants And ToddlersInfant...   \n",
       "\n",
       "                                       SourceAgeClass  \\\n",
       "15  InfantsInfantsInfantsInfantsInfantsInfantsInfa...   \n",
       "\n",
       "                                               Gender  Number_of_consumers  \n",
       "15  AllAllAllAllAllAllAllAllAllAllAllAllAllAllAllA...               503329  "
      ]
     },
     "execution_count": 164,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_ctry = food_all.groupby(['Country','Number_of_subjects']).sum().reset_index()\n",
    "food_ctry = food_ctry.groupby(['Country']).sum().reset_index()\n",
    "food_ctry.loc[food_ctry['Country'] == \"France\"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 165,
   "id": "b6621529-073d-46f1-94bf-43846133cc02",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "41"
      ]
     },
     "execution_count": 165,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_ctry['Country'].nunique()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6d64c4c4-e0f5-4c22-9331-feaf87e17c58",
   "metadata": {
    "tags": []
   },
   "source": [
    "### wychodzi na to że ta metoda daję dobrą ilość badnaych wczęsniej zakłądana i nic nei trace w ten sposób a ilość krajów jest dobra"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 166,
   "id": "c77a7526-ee90-422d-8aa5-650d106d4942",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "522791"
      ]
     },
     "execution_count": 166,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "sub_over_time = food_all.groupby(['Year', 'Number_of_subjects']).sum().reset_index()\n",
    "sub_over_time = sub_over_time.groupby(['Year']).sum().reset_index()\n",
    "sub_over_time['Number_of_subjects'].sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 167,
   "id": "46fbab38-213e-48aa-8dbd-634a8e5757d0",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "mask = food['AgeClass']== 'All'\n",
    "food = food[~mask]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 168,
   "id": "f2570cfd-8838-43f8-be92-384246d2e73e",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "food_all = food.loc[food['Gender'] == \"All\"]\n",
    "food_fem = food.loc[food['Gender'] == \"Female\"]\n",
    "food_men = food.loc[food['Gender'] == \"Male\"]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 169,
   "id": "5b04cf57-d040-4d97-bdce-a67ad85bb8e8",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Country                0\n",
       "Year                   0\n",
       "FoodCode               0\n",
       "FoodName               0\n",
       "AgeClass               0\n",
       "SourceAgeClass         0\n",
       "Gender                 0\n",
       "Number_of_consumers    0\n",
       "Number_of_subjects     0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 169,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all.count() + food_fem.count() + food_men.count() - food.count() "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "853f0a09-6ebf-4728-a584-2a33f579fea2",
   "metadata": {},
   "source": [
    "### wychodzi 0 czyli wszystko jest dobrze i nie ma strat"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 170,
   "id": "e94e665b-df79-433f-bfb6-5c8fd273f1f7",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "41"
      ]
     },
     "execution_count": 170,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_all['Country'].nunique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 171,
   "id": "9f4afb91-d465-453e-a48e-d2c306433bfe",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "41"
      ]
     },
     "execution_count": 171,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_fem['Country'].nunique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 172,
   "id": "ff947391-a448-47db-899f-755d1d3ddabe",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "32"
      ]
     },
     "execution_count": 172,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_men['Country'].nunique()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "68c0d4cc-0084-42ab-acaa-c7749e636674",
   "metadata": {},
   "source": [
    "### ilości krajów się zgadzają\n",
    "### chyba wszystkie dane są wyczyszczone i uporządkowane żeby móc robić wykresy, wiem jak osiągnąć najbardziej zbliżony do rzeczywistości wynik wiec wiec wszystko powinno być fine\n",
    "### sprawdzam przy jakim grupowaniu suma Number_of_subjects jest najwieksza i z tej będę kożystac. tak samo będę robić przy innych wykresach"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 173,
   "id": "ac4b2714-69df-459b-ba0f-56bd16cf7b4d",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "312217"
      ]
     },
     "execution_count": 173,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "sub_over_time = food_all.groupby(['Year', 'Number_of_subjects','SourceAgeClass']).sum().reset_index()\n",
    "sub_over_time = sub_over_time.groupby(['Year']).sum().reset_index()\n",
    "sub_over_time['Number_of_subjects'].sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c4466c56-08dd-4462-8c8d-03b35ecba372",
   "metadata": {},
   "source": [
    "# 📊 Wykres: Ilość badanych na przestrzeni lat.<a id=\"sub_over_time\"></a> [&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 174,
   "id": "929e022c-e011-4b0a-b1d3-93eda2e550ec",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "        <script type=\"text/javascript\">\n",
       "        window.PlotlyConfig = {MathJaxConfig: 'local'};\n",
       "        if (window.MathJax && window.MathJax.Hub && window.MathJax.Hub.Config) {window.MathJax.Hub.Config({SVG: {font: \"STIX-Web\"}});}\n",
       "        if (typeof require !== 'undefined') {\n",
       "        require.undef(\"plotly\");\n",
       "        requirejs.config({\n",
       "            paths: {\n",
       "                'plotly': ['https://cdn.plot.ly/plotly-2.12.1.min']\n",
       "            }\n",
       "        });\n",
       "        require(['plotly'], function(Plotly) {\n",
       "            window._Plotly = Plotly;\n",
       "        });\n",
       "        }\n",
       "        </script>\n",
       "        "
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<div>                            <div id=\"e3860080-29d4-468f-b485-715141432e8f\" class=\"plotly-graph-div\" style=\"height:525px; width:100%;\"></div>            <script type=\"text/javascript\">                require([\"plotly\"], function(Plotly) {                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById(\"e3860080-29d4-468f-b485-715141432e8f\")) {                    Plotly.newPlot(                        \"e3860080-29d4-468f-b485-715141432e8f\",                        [{\"hovertemplate\":\"Year=%{x}<br>Number of Subjects=%{y:,}<extra></extra>\",\"legendgroup\":\"\",\"line\":{\"color\":\"#636efa\",\"dash\":\"solid\"},\"marker\":{\"symbol\":\"circle\"},\"mode\":\"lines\",\"name\":\"\",\"orientation\":\"v\",\"showlegend\":false,\"x\":[1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018],\"xaxis\":\"x\",\"y\":[2168,382,410,6094,1750,66833,8687,4971,2700,9023,13649,6484,2075,103733,5996,24453,1700,12207,27950,6377,4001,574],\"yaxis\":\"y\",\"type\":\"scatter\"}],                        {\"template\":{\"data\":{\"histogram2dcontour\":[{\"type\":\"histogram2dcontour\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"choropleth\":[{\"type\":\"choropleth\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}],\"histogram2d\":[{\"type\":\"histogram2d\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"heatmap\":[{\"type\":\"heatmap\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"heatmapgl\":[{\"type\":\"heatmapgl\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"contourcarpet\":[{\"type\":\"contourcarpet\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}],\"contour\":[{\"type\":\"contour\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"surface\":[{\"type\":\"surface\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"mesh3d\":[{\"type\":\"mesh3d\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}],\"scatter\":[{\"fillpattern\":{\"fillmode\":\"overlay\",\"size\":10,\"solidity\":0.2},\"type\":\"scatter\"}],\"parcoords\":[{\"type\":\"parcoords\",\"line\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scatterpolargl\":[{\"type\":\"scatterpolargl\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"bar\":[{\"error_x\":{\"color\":\"#2a3f5f\"},\"error_y\":{\"color\":\"#2a3f5f\"},\"marker\":{\"line\":{\"color\":\"#E5ECF6\",\"width\":0.5},\"pattern\":{\"fillmode\":\"overlay\",\"size\":10,\"solidity\":0.2}},\"type\":\"bar\"}],\"scattergeo\":[{\"type\":\"scattergeo\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scatterpolar\":[{\"type\":\"scatterpolar\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"histogram\":[{\"marker\":{\"pattern\":{\"fillmode\":\"overlay\",\"size\":10,\"solidity\":0.2}},\"type\":\"histogram\"}],\"scattergl\":[{\"type\":\"scattergl\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scatter3d\":[{\"type\":\"scatter3d\",\"line\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}},\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scattermapbox\":[{\"type\":\"scattermapbox\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scatterternary\":[{\"type\":\"scatterternary\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scattercarpet\":[{\"type\":\"scattercarpet\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"carpet\":[{\"aaxis\":{\"endlinecolor\":\"#2a3f5f\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"minorgridcolor\":\"white\",\"startlinecolor\":\"#2a3f5f\"},\"baxis\":{\"endlinecolor\":\"#2a3f5f\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"minorgridcolor\":\"white\",\"startlinecolor\":\"#2a3f5f\"},\"type\":\"carpet\"}],\"table\":[{\"cells\":{\"fill\":{\"color\":\"#EBF0F8\"},\"line\":{\"color\":\"white\"}},\"header\":{\"fill\":{\"color\":\"#C8D4E3\"},\"line\":{\"color\":\"white\"}},\"type\":\"table\"}],\"barpolar\":[{\"marker\":{\"line\":{\"color\":\"#E5ECF6\",\"width\":0.5},\"pattern\":{\"fillmode\":\"overlay\",\"size\":10,\"solidity\":0.2}},\"type\":\"barpolar\"}],\"pie\":[{\"automargin\":true,\"type\":\"pie\"}]},\"layout\":{\"autotypenumbers\":\"strict\",\"colorway\":[\"#636efa\",\"#EF553B\",\"#00cc96\",\"#ab63fa\",\"#FFA15A\",\"#19d3f3\",\"#FF6692\",\"#B6E880\",\"#FF97FF\",\"#FECB52\"],\"font\":{\"color\":\"#2a3f5f\"},\"hovermode\":\"closest\",\"hoverlabel\":{\"align\":\"left\"},\"paper_bgcolor\":\"white\",\"plot_bgcolor\":\"#E5ECF6\",\"polar\":{\"bgcolor\":\"#E5ECF6\",\"angularaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"},\"radialaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"}},\"ternary\":{\"bgcolor\":\"#E5ECF6\",\"aaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"},\"baxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"},\"caxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"}},\"coloraxis\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}},\"colorscale\":{\"sequential\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]],\"sequentialminus\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]],\"diverging\":[[0,\"#8e0152\"],[0.1,\"#c51b7d\"],[0.2,\"#de77ae\"],[0.3,\"#f1b6da\"],[0.4,\"#fde0ef\"],[0.5,\"#f7f7f7\"],[0.6,\"#e6f5d0\"],[0.7,\"#b8e186\"],[0.8,\"#7fbc41\"],[0.9,\"#4d9221\"],[1,\"#276419\"]]},\"xaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\",\"title\":{\"standoff\":15},\"zerolinecolor\":\"white\",\"automargin\":true,\"zerolinewidth\":2},\"yaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\",\"title\":{\"standoff\":15},\"zerolinecolor\":\"white\",\"automargin\":true,\"zerolinewidth\":2},\"scene\":{\"xaxis\":{\"backgroundcolor\":\"#E5ECF6\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"showbackground\":true,\"ticks\":\"\",\"zerolinecolor\":\"white\",\"gridwidth\":2},\"yaxis\":{\"backgroundcolor\":\"#E5ECF6\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"showbackground\":true,\"ticks\":\"\",\"zerolinecolor\":\"white\",\"gridwidth\":2},\"zaxis\":{\"backgroundcolor\":\"#E5ECF6\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"showbackground\":true,\"ticks\":\"\",\"zerolinecolor\":\"white\",\"gridwidth\":2}},\"shapedefaults\":{\"line\":{\"color\":\"#2a3f5f\"}},\"annotationdefaults\":{\"arrowcolor\":\"#2a3f5f\",\"arrowhead\":0,\"arrowwidth\":1},\"geo\":{\"bgcolor\":\"white\",\"landcolor\":\"#E5ECF6\",\"subunitcolor\":\"white\",\"showland\":true,\"showlakes\":true,\"lakecolor\":\"white\"},\"title\":{\"x\":0.05},\"mapbox\":{\"style\":\"light\"}}},\"xaxis\":{\"anchor\":\"y\",\"domain\":[0.0,1.0],\"title\":{\"text\":\"Year\"}},\"yaxis\":{\"anchor\":\"x\",\"domain\":[0.0,1.0],\"title\":{\"text\":\"Number of Subjects\"}},\"legend\":{\"tracegroupgap\":0},\"title\":{\"text\":\"over time\"}},                        {\"responsive\": true}                    ).then(function(){\n",
       "                            \n",
       "var gd = document.getElementById('e3860080-29d4-468f-b485-715141432e8f');\n",
       "var x = new MutationObserver(function (mutations, observer) {{\n",
       "        var display = window.getComputedStyle(gd).display;\n",
       "        if (!display || display === 'none') {{\n",
       "            console.log([gd, 'removed!']);\n",
       "            Plotly.purge(gd);\n",
       "            observer.disconnect();\n",
       "        }}\n",
       "}});\n",
       "\n",
       "// Listen for the removal of the full notebook cells\n",
       "var notebookContainer = gd.closest('#notebook-container');\n",
       "if (notebookContainer) {{\n",
       "    x.observe(notebookContainer, {childList: true});\n",
       "}}\n",
       "\n",
       "// Listen for the clearing of the current output cell\n",
       "var outputEl = gd.closest('.output');\n",
       "if (outputEl) {{\n",
       "    x.observe(outputEl, {childList: true});\n",
       "}}\n",
       "\n",
       "                        })                };                });            </script>        </div>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "hello = px.line(sub_over_time, x=\"Year\", y=\"Number_of_subjects\", title=\"over time\", labels={'Number_of_subjects':'Number of Subjects', 'FoodName': 'Food Names' } , hover_data={'Number_of_subjects':':,'})\n",
    "hello.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0bfcb066-055d-45d3-b78d-0eb4c12e766d",
   "metadata": {},
   "source": [
    "# Wnioski <a id=\"sub_over_time_wnio\"></a> [&uarr;](#top)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cdd6261c-7b76-416a-a287-97734f8cb882",
   "metadata": {},
   "source": [
    "### Jak widać dane są głównie z 202 i 2010. Najwyraźniej wtedy było albo najwieksze badanie albo najwiecej badań. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 175,
   "id": "39825e42-d1e8-4e53-a133-e8623955ad4d",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([   36,   625,   838,  1393,  2235,  9844, 18143, 33719])"
      ]
     },
     "execution_count": 175,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_2002 = food_all.loc[food_all['Year'] == 2002]\n",
    "food_2002 = food_2002.groupby(['Number_of_subjects','SourceAgeClass']).sum().reset_index()\n",
    "food_2002['Number_of_subjects'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 176,
   "id": "7e12b510-0e64-424d-a179-dbc7e6229127",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([    1,     2,    12,    25,    27,    40,    49,    67,    72,\n",
       "         128,   237,   289,   295,   308,   450,   463,   477,   478,\n",
       "         516,   517,  1205,  1418,  1430,  1595,  2669,  4330,  5215,\n",
       "        9446, 33029, 38942])"
      ]
     },
     "execution_count": 176,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_2010 = food_all.loc[food_all['Year'] == 2010]\n",
    "food_2010 = food_2010.groupby(['Number_of_subjects','SourceAgeClass']).sum().reset_index()\n",
    "food_2010['Number_of_subjects'].unique()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8d48f259-0f5f-4402-8089-cb97f0341e73",
   "metadata": {},
   "source": [
    "### jak widać głównie tutaj miały znaczenie duże badania ale również było troche tych badań wiec jest to zawsze plus bo zwiększa to wiarygodność i zmiejsza błąd z badań(jak to ianczej nazwać?)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 177,
   "id": "fb7cba05-36ea-46b6-8dae-79cdfdd466e5",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "312217"
      ]
     },
     "execution_count": 177,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_ctry = food_all.groupby(['Country', 'Number_of_subjects','SourceAgeClass','AgeClass']).sum().reset_index()\n",
    "food_ctry = food_ctry.groupby(['Country', 'Number_of_subjects','SourceAgeClass']).sum().reset_index()\n",
    "food_ctry = food_ctry.groupby(['Country']).sum().reset_index().sort_values(by='Number_of_subjects', ascending=False)\n",
    "\n",
    "food_ctry['Number_of_subjects'].sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ed5f699c-4f33-4d6b-bb29-a30ab905d5d8",
   "metadata": {},
   "source": [
    "# 📊 Wykres: Ilość badanych dla poszczególnych krajów.<a id=\"country_sub\"></a>[&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 178,
   "id": "c59837e7-26bd-406a-8799-d7900bc4fa87",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8005/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x29a5001d0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#testowanie dwustronnego suwaka\n",
    "\n",
    "app = JupyterDash(__name__)\n",
    "server = app.server\n",
    "app.layout = html.Div([\n",
    "    dcc.Graph(id='graph-with-slider'),\n",
    "    dcc.RangeSlider(\n",
    "        min=0,\n",
    "        max=food_ctry['Number_of_subjects'].count(), # max i min wartości możliwe do wyświetlenia\n",
    "        step=1,\n",
    "        id='my-range-slider',\n",
    "\t\tvalue=[0,food_ctry['Number_of_subjects'].count()], #wartości wyswietlane na początku\n",
    "    )\n",
    "    \n",
    "])\n",
    "\n",
    "@app.callback( #porozumiewanie się graphu z suwakiem\n",
    "    Output(\"graph-with-slider\", \"figure\"), \n",
    "    Input('my-range-slider', 'value'))\n",
    "def update_bar_chart(value): #funkcja updateująca wykres\n",
    "    v1=value[0]\n",
    "    v2=value[1] #dzięki takiemu rozdzieleniu mogę przekazać wartości do iloc\n",
    "    dff = food_ctry.iloc[v1:v2] # wybieram z jakiego przedziału dane mają się pokazywać po nr rzędów\n",
    "    fig = px.bar(dff, x=\"Country\", y=\"Number_of_subjects\", title=\"Number of subjects per country\", labels={'Number_of_subjects':'Number of subjects', 'Country': 'Countries' },hover_data={'Number_of_subjects':':,'})\n",
    "    fig.update_xaxes(tickangle=40) #pochylenie nazw na x żeby było łatwiej czytać \n",
    "    return fig\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(mode='inline', port=\"8005\") #mode inline po to żeby wyswietlało się w notebooku, a nie poza. Port dla każdego wykresu korzystającego z JupyterDash będzie inny bo \n",
    "    #inaczej pokazuje się ten sam wykres gdziekolwiek był użyty JupyterDash\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "56001f0a-a944-4184-aa69-74df2809eda6",
   "metadata": {},
   "source": [
    "### <a id=\"country_sub_wnio\"></a>[&uarr;](#top) Na wykresie bardzo dobrze widać jak duża jest dysproporcja, co do ilości osób w zależności od kraju. Znaczy to, że wyciągnięte wnioski mogą być zachwiane i należy o tym pamiętać podczas analizy.\n",
    "### Dla dokładności sprawdzę jak duża jest ta dysproporcja i jak rozkłada się to pod względem kontynentów."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 179,
   "id": "af24aa1b-7523-4934-b3eb-84469eedc648",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "194387"
      ]
     },
     "execution_count": 179,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "top5 = food_ctry['Number_of_subjects'].iloc[0:5].sum()\n",
    "top5"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 180,
   "id": "6e597486-a11e-4a7f-820b-fd72ea2875e9",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "117830"
      ]
     },
     "execution_count": 180,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "rest = food_ctry['Number_of_subjects'].iloc[5:].sum()\n",
    "rest"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 181,
   "id": "ce5bd260-207d-4832-a649-70586e5462b9",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1.6497241789018078"
      ]
     },
     "execution_count": 181,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "top5/rest"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9e58342c-7151-480a-a382-64cc3c2c131c",
   "metadata": {},
   "source": [
    "### Jak widać top 5 krajów ma 1.65 razy więcej badanych niż reszta krajów, jest to bardzo duża dysporporcja, lecz nie dyskredytuje to od razu analizy wszystkich danych.\n",
    "# Tworzenie kolumny z kodami i nazwami kontynentów. <a id=\"kont\"></a>[&uarr;](#top)\n",
    "### Rozbicie na kontynenty, pozwoli zobaczyć jak użyteczna będzie globalna analiza i czy nie lepiej będzie analizować, każdy kontynent odrębnie. Użyję do tego biblioteki pycountry_convert."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 182,
   "id": "e21dc33d-ccaf-49f1-955d-fbd8a3e16370",
   "metadata": {},
   "outputs": [],
   "source": [
    "def convert(row): # funkcja przypisująca kod kontynentu w zależności od kraju\n",
    "    cn_code = pc.country_name_to_country_alpha2(row.Country, cn_name_format=\"default\")\n",
    "    conti_code = pc.country_alpha2_to_continent_code(cn_code)\n",
    "    return conti_code"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "41291385-7792-4115-a95e-a24d3c0d934e",
   "metadata": {},
   "source": [
    "### Trzeba zamienić nazwy kilku krajów, bo biblioteka pycountry_convert korzysta z innych nazw krajów niż te które są w dataframe."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 183,
   "id": "14ca14c2-6e50-4ce3-84eb-d5e3c82fd808",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "continent = food\n",
    "ctry_change = {\n",
    "\t'Republic Of Korea' : 'South Korea',\n",
    "    'Bolivia (Plurinational State Of)' : 'Bolivia',\n",
    "    'United States Of America' : 'United States of America',\n",
    "    \"Lao People'S Democratic Republic\" : \"Lao People's Democratic Republic\",\n",
    "    \"Democratic Republic Of The Congo\" : \"Democratic Republic of the Congo\"\n",
    "}\n",
    "continent = continent.replace(ctry_change)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 184,
   "id": "267f15f1-765c-45dc-bfee-912d6f07c91c",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>ContinentCode</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>812</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>All</td>\n",
       "      <td>10</td>\n",
       "      <td>838</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>813</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>Female</td>\n",
       "      <td>4</td>\n",
       "      <td>376</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>814</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>Male</td>\n",
       "      <td>6</td>\n",
       "      <td>462</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>815</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000T</td>\n",
       "      <td>Maize Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>All</td>\n",
       "      <td>28</td>\n",
       "      <td>838</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>816</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000T</td>\n",
       "      <td>Maize Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>Female</td>\n",
       "      <td>11</td>\n",
       "      <td>376</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272333</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A03LB</td>\n",
       "      <td>Tea Beverages</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>Female</td>\n",
       "      <td>10</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272335</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A03LB</td>\n",
       "      <td>Tea Beverages</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>10</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272337</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A0EQN</td>\n",
       "      <td>Soft Drinks With Minor Amounts Of Fruits Or Fl...</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>Female</td>\n",
       "      <td>8</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272339</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A0EQN</td>\n",
       "      <td>Soft Drinks With Minor Amounts Of Fruits Or Fl...</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>8</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272341</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A0F4S</td>\n",
       "      <td>Coconut Water</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>Female</td>\n",
       "      <td>7</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>255080 rows × 10 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "       Country  Year FoodCode  \\\n",
       "812      China  2002    A000G   \n",
       "813      China  2002    A000G   \n",
       "814      China  2002    A000G   \n",
       "815      China  2002    A000T   \n",
       "816      China  2002    A000T   \n",
       "...        ...   ...      ...   \n",
       "272333   India  2015    A03LB   \n",
       "272335   India  2015    A03LB   \n",
       "272337   India  2015    A0EQN   \n",
       "272339   India  2015    A0EQN   \n",
       "272341   India  2015    A0F4S   \n",
       "\n",
       "                                                 FoodName  \\\n",
       "812                                             Oat Grain   \n",
       "813                                             Oat Grain   \n",
       "814                                             Oat Grain   \n",
       "815                                           Maize Grain   \n",
       "816                                           Maize Grain   \n",
       "...                                                   ...   \n",
       "272333                                      Tea Beverages   \n",
       "272335                                      Tea Beverages   \n",
       "272337  Soft Drinks With Minor Amounts Of Fruits Or Fl...   \n",
       "272339  Soft Drinks With Minor Amounts Of Fruits Or Fl...   \n",
       "272341                                      Coconut Water   \n",
       "\n",
       "                    AgeClass SourceAgeClass  Gender  Number_of_consumers  \\\n",
       "812     Infants And Toddlers    0-35 Months     All                   10   \n",
       "813     Infants And Toddlers    0-35 Months  Female                    4   \n",
       "814     Infants And Toddlers    0-35 Months    Male                    6   \n",
       "815     Infants And Toddlers    0-35 Months     All                   28   \n",
       "816     Infants And Toddlers    0-35 Months  Female                   11   \n",
       "...                      ...            ...     ...                  ...   \n",
       "272333    Adults And Elderly    15-49 Years  Female                   10   \n",
       "272335    Adults And Elderly    15-49 Years     All                   10   \n",
       "272337    Adults And Elderly    15-49 Years  Female                    8   \n",
       "272339    Adults And Elderly    15-49 Years     All                    8   \n",
       "272341    Adults And Elderly    15-49 Years  Female                    7   \n",
       "\n",
       "        Number_of_subjects ContinentCode  \n",
       "812                    838            AS  \n",
       "813                    376            AS  \n",
       "814                    462            AS  \n",
       "815                    838            AS  \n",
       "816                    376            AS  \n",
       "...                    ...           ...  \n",
       "272333                 242            AS  \n",
       "272335                 242            AS  \n",
       "272337                 242            AS  \n",
       "272339                 242            AS  \n",
       "272341                 242            AS  \n",
       "\n",
       "[255080 rows x 10 columns]"
      ]
     },
     "execution_count": 184,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "continent['ContinentCode'] = continent.apply(convert, axis=1)\n",
    "continent"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "91dc6cd2-ae1a-4861-bb2e-2cd4a89d5ba3",
   "metadata": {},
   "source": [
    "### Mam kody kontynentów, więc niby można by tak to zostawić ale uważam, że dużo ładniej i czytelniej jest jak będą też widoczne nazwy kontynentów."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 185,
   "id": "bee7d612-67f0-4924-b731-c9b57019cddb",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['AS', 'EU', 'NA', 'SA', 'AF'], dtype=object)"
      ]
     },
     "execution_count": 185,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "continent['ContinentCode'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 186,
   "id": "dda2555c-eb35-4746-880a-f676baea61ab",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Country</th>\n",
       "      <th>Year</th>\n",
       "      <th>FoodCode</th>\n",
       "      <th>FoodName</th>\n",
       "      <th>AgeClass</th>\n",
       "      <th>SourceAgeClass</th>\n",
       "      <th>Gender</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>ContinentCode</th>\n",
       "      <th>Continent</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>812</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>All</td>\n",
       "      <td>10</td>\n",
       "      <td>838</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>813</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>Female</td>\n",
       "      <td>4</td>\n",
       "      <td>376</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>814</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000G</td>\n",
       "      <td>Oat Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>Male</td>\n",
       "      <td>6</td>\n",
       "      <td>462</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>815</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000T</td>\n",
       "      <td>Maize Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>All</td>\n",
       "      <td>28</td>\n",
       "      <td>838</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>816</th>\n",
       "      <td>China</td>\n",
       "      <td>2002</td>\n",
       "      <td>A000T</td>\n",
       "      <td>Maize Grain</td>\n",
       "      <td>Infants And Toddlers</td>\n",
       "      <td>0-35 Months</td>\n",
       "      <td>Female</td>\n",
       "      <td>11</td>\n",
       "      <td>376</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272333</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A03LB</td>\n",
       "      <td>Tea Beverages</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>Female</td>\n",
       "      <td>10</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272335</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A03LB</td>\n",
       "      <td>Tea Beverages</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>10</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272337</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A0EQN</td>\n",
       "      <td>Soft Drinks With Minor Amounts Of Fruits Or Fl...</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>Female</td>\n",
       "      <td>8</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272339</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A0EQN</td>\n",
       "      <td>Soft Drinks With Minor Amounts Of Fruits Or Fl...</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>All</td>\n",
       "      <td>8</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>272341</th>\n",
       "      <td>India</td>\n",
       "      <td>2015</td>\n",
       "      <td>A0F4S</td>\n",
       "      <td>Coconut Water</td>\n",
       "      <td>Adults And Elderly</td>\n",
       "      <td>15-49 Years</td>\n",
       "      <td>Female</td>\n",
       "      <td>7</td>\n",
       "      <td>242</td>\n",
       "      <td>AS</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>255080 rows × 11 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "       Country  Year FoodCode  \\\n",
       "812      China  2002    A000G   \n",
       "813      China  2002    A000G   \n",
       "814      China  2002    A000G   \n",
       "815      China  2002    A000T   \n",
       "816      China  2002    A000T   \n",
       "...        ...   ...      ...   \n",
       "272333   India  2015    A03LB   \n",
       "272335   India  2015    A03LB   \n",
       "272337   India  2015    A0EQN   \n",
       "272339   India  2015    A0EQN   \n",
       "272341   India  2015    A0F4S   \n",
       "\n",
       "                                                 FoodName  \\\n",
       "812                                             Oat Grain   \n",
       "813                                             Oat Grain   \n",
       "814                                             Oat Grain   \n",
       "815                                           Maize Grain   \n",
       "816                                           Maize Grain   \n",
       "...                                                   ...   \n",
       "272333                                      Tea Beverages   \n",
       "272335                                      Tea Beverages   \n",
       "272337  Soft Drinks With Minor Amounts Of Fruits Or Fl...   \n",
       "272339  Soft Drinks With Minor Amounts Of Fruits Or Fl...   \n",
       "272341                                      Coconut Water   \n",
       "\n",
       "                    AgeClass SourceAgeClass  Gender  Number_of_consumers  \\\n",
       "812     Infants And Toddlers    0-35 Months     All                   10   \n",
       "813     Infants And Toddlers    0-35 Months  Female                    4   \n",
       "814     Infants And Toddlers    0-35 Months    Male                    6   \n",
       "815     Infants And Toddlers    0-35 Months     All                   28   \n",
       "816     Infants And Toddlers    0-35 Months  Female                   11   \n",
       "...                      ...            ...     ...                  ...   \n",
       "272333    Adults And Elderly    15-49 Years  Female                   10   \n",
       "272335    Adults And Elderly    15-49 Years     All                   10   \n",
       "272337    Adults And Elderly    15-49 Years  Female                    8   \n",
       "272339    Adults And Elderly    15-49 Years     All                    8   \n",
       "272341    Adults And Elderly    15-49 Years  Female                    7   \n",
       "\n",
       "        Number_of_subjects ContinentCode Continent  \n",
       "812                    838            AS      Asia  \n",
       "813                    376            AS      Asia  \n",
       "814                    462            AS      Asia  \n",
       "815                    838            AS      Asia  \n",
       "816                    376            AS      Asia  \n",
       "...                    ...           ...       ...  \n",
       "272333                 242            AS      Asia  \n",
       "272335                 242            AS      Asia  \n",
       "272337                 242            AS      Asia  \n",
       "272339                 242            AS      Asia  \n",
       "272341                 242            AS      Asia  \n",
       "\n",
       "[255080 rows x 11 columns]"
      ]
     },
     "execution_count": 186,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "conti_names = {\t# stworzenie słownika dla kontynentów, żeby móc zamienić kody kontynentów na nazwy kontynentów\n",
    "\t\t\t\t'AS' : 'Asia',\n",
    "\t\t\t\t'EU' : 'Europe',\n",
    "                'NA' : 'North America',\n",
    "                'SA' : 'South America',\n",
    "                'AF' : 'Africa'\n",
    "                }\n",
    "continent['Continent'] = continent['ContinentCode'].map(conti_names)\n",
    "continent"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 187,
   "id": "9870ccc0-c284-4459-81d8-fa227bf7884e",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['Asia', 'Europe', 'North America', 'South America', 'Africa'],\n",
       "      dtype=object)"
      ]
     },
     "execution_count": 187,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "continent['Continent'].unique()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "82f86ce0-1381-4833-9428-c53e6a05ad2e",
   "metadata": {},
   "source": [
    "### Jak widać wszystko ładnie się udało, więc mogę przypisać continent do food i ponownie stworzyć dataframes dla każdej płci."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 188,
   "id": "522f7694-a8a0-49d5-bae0-59e6afb33346",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "food = continent\n",
    "\n",
    "food_all = food.loc[food['Gender'] == \"All\"]\n",
    "food_fem = food.loc[food['Gender'] == \"Female\"]\n",
    "food_men = food.loc[food['Gender'] == \"Male\"]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 189,
   "id": "9cb59eaf-9e63-49ac-a2b6-be20bf4c25fd",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "ContinentCode         SAASSAASASNAASASNANANAEUNAEUNAASEUASEUEUEUEUEU...\n",
       "Number_of_subjects                                               312217\n",
       "dtype: object"
      ]
     },
     "execution_count": 189,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_con = food_all.groupby(['Country','SourceAgeClass','ContinentCode','Number_of_subjects']).sum().reset_index()\n",
    "food_con = food_con[['ContinentCode','Number_of_subjects']].sort_values(by='Number_of_subjects', ascending=False)\n",
    "\n",
    "food_con.sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ba0b15aa-d41d-4373-bcd3-74abc160a2a1",
   "metadata": {},
   "source": [
    "### Ilość subjectów jest taka jak wczesniej czyli 312217 wiec super"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6b8edabb-4751-4bd8-b391-b26000d1839f",
   "metadata": {},
   "source": [
    "###  Niestety kontynenty też są zgrupowane, więc muszę odciać wszystko poza pierwszymi literami kodu, co pozwoli to dobrze podsumować.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 190,
   "id": "2b6581c2-12b9-4420-a123-158cff31aa94",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ContinentCode</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>EU</td>\n",
       "      <td>99205</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>AS</td>\n",
       "      <td>97308</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>SA</td>\n",
       "      <td>72124</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>NA</td>\n",
       "      <td>37676</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>AF</td>\n",
       "      <td>5904</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  ContinentCode  Number_of_subjects\n",
       "2            EU               99205\n",
       "1            AS               97308\n",
       "4            SA               72124\n",
       "3            NA               37676\n",
       "0            AF                5904"
      ]
     },
     "execution_count": 190,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_con['ContinentCode'] = food_con['ContinentCode'].apply(lambda x: x[0:2])\n",
    "food_con = food_con.groupby(['ContinentCode']).sum().reset_index().sort_values(by='Number_of_subjects', ascending=False)\n",
    "food_con"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5c26d809-fc14-40d7-b92c-92daf3d601f6",
   "metadata": {},
   "source": [
    "### Wszystko poszło dobrze, więc mogę teraz wizualizować, tylko jeszcze dodam nazwy kontynentów."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 191,
   "id": "5fbd4f84-323b-447c-bf3b-85c5be2453bd",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ContinentCode</th>\n",
       "      <th>Number_of_subjects</th>\n",
       "      <th>Continent</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>EU</td>\n",
       "      <td>99205</td>\n",
       "      <td>Europe</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>AS</td>\n",
       "      <td>97308</td>\n",
       "      <td>Asia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>SA</td>\n",
       "      <td>72124</td>\n",
       "      <td>South America</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>NA</td>\n",
       "      <td>37676</td>\n",
       "      <td>North America</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>AF</td>\n",
       "      <td>5904</td>\n",
       "      <td>Africa</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  ContinentCode  Number_of_subjects      Continent\n",
       "2            EU               99205         Europe\n",
       "1            AS               97308           Asia\n",
       "4            SA               72124  South America\n",
       "3            NA               37676  North America\n",
       "0            AF                5904         Africa"
      ]
     },
     "execution_count": 191,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "food_con['Continent'] = food_con['ContinentCode'].map(conti_names)\n",
    "food_con"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b7872ff3-13ce-472b-911a-f72f26c33cc5",
   "metadata": {},
   "source": [
    "# 📊 Wykres: Procentowy udział badanych patrząc na kontynent.<a id=\"kont_sub\"></a> [&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 192,
   "id": "df1409fb-2b96-4e5a-a8c3-fe99a9d6d88e",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>                            <div id=\"470a5171-38d6-4777-a986-e50000a12b1f\" class=\"plotly-graph-div\" style=\"height:525px; width:100%;\"></div>            <script type=\"text/javascript\">                require([\"plotly\"], function(Plotly) {                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById(\"470a5171-38d6-4777-a986-e50000a12b1f\")) {                    Plotly.newPlot(                        \"470a5171-38d6-4777-a986-e50000a12b1f\",                        [{\"customdata\":[[99205],[97308],[72124],[37676],[5904]],\"domain\":{\"x\":[0.0,1.0],\"y\":[0.0,1.0]},\"hovertemplate\":\"Continent=%{label}<br>Number_of_subjects=%{customdata[0]:,}<extra></extra>\",\"labels\":[\"Europe\",\"Asia\",\"South America\",\"North America\",\"Africa\"],\"legendgroup\":\"\",\"name\":\"\",\"showlegend\":true,\"values\":[99205,97308,72124,37676,5904],\"type\":\"pie\"}],                        {\"template\":{\"data\":{\"histogram2dcontour\":[{\"type\":\"histogram2dcontour\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"choropleth\":[{\"type\":\"choropleth\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}],\"histogram2d\":[{\"type\":\"histogram2d\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"heatmap\":[{\"type\":\"heatmap\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"heatmapgl\":[{\"type\":\"heatmapgl\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"contourcarpet\":[{\"type\":\"contourcarpet\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}],\"contour\":[{\"type\":\"contour\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"surface\":[{\"type\":\"surface\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"},\"colorscale\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]]}],\"mesh3d\":[{\"type\":\"mesh3d\",\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}],\"scatter\":[{\"fillpattern\":{\"fillmode\":\"overlay\",\"size\":10,\"solidity\":0.2},\"type\":\"scatter\"}],\"parcoords\":[{\"type\":\"parcoords\",\"line\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scatterpolargl\":[{\"type\":\"scatterpolargl\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"bar\":[{\"error_x\":{\"color\":\"#2a3f5f\"},\"error_y\":{\"color\":\"#2a3f5f\"},\"marker\":{\"line\":{\"color\":\"#E5ECF6\",\"width\":0.5},\"pattern\":{\"fillmode\":\"overlay\",\"size\":10,\"solidity\":0.2}},\"type\":\"bar\"}],\"scattergeo\":[{\"type\":\"scattergeo\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scatterpolar\":[{\"type\":\"scatterpolar\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"histogram\":[{\"marker\":{\"pattern\":{\"fillmode\":\"overlay\",\"size\":10,\"solidity\":0.2}},\"type\":\"histogram\"}],\"scattergl\":[{\"type\":\"scattergl\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scatter3d\":[{\"type\":\"scatter3d\",\"line\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}},\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scattermapbox\":[{\"type\":\"scattermapbox\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scatterternary\":[{\"type\":\"scatterternary\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"scattercarpet\":[{\"type\":\"scattercarpet\",\"marker\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}}}],\"carpet\":[{\"aaxis\":{\"endlinecolor\":\"#2a3f5f\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"minorgridcolor\":\"white\",\"startlinecolor\":\"#2a3f5f\"},\"baxis\":{\"endlinecolor\":\"#2a3f5f\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"minorgridcolor\":\"white\",\"startlinecolor\":\"#2a3f5f\"},\"type\":\"carpet\"}],\"table\":[{\"cells\":{\"fill\":{\"color\":\"#EBF0F8\"},\"line\":{\"color\":\"white\"}},\"header\":{\"fill\":{\"color\":\"#C8D4E3\"},\"line\":{\"color\":\"white\"}},\"type\":\"table\"}],\"barpolar\":[{\"marker\":{\"line\":{\"color\":\"#E5ECF6\",\"width\":0.5},\"pattern\":{\"fillmode\":\"overlay\",\"size\":10,\"solidity\":0.2}},\"type\":\"barpolar\"}],\"pie\":[{\"automargin\":true,\"type\":\"pie\"}]},\"layout\":{\"autotypenumbers\":\"strict\",\"colorway\":[\"#636efa\",\"#EF553B\",\"#00cc96\",\"#ab63fa\",\"#FFA15A\",\"#19d3f3\",\"#FF6692\",\"#B6E880\",\"#FF97FF\",\"#FECB52\"],\"font\":{\"color\":\"#2a3f5f\"},\"hovermode\":\"closest\",\"hoverlabel\":{\"align\":\"left\"},\"paper_bgcolor\":\"white\",\"plot_bgcolor\":\"#E5ECF6\",\"polar\":{\"bgcolor\":\"#E5ECF6\",\"angularaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"},\"radialaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"}},\"ternary\":{\"bgcolor\":\"#E5ECF6\",\"aaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"},\"baxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"},\"caxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\"}},\"coloraxis\":{\"colorbar\":{\"outlinewidth\":0,\"ticks\":\"\"}},\"colorscale\":{\"sequential\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]],\"sequentialminus\":[[0.0,\"#0d0887\"],[0.1111111111111111,\"#46039f\"],[0.2222222222222222,\"#7201a8\"],[0.3333333333333333,\"#9c179e\"],[0.4444444444444444,\"#bd3786\"],[0.5555555555555556,\"#d8576b\"],[0.6666666666666666,\"#ed7953\"],[0.7777777777777778,\"#fb9f3a\"],[0.8888888888888888,\"#fdca26\"],[1.0,\"#f0f921\"]],\"diverging\":[[0,\"#8e0152\"],[0.1,\"#c51b7d\"],[0.2,\"#de77ae\"],[0.3,\"#f1b6da\"],[0.4,\"#fde0ef\"],[0.5,\"#f7f7f7\"],[0.6,\"#e6f5d0\"],[0.7,\"#b8e186\"],[0.8,\"#7fbc41\"],[0.9,\"#4d9221\"],[1,\"#276419\"]]},\"xaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\",\"title\":{\"standoff\":15},\"zerolinecolor\":\"white\",\"automargin\":true,\"zerolinewidth\":2},\"yaxis\":{\"gridcolor\":\"white\",\"linecolor\":\"white\",\"ticks\":\"\",\"title\":{\"standoff\":15},\"zerolinecolor\":\"white\",\"automargin\":true,\"zerolinewidth\":2},\"scene\":{\"xaxis\":{\"backgroundcolor\":\"#E5ECF6\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"showbackground\":true,\"ticks\":\"\",\"zerolinecolor\":\"white\",\"gridwidth\":2},\"yaxis\":{\"backgroundcolor\":\"#E5ECF6\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"showbackground\":true,\"ticks\":\"\",\"zerolinecolor\":\"white\",\"gridwidth\":2},\"zaxis\":{\"backgroundcolor\":\"#E5ECF6\",\"gridcolor\":\"white\",\"linecolor\":\"white\",\"showbackground\":true,\"ticks\":\"\",\"zerolinecolor\":\"white\",\"gridwidth\":2}},\"shapedefaults\":{\"line\":{\"color\":\"#2a3f5f\"}},\"annotationdefaults\":{\"arrowcolor\":\"#2a3f5f\",\"arrowhead\":0,\"arrowwidth\":1},\"geo\":{\"bgcolor\":\"white\",\"landcolor\":\"#E5ECF6\",\"subunitcolor\":\"white\",\"showland\":true,\"showlakes\":true,\"lakecolor\":\"white\"},\"title\":{\"x\":0.05},\"mapbox\":{\"style\":\"light\"}}},\"legend\":{\"tracegroupgap\":0},\"title\":{\"text\":\"Percent of subjects per Continents\"},\"piecolorway\":[\"rgb(103,0,31)\",\"rgb(178,24,43)\",\"rgb(214,96,77)\",\"rgb(244,165,130)\",\"rgb(253,219,199)\",\"rgb(247,247,247)\",\"rgb(209,229,240)\",\"rgb(146,197,222)\",\"rgb(67,147,195)\",\"rgb(33,102,172)\",\"rgb(5,48,97)\"]},                        {\"responsive\": true}                    ).then(function(){\n",
       "                            \n",
       "var gd = document.getElementById('470a5171-38d6-4777-a986-e50000a12b1f');\n",
       "var x = new MutationObserver(function (mutations, observer) {{\n",
       "        var display = window.getComputedStyle(gd).display;\n",
       "        if (!display || display === 'none') {{\n",
       "            console.log([gd, 'removed!']);\n",
       "            Plotly.purge(gd);\n",
       "            observer.disconnect();\n",
       "        }}\n",
       "}});\n",
       "\n",
       "// Listen for the removal of the full notebook cells\n",
       "var notebookContainer = gd.closest('#notebook-container');\n",
       "if (notebookContainer) {{\n",
       "    x.observe(notebookContainer, {childList: true});\n",
       "}}\n",
       "\n",
       "// Listen for the clearing of the current output cell\n",
       "var outputEl = gd.closest('.output');\n",
       "if (outputEl) {{\n",
       "    x.observe(outputEl, {childList: true});\n",
       "}}\n",
       "\n",
       "                        })                };                });            </script>        </div>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig = px.pie(food_con, values='Number_of_subjects', names='Continent', title='Percent of subjects per Continents',color_discrete_sequence=px.colors.sequential.RdBu, hover_data={'Number_of_subjects':':,'})\n",
    "fig.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cbebd619-2db1-40de-b648-f7dafbbbeb82",
   "metadata": {
    "tags": []
   },
   "source": [
    "### <a id=\"kont_sub_wnio\"></a> [&uarr;](#top) Na tym wykresie widać, ze rozłożenie badancyh między kontynentami nie jest takie złe. Wiadomo Afryka najgorzej wypada i gdyby chcieć wyciągnąć informacje dla Afryki, to można to robić tylko dla Afryki i nie sugerować się ogólnymi wynikami. Natomiast reszta kontynentów nawet równo się rozkłada, nadal dla dokładnych informacji należy sprawdzać konkretne kontynenty ale i tak już ogólna analiza może dać sensowne informacje."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "23b697fc-cb4e-4253-b95f-d5069264fcdb",
   "metadata": {},
   "source": [
    "### Teraz czas na sprawdzenie najpopularniejszych produktów"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 193,
   "id": "a00036e3-a4cf-4dce-b1f5-66f4345638e9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>FoodName</th>\n",
       "      <th>Number_of_consumers</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>(All Cereals)</td>\n",
       "      <td>142214</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2811</th>\n",
       "      <td>Wheat Bread And Rolls, White (Refined Flour)</td>\n",
       "      <td>135436</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1836</th>\n",
       "      <td>Onions</td>\n",
       "      <td>112344</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2249</th>\n",
       "      <td>Rice Grain, Polished</td>\n",
       "      <td>105857</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1997</th>\n",
       "      <td>Pig Fresh Meat</td>\n",
       "      <td>104118</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2652</th>\n",
       "      <td>Tap Water</td>\n",
       "      <td>92605</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2092</th>\n",
       "      <td>Potatoes</td>\n",
       "      <td>89154</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>375</th>\n",
       "      <td>Carrots</td>\n",
       "      <td>87843</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1126</th>\n",
       "      <td>Garlic</td>\n",
       "      <td>84415</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2243</th>\n",
       "      <td>Rice Grain</td>\n",
       "      <td>82719</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                          FoodName  Number_of_consumers\n",
       "1                                    (All Cereals)               142214\n",
       "2811  Wheat Bread And Rolls, White (Refined Flour)               135436\n",
       "1836                                        Onions               112344\n",
       "2249                          Rice Grain, Polished               105857\n",
       "1997                                Pig Fresh Meat               104118\n",
       "2652                                     Tap Water                92605\n",
       "2092                                      Potatoes                89154\n",
       "375                                        Carrots                87843\n",
       "1126                                        Garlic                84415\n",
       "2243                                    Rice Grain                82719"
      ]
     },
     "execution_count": 193,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "most_consumed_all = food_all.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)\n",
    "most_consumed_fem = food_fem.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)\n",
    "most_consumed_men = food_men.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)\n",
    "most_consumed_all[['FoodName','Number_of_consumers']].head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7109d4a9-0139-468b-82f2-ac8522d49d50",
   "metadata": {},
   "source": [
    "# 📊 Wykres: Najpopularniejsze produkty na świecie. <a id=\"food_world\"></a>[&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 194,
   "id": "bc27c113-cc57-4673-a3cf-8d83c76e8f2a",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8006/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x2a5ec0750>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "app = JupyterDash(__name__)\n",
    "server = app.server\n",
    "app.layout = html.Div([\n",
    "    dcc.Graph(id='graph-with-slider'),\n",
    "    dcc.RangeSlider(\n",
    "        min=0,\n",
    "        max=75, \n",
    "        step=1,\n",
    "        id='my-range-slider',\n",
    "\t\tvalue=[0,30], \n",
    "    )\n",
    "    \n",
    "])\n",
    "\n",
    "@app.callback( \n",
    "    Output(\"graph-with-slider\", \"figure\"), \n",
    "    Input('my-range-slider', 'value'))\n",
    "def update_bar_chart(value):\n",
    "    v1=value[0]\n",
    "    v2=value[1] \n",
    "    dff = most_consumed_all.iloc[v1:v2] \n",
    "    fig = px.bar(dff, x=\"FoodName\", y=\"Number_of_consumers\", \n",
    "       \ttitle=\"Most popular foods in the World\", \n",
    "       \tlabels={'Number_of_consumers':'Number of comsumers', 'FoodName': 'Food Names' },\n",
    "      \tcolor_discrete_sequence=[\"green\"],\n",
    "        hover_data={'Number_of_consumers':':,'})\n",
    "    fig.update_xaxes(tickangle=40) \n",
    "    return fig\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(mode='inline', port=\"8006\") "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "018c8139-d2fb-4d57-bd90-7a9a38f8921c",
   "metadata": {},
   "source": [
    "# 📊 Wykres: Najpopularniejsze produkty w Europie. <a id=\"food_eu\"></a>[&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 195,
   "id": "fe42f10f-b3a7-4926-b961-03b70aa4df88",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "food_all = food.loc[food['Gender'] == \"All\"]\n",
    "food_all_eu = food_all.loc[food_all['Continent'] == \"Europe\"]\n",
    "most_consumed_all_eu = food_all_eu.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 196,
   "id": "ae678349-fe35-48b0-b131-af32f767bf35",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8015/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x29a503790>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "app = JupyterDash(__name__)\n",
    "server = app.server\n",
    "app.layout = html.Div([\n",
    "    dcc.Graph(id='graph-with-slider'),\n",
    "    dcc.RangeSlider(\n",
    "        min=0,\n",
    "        max=75, \n",
    "        step=1,\n",
    "        id='my-range-slider',\n",
    "\t\tvalue=[0,30], \n",
    "    )\n",
    "    \n",
    "])\n",
    "\n",
    "@app.callback( \n",
    "    Output(\"graph-with-slider\", \"figure\"), \n",
    "    Input('my-range-slider', 'value'))\n",
    "def update_bar_chart(value): \n",
    "    v1=value[0]\n",
    "    v2=value[1] \n",
    "    dff = most_consumed_all_eu.iloc[v1:v2] \n",
    "    fig = px.bar(dff, x=\"FoodName\", y=\"Number_of_consumers\", \n",
    "       title=\"Most popular food in Europe\", \n",
    "       labels={'Number_of_consumers':'Number of comsumers', 'FoodName': 'Food Names' },\n",
    "      \tcolor_discrete_sequence=[\"blue\"],\n",
    "        hover_data={'Number_of_consumers':':,'})\n",
    "    fig.update_xaxes(tickangle=40)\n",
    "    return fig\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(mode='inline',port=\"8015\") "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2178580a-9321-482f-8da5-f6c5010c0da5",
   "metadata": {},
   "source": [
    "### Dla wygody porównywania dodamn te wykresy obok siebie."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b6ddb38e-be0c-43b9-bc79-6f0800e529bc",
   "metadata": {},
   "source": [
    "# 📊 Wykresy: Porównanie wykresów najpopularniejsze produkty na świecie i w Europie <a id=\"food_world_eu\"></a>[&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 197,
   "id": "b3890473-4b9f-47a9-b60a-a0c03523b21f",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8007/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x2c16fc4d0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "app = JupyterDash(__name__)\n",
    "server = app.server\n",
    "app.layout = html.Div([\n",
    "    dcc.Graph(id='graph-with-slider'),\n",
    "    dcc.RangeSlider(\n",
    "        min=0,\n",
    "        max=75, \n",
    "        step=1,\n",
    "        id='my-range-slider',\n",
    "\t\tvalue=[0,30], \n",
    "    )\n",
    "    \n",
    "])\n",
    "\n",
    "@app.callback( \n",
    "    Output(\"graph-with-slider\", \"figure\"), \n",
    "    Input('my-range-slider', 'value'))\n",
    "def update_bar_chart(value): \n",
    "    v1=value[0]\n",
    "    v2=value[1] \n",
    "    dff_world = most_consumed_all.iloc[v1:v2] \n",
    "    dff_eu = most_consumed_all_eu.iloc[v1:v2]\n",
    "    first_line = go.Bar(x=dff_eu[\"FoodName\"], y=dff_eu[\"Number_of_consumers\"], name=\"Europe\", marker=dict(color='blue'), hovertemplate = 'Number of consumers=%{y:,}')\n",
    "    second_line = go.Bar(x=dff_world[\"FoodName\"], y=dff_world[\"Number_of_consumers\"], name=\"World\", marker=dict(color='green'), hovertemplate = 'Number of consumers=%{y:,}')\n",
    "    fig = make_subplots(rows=1, cols=2)\n",
    "    fig.add_trace(first_line,row=1, col=1)\n",
    "    fig.add_trace(second_line,row=1, col=2)\n",
    "    fig.update_layout(title_text=\"Most popular foods for Europe and World\")\n",
    "    fig.update_xaxes(tickangle=40) \n",
    "    \n",
    "    return fig\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(mode='inline', port=\"8007\") "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "393c8768-66ca-40f4-b507-1c27879a57ee",
   "metadata": {},
   "source": [
    "### <a id=\"food_world_eu_wnio\"></a>[&uarr;](#top) Porównując dwa wykresy widać, że Europa zamiast płatków śniadaniowych na pierszym miejscu ma wodę z kranu. Może to być połączone z wyższym bezpieczeństwem wody z kranu w Europie [[3]](#źr). Następnie należy sie zastanowić nad wysokim miejscem pieczywa białego, cebuli, marchewki, masła, kurczaka, pomidorów, czosnku, oliwy z oliwek i mleka. Powodem może być duży wpływ Francji i Włoch na kuchnię Europy.\n",
    "### Mleko które też jak widać częściej jest spożywane w Europie niż w reszcie świata, co może wynikać z mniejszej nietoleracji laktozy w Europie [[5]](#źr). Wysokie miejsce margaryny, soli i cukru może tłumaczyć częste zachorowania na wysokie ciśnienie tętnicze[[4]](#źr)."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "77650cab-ec8e-41f6-a96f-df64b044ee07",
   "metadata": {},
   "source": [
    "# 📊 Wykresy: Najpopularniejsze produkty u mężczyzn i kobiet. <a id=\"food_world_gen\"></a>[&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 198,
   "id": "58cb8ce6-3edb-4bcb-9e27-86f6069be670",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8008/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x2a5ec2f10>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "app = JupyterDash(__name__)\n",
    "server = app.server\n",
    "app.layout = html.Div([\n",
    "    dcc.Graph(id='graph-with-slider'),\n",
    "    dcc.RangeSlider(\n",
    "        min=0,\n",
    "        max=75, \n",
    "        step=1,\n",
    "        id='my-range-slider',\n",
    "\t\tvalue=[0,30], \n",
    "    )\n",
    "    \n",
    "])\n",
    "\n",
    "@app.callback(\n",
    "    Output(\"graph-with-slider\", \"figure\"), \n",
    "    Input('my-range-slider', 'value'))\n",
    "def update_bar_chart(value): \n",
    "    v1=value[0]\n",
    "    v2=value[1] \n",
    "    dff_men = most_consumed_men.iloc[v1:v2] \n",
    "    dff_fem = most_consumed_fem.iloc[v1:v2]\n",
    "    first_line = go.Bar(x=dff_men[\"FoodName\"], y=dff_men[\"Number_of_consumers\"], name=\"Male\", hovertemplate = 'Number of consumers=%{y:,}')\n",
    "    second_line = go.Bar(x=dff_fem[\"FoodName\"], y=dff_fem[\"Number_of_consumers\"], name=\"Female\", hovertemplate = 'Number of consumers=%{y:,}')\n",
    "    fig = make_subplots(rows=1, cols=2)\n",
    "    fig.add_trace(first_line,row=1, col=1)\n",
    "    fig.add_trace(second_line,row=1, col=2)\n",
    "    fig.update_layout(title_text=\"Most popular foods for men and women\")\n",
    "    fig.update_xaxes(tickangle=40) \n",
    "    return fig\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(mode='inline',port=\"8008\") "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "eb4cd72d-e46c-4adb-8230-1a72fc2ee6b8",
   "metadata": {},
   "source": [
    "### <a id=\"food_world_gen_wnio\"></a>[&uarr;](#top) Nie ma dużej różnicy między płciami jedynie kobiety mają na wyższym miejscu płatki śniadaniowe oraz warzywa i ryż, a natomiast mężczyźni mają na wyższym miejscu białą mąkę, białe pieczywo i mięso wieprzowe."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "550303e9-f901-46b3-91dd-031310623649",
   "metadata": {},
   "source": [
    "# Wykresy: najpopularniejsze produkty dla mężczyzn i kobiet w Europie. <a id=\"food_eu_gen\"></a>[&uarr;](#top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 199,
   "id": "1e2076c4-95ed-4b39-b235-a758eeae73bc",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8009/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x2c2174610>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "food_fem_eu = food_fem.loc[food_fem['Continent'] == \"Europe\"]\n",
    "food_men_eu = food_men.loc[food_men['Continent'] == \"Europe\"]\n",
    "most_consumed_fem_eu = food_fem_eu.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)\n",
    "most_consumed_men_eu = food_men_eu.groupby(['FoodName']).sum().reset_index().sort_values(by='Number_of_consumers', ascending=False)\n",
    "\n",
    "app = JupyterDash(__name__)\n",
    "server = app.server\n",
    "app.layout = html.Div([\n",
    "    dcc.Graph(id='graph-with-slider'),\n",
    "    dcc.RangeSlider(\n",
    "        min=0,\n",
    "        max=75, \n",
    "        step=1,\n",
    "        id='my-range-slider',\n",
    "\t\tvalue=[0,30], \n",
    "    )\n",
    "    \n",
    "])\n",
    "\n",
    "@app.callback( \n",
    "    Output(\"graph-with-slider\", \"figure\"), \n",
    "    Input('my-range-slider', 'value'))\n",
    "def update_bar_chart(value): #funkcja updateująca wykres\n",
    "    v1=value[0]\n",
    "    v2=value[1] \n",
    "    dff_men = most_consumed_men_eu.iloc[v1:v2] \n",
    "    dff_fem = most_consumed_fem_eu.iloc[v1:v2]\n",
    "    first_line = go.Bar(x=dff_men[\"FoodName\"], y=dff_men[\"Number_of_consumers\"], name=\"Male\", hovertemplate = 'Number of consumers=%{y:,}')\n",
    "    second_line = go.Bar(x=dff_fem[\"FoodName\"], y=dff_fem[\"Number_of_consumers\"], name=\"Female\", hovertemplate = 'Number of consumers=%{y:,}')\n",
    "    fig = make_subplots(rows=1, cols=2)\n",
    "    fig.add_trace(first_line,row=1, col=1)\n",
    "    fig.add_trace(second_line,row=1, col=2)\n",
    "    fig.update_layout(title_text=\"Most popular foods for men and women in EU\")\n",
    "    fig.update_xaxes(tickangle=40) \n",
    "    return fig\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(mode='inline',port=\"8009\") "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "61750c0c-efb6-4f51-bcfb-92404b2f69b3",
   "metadata": {},
   "source": [
    "### <a id=\"food_eu_gen_wnio\"></a>[&uarr;](#top) W Europie podobnie jak na świecie małe różnice między płciami. Jedynie mężczyźni spożywają wiecej mięsa kurczaka oraz soli. Największa różnica jest w przypadku mięsa wieprzowego, u kobiet wypada z top15 a u mężczyzn zajmuje 10 miejsce. Kobiety jedynie spożywają więcej cukru."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "23ff2228-632a-4fc0-a11d-c210af05638d",
   "metadata": {},
   "source": [
    "# Podsumowanie 🧠 <a id=\"Podsumowanie\"></a>[&uarr;](#top)\n",
    "### Jak widać nawet w bazach danych branych z renomowanych źródeł znajdują sie puste dane, błędy i niejasności. To jak dużą część tego notatnika zajmowało czyszczenie danych i obchodzenie problemów pokazuje jak przydatna jest czysta i dobrze zbudowana baza danych.\n",
    "### Z uporządkowanych danych dało się wywnioskować to, że: \n",
    "1. Na świecie płatki śniadaniowe, mięso wieprzowe, ryż są bardziej popularne niż w Europie\n",
    "1. W Europie bardziej popularne niż na świecie są mięso z kurczaka, mleko, ryż, margaryna, oliwa z oliwek, banany, masło\n",
    "1. Woda z kranu jest popularniejsza w Europie niż na świecie\n",
    "1. Nie ma wielu różnic między płciami jeżeli chodzi o spożywane produkty\n",
    "1. Mężczyźni w Europie spożywają wiecej mięsa wieprzowego oraz soli od kobiet\n",
    "1. Kobiety w Europie spożywają więcej cukru od mężczyzn\n",
    "### Mam nadzieję, że była to przyjemna lektura i pokazała ciekawe zależności w świecie jedzenia. Do zobaczenia."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d70e4b8c-2be5-44c7-a347-8510ec9eb58a",
   "metadata": {},
   "source": [
    "# Możliwe zakłamania: ⚠️<a id=\"risk\"></a>[&uarr;](#top)\n",
    "1. Założenie, że każde badanie ma różną ilość badanych i w ten sposób grupowanie badanych.\n",
    "1. Brak grupy wiekowej All dla wszystkich krajów.\n",
    "1. Własne opinie i przeświadczenia.\n",
    "1. Brak legendy do bazy danych.\n",
    "1. Dane mężczyzn są z mniejszej ilości krajów.\n",
    "1. Brak Polski i sprawdzanie dlanych dla Europy"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "04d6d3e2-bd92-4451-be4d-4509efe962c4",
   "metadata": {},
   "source": [
    "# Źródła:📱  [&uarr;](#top) <a id=\"źr\"></a>\n",
    "1. Gif: https://www.slynyrd.com/blog/2020/9/30/pixelblog-30-food \n",
    "1. Baza danych: https://apps.who.int/foscollab/Download/DownloadConso\n",
    "1. Dane na temat jakości wody na świecie: https://worldpopulationreview.com/country-rankings/water-quality-by-country\n",
    "\t1. https://vividmaps.com/tap-water-safe-to-drink/\n",
    "1. Badania na temat wpływu soli i cukru na ciśnienie tętnicze: https://sci-hub.se/10.1007/s00424-014-1677-x\n",
    "\t1. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4896734/\n",
    "    1. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6770596/\n",
    "1. Dane na temat nietolerancji laktozy na świecie: https://worldpopulationreview.com/country-rankings/lactose-intolerance-by-country"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
