library(tidyverse)
library(sf)
library(tmap)
library(monochromeR)

lots <- st_read("C:/Users/Nissim/Desktop/Vacant Lots Project/vacant-lots-proj/vacancy_guncrime_dash/joined_gdf.geojson")

pal <- generate_palette("#9b2226", 'go_lighter', 6, view_palette = FALSE)

levels <- c("Top 1%", 
            "Top 5%",
            "Top 10%",
            "Top 25%",
            "Top 50%",
            "Bottom 50%")

lots$guncrime_density <- ordered(lots$guncrime_density, levels = levels)

tmap_mode('view')

tm_shape(lots) +
  tm_polygons(col = 'guncrime_density',
              border.alpha = 0,
              palette = pal)
