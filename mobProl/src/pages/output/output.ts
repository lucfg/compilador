import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ViewController } from 'ionic-angular';
//import { varTuple } from './../../models/varTuple'

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
    this.executeQuadruples(this.currentDepth);
  }

  // Quadruple reader
  programIndex = [0];
  currentDepth = 0;
  
  memory: HashTable<varTuple> = {};

  

  executeQuadruples(depth) {
    let curQuad = this.quadruples[this.programIndex[depth]];

    // Goto main
    if (this.programIndex[depth] == 0) {
      this.programIndex[0] = curQuad[3];
      curQuad = this.quadruples[this.programIndex[depth]];
    }

    let arg1 = curQuad[1];
    let arg2 = curQuad[2];
    let arg3 = curQuad[3];

    let arg1isConst = arg1.indexOf('*') > -1 || arg1 == "True" || arg1 == "False";
    let arg2isConst = arg2.indexOf('*') > -1 || arg2 == "True" || arg2 == "False";
    //let arg3isConst = arg3.indexOf('*') > -1 || arg3 == "True" || arg3 == "False";

    var arg1Const;
    var arg2Const;
    if (arg1 == "True") {
      arg1Const = true;
    }
    else if (arg1 == "False") {
      arg1Const = false;
    }
    else {
      let cleanString1 = arg1.replace('*', '');
      arg1Const = Number(cleanString1);
    }

    if (arg2 == "True") {
      arg2Const = true;
    }
    else if (arg2 == "False") {
      arg2Const = false;
    }
    else {
      let cleanString2 = arg2.replace('*', '');
      arg1Const = Number(cleanString2);
    }

    
    switch (curQuad[0].toLowerCase()) {
      // GoTo's
      case "goto":
        console.log("Going from " + this.programIndex[depth] + " in level " + depth + " to " + curQuad[3]);
        this.programIndex[depth] = curQuad[3];
        break;

      // Statements
      case "=":
        console.log("Assigning to address " + arg3);
        this.memory[arg3] = new varTuple( arg1isConst ? arg1Const : this.memory[arg1] );
        break;

      // Expressions
      case "+":
        if (arg2.indexOf('*') > -1)  // is constant
        console.log("summing to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) + (arg2isConst ? arg2Const : this.memory[arg2]));
        break;

      case "-":
        console.log("subtracting to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) - (arg2isConst ? arg2Const : this.memory[arg2]));
        break;
      
      case "/":
        console.log("dividing to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) / (arg2isConst ? arg2Const : this.memory[arg2]));
        break;

      case "*":
        console.log("summing to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) * (arg2isConst ? arg2Const : this.memory[arg2]));
        break;

      case "&&":
        console.log("boolean and to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) && (arg2isConst ? arg2Const : this.memory[arg2]));
        break;
      
      case "||":
        console.log("boolean or to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) || (arg2isConst ? arg2Const : this.memory[arg2]));
        break;

      case "==":
        console.log("equals to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) == (arg2isConst ? arg2Const : this.memory[arg2]));
        break;

      case "<=":
        console.log("less or equals to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) <= (arg2isConst ? arg2Const : this.memory[arg2]));
        break;

      case ">=":
        console.log("more or equals to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) >= (arg2isConst ? arg2Const : this.memory[arg2]));
        break;

      case "<":
        console.log("less than to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) < (arg2isConst ? arg2Const : this.memory[arg2]));
        break;

      case ">":
        console.log("more than to dir " + arg3)
        this.memory[arg3] = new varTuple((arg1isConst ? arg1Const : this.memory[arg1]) > (arg2isConst ? arg2Const : this.memory[arg2]));
        break;
    
      // Ignore other quads
      default:
        console.log("Ignoring quad: " + JSON.stringify(curQuad));
        break;
    }
  }

  /**
   * Checks the range of the address and returns the type to assign
   * @param address the address of the variable to check
   */
  getType(address: number) {
    if ((address >= 0 && address < 5001)
       || (address >= 15001 && address < 20001)
       || (address >= 30001 && address < 35001)) {
      return 'int';
    }
    else if ((address >= 5001 && address < 10001)
    || (address >= 20001 && address < 25001)
    || (address >= 35001 && address < 40001)
    ) {
      return 'decim';
    }
    else if ((address >= 10001 && address < 15001)
    || (address >= 25001 && address < 30001)
    || (address >= 40001 && address < 45001)) {
      return 'bool';
    }
    else {
      return 'error';
    } 
  }

  close() {
    this.viewCtrl.dismiss();
  }
}

export class varTuple {
  //value: any;
  constructor(public value: any) {
      this.value = value;
  }
}

interface HashTable<T> {
  [key: number]: T;
}