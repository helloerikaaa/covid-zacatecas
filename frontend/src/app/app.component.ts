import { Component, OnInit } from '@angular/core';
import { FirebaseService } from '../app/firebase.service';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  public positivos = 0;
  public sospechosos = 0;
  public negativos = 0;
  public total = 0;
  public hombres = 0;
  public mujeres = 0;
  public hospitalizados = 0;
  public ambulatorios = 0;
  public casosContacto = 0;
  public fecha = ''

  public neumo = 0;
  public diabetes = 0;
  public epoc = 0;
  public asma = 0;
  public inmuno = 0;
  public hiper = 0;
  public cardio = 0;
  public obsesidad = 0;
  public renal = 0;
  public tabaquismo = 0;

  public intubado = 0;
  public uci = 0;

  public actualizacion = 0;

  public edadesLabels = []
  public edadesData = []

  public casosLabels = []
  public positivosData = []
  public negativosData = []
  public sospechososData = []

  public municipiosNombres = []
  public municipiosTotales = []

  constructor(
    private firestoreService: FirebaseService
  ) { }

  ngOnInit() {

    this.firestoreService.getFechaActualizacion().subscribe((actualizacionSnapshot) => {
      actualizacionSnapshot.forEach((actualizacionData: any) => {
        this.actualizacion = actualizacionData.payload.doc.data().fecha;
      });
    });

    this.firestoreService.getTotalDia().subscribe((casosSnapshot) => {
      casosSnapshot.forEach((casosData: any) => {
        this.positivos = casosData.payload.doc.data().positivos;
        this.negativos = casosData.payload.doc.data().negativos;
        this.sospechosos = casosData.payload.doc.data().sospechosos;
        this.total = casosData.payload.doc.data().total;
        this.mujeres = casosData.payload.doc.data().mujeres;
        this.hombres = casosData.payload.doc.data().hombres;
        this.hospitalizados = casosData.payload.doc.data().hospitalizados;
        this.ambulatorios = casosData.payload.doc.data().ambulatorios;
        this.casosContacto = casosData.payload.doc.data().casos_contacto;
        this.fecha = casosData.payload.doc.data().fecha;
      });
    });

    this.firestoreService.getTotalPositivosPorDia().subscribe((diaSnapshot) => {
      diaSnapshot.forEach((diaData: any) => {
        this.casosLabels.push(diaData.payload.doc.data().fecha);
        this.positivosData.push(diaData.payload.doc.data().positivos);
        this.negativosData.push(diaData.payload.doc.data().negativos);
        this.sospechososData.push(diaData.payload.doc.data().sospechosos);

        this.makeDiasChart(this.casosLabels, this.positivosData)
      });
    });

    this.firestoreService.getTotalPositivosPorMunicipio().subscribe((municipioSnapshot) => {
      municipioSnapshot.forEach((municipioData: any) => {
        this.municipiosNombres.push(municipioData.payload.doc.data().municipio);
        this.municipiosTotales.push(municipioData.payload.doc.data().total);
      });
    });

    this.firestoreService.getTotalPositivosPorEdad().subscribe((diaSnapshot) => {
      diaSnapshot.forEach((diaData: any) => {
        this.edadesLabels.push(diaData.payload.doc.data().edad);
        this.edadesData.push(diaData.payload.doc.data().total);

        this.makeEdadesChart(this.edadesLabels, this.edadesData)
      });
    });

    this.firestoreService.getTotalEnfermedades().subscribe((enfermedadesSnapshot) => {
      enfermedadesSnapshot.forEach((enfermedadesData: any) => {
        this.fecha = enfermedadesData.payload.doc.data().fecha;
        this.neumo = enfermedadesData.payload.doc.data().neumo;
        this.diabetes = enfermedadesData.payload.doc.data().diabetes;
        this.epoc = enfermedadesData.payload.doc.data().epoc;
        this.asma = enfermedadesData.payload.doc.data().asma;
        this.inmuno = enfermedadesData.payload.doc.data().inmuno;
        this.hiper = enfermedadesData.payload.doc.data().hiper;
        this.cardio = enfermedadesData.payload.doc.data().cardio;
        this.obsesidad = enfermedadesData.payload.doc.data().obesidad;
        this.renal = enfermedadesData.payload.doc.data().renal;
        this.tabaquismo = enfermedadesData.payload.doc.data().tabaquismo;
        this.uci = enfermedadesData.payload.doc.data().uci;
        this.intubado = enfermedadesData.payload.doc.data().intubado;
      });
    });
  }

  public makeDiasChart(labelsCasos: string[], dataPositivos: number[]) {
    var ctx = document.getElementById("chartCasos");
    var chartCasos = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {

        labels: labelsCasos,
        datasets: [
          {
            label: 'Total de casos positivos en el estado',
            data: dataPositivos,
            backgroundColor: "rgba(220,220,220,0)",
            borderColor: '#dc3545'
          }
        ]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        // Container for pan options
        pan: {
          // Boolean to enable panning
          enabled: true,

          // Panning directions. 
          mode: 'x',

          speed: 1
        },

        // Container for zoom options
        zoom: {
          // enable zooming
          enabled: true,
          // Zooming directions. 
          mode: 'x',
        },
        responsive: true
      }
    });
  }

  public makeEdadesChart(labelsEdades: string[], dataTotal: number[]) {
    var ctx = document.getElementById("edadesChart");
    var chartCasos = new Chart(ctx, {
      type: 'bar',
      responsive: true,
      data: {

        labels: labelsEdades,
        datasets: [
          {
            label: 'Edad de casos positivos',
            data: dataTotal,
            backgroundColor: "#16aaff",
            borderColor: '#16aaff'
          }
        ]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        // Container for pan options
        pan: {
          // Boolean to enable panning
          enabled: true,

          // Panning directions. 
          mode: 'x',

          speed: 1
        },

        // Container for zoom options
        zoom: {
          // enable zooming
          enabled: true,
          // Zooming directions. 
          mode: 'x',
        },
        responsive: true
      }
    });
  }

  public makeRecreacionChart(labelsCasos: string[], dataPositivos: number[]) {
    var ctx = document.getElementById("recreacionChart");
    var chartCasos = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {

        labels: labelsCasos,
        datasets: [
          {
            label: 'Porcentaje de movilidad cada cuatro días',
            data: dataPositivos,
            backgroundColor: "rgba(220,220,220,0)",
            borderColor: '#a29bfe'
          }
        ]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        // Container for pan options
        pan: {
          // Boolean to enable panning
          enabled: true,

          // Panning directions. 
          mode: 'x',

          speed: 1
        },

        // Container for zoom options
        zoom: {
          // enable zooming
          enabled: true,
          // Zooming directions. 
          mode: 'x',
        },
        responsive: true
      }
    });
  }

  public makeTrabajoChart(labelsCasos: string[], dataPositivos: number[]) {
    var ctx = document.getElementById("trabajoChart");
    var chartCasos = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {

        labels: labelsCasos,
        datasets: [
          {
            label: 'Porcentaje de movilidad cada cuatro días',
            data: dataPositivos,
            backgroundColor: "rgba(220,220,220,0)",
            borderColor: '#636e72'
          }
        ]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        // Container for pan options
        pan: {
          // Boolean to enable panning
          enabled: true,

          // Panning directions. 
          mode: 'x',

          speed: 1
        },

        // Container for zoom options
        zoom: {
          // enable zooming
          enabled: true,
          // Zooming directions. 
          mode: 'x',
        },
        responsive: true
      }
    });
  }

  public makeResidencialChart(labelsCasos: string[], dataPositivos: number[]) {
    var ctx = document.getElementById("residencialChart");
    var chartCasos = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {

        labels: labelsCasos,
        datasets: [
          {
            label: 'Porcentaje de movilidad cada cuatro días',
            data: dataPositivos,
            backgroundColor: "rgba(220,220,220,0)",
            borderColor: '#f19066'
          }
        ]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        // Container for pan options
        pan: {
          // Boolean to enable panning
          enabled: true,

          // Panning directions. 
          mode: 'x',

          speed: 1
        },

        // Container for zoom options
        zoom: {
          // enable zooming
          enabled: true,
          // Zooming directions. 
          mode: 'x',
        },
        responsive: true
      }
    });
  }

  public makeTransporteChart(labelsCasos: string[], dataPositivos: number[]) {
    var ctx = document.getElementById("transporteChart");
    var chartCasos = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {

        labels: labelsCasos,
        datasets: [
          {
            label: 'Porcentaje de movilidad cada cuatro días',
            data: dataPositivos,
            backgroundColor: "rgba(220,220,220,0)",
            borderColor: '#3dc1d3'
          }
        ]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        // Container for pan options
        pan: {
          // Boolean to enable panning
          enabled: true,

          // Panning directions. 
          mode: 'x',

          speed: 1
        },

        // Container for zoom options
        zoom: {
          // enable zooming
          enabled: true,
          // Zooming directions. 
          mode: 'x',
        },
        responsive: true
      }
    });
  }

}
