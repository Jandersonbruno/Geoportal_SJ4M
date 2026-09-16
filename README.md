# Geoportal SJ4M

Portal cartográfico web estático de São José dos Quatro Marcos (MT), construído em HTML + [Leaflet](https://leafletjs.com/), sem backend.

## Estrutura

```
index.html   → aplicação completa (mapa, camadas, busca, medição, croqui)
Shp/         → GeoJSON de origem (exportados do QGIS) + metadados .qmd
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
- Exportar tabela de atributos em XLSX, com seleção de uma ou mais camadas (uma aba por camada no arquivo)
- Rótulo de Tipologia sobre as edificações a partir de zoom bem próximo (escala ~10 m)
- Campo do painel de atributos acende ao passar o mouse por cima

## Publicação

Hospedado como site estático via [GitHub Pages](https://pages.github.com/): https://jandersonbruno.github.io/Geoportal_SJ4M/

O site é servido diretamente da branch `main` — qualquer `git push` para ela atualiza o portal publicado em ~1 minuto, sem passo de build manual.

### Como publicar uma alteração

1. Edite `index.html` (ou os arquivos em `Shp/`)
2. Confira o resultado abrindo `index.html` localmente no navegador
3. Envie para o GitHub:
   ```powershell
   .\publicar.ps1 "descrição curta da mudança"
   ```
   (ou manualmente: `git add -A`, `git commit -m "..."`, `git push`)
4. Aguarde ~1 min e confira em https://jandersonbruno.github.io/Geoportal_SJ4M/

### Sobre a ortofoto (`IMG/`)

Os arquivos de ortofoto/raster de trabalho (`.tif`, `.ecw`) ficam fora do repositório (ver `.gitignore`) por serem grandes demais para o GitHub. Depois de recortados no limite urbano, devem ser convertidos em tiles (XYZ) e hospedados separadamente antes de virar uma opção de basemap no portal.
