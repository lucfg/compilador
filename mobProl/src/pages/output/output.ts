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

  // Quadruple reader
  programIndex = [0];
  currentDepth = 0;

  executeQuadruples(depth) {
    let curQuad = this.quadruples[this.programIndex[depth]];

    // Goto main
    if (this.programIndex[depth] == 0) {
      this.programIndex[0] = curQuad[3];
      curQuad = this.quadruples[this.programIndex[depth]];
    }

    switch (curQuad[0].toLowerCase()) {
      case "goto":
        
        break;
    
      // Ignore other quads
      default:
        console.log("Ignoring quad: " + JSON.stringify(curQuad));
        break;
    }
  }

  close() {
    this.viewCtrl.dismiss();
  }
}
