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
   * @param error If true, stops executing more quadruples
   */
  executeQuadruples(programIndex: number, error?: boolean) {
    if (error) {
      return false;
    }

    // Prepare arguments to work them later
    let curQuad = this.quadruples[programIndex];
    console.log("RUNNING QUAD " + programIndex + ": " + JSON.stringify(curQuad));

    let instruction = curQuad[0];
    let rawArg1 = curQuad[1];
    let rawArg2 = curQuad[2];
    let rawArg3 = curQuad[3];

    var arg1;
    var arg2;
    var arg3 = Number(rawArg3);

    let isConstantArg1 = true;
    let isConstantArg2 = true;

    // Get arg1's value
    if (rawArg1.indexOf('*') > -1) { // Check for numbers (both int and float)
      let cleanString1 = rawArg1.replace(/\*/g, '');
      //console.log("Cleaned string 1 is: " + cleanString1 + arg1isConst);
      arg1 = Number(cleanString1);
    }
    else if (rawArg1.indexOf('/') > -1) { // Check for string values
      let cleanString1 = rawArg1.replace(/\//g, '');
      arg1 = cleanString1;
    }
    else if (rawArg1 == "true") {
      arg1 = true;
    }
    else if (rawArg1 == "false") {
      arg1 = false;
    } else if (rawArg1 == "") { // no arg provided
      arg1 = null;
    } else { // arg is address
      if (!isNaN(Number(rawArg1))) {
        if (this.memory[Number(rawArg1)] == null) {
          console.log("Error: variable is not initialized.");
          alert("You are trying to use a variable without giving it a value first.");
          return false;
        }
        else {
          console.log("arg1 is an addr (" + rawArg1 + ") and it points to " + this.memory[Number(rawArg1)]);
          arg1 = this.memory[Number(rawArg1)].value;
          isConstantArg1 = false;
        }
      }
      else { // arg is a string (unexpected by memory)
        console.log("Arg1 is an unexpected string.");
        arg1 = rawArg1;
      }
    }

    // Get arg2's value
    if (rawArg2.indexOf('*') > -1) {
      let cleanString1 = rawArg2.replace(/\*/g, '');
      //console.log("Cleaned string 1 is: " + cleanString1 + arg2isConst);
      arg2 = Number(cleanString1);
    }
    else if (rawArg2.indexOf('/') > -1) { // Check for string values
      let cleanString2 = rawArg2.replace(/\//g, '');
      arg2 = cleanString2;
    }
    else if (rawArg2 == "true") {
      arg2 = true;
    }
    else if (rawArg2 == "false") {
      arg2 = false;
    } else if (rawArg2 == "") { // No arg provided
      arg2 = null;
    } else { // arg is address
      if (!isNaN(Number(rawArg2))) {
        if (this.memory[Number(rawArg1)] == null) {
          console.log("Error: variable is not initialized.");
          alert("You are trying to use a variable without giving it a value first.");
          return false;
        }
        else {
          console.log("arg2 is an addr (" + rawArg2 + ") and it points to " + this.memory[Number(rawArg2)]);
          arg2 = this.memory[Number(rawArg2)].value;
          isConstantArg2 = false;
        }
      }
      else { // arg is a string (unexpected by memory)
        console.log("Arg2 is an unexpected string.");
        arg1 = rawArg2;
      }
    }


    // Handle instruction
      // debugging helpers
    let arg1Log = arg1 + (isConstantArg1 ? " (const)" : " (addr: " + Number(rawArg1) + ")");
    let arg2Log = arg2 + (isConstantArg2 ? " (const)" : " (addr: " + Number(rawArg2) + ")");

    switch (instruction.toLowerCase()) {
      // ======= GoTo's =======
      case "goto":
        console.log("Going from " + programIndex + " to " + arg3);
        return this.executeQuadruples(arg3);

      case "gotof":
        if (arg1) {
          console.log("Arg1 is false, going from " + programIndex + " to " + arg3);
          return this.executeQuadruples(arg3);
        }
        else {
          console.log("Arg1 is true; ignoring quadruple...")
        }
        break;

      case "gosub":
        console.log("Calling function in quad " + arg1);
        this.executeQuadruples(arg3);
        break;
      
      case "endproc":
        console.log("Finished function. Returning to main process...");
        return true;

      case "end":
        console.log("Reached end of quadruples.");
        return true;

      // ======= Statements =======
      case "=":
        console.log("Assigning " + arg1Log + " to " + arg3);
        this.memory[arg3] = new varTuple(arg1);
        break;

      case "++":
        console.log("Adding 1 to " + arg3);
        if (!error) {
          this.memory[arg3].value++;
        }
        break;

      case "--":
        console.log("Subtracting 1 to " + arg3);
        if (!error) {
          this.memory[arg3].value--;
        }
        break;

      case "param":
        console.log("Setting " + arg1Log + " as param for function to " + arg3);
        this.memory[arg3] = new varTuple(arg1);
        break;

      case "era":
        console.log("Reading params for function call...");
        break;

      case "ret":
        console.log("Setting return to addr " + arg3 + " as " + arg1Log);
        this.memory[arg3] = new varTuple(arg1);
        break;

      case "print":
        console.log("Outputting: " + arg1Log);
        this.outputLines.push(arg1);
        break;

      case "ver":
        // TODO: revisar que funcione y agregar
        console.log("Checking that array index is correct.");
        break;

      // ======= Expressions =======
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
        console.log("(TODO) <= to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 <= arg2);
        break;

      case ">=":
        console.log("(TODO) >= to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 >= arg2);
        break;

      case "<": //TODO: are the arguments of these switched by the compiler??
        console.log("(TODO) < to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 < arg2);
        break;

      case ">":
        console.log("(TODO) > to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 > arg2);
        break;

      // ======= Logs =======
      case "main":
        console.log("Entering main...");
        break;

      case "func":
        console.log("Entering function " + arg1 + "...");
        break;
    
      // Ignore other quads
      default:
        console.log("Ignoring quad: " + JSON.stringify(curQuad));
        break;
    }

    // Handle next quadruple
    return this.executeQuadruples(programIndex + 1);
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