
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Regresion Lineal Multiple
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

A1_OA_Da = 16                     # Day Align
A1_OA_Ta = "America/Mexico_City"  # Time Align

A1_OA_Ai = "101-004-2221697-001"  # Id de cuenta
A1_OA_At = "practice"             # Tipo de cuenta

A1_OA_In = "EUR_USD"              # Instrumento
A1_OA_Gn = "H1"                   # Granularidad de velas

A1_OA_Ak = "a" + "da4a61b0d5bc0e5939365e01450b614" + "-4121f84f01ad78942c46fc3ac777baa" + "6"

params = {"granularity": A1_OA_Gn, "price": "M", "dailyAlignment": A1_OA_Da, "alignmentTimezone": A1_OA_Ta,
          "from": "2017-01-01T00:00:00Z", "to": "2017-03-31T00:00:00Z"}
