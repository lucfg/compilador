// import { varTuple } from './output';
import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ViewController, AlertController } from 'ionic-angular';

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
              public viewCtrl: ViewController,
              public alertCtrl: AlertController
  ) {
    this.programName = this.navParams.data.programName;
    this.quadruples = this.navParams.data.quadruples;
  }

  async ionViewDidLoad() {
    this.run();
  }

  run() {
    try {
      this.executeQuadruples(0, 0);
    } catch (err) {
      console.log(err);
      alert("Seems like you have an infinite loop.");
    }
    // console.log("Resulting memory:");
    // console.log(this.memory);
    console.log("Resulting virtual memory:");
    console.log(this.funcArguments);
  }

  // Quadruple reader
  outputLines: string[] = []; 
  memory: HashTable<varTuple> = {};
  funcArguments = [{}]; // Each index represents the depth of the program. Each index contains a json object that has the arguments and their values of the function. It starts with an empty object at index 0, as main has depth 0 and no arguments.

  /**
   * Reads a quadruple on the given index and handles it accordingly
   * @param programIndex Index of the quadruple to rea
   * @param depth depth at which the program is running (0 for main)
   * @param error If true, stops executing more quadruples
   */
  async executeQuadruples(programIndex: number, depth: number, sendingParams?: boolean, error?: boolean) {
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
    var arg3 = Number(rawArg3); // TODO: handle const values for verif of arrays

    let isConstantArg1 = true;
    let isConstantArg2 = true;
    let mustBeInitializedArg1 = true;
    let mustBeInitializedArg2 = true;

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
    else if (rawArg1.indexOf('(') > -1) { // Check for array references
      let cleanString1 = rawArg1.replace(/\(/g, '');
      cleanString1 = cleanString1.replace(/\)/g, '');
      let referenceAddress = cleanString1;
      let address = this.funcArguments[depth][referenceAddress.toString()];
      arg1 = this.funcArguments[depth][address.toString()];
    }
    else if (rawArg1 == "true") {
      arg1 = true;
    }
    else if (rawArg1 == "false") {
      arg1 = false;
    } else if (rawArg1 == "") { // no arg provided
      arg1 = null;
      mustBeInitializedArg1 = false;
    } else { // arg is meant to be an address
      if (isNaN(Number(rawArg1))) { // Handle unexpected strings
        console.log("Arg1 is an unexpected string.");
        arg1 = rawArg1;
        mustBeInitializedArg1 = false;
      }
      else {
        let funcArgVal = this.funcArguments[depth][rawArg1.toString()];
        if (funcArgVal != null) {
          // console.log("arg1 is an argument and its value is " + funcArgVal);
          arg1 = funcArgVal;
        }
        else { // Variable is not initialized
          console.log("Error: arg1 is not initialized for depth " + depth);
          console.log(this.funcArguments);
          alert("You are trying to use a variable without giving it a value first.");
          return false;
        }
      }
    }

    if (mustBeInitializedArg1 && arg1 == null) {
      console.log("Initialization error: arg1 is not initialized for depth " + depth);
      console.log(this.funcArguments);
      alert("You are trying to use a variable without giving it a value first.");
      return false;
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
    else if (rawArg2.indexOf('(') > -1) { // Check for array references
      let cleanString2 = rawArg2.replace(/\(/g, '');
      cleanString2 = cleanString2.replace(/\)/g, '');
      let referenceAddress = cleanString2;
      let address = this.funcArguments[depth][referenceAddress.toString()];
      arg2 = this.funcArguments[depth][address.toString()];
    }
    else if (rawArg2 == "true") {
      arg2 = true;
    }
    else if (rawArg2 == "false") {
      arg2 = false;
    } else if (rawArg2 == "") { // No arg provided
      arg2 = null;
      mustBeInitializedArg2 = false;
    } else { // arg is meant to be an address
      if (isNaN(Number(rawArg2))) { // Handle unexpected strings
        console.log("Arg2 is an unexpected string.");
        arg2 = rawArg2;
        mustBeInitializedArg2 = false;
      }
      else {
        let funcArgVal = this.funcArguments[depth][rawArg2.toString()];
        if (funcArgVal != null) {
          // console.log("arg2 is an argument and its value is " + funcArgVal);
          arg2 = funcArgVal;
        }
        else { // Variable is not initialized
          console.log("Error: arg2 is not initialized for depth " + depth);
          console.log(this.funcArguments);
          alert("You are trying to use a variable without giving it a value first.");
          return false;
        }
      }
    }

    if (mustBeInitializedArg2 && arg2 == null) {
      console.log("Initialization error: arg2 is not initialized for depth " + depth);
      console.log(this.funcArguments);
      alert("You are trying to use a variable without giving it a value first.");
      return false;
    }

    // Get arg'3 value (mostly, an address)
    if (rawArg3.indexOf('*') > -1) { // Arg was sent as an integer value
      let cleanString3 = rawArg3.replace(/\*/g, '');
      arg3 = Number(cleanString3);
    }
    else if (rawArg3.indexOf('(') > -1) { // Check for array references
      let cleanString3 = rawArg3.replace(/\(/g, '');
      cleanString3 = cleanString3.replace(/\)/g, '');
      let referenceAddress = cleanString3;
      let address = this.funcArguments[depth][referenceAddress.toString()];
      // arg2 = this.funcArguments[depth][address.toString()];
      arg3 = address;
    }
    else {
      arg3 = Number(rawArg3); // Arg is an address
    }


    // Handle instruction
      // debugging helpers
    let arg1Log = arg1 + (isConstantArg1 ? " (const)" : " (addr: " + Number(rawArg1) + ")");
    let arg2Log = arg2 + (isConstantArg2 ? " (const)" : " (addr: " + Number(rawArg2) + ")");

    // console.log("debug: depth= " + depth + " arg1=" + arg1Log + "arg2=" + arg2Log);

    switch (instruction.toLowerCase()) {
      // ======= GoTo's =======
      case "goto":
        if (arg3 > 0) {
          console.log("Going from " + programIndex + " to " + arg3 + " in depth " + depth);
          return this.executeQuadruples(arg3, depth);
        }        
        else {
          console.log("Ignoring redundant goto");
        }
        break;

      case "gotof":
        if (!arg1) {
          console.log("Arg1 is false, going from " + programIndex + " to " + arg3 + " in depth " + depth);
          return this.executeQuadruples(arg3, depth);
        }
        else {
          console.log("Arg1 is true; ignoring quadruple...")
        }
        break;

      case "gosub":
        console.log("Calling function in quad " + arg1 + " with the following params.");
        console.log(JSON.stringify(this.funcArguments[depth]));
        if (!this.executeQuadruples(arg3, depth+1, false)) {
          return false;
        }
        sendingParams = false; // Here, function has already been ran, so depth must be returned to previous value
        break;
      
      case "endproc":
        console.log("Finished function. Freeing memory and returning to main process...");
        this.funcArguments.pop();
        return true;

      case "end":
        console.log("Reached end of quadruples.");
        return true;

      // ======= Statements =======
      case "=":
        console.log("Assigning " + arg1Log + " to " + arg3 + " in depth " + depth);
        this.funcArguments[depth][arg3.toString()] = arg1;
        // this.memory[arg3] = new varTuple(arg1);
        break;

      case "++":
        console.log("Adding 1 to " + arg3 + " in depth " + depth);
        if (!error) {
          this.funcArguments[depth][arg3.toString()]++;
          // this.memory[arg3].value++;
        }
        break;

      case "--":
        console.log("Subtracting 1 to " + arg3 + " in depth " + depth);
        if (!error) {
          this.funcArguments[depth][arg3.toString()]--;
          // this.memory[arg3].value--;
        }
        break;

      case "param":
        console.log("Setting " + arg1Log + " as param with name " + arg2Log + " for function with depth " + depth + ".");
        this.funcArguments[depth+1][arg2.toString()] = arg1
        // console.log("Setting param " + arg2Log + " to addr " + arg3 + " with value " + arg1);
        // this.memory[arg3] = new varTuple(arg1);
        // this.funcArguments[depth][arg2.toString()] = arg3;
        break;

      case "era": // Prepares arguments memory for param reading
        console.log("Reading params for function call...");
        sendingParams = true;
        this.funcArguments.push({});
        break;

      case "ret":
        console.log("Setting return to addr " + arg3 + " as " + arg1Log + " for lower depth " + depth);
        this.funcArguments[depth - 1][arg3.toString()] = arg1;
        // this.memory[arg3] = new varTuple(arg1);
        break;

      case "print":
        console.log("Outputting: " + arg1Log);
        this.outputLines.push(arg1);
        break;

      case "read":
        console.log("Reading input to address " + arg3);
        this.readVariable(arg3, programIndex, depth); // TODO: does this cause problems when using funcs?
        return true;

      case "ver":
        // TODO: revisar que funcione y agregar
        console.log("Checking that array index is correct.");
        break;

      // ======= Arrays =======
      case "ver":
        console.log("Checking that given index " + arg1Log + " is within array bounds " + arg2Log + arg3);
        if (arg1 < arg2 || arg1 > arg3) {
          console.log("Error: array index (" + arg1Log + ") is out of bounds (" + arg2Log + "-" + arg3 + ")");
          alert("Array index is out of bounds.");
          return false;
        }
        break;

      // ======= Expressions =======
      case "+":
        console.log("Summing to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 + arg2;
        // this.memory[arg3] = new varTuple(arg1 + arg2);
        break;

      case "-":
        console.log("Subtracting to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 - arg2;
        // this.memory[arg3] = new varTuple(arg1 - arg2);
        break;
      
      case "/":
        console.log("Dividing to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 / arg2;
        // this.memory[arg3] = new varTuple(arg1 / arg2);
        break;

      case "*":
        console.log("Multiplying to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 * arg2;
        // this.memory[arg3] = new varTuple(arg1 * arg2);
        break;

      case "&&":
        console.log("AND to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 && arg2;
        // this.memory[arg3] = new varTuple(arg1 && arg2);
        break;
      
      case "||":
        console.log("OR to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.memory[arg3] = new varTuple(arg1 || arg2);
        break;

      case "==":
        console.log("== to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 == arg2;
        // this.memory[arg3] = new varTuple(arg1 == arg2);
        break;

      case "<=":
        console.log("(TODO) <= to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 <= arg2;
        // this.memory[arg3] = new varTuple(arg1 <= arg2);
        break;

      case ">=":
        console.log("(TODO) >= to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 >= arg2;
        // this.memory[arg3] = new varTuple(arg1 >= arg2);
        break;

      case "<": //TODO: are the arguments of these switched by the compiler??
        console.log("(TODO) < to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 < arg2;
        // this.memory[arg3] = new varTuple(arg1 < arg2);
        break;

      case ">":
        console.log("(TODO) > to dir " + arg3 + " values " + arg1Log + " and " + arg2Log);
        this.funcArguments[depth][arg3.toString()] = arg1 > arg2;
        // this.memory[arg3] = new varTuple(arg1 > arg2);
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
    return this.executeQuadruples(programIndex + 1, depth, sendingParams);
  }

  /**
   * Asks the user to input some data to give to a variable.
   * @param address address in memory to which to return the value of the variable to
   */
  async readVariable(address: number, currentQuad: number, currentDepth: number) {
    let alert = this.alertCtrl.create({
      // title: (this.outputLines.length > 0 ? this.outputLines[this.outputLines.length-1] : ""),
      message: (this.outputLines.length > 0 ? this.outputLines[this.outputLines.length-1] : ""),
      inputs: [
        {
          name: 'input',
          type: 'number'
        }
      ],
      buttons: [
        {
          text: 'Accept',
          handler: data => {
            // this.memory[address] = new varTuple(Number(data.input));
            this.funcArguments[currentDepth][address.toString()] = Number(data.input);
            this.executeQuadruples(currentQuad+1, currentDepth);
          }
        }
      ]
    });

    alert.present();
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