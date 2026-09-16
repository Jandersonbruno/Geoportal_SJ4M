# Geoportal SJ4M

Portal cartográfico web estático de São José dos Quatro Marcos (MT), construído em HTML + [Leaflet](https://leafletjs.com/), sem backend.

## Estrutura

```
Geoportal_SJ4M.html   → aplicação completa (mapa, camadas, busca, medição, croqui)
Shp/                  → GeoJSON de origem (exportados do QGIS) + metadados .qmd
```

## Camadas exibidas

- Lotes
- Edificações
- Logradouro
- Canteiros
- Bairros
- Hidrografia

## Funcionalidades

- Basemaps: Google Satélite / OpenStreetMap
- Painel de camadas com liga/desliga
- Busca por código de lote, bairro e logradouro
- Painel de informações ao clicar em uma feição
- Ferramenta de medição de distância e área
- Editor de croqui (desenho de polígono/linha/texto) com guia A4 para impressão

## Publicação

Hospedado como site estático via [GitHub Pages](https://pages.github.com/).
