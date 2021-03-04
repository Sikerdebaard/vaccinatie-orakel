![AutoUpdate](https://github.com/Sikerdebaard/netherlands-vaccinations-scraper/workflows/AutoUpdate/badge.svg)

# Het vaccinatie orakel
Een ensemble aan modellen die de vaccinatiegraad voorspellen.

## Meest recente voorspelling van het orakel
![data/ensemble.png](data/ensemble.png)
[data/ensemble.csv]()

## Uitleg databestanden
Voor de scope van deze readme houden we het bij het documenteren van de csv bestanden. Soms zijn er gelijknamige png bestanden, dit zijn vaak grafieken die de data inzichtelijk trachten te maken. Ook kan het voorkomen dat er een gelijknamige json te vinden is. Die bevatten vaak dezelfde data als de gelijknamige csv. Wij geven geen garantie dat de jsons in de toekomst blijven bestaan, gebruik daarom dus de csv bestanden.

### [data/ensemble.csv](data/ensemble.csv)
Dit is de output van het ensemble en dit is dus zeer waarschijnlijk de file die je zoekt.  

`total_vaccinations` aantal doses geinjecteerd  
`people_vaccinated` aantal mensen dat tenminste een prik heeft ontvangen  
`people_fully_vaccinated` aantal mensen volledig gevaccineerd  

### [data/metrics.csv](data/metrics.csv)
Kwantitatieve metrics die een beeld geven hoe correct het ensemble en de verschillende modellen zijn.  

`metric` naam van de metric  
`ensemble` metrics voor het `ensemble.csv`  
`@<naam>` de naam van het model, op dit moment tevens de twitter-handle van de betreffende source  

### [data/intersect-metrics.csv](data/intersect-metrics.csv)
Kwantitatieve metrics die een beeld geven hoe correct het ensemble en de verschillende modellen zijn. Het verschil tussen deze metrics en de hierboven genoemde metrics is dat de metrics alleen berekend worden over datapunten waarvoor alle modellen een voorspelling hebben.

`model` naam van het model  
`explained_variance` [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.explained_variance_score.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.explained_variance_score.html)  
`mean_squared_log_error` [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_log_error.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_log_error.html)  
`r2` [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.htm](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.htm)  
`MAE` [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html)  
`MSE` [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html)
`RMSE` Square Root of MSE  

### [data/models](data/models)
De csv bestanden in deze folder zijn de outputs van de individuele modellen. Deze worden in een ensemble samengevoegd.  

`total_vaccinations` aantal doses geinjecteerd  
`people_vaccinated` aantal mensen die tenminste een prik hebben ontvangen  
`people_fully_vaccinated` aantal mensen volledig gevaccineerd  
