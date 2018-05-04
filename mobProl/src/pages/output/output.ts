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
    this.executeQuadruples(0);
    console.log("Resulting memory:");
    console.log(this.memory);
  }

  // Quadruple reader
  outputLines: string[] = []; 
  memory: HashTable<varTuple> = {};

  /**
   * Reads a quadruple on the given index and handles it accordingly
   * @param programIndex Index of the quadruple to rea
   */
  executeQuadruples(programIndex: number) {
    // Prepare arguments to work them later
    let curQuad = this.quadruples[programIndex];
    console.log("Running quad: " + JSON.stringify(curQuad));

    let instruction = curQuad[0];
    let rawArg1 = curQuad[1];
    let rawArg2 = curQuad[2];
    let rawArg3 = curQuad[3];

    var arg1;
    var arg2;
    var arg3 = rawArg3;

    let isConstantArg1 = true;
    let isConstantArg2 = true;

    // Get arg1's value
    if (rawArg1.indexOf('*') > -1) {
      let cleanString1 = arg1.replace(/\*/g, '');
      //console.log("Cleaned string 1 is: " + cleanString1 + arg1isConst);
      arg1 = Number(cleanString1); // TODO: this probably won't work with strings
    }
    else if (rawArg1 == "true") {
      arg1 = true;
    }
    else if (rawArg1 == "false") {
      arg1 = false;
    } else { // arg is address
      arg1 = this.memory[Number(rawArg1)].value;
      isConstantArg1 = false;
    }

    // Get arg2's value
    if (rawArg2.indexOf('*') > -1) {
      let cleanString1 = arg2.replace(/\*/g, '');
      //console.log("Cleaned string 1 is: " + cleanString1 + arg2isConst);
      arg2 = Number(cleanString1); // TODO: this probably won't work with strings
    }
    else if (rawArg2 == "true") {
      arg2 = true;
    }
    else if (rawArg2 == "false") {
      arg2 = false;
    } else { // arg is address
      arg2 = this.memory[Number(rawArg2)].value;
      isConstantArg2 = false;
    }


    // Handle instruction
      // debugging helpers
    let arg1Log = arg1 + (isConstantArg1 ? " (const)" : " (addr: " + Number(rawArg1) + ")");
    let arg2Log = arg2 + (isConstantArg2 ? " (const)" : " (addr: " + Number(rawArg2) + ")");

    switch (curQuad[0].toLowerCase()) {
      // GoTo's
      case "goto":
        console.log("Going from " + programIndex + " to " + arg3);
        this.executeQuadruples(arg3);
        return;

      case "gotof":
        if (arg1) {
          console.log("Arg1 is false, going from " + programIndex + " to " + arg3);
          this.executeQuadruples(arg3);
          return;
        }
        else {
          console.log("Arg1 is true; ignoring quadruple...")
        }
        break;

      // Statements
      case "=":
        console.log("Assigning " + arg1Log + " to " + arg3);
        this.memory[arg3] = new varTuple(arg1);
        break;

      case "print":
        console.log("Outputting: " + arg1Log);
        this.outputLines.push(arg1);
        break;

      // Expressions
      case "+":
        console.log("Summing to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 + arg2);
        break;

      case "-":
        console.log("Subtracting to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 - arg2);
        break;
      
      case "/":
        console.log("Dividing to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 / arg2);
        break;

      case "*":
        console.log("Multiplying to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 * arg2);
        break;

      case "&&":
        console.log("AND to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 && arg2);
        break;
      
      case "||":
        console.log("OR to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 || arg2);
        break;

      case "==":
        console.log("== to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 == arg2);
        break;

      case "<=":
        console.log("<= to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 <= arg2);
        break;

      case ">=":
        console.log(">= to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 >= arg2);
        break;

      case "<": //TODO: are the arguments of these switched by the compiler??
        console.log("< to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 < arg2);
        break;

      case ">":
        console.log("> to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 > arg2);
        break;

      case "end":
        console.log("Reached end of quadruples.");
        return;
    
      // Ignore other quads
      default:
        console.log("Ignoring quad: " + JSON.stringify(curQuad));
        break;
    }

    this.executeQuadruples(programIndex + 1);
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