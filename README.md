# Graph Explorer

SOK projekat: platforma za vizualizaciju grafova sa plugin-ovima za ucitavanje i prikaz podataka.

## Tim

- Ilija Todorovic SV31/2024
- Aleksandar Spasojevic SV68/2024
- Stefan Dragovic SV35/2024

## Struktura projekta

| Folder | Komponenta | Opis                                                        |
|---|---|-------------------------------------------------------------|
| `api` | `sok-api` | Model grafa i apstrakcije plugin-ova                        |
| `platform` | `sok-core` | Platforma: prepoznavanje plugin-ova, pretraga i filtriranje |
| `json_datasource` | `sok-json-datasource` | Data source plugin za JSON                                  |
| `xml_datasource` | `sok-xml-datasource` | Data source plugin za XML                                   |
| `simple_visualizer` | `sok-simple-visualizer` | Visualizer plugin za jednostavan prikaz                     |
| `block_visualizer` | `sok-block-visualizer` | Visualizer plugin za prikaz cvorova kao blokova             |
| `graph_explorer` | — | Django web aplikacija                                       |

## Instalacija

Potreban je Python 3.11 ili noviji.

1. Napraviti i aktivirati virtuelno okruzenje:

   ```shell
   python -m venv venv
   ```

   Windows:
   ```shell
   venv\Scripts\activate
   ```

   Linux / macOS:
   ```shell
   source venv/bin/activate
   ```

2. Instalirati neophodne pakete:

   ```shell
   pip install -r requirements.txt
   ```

3. Instalirati komponente i plugin-ove:

   ```shell
   pip install -e ./api -e ./platform -e ./json_datasource -e ./xml_datasource -e ./simple_visualizer -e ./block_visualizer
   ```

## Pokretanje

```shell
cd graph_explorer
python manage.py runserver
```

Aplikacija je dostupna na http://127.0.0.1:8000.