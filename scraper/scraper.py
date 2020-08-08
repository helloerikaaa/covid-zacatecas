import glob
import urllib.request
import zipfile
import csv
import os

import pandas as pd

import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore


class Scraper:

    def __init__(self):
        self.download_zip()
        self.unzip_data()
        list_of_files = glob.glob('data/*.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        self.data_file_path = latest_file

        print(latest_file)

        self.df = pd.read_csv(self.data_file_path, encoding="latin-1")
        self.df = self.df.drop(['ID_REGISTRO'], axis=1)
        self.df = self.df[self.df['ENTIDAD_RES'] == 32]

        self.municipios = ['APOZOL','APULCO','ATOLINGA','BENITO JUÁREZ',
                           'CALERA','CAÑITAS DE FELIPE PESCADOR','CONCEPCIÓN DEL ORO',
                           'CUAUHTÉMOC','CHALCHIHUITES','FRESNILLO','TRINIDAD GARCÍA DE LA CADENA',
                           'GENARO CODINA','GENERAL ENRIQUE ESTRADA','GENERAL FRANCISCO R. MURGUÍA',
                           'EL PLATEADO DE JOAQUÍN AMARO','GENERAL PÁNFILO NATERA','GUADALUPE','HUANUSCO',
                           'JALPA','JEREZ','JIMÉNEZ DEL TEUL','JUAN ALDAMA','JUCHIPILA','LORETO','LUIS MOYA',
                           'MAZAPIL','MELCHOR OCAMPO','MEZQUITAL DEL ORO','MIGUEL AUZA','MOMAX','MONTE ESCOBEDO',
                           'MORELOS','MOYAHUA DE ESTRADA','NOCHISTLÁN DE MEJÍA','NORIA DE ÁNGELES',
                           'OJOCALIENTE','PÁNUCO','PINOS','RÍO GRANDE','SAIN ALTO','EL SALVADOR','SOMBRERETE',
                           'SUSTICACÁN','TABASCO','TEPECHITLÁN','TEPETONGO','TEÚL DE GONZÁLEZ ORTEGA',
                           'TLALTENANGO DE SÁNCHEZ ROMÁN','VALPARAÍSO','VETAGRANDE','VILLA DE COS','VILLA GARCÍA',
                           'VILLA GONZÁLEZ ORTEGA','VILLA HIDALGO','VILLANUEVA','ZACATECAS','TRANCOSO','SANTA MARÍA DE LA PAZ']

        if not firebase_admin._apps:
            cred = credentials.Certificate("zac-covid-firebase-adminsdk-qtrba-46c789cff6.json")
            app = firebase_admin.initialize_app(cred)

        
    def download_zip(self):
        with urllib.request.urlopen('http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip') as dl_file:
            with open('data.zip', 'wb') as out_file:
                out_file.write(dl_file.read())

    def unzip_data(self):
        with zipfile.ZipFile('data.zip', 'r') as zip_ref:
            zip_ref.extractall('data/')
        os.remove("data.zip")
    
    def get_fecha(self):
        fechas = self.df['FECHA_ACTUALIZACION'].unique()
        self.fecha = fechas[0]

        return self.fecha
    
    def get_total_casos_estado(self):
        return len(self.df.values.tolist())
    
    def get_total_casos_positivos(self):
        positivos_total = []
        positivos = self.df[self.df['RESULTADO'] == 1]
        positivos_total = positivos.values.tolist()

        return len(positivos_total)
    
    def get_total_casos_negativos(self):
        negativos_total = []
        negativos = self.df[self.df['RESULTADO'] == 2]
        negativos_total = negativos.values.tolist()

        return len(negativos_total)
    
    def get_total_casos_sospechosos(self):
        sospechosos_total = []
        sospechosos = self.df[self.df['RESULTADO'] == 3]
        sospechosos_total = sospechosos.values.tolist()

        return len(sospechosos_total)
    
    def get_positivos_casos_municipios(self):
        positivos_municipios = []
        municipios_casos = []
        self.df = self.df[self.df['RESULTADO'] == 1]
        zc_list = self.df['MUNICIPIO_RES'].values.tolist()
        list_unicos = self.df['MUNICIPIO_RES'].unique()
        list_unicos.sort()
        for x in list_unicos:
            municipios_casos.append(self.municipios[x-1])
            positivos_municipios.append(zc_list.count(x))
            
        return positivos_municipios
    
    def get_total_mujeres_positivo(self):
        mujeres = self.df[self.df['SEXO'] == 2]
        mujeres_list = mujeres[self.df['RESULTADO'] == 1].values.tolist()

        return len(mujeres_list)
    
    def get_total_hombres_positivo(self):
        hombres = self.df[self.df['SEXO'] == 1]
        hombres_list = hombres[self.df['RESULTADO'] == 1].values.tolist()

        return len(hombres_list)
    
    def get_porcentaje_hombres(self):
        porcentaje = 0
        positivos = self.get_total_hombres_positivo()
        total_positivos = self.get_total_casos_positivos()

        try:
            porcentaje = (positivos/total_positivos) * 100
        except:
            pass

        return round(porcentaje)

    def get_porcentaje_mujeres(self):
        porcentaje = 0
        positivos = self.get_total_mujeres_positivo()
        total_positivos = self.get_total_casos_positivos()

        try:
            porcentaje = (positivos/total_positivos) * 100
        except:
            pass

        return round(porcentaje)

    def get_total_casos_defuncion(self):
        defuncion_total = []
        defuncion = self.df[self.df['FECHA_DEF'].str.contains('2020')]
        defuncion_total = defuncion.values.tolist()

        print(defuncion_total)
        print(len(defuncion_total))
        return len(defuncion_total)
    
    def get_caso_ambulatorio(self):
        ambulatorio = self.df[self.df['TIPO_PACIENTE'] == 1]
        ambulatorio_list = ambulatorio[self.df['RESULTADO'] == 1].values.tolist()

        return len(ambulatorio_list)
    
    def get_caso_hospitalizado(self):
        hospitalizado = self.df[self.df['TIPO_PACIENTE'] == 2]
        hospitalizado_list = hospitalizado[self.df['RESULTADO'] == 1].values.tolist()

        return len(hospitalizado_list)
    
    def get_porcentaje_ambulatorios(self):
        porcentaje = 0
        positivos = self.get_caso_ambulatorio()
        total_positivos = self.get_total_casos_positivos()

        try:
            porcentaje = (positivos/total_positivos) * 100
        except:
            pass

        return round(porcentaje)
    
    def get_porcentaje_hospitalizados(self):
        porcentaje = 0
        positivos = self.get_caso_hospitalizado()
        total_positivos = self.get_total_casos_positivos()

        try:
            porcentaje = (positivos/total_positivos) * 100
        except:
            pass

        return round(porcentaje)
    
    def get_caso_contacto(self):
        contacto = self.df[self.df['OTRO_CASO'] == 1]
        contacto_list = contacto[self.df['RESULTADO'] == 1].values.tolist()

        return len(contacto_list)
    
    def get_porcentaje_contactos(self):
        porcentaje = 0
        contactos = self.get_caso_contacto()
        total_positivos = self.get_total_casos_positivos()

        try:
            porcentaje = (contactos/total_positivos) * 100
        except:
            pass

        return round(porcentaje)
    
    def get_total_neumo_positivo(self):
        neumo = self.df[self.df['NEUMONIA'] == 1]
        neumo_list = neumo[self.df['RESULTADO'] == 1].values.tolist()

        return len(neumo_list)
    
    def get_total_daibetes_positivo(self):
        diabetes = self.df[self.df['NEUMONIA'] == 1]
        diabetes_list = diabetes[self.df['RESULTADO'] == 1].values.tolist()

        return len(diabetes_list)
    
    def get_total_epoc_positivo(self):
        epoc = self.df[self.df['EPOC'] == 1]
        epoc_list = epoc[self.df['RESULTADO'] == 1].values.tolist()

        return len(epoc_list)

    def get_total_asma_positivo(self):
        asma = self.df[self.df['ASMA'] == 1]
        asma_list = asma[self.df['RESULTADO'] == 1].values.tolist()

        return len(asma_list)

    def get_total_inmuno_positivo(self):
        inmuno = self.df[self.df['INMUSUPR'] == 1]
        inmuno_list = inmuno[self.df['RESULTADO'] == 1].values.tolist()

        return len(inmuno_list)
    
    def get_total_hiper_positivo(self):
        hiper = self.df[self.df['HIPERTENSION'] == 1]
        hiper_list = hiper[self.df['RESULTADO'] == 1].values.tolist()

        return len(hiper_list)
    
    def get_total_cardio_positivo(self):
        cardio = self.df[self.df['CARDIOVASCULAR'] == 1]
        cardio_list = cardio[self.df['RESULTADO'] == 1].values.tolist()

        return len(cardio_list)
    
    def get_total_obsesidad_positivo(self):
        obesidad = self.df[self.df['OBESIDAD'] == 1]
        obesidad_list = obesidad[self.df['RESULTADO'] == 1].values.tolist()

        return len(obesidad_list)
    
    def get_total_renal_positivo(self):
        renal_list = self.df[self.df['RENAL_CRONICA'] == 1].values.tolist()

        return len(renal_list)
    
    def get_total_tabaquismo_positivo(self):
        tabaquismo_list = self.df[self.df['TABAQUISMO'] == 99].values.tolist()

        return len(tabaquismo_list)

    def get_caso_uci(self):
        uci = self.df[self.df['UCI'] == 1]
        uci_list = uci[self.df['RESULTADO'] == 1].values.tolist()

        return len(uci_list)
    
    def get_caso_intubado(self):
        intubado = self.df[self.df['INTUBADO'] == 1]
        uci_list = intubado[self.df['RESULTADO'] == 1].values.tolist()

        return len(uci_list)
    
    def save_positivos_casos_municipios(self):
        self.store = firestore.client()
        self.df = self.df[self.df['RESULTADO'] == 1]
        zc_list = self.df['MUNICIPIO_RES'].values.tolist()
        list_unicos = self.df['MUNICIPIO_RES'].unique()
        list_unicos.sort()
        for x in list_unicos:
            self.store.collection("zacatecas-municipios").document(self.municipios[x-1]).set({u'municipio':self.municipios[x-1], u'total': zc_list.count(x)})

    def save_caso(self):
        self.store = firestore.client()
        total = self.get_total_casos_estado()
        positivos = self.get_total_casos_positivos()
        negativos = self.get_total_casos_negativos()
        sospechosos = self.get_total_casos_sospechosos()
        hombres = self.get_porcentaje_hombres()
        mujeres = self.get_porcentaje_mujeres()
        hospitalizados = self.get_porcentaje_hospitalizados()
        ambulatorios = self.get_porcentaje_ambulatorios()
        casos_contacto = self.get_porcentaje_contactos()
        fecha = self.get_fecha()
        
        self.store.collection("zacatecas-covid").document(fecha).set({
            u'total': total,
            u'positivos': positivos,
            u'negativos': negativos,
            u'sospechosos': sospechosos,
            u'hombres': hombres,
            u'mujeres': mujeres,
            u'hospitalizados': hospitalizados,
            u'ambulatorios': ambulatorios,
            u'casos_contacto': casos_contacto, 
            u'fecha': fecha
            })
        
        print("Nuevos casos actualizados")
    
    def save_edad_positivos(self):
        edades = []
        edad = self.df[self.df['RESULTADO'] == 1]
        edades = edad['EDAD'].values.tolist()
        self.store = firestore.client()
        for edad in edades:
            self.store.collection("zacatecas-edades").document('A'+str(edad)).set({u'edad': edad, u'total': edades.count(edad)})
        
        print("Edades de casos actualizadas")

    def save_fecha_actualizacion(self):
        print(self.get_fecha())
        self.store = firestore.client()
        self.store.collection("zacatecas-actualizacion").document(self.get_fecha()).set({u'fecha': self.get_fecha()})

        print("Última fecha de actualización guardada")
    
    def save_enfermedades_caso(self):
        self.store = firestore.client()
        neumo = self.get_total_neumo_positivo()
        diabetes = self.get_total_daibetes_positivo()
        epoc = self.get_total_epoc_positivo()
        asma = self.get_total_asma_positivo()
        inmuno = self.get_total_inmuno_positivo()
        hiper = self.get_total_hiper_positivo()
        cardio = self.get_total_cardio_positivo()
        obesidad = self.get_total_obsesidad_positivo()
        renal = self.get_total_renal_positivo()
        tabaquismo = self.get_total_tabaquismo_positivo()
        uci = self.get_caso_uci()
        intubados = self.get_caso_intubado()
        fecha = self.get_fecha()
        
        self.store.collection("zacatecas-enfermedades").document(fecha).set({
            u'neumo': neumo,
            u'diabetes': diabetes,
            u'epoc': epoc,
            u'asma': asma,
            u'inmuno': inmuno,
            u'hiper': hiper,
            u'cardio': cardio,
            u'obesidad': obesidad,
            u'renal': renal, 
            u'tabaquismo': tabaquismo, 
            u'uci': uci, 
            u'intubado': intubados, 
            u'fecha': fecha
            })
        
        print("Enfermedades de casos actualizadas")


def main():
    scraper = Scraper()
    scraper.save_fecha_actualizacion()
    scraper.save_caso()
    scraper.save_edad_positivos()
    scraper.save_positivos_casos_municipios()
    scraper.save_enfermedades_caso()


if __name__ == "__main__":
    main()