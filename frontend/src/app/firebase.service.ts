import { Injectable } from '@angular/core';
import { AngularFirestore, AngularFirestoreDocument } from '@angular/fire/firestore';
import { Observable } from 'rxjs';import { ArrayType } from '@angular/compiler';

@Injectable({
  providedIn: 'root'
})
export class FirebaseService {

  constructor(
    private firestore: AngularFirestore,
  ) { }

  public getTotalDia() {
    return this.firestore.collection('zacatecas-covid', ref => ref.orderBy("fecha", "asc")).snapshotChanges();
  }

  public getTotalPositivosPorDia() {
    return this.firestore.collection('zacatecas-covid').snapshotChanges();
  }

  public getFechaActualizacion() {
    return this.firestore.collection('zacatecas-actualizacion').snapshotChanges();
  }

  public getTotalPositivosPorEdad() {
    return this.firestore.collection('zacatecas-edades').snapshotChanges();
  }

  public getTotalPositivosPorMunicipio() {
    return this.firestore.collection('zacatecas-municipios', ref => ref.orderBy("total", "desc")).snapshotChanges();
  }

  public getTotalEnfermedades() {
    return this.firestore.collection('zacatecas-enfermedades', ref => ref.orderBy("fecha", "desc")).snapshotChanges();
  }

  public getMovilidadResidencial() {
    return this.firestore.collection('zacatecas-residencial').snapshotChanges();
  }

  public getMovilidadTrabajo() {
    return this.firestore.collection('zacatecas-trabajo').snapshotChanges();
  }

  public getMovilidadTransito() {
    return this.firestore.collection('zacatecas-transito').snapshotChanges();
  }

  public getMovilidadRecreativa() {
    return this.firestore.collection('zacatecas-recreacion').snapshotChanges();
  }

}
