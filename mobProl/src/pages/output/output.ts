import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ViewController } from 'ionic-angular';

/**
 * Generated class for the OutputPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-output',
  templateUrl: 'output.html',
})
export class OutputPage {
  programName = "missingName";
  quadruples = [];

  constructor(
              public navCtrl: NavController, 
              public navParams: NavParams,
              public viewCtrl: ViewController
  ) {
    this.programName = this.navParams.data.programName;
    this.quadruples = this.navParams.data.quadruples;
  }

  ionViewDidLoad() {
  }

  close() {
    this.viewCtrl.dismiss();
  }
}
